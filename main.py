import uvicorn
from fastapi import FastAPI
from routes.players import router as router_player
from routes.games import router as router_game
from routes.categories import router as router_categories
from routes.platforms import router as router_platforms

app = FastAPI()


app.include_router(router_player)
app.include_router(router_game)
app.include_router(router_categories)
app.include_router(router_platforms)


@app.get("/")
def read_root():
    return {"Hello": "Player"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
