from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Query, Router, Status
from ninja.pagination import LimitOffsetPagination, paginate

from races.models import Race
from races.schemas import Message, RaceFilter, RaceIn, RaceOut, RacePatch, RecordsOut
from races.utils import get_list_categories, get_record

router = Router(tags=["Races"])


@router.get("/records", response=RecordsOut, summary="Personal records by distance")
def get_records(request: HttpRequest):
    return RecordsOut(
        records={
            category: get_record(request.user, category)
            for category in get_list_categories()
        }
    )


@router.get("/", response=list[RaceOut], summary="List races for the current user")
@paginate(LimitOffsetPagination)
def list_races(request: HttpRequest, filters: RaceFilter = Query(...)):
    qs = Race.objects.filter(user=request.user).select_related("user")
    return filters.filter(qs)


@router.post("/", response={201: RaceOut}, summary="Create a race")
def create_race(request: HttpRequest, payload: RaceIn):
    race = Race.objects.create(user=request.user, **payload.dict())
    return Status(201, race)


@router.get("/{race_id}", response=RaceOut, summary="Retrieve a race")
def get_race(request: HttpRequest, race_id: int):
    return get_object_or_404(Race, id=race_id, user=request.user)


@router.put("/{race_id}", response=RaceOut, summary="Replace a race")
def update_race(request: HttpRequest, race_id: int, payload: RaceIn):
    race = get_object_or_404(Race, id=race_id, user=request.user)
    for attr, value in payload.dict().items():
        setattr(race, attr, value)
    race.save()
    return race


@router.patch("/{race_id}", response=RaceOut, summary="Partially update a race")
def patch_race(request: HttpRequest, race_id: int, payload: RacePatch):
    race = get_object_or_404(Race, id=race_id, user=request.user)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(race, attr, value)
    race.save()
    return race


@router.delete(
    "/{race_id}",
    response={204: None, 404: Message},
    summary="Delete a race",
)
def delete_race(request: HttpRequest, race_id: int):
    race = get_object_or_404(Race, id=race_id, user=request.user)
    race.delete()
    return Status(204, None)
