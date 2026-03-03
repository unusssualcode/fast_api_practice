from fastapi import Query, APIRouter
from schemas.hotels import Hotel, HotelPATCH


router=APIRouter(prefix="/hotels",  tags=["Hotels"])


hotels = [
    {"id":1, "title":"Reni", "name":"reni"},
    {"id":2, "title":"Izmail", "name":"izmail"}
]


@router.get("")
def get_hotels(
    id: int | None = Query(None, description="Id"),
    title:str | None = Query(None, description="Title")
):
    hotels_ =[]
    for hotel in hotels:
        if title and hotel["title"] != title:
            continue
        if id and hotel["id"] != id:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id":hotels[-1]["id"]+1,
        "title":hotel_data.title, 
        "name":hotel_data.name
    })
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

