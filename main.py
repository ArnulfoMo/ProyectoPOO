from fastapi import FastAPI
from routes.players import router as router_player
from routes.games import router as router_game
from routes.categories import router as router_categories

app = FastAPI()


app.include_router(router_player)
app.include_router(router_game)
app.include_router(router_categories)


@app.get("/")
def read_root():
    return {"Hello": "Player"}
