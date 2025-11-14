import json
import logging

from fastapi import HTTPException

from models.players import Player
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            return []

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
        raise HTTPException(status_code=404, detail=f"Database error { str(e) }")

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
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

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