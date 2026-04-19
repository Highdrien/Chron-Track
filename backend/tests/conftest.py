from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.test import Client

from races.models import Race


@pytest.fixture
def user(db):
    return User.objects.create_user(username="runner", password="testpass123")


@pytest.fixture
def auth_client(user):
    client = Client()
    client.login(username="runner", password="testpass123")
    return client


@pytest.fixture
def race_data():
    return {
        "name": "Trail des Templiers",
        "date": "2026-10-25",
        "distance": "75.00",
        "time": "10:30:00",
        "edition": "2026",
        "elevation_gain": "3200.00",
        "location": "Millau",
        "number_of_participants": 2500,
        "global_ranking": 150,
        "category_ranking": 30,
    }


@pytest.fixture
def race(user):
    return Race.objects.create(
        user=user,
        name="Trail des Templiers",
        date=date(2026, 10, 25),
        distance=Decimal("75.00"),
        time=timedelta(hours=10, minutes=30),
        edition="2026",
        elevation_gain=Decimal("3200.00"),
        location="Millau",
        number_of_participants=2500,
        global_ranking=150,
        category_ranking=30,
    )
