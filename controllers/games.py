import json
import logging

from fastapi import HTTPException

from models.games import Game
from models.players_games import PlayerGame
from models.games_platforms import GamePlatform
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
#                    CRUD OPERATIONS FOR GAMES
# ============================================================

async def get_one( id:int ) -> Game:

    selectscript = """
        SELECT g.id
            , g.categories_id
            , c.name as category_name
            , g.title
            , g.release_date
        FROM gamehub.games g
        INNER JOIN gamehub.categories c on g.categories_id = c.id
        WHERE g.id = ?;
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
            raise HTTPException(status_code=404, detail="Game not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")
    
async def get_all() -> list[Game]:

    selectscript = """
        SELECT g.id
            , g.categories_id
            , c.name as category_name
            , g.title
            , g.release_date
        FROM gamehub.games g
        INNER JOIN gamehub.categories c on g.categories_id = c.id;
    """

    result_dict = []

    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def create_game( game: Game ) -> Game:
    
    createscript = """
        INSERT INTO [gamehub].[games] ( [categories_id] ,[title] ,[release_date]) 
        OUTPUT INSERTED.[id]
        VALUES ( ?, ?, ?);
    """

    params = (
        game.categories_id
        , game.title
        , game.release_date
    )

    insert_result = None

    try:
        # Es para obtener el id generado con OUTPUT
        insert_result = await execute_query_json(createscript, params, needs_commit=True)
        insert_dict = json.loads(insert_result)

        if len(insert_dict) == 0 or "id" not in insert_dict[0]:
            raise HTTPException(status_code=500, detail="No se pudo recuperar el ID insertado.")

        new_id = insert_dict[0]["id"]


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT g.id
            , g.categories_id
            , c.name as category_name
            , g.title
            , g.release_date
        FROM gamehub.games g
        INNER JOIN gamehub.categories c on g.categories_id = c.id
        WHERE g.id = ?;
    """

    params = [new_id]

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

async def update_game( game:Game ) -> Game:

    dict = game.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [gamehub].[games]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( game.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    sqlfind: str = """
        SELECT g.id
            , g.categories_id
            , c.name as category_name
            , g.title
            , g.release_date
        FROM gamehub.games g
        INNER JOIN gamehub.categories c on g.categories_id = c.id
        WHERE g.id = ?;
    """

    params = [game.id]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Game not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")

async def delete_game( id:int ) -> str:

    deletescript = """
        DELETE FROM [gamehub].[games]
        WHERE [id] = ?
    """

    params = [id]

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
# ============================================================
#          GAME ↔ PLAYERS RELATION (players_games)
# ============================================================

async def get_all_players( game_id: int ) -> list[PlayerGame]:

    selectscript = """
        SELECT pc.player_id
            ,p.nickname 
            ,pc.game_id
            ,g.title
            ,pc.registered_date
        FROM gamehub.players_games pc 
        INNER JOIN gamehub.players p  ON pc.player_id = p.id 
        INNER JOIN gamehub.games g ON pc.game_id = g.id
        WHERE pc.game_id = ?;
    """

    params=[game_id]

    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        #Validacion de elemento vacio
        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="No games found for the player")
        
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")
    

# ============================================================
#        GAME ↔ PLATFORMS RELATION (games_platforms)
# ============================================================

async def get_one_platform( games_id: int, platforms_id:int ) -> PlayerGame:

    selectscript = """
        SELECT gp.games_id as game_id
            , g.title
            , gp.platforms_id as platform_id
            , p.name as platform_name
            , gp.active
        FROM gamehub.games_platforms gp
        INNER JOIN gamehub.platforms p  ON gp.platforms_id = p.id 
        INNER JOIN gamehub.games g ON gp.games_id = g.id
        WHERE gp.games_id = ?
        AND gp.platforms_id = ?;
    """

    params = [games_id, platforms_id]

    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        #Validacion de elemento vacio
        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="No platform found for the game")
        
        return result_dict[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")
    
async def get_all_platforms( games_id: int ) -> list[GamePlatform]:

    selectscript = """
        SELECT gp.games_id as game_id
            , g.title
            , gp.platforms_id as platform_id
            , p.name as platform_name
            , gp.active
        FROM gamehub.games_platforms gp
        INNER JOIN gamehub.platforms p  ON gp.platforms_id = p.id 
        INNER JOIN gamehub.games g ON gp.games_id = g.id
        WHERE gp.games_id = ?;
    """

    params=[games_id]

    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        #Validacion de elemento vacio
        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="No platforms found for the game")
        
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")
    
async def add_platform( games_id: int, platforms_id:int ) -> PlayerGame:
    
    createscript = """
        INSERT INTO [gamehub].[games_platforms] ( [games_id] ,[platforms_id] ,[active]) 
        VALUES ( ?, ?, ?);
    """

    params = (
        games_id
        , platforms_id
        , True
    )


    try:
        insert_result = await execute_query_json( createscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT gp.games_id as game_id
            , g.title
            , gp.platforms_id as platform_id
            , p.name as platform_name
            , gp.active
        FROM gamehub.games_platforms gp
        INNER JOIN gamehub.platforms p  ON gp.platforms_id = p.id 
        INNER JOIN gamehub.games g ON gp.games_id = g.id
        WHERE gp.games_id = ?
        AND gp.platforms_id = ?;
    """

    params = [games_id, platforms_id]

    try:
        result = await execute_query_json(sqlfind, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error { str(e) }")


async def update_platform_info(platform_data: GamePlatform) -> GamePlatform:
    dict = platform_data.model_dump(exclude_none=True)
    keys = [ k for k in  dict.keys() ]
    keys.remove('games_id')
    keys.remove('platforms_id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [gamehub].[games_platforms]
        SET {variables}
        WHERE [games_id] = ? AND [platforms_id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( platform_data.games_id )
    params.append( platform_data.platforms_id )

    try:
        await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    select_script = """
        SELECT gp.games_id as game_id
            , g.title
            , gp.platforms_id as platform_id
            , p.name as platform_name
            , gp.active
        FROM gamehub.games_platforms gp
        INNER JOIN gamehub.platforms p  ON gp.platforms_id = p.id 
        INNER JOIN gamehub.games g ON gp.games_id = g.id
        WHERE gp.games_id = ?
        AND gp.platforms_id = ?;
    """

    params = [platform_data.games_id, platform_data.platforms_id]

    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def remove_platform( games_id:int, platforms_id:int ) -> str:

    deletescript = """
        DELETE FROM [gamehub].[games_platforms]
        WHERE [games_id] = ? AND [platforms_id] = ?
    """

    params = [games_id, platforms_id]

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "PLATFORM REMOVE"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    