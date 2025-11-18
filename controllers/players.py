import json
import logging

from fastapi import HTTPException

from models.players import Player
from utils.database import execute_query_json

from models.players_games import PlayerGame

from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================
#                 CRUD OPERATIONS FOR PLAYERS
# ============================================================


async def get_one( id:int ) -> Player:

    selectscript = """
        SELECT [id]
            ,[firstname]
            ,[lastname]
            ,[nickname]
            ,[email]
            ,[birth_date]
        FROM [gamehub].[players]
        WHERE [id] = ?;
    """

    params = [id]
    result_dict = []

    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        #Validacion de elemento vacio
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Player not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")
    
async def get_all() -> list[Player]:

    selectscript = """
        SELECT [id]
            ,[firstname]
            ,[lastname]
            ,[nickname]
            ,[email]
            ,[birth_date]
        FROM [gamehub].[players]
    """

    result_dict = []

    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def create_player( player: Player ) -> Player:
    
    createscript = """
        INSERT INTO [gamehub].[players] ( [firstname] ,[lastname] ,[nickname] ,[email] ,[birth_date]) 
        VALUES ( ?, ?, ?, ? ,? );
    """

    params = (
        player.firstname
        , player.lastname
        , player.nickname
        , player.email
        , player.birth_date
    )

    insert_result = None

    try:
        insert_result = await execute_query_json( createscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT [id]
            ,[firstname]
            ,[lastname]
            ,[nickname]
            ,[email]
            ,[birth_date]
        FROM [gamehub].[players]
        WHERE [nickname] = ?;
    """

    params = [player.nickname]

    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        #Validacion de elemento vacio
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error { str(e) }")

async def update_player( player:Player ) -> Player:

    dict = player.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [gamehub].[players]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( player.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    sqlfind: str = """
        SELECT [id]
            ,[firstname]
            ,[lastname]
            ,[nickname]
            ,[email]
            ,[birth_date]
        FROM [gamehub].[players]
        WHERE [id] = ?;
    """

    params = [player.id]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Player not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")

async def delete_player( id:int ) -> str:

    deletescript = """
        DELETE FROM [gamehub].[players]
        WHERE [id] = ?
    """

    params = [id]

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    

# ============================================================
#           PLAYER ↔ GAMES RELATION (players_games)
# ============================================================


async def get_one_game( player_id: int, game_id:int ) -> PlayerGame:

    selectscript = """
        SELECT pc.player_id
            ,p.nickname 
            ,pc.game_id
            ,g.title
            ,pc.registered_date
        FROM gamehub.players_games pc 
        INNER JOIN gamehub.players p  ON pc.player_id = p.id 
        INNER JOIN gamehub.games g ON pc.game_id = g.id
        WHERE pc.player_id = ?
        and pc.game_id = ?;
    """

    params = [player_id, game_id]

    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        #Validacion de elemento vacio
        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="No games found for the player")
        
        return result_dict[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")
    
async def get_all_games( player_id: int ) -> list[PlayerGame]:

    selectscript = """
        SELECT pc.player_id
            ,p.nickname 
            ,pc.game_id
            ,g.title
            ,pc.registered_date
        FROM gamehub.players_games pc 
        INNER JOIN gamehub.players p  ON pc.player_id = p.id 
        INNER JOIN gamehub.games g ON pc.game_id = g.id
        WHERE pc.player_id = ?;
    """

    params=[player_id]

    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        #Validacion de elemento vacio
        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="No games found for the player")
        
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")
    
async def add_game( player_id: int, game_id:int ) -> PlayerGame:
    
    createscript = """
        INSERT INTO [gamehub].[players_games] ( [player_id] ,[game_id] ,[registered_date]) 
        VALUES ( ?, ?, ?);
    """

    params = (
        player_id
        , game_id
        , datetime.now()
    )


    try:
        insert_result = await execute_query_json( createscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT pc.player_id
            ,p.nickname 
            ,pc.game_id
            ,g.title
            ,pc.registered_date
        FROM gamehub.players_games pc 
        INNER JOIN gamehub.players p  ON pc.player_id = p.id 
        INNER JOIN gamehub.games g ON pc.game_id = g.id
        WHERE pc.player_id = ?
        and pc.game_id = ?;
    """

    params = [player_id, game_id]

    try:
        result = await execute_query_json(sqlfind, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error { str(e) }")


async def remove_game( player_id:int, game_id:int ) -> str:

    deletescript = """
        DELETE FROM [gamehub].[players_games]
        WHERE [player_id] = ? AND [game_id] = ?
    """

    params = [player_id, game_id]

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "GAME REMOVE"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    