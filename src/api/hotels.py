from typing import Annotated
from sqlalchemy import insert

from fastapi import Query, APIRouter, Body, Depends
from models.hotels import HotelsOrm
from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker


router=APIRouter(prefix="/hotels",  tags=["Hotels"])


hotels = [
    { "id": 1, "title": "Hotel Laguna", "name": "hotel-laguna-reni" },
    { "id": 2, "title": "Hotel Uyut", "name": "hotel-uyut-reni" },
    { "id": 3, "title": "Hotel Dunay", "name": "hotel-dunay-reni" },
    { "id": 4, "title": "Hotel Bessarabia", "name": "hotel-bessarabia-izmail" },
    { "id": 5, "title": "Hotel Old Town", "name": "hotel-old-town-izmail" },
    { "id": 6, "title": "VIP Hotel", "name": "vip-hotel-izmail" },
    { "id": 7, "title": "Hotel Green Hall", "name": "hotel-green-hall-izmail" }
]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Id"),
    title: str | None = Query(None, description="Title"),

):
    hotels_ =[]
    for hotel in hotels:
        if title and hotel["title"] != title:
            continue
        if id and hotel["id"] != id:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:    
        return hotels_[pagination.per_page*(pagination.page - 1):][:pagination.per_page]
    return hotels_


@router.post("")
async def create_hotel(hotel_data: Hotel=Body(openapi_examples={
    "1":{"summary":"Odessa", "value":{
        "title": "Odessa 5 stars hotel",
        "location":"odessa_5_stars"
    }}
})):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(compile_kwargs={"literal_binds":True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    
    return {"status":"OK"}


@router.patch("/{hotel_id}", summary="Partial editing hotels", description="Here you can update info about hotels")
def edit_hotel(
        hotel_id:int,
        hotel_data: HotelPATCH,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"]==hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status":"OK"}


@router.put("/{hotel_id}")
def partially_edit_hotel(hotel_id:int,hotel_data:Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"]==hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status":"OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status":"OK"}

