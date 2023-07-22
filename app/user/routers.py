from fastapi import APIRouter, HTTPException
from user.models import UserSchema, UserResponse
from fastapi import Request, APIRouter, Depends
from sql.config import get_db_instance
from user.crud import add_user_to_db
import asyncio

user_router = APIRouter(prefix="/v1/user")


@user_router.post("/add", response_model=UserResponse)
async def add_user(request: UserSchema, db=Depends(get_db_instance)):
    result = await add_user_to_db(request,db=db)
    return result
    