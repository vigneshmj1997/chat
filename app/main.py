from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import logging
import uvicorn
from chat.routers import chat_router
from user.routers import user_router
from utils import connect_to_broker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Connect to the RabbitMQ broker when the app starts
    app.state.rabbitmq_connection = await connect_to_broker()

@app.on_event("shutdown")
async def shutdown_event():
    # Close the RabbitMQ connection when the app shuts down
    await app.state.rabbitmq_connection.close()




app.include_router(user_router)
app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)