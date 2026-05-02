import json
from datetime import date, timedelta
from decimal import Decimal

from django.test import Client

from races.models import Race

API_BASE = "/api/races/"


class TestListRaces:
    def test_unauthenticated_returns_401(self, db):
        client = Client()
        resp = client.get(API_BASE)
        assert resp.status_code == 401

    def test_list_returns_own_races(self, auth_client, race):
        resp = auth_client.get(API_BASE)
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] == 1
        assert data["items"][0]["name"] == "Trail des Templiers"

    def test_list_excludes_other_users(self, auth_client, race, user):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        other = User.objects.create_user(
            username="other",
            password="other123",
            email="other@test.com",
        )
        Race.objects.create(
            user=other,
            name="Other Race",
            date=date(2026, 5, 1),
            distance=Decimal("10"),
            time=timedelta(hours=1),
        )
        resp = auth_client.get(API_BASE)
        data = resp.json()
        assert data["count"] == 1

    def test_list_filter_by_name(self, auth_client, race):
        resp = auth_client.get(API_BASE + "?name=Templiers")
        data = resp.json()
        assert data["count"] == 1

    def test_list_filter_by_name_no_match(self, auth_client, race):
        resp = auth_client.get(API_BASE + "?name=Marathon")
        data = resp.json()
        assert data["count"] == 0


class TestCreateRace:
    def test_create_success(self, auth_client, race_data):
        resp = auth_client.post(
            API_BASE,
            data=json.dumps(race_data),
            content_type="application/json",
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Trail des Templiers"
        assert data["speed"] is not None
        assert data["pace"] is not None

    def test_create_minimal(self, auth_client):
        payload = {
            "name": "10K",
            "date": "2026-03-15",
            "distance": "10.00",
            "time": "00:45:00",
        }
        resp = auth_client.post(
            API_BASE,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 201

    def test_create_unauthenticated(self, db, race_data):
        client = Client()
        resp = client.post(
            API_BASE,
            data=json.dumps(race_data),
            content_type="application/json",
        )
        assert resp.status_code == 401


class TestGetRace:
    def test_get_success(self, auth_client, race):
        resp = auth_client.get(f"{API_BASE}{race.id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Trail des Templiers"

    def test_get_nonexistent(self, auth_client, db):
        resp = auth_client.get(f"{API_BASE}99999")
        assert resp.status_code == 404

    def test_get_other_users_race(self, auth_client, user):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        other = User.objects.create_user(
            username="other2",
            password="other123",
            email="other2@test.com",
        )
        other_race = Race.objects.create(
            user=other,
            name="Secret Race",
            date=date(2026, 1, 1),
            distance=Decimal("5"),
            time=timedelta(minutes=25),
        )
        resp = auth_client.get(f"{API_BASE}{other_race.id}")
        assert resp.status_code == 404


class TestUpdateRace:
    def test_put_success(self, auth_client, race):
        payload = {
            "name": "Trail Updated",
            "date": "2026-10-25",
            "distance": "80.00",
            "time": "11:00:00",
        }
        resp = auth_client.put(
            f"{API_BASE}{race.id}",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Trail Updated"
        assert resp.json()["distance"] == "80.00"

    def test_patch_success(self, auth_client, race):
        payload = {"name": "Trail Patched"}
        resp = auth_client.patch(
            f"{API_BASE}{race.id}",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Trail Patched"
        assert resp.json()["distance"] == "75.00"

    def test_patch_recalculates_speed(self, auth_client, race):
        old_speed = race.speed
        payload = {"distance": "100.00"}
        resp = auth_client.patch(
            f"{API_BASE}{race.id}",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        new_speed = Decimal(resp.json()["speed"])
        assert new_speed != old_speed

    def test_put_nonexistent(self, auth_client, db):
        payload = {
            "name": "X",
            "date": "2026-01-01",
            "distance": "10.00",
            "time": "01:00:00",
        }
        resp = auth_client.put(
            f"{API_BASE}99999",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 404


class TestDeleteRace:
    def test_delete_success(self, auth_client, race):
        resp = auth_client.delete(f"{API_BASE}{race.id}")
        assert resp.status_code == 204
        assert not Race.objects.filter(id=race.id).exists()

    def test_delete_nonexistent(self, auth_client, db):
        resp = auth_client.delete(f"{API_BASE}99999")
        assert resp.status_code == 404

    def test_delete_other_users_race(self, auth_client, user):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        other = User.objects.create_user(
            username="other3",
            password="other123",
            email="other3@test.com",
        )
        other_race = Race.objects.create(
            user=other,
            name="Not Mine",
            date=date(2026, 1, 1),
            distance=Decimal("5"),
            time=timedelta(minutes=25),
        )
        resp = auth_client.delete(f"{API_BASE}{other_race.id}")
        assert resp.status_code == 404
        assert Race.objects.filter(id=other_race.id).exists()
