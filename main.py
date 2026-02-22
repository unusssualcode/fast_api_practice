from fastapi import FastAPI
import uvicorn


app = FastAPI()


hotels = [
    {"id":1, "title":"Reni"},
    {"id":2, "title":"Izmail"}
]


@app.get("/hotels")
def get_hotels(
    title:str
):
    return [hotel for hotel in hotels if hotel["title"] == title]


if __name__=="__main__":
    uvicorn.run("main:app", reload=True)g