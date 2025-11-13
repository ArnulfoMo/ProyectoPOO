from fastapi import APIRouter, status
from models.players import Player

from controllers.players import (
    get_one
    , get_all
    , create_player
    , update_player
)

router = APIRouter(prefix="/players")

@router.get("/{id}", tags=["Players"], status_code=status.HTTP_200_OK)
async def get_one_player( id:int ):
    result: Player = await get_one(id)
    return result

@router.get( "/", tags=["Players"], status_code=status.HTTP_200_OK)
async def get_all_players():
    result = await get_all()
    return result

@router.post( "/", tags=["Players"], status_code=status.HTTP_201_CREATED)
async def create_new_player(player_data: Player):
    result = await create_player(player_data)
    return result

@router.put("/{id}", tags=["Players"], status_code=status.HTTP_201_CREATED)
async def update_player_information( id:int, player_data:Player ):
    player_data.id = id
    result = await update_player(player_data)
    return result



