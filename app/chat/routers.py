from fastapi import APIRouter
from fastapi import APIRouter, Depends
from fastapi import WebSocket
from chat.crud import send_message,get_unread_messages
from sql.config import get_db_instance

chat_router = APIRouter(prefix="/v1/chat")


@chat_router.websocket("/ws/{user_email}")
async def chat_ws(websocket: WebSocket, user_email: str):
    _ = await send_message(websocket, user_email)
    

@chat_router.get("/unread/{user_email}")
async def get_unread_chat(user_email: str, db=Depends(get_db_instance)):
    response = await get_unread_messages(user_email, db)