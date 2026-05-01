from typing import Annotated
from sqlalchemy import engine, insert, select, func

from fastapi import Query, APIRouter, Body, Depends
from models.hotels import HotelsOrm
from repositories.hotels import HotelsRepository
from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker


router=APIRouter(prefix="/hotels",  tags=["Hotels"])



@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description="Location"),
    title: str | None = Query(None, description="Title"), 
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location = location,
            title = title,
            limit = per_page,
            offset = per_page * (pagination.page - 1)
        )


    # if pagination.page and pagination.per_page:    
    #     return hotels_[pagination.per_page*(pagination.page - 1):][:pagination.per_page]


@router.post("")
async def create_hotel(hotel_data: Hotel=Body(openapi_examples={
    "1":{"summary":"Odessa", "value":{
        "title": "Odessa 5 stars hotel",
        "location":"odessa_5_stars"
    }}
})):
    async with async_session_maker() as session:
        # add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds":True}))
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    
    return {"status":"OK", "data": hotel}


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
async def partially_edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id = hotel_id)
        await session.commit()
    return {"status":"OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id = hotel_id)
        await session.commit()
    return {"status":"OK"}

