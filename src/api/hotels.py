from fastapi import Query, APIRouter, Body
from repositories.hotels import HotelsRepository
from schemas.hotels import Hotel, HotelAdd, HotelPATCH
from src.api.dependencies import DBDep, PaginationDep
# from src.database import async_session_maker


router=APIRouter(prefix="/hotels",  tags=["Hotels"])



@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Location"),
    title: str | None = Query(None, description="Title"), 
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location = location,
        title = title,
        limit = per_page,
        offset = per_page * (pagination.page - 1)
    )


    # if pagination.page and pagination.per_page:    
    #     return hotels_[pagination.per_page*(pagination.page - 1):][:pagination.per_page]


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id = hotel_id)
    # async with async_session_maker() as session:
    #     return await HotelsRepository(session).get_one_or_none(id = hotel_id)


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1":{"summary":"Odessa", "value":{
        "title": "Odessa 5 stars hotel",
        "location":"odessa_5_stars"
    }}
})):
        # add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds":True}))
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}

    # async with async_session_maker() as session:
    #     hotel = await HotelsRepository(session).add(hotel_data)
    #     await session.commit()
    # return {"status": "OK", "data": hotel}


@router.patch("/{hotel_id}", summary = "Partial editing hotels", description="Here you can update info about hotels")
async def edit_hotel(
        hotel_id:int,
        hotel_data: HotelPATCH,
        db: DBDep
):
    await db.hotels.edit(hotel_data, exclude_unset = True, id = hotel_id)
    await db.commit()
    return {"status": "OK"}

    # async with async_session_maker() as session:
    #     await HotelsRepository(session).edit(hotel_data, exclude_unset = True, id = hotel_id)
    #     await session.commit()
    # return {"status": "OK"}


@router.put("/{hotel_id}")
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelAdd, db:DBDep):
    await db.hotels.edit(hotel_data, id = hotel_id)
    await db.commit()
    return {"status": "OK"}
    # async with async_session_maker() as session:
    #     await HotelsRepository(session).edit(hotel_data, id = hotel_id)
    #     await session.commit()
    # return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db:DBDep):
    await db.hotels.delete(id = hotel_id)
    await db.commit()
    return {"status":"OK"}

    # async with async_session_maker() as session:
    #     await HotelsRepository(session).delete(id = hotel_id)
    #     await session.commit()
    # return {"status":"OK"}

