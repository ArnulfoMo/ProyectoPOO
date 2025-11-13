from fastapi import FastAPI
from routes.players import router as router_player

app = FastAPI()


app.include_router(router_player)


@app.get("/")
def read_root():
    return {"Hello": "Player"}
