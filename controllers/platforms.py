import json
import logging

from fastapi import HTTPException

from models.platforms import Platform
from models.games_platforms import GamePlatform
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
#                 CRUD OPERATIONS FOR PLATFORMS
# ============================================================

async def get_one( id:int ) -> Platform:

    selectscript = """
        SELECT [id]
            ,[name]
            ,[release_date]
        FROM [gamehub].[platforms]
        WHERE [id] = ?
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
            raise HTTPException(status_code=404, detail="Platform not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")
    
async def get_all() -> list[Platform]:

    selectscript = """
        SELECT [id]
            ,[name]
            ,[release_date]
        FROM [gamehub].[platforms]
    """

    result_dict = []

    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def create_platform( platform: Platform ) -> Platform:
    
    createscript = """
        INSERT INTO [gamehub].[platforms] ( [name] ,[release_date]) 
        VALUES ( ?, ?);
    """

    params = (
        platform.name
        , platform.release_date
    )

    insert_result = None

    try:
        insert_result = await execute_query_json( createscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT [id]
            ,[name]
            ,[release_date]
        FROM [gamehub].[platforms]
        WHERE [name] = ?
    """

    params = [platform.name]

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

async def update_platform( platform:Platform ) -> Platform:

    dict = platform.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [gamehub].[platforms]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( platform.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    sqlfind: str = """
        SELECT [id]
            ,[name]
            ,[release_date]
        FROM [gamehub].[platforms]
        WHERE [id] = ?
    """

    params = [platform.id]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Platform not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")

async def delete_platform( id:int ) -> str:

    deletescript = """
        DELETE FROM [gamehub].[platforms]
        WHERE [id] = ?
    """

    params = [id]

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    
# ============================================================
#          PLATFORM ↔ GAMES RELATION (games_platforms)
# ============================================================

async def get_all_games( platforms_id: int ) -> list[GamePlatform]:

    selectscript = """
        SELECT gp.games_id as game_id
            , g.title
            , gp.platforms_id as platform_id
            , p.name as platform_name
            , gp.active
        FROM gamehub.games_platforms gp
        INNER JOIN gamehub.platforms p  ON gp.platforms_id = p.id 
        INNER JOIN gamehub.games g ON gp.games_id = g.id
        WHERE gp.platforms_id = ?;
    """

    params=[platforms_id]

    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        #Validacion de elemento vacio
        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="No games found for the platform")
        
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")