from fastapi import APIRouter, status
from models.categories import Category

from controllers.categories import (
    get_one
    , get_all
    , create_category
    , update_category
    , delete_category
)

router = APIRouter(prefix="/categories")

@router.get("/{id}", tags=["Categories"], status_code=status.HTTP_200_OK)
async def get_one_category( id:int ):
    result: Category = await get_one(id)
    return result

@router.get( "/", tags=["Categories"], status_code=status.HTTP_200_OK)
async def get_all_category():
    result = await get_all()
    return result

@router.post( "/", tags=["Categories"], status_code=status.HTTP_201_CREATED)
async def create_new_category(category_data: Category):
    result = await create_category(category_data)
    return result

@router.put("/{id}", tags=["Categories"], status_code=status.HTTP_201_CREATED)
async def update_category_information( id:int, category_data:Category ):
    category_data.id = id
    result = await update_category(category_data)
    return result

@router.delete("/{id}", tags=["Categories"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_information( id:int ):
    status: str = await delete_category(id)
    return status




