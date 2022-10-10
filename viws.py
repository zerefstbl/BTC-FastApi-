from fastapi import APIRouter, HTTPException

from asyncio import gather

from services import UserService, FavoriteService, AssetService

from typing import List

from schemas import StandardOutput, UserCreateInput, ErrorOutput, UserFavoriteAdd, UserListInput, DaySummaryOutput

user_router = APIRouter(prefix='/user')

assets_router = APIRouter(prefix='/assets')


@user_router.post('/create', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def user_create(user_input: UserCreateInput):
    try:
        await UserService.create_user(name=user_input.name)

        return StandardOutput(message='OK')
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@user_router.delete('/delete/{user_id}', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def user_delete(user_id: int):
    try:
        await UserService.delete_user(user_id)

        return StandardOutput(message='OK')
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@user_router.post('/favorite/add', response_model=StandardOutput)
async def user_favorite_add(data: UserFavoriteAdd):
    try:
        print(data.user_id)
        await FavoriteService.add_favorite(user_id=data.user_id, symbol=data.symbol)

        return StandardOutput(message='Tudo certo')
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@user_router.delete('/favorite/delete', response_model=StandardOutput)
async def user_favorite_delete(data: UserFavoriteAdd):
    try:
        await FavoriteService.delete_favorite(user_id=data.user_id, symbol=data.symbol)

        return StandardOutput(message='Deu certo')
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@user_router.get('/list', response_model=List[UserListInput])
async def user_list():
    try:
        return await UserService.list_user()
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.get('/teste/{user_id}', response_model=List[DaySummaryOutput])
async def day_summary(user_id: int):
    print('oioioio')
    try:
        user = await UserService.get_by_id(user_id)
        favorites_symbols = [favorite.symbol for favorite in user.favorites]
        results = [AssetService.day_summary(symbol=symbol) for symbol in favorites_symbols]
        
        return await gather(*results)
    except Exception as error:
        print(error)
        raise HTTPException(400, detail=str(error))