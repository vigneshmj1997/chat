from user.schemas import User  # Should be declared before Chat
from chat.schemas import ChatMessage
from chat.models import MessageStatus
from sql.config import get_db_instance
from fastapi import WebSocket
import aio_pika
from fastapi.websockets import WebSocketDisconnect
import json
import logging
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session
from utils import connect_to_broker
from datetime import datetime
from sqlalchemy import not_


class Message:
    def __init__(self, from_user_email: str, to_user_email: str, message: str):
        self.from_user_email = from_user_email
        self.to_user_email = to_user_email
        self.message = message


def get_user_id_by_email(email: str, db: Session):
    """Get a specific user's ID by their e-mail address"""
    try:
        # Query the User table to get the user with the matching email
        logging.info(email)
        user = db.query(User).filter(User.email == email).one()

        # Close the session to release resources
        db.close()

        # Return the user_id of the user with the matching email
        return user.id

    except NoResultFound:
        logging.error(NoResultFound)
        return None


async def send_message(websocket: WebSocket, user_email: str):

    # Establish the WebSocket connection
    await websocket.accept()
    # Connect to the RabbitMQ broker
    connection = await connect_to_broker()

    # Create a channel
    channel = await connection.channel()

    # Declare a topic exchange
    exchange = await channel.declare_exchange(
        "chat_exchange", aio_pika.ExchangeType.TOPIC
    )

    # Declare a queue for the user
    queue_name = f"user_queue_{user_email}"
    queue = await channel.declare_queue(queue_name, durable=True)

    # Bind the queue to the exchange using the user_email as the routing key
    await queue.bind(exchange, routing_key=user_email)

    # Initialize the message status
    message_status = MessageStatus.NOT_SENT

    try:
        while True:
            # Wait for a message from the WebSocket client
            data = await websocket.receive_text()

            # Parse the message data
            data = json.loads(data)
            logging.info(data)
            to_user_email = data.get("to_user")
            message_content = data.get("message")

            if to_user_email:
                # Send the message to the specified user's queue
                message = Message(
                    from_user_email=user_email,
                    to_user_email=to_user_email,
                    message=message_content,
                )
                await exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(message.__dict__).encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    ),
                    routing_key=to_user_email,
                )
            # If the message is sent successfully, update the message status
            message_status = MessageStatus.SENT
    except WebSocketDisconnect:
        # Handle WebSocket disconnect here if needed
        logging.error(WebSocketDisconnect)
        
    except Exception as e:
        # Handle all other exception here
        logging.error(f"Exceptoion due to {str(e)}")
        
    finally:
        # Clean up the resources after WebSocket disconnects
        await connection.close()
        # Get the current timestamp
        current_timestamp = datetime.utcnow()

        # Add message to bd
        with get_db_instance() as db:
            db_message = ChatMessage(
                sender_id=get_user_id_by_email(user_email, db),
                receiver_id=get_user_id_by_email(to_user_email, db),
                message=message_content,
                timestamp=current_timestamp,
                read=True if message_status == MessageStatus.SENT else False
            )
            db.add(db_message)
            db.commit()

        
def get_unread_messages(user_email: str, db: Session):

    receiver_id = get_user_id_by_email(user_email, db)

    try:
        # Query the ChatMessage table for unread messages for the specified receiver_id
        unread_messages = db.query(ChatMessage).filter(
            ChatMessage.receiver_id == receiver_id,
            not_(ChatMessage.read)
        ).order_by(ChatMessage.timestamp).all()

        # Group the messages by sender_id
        grouped_messages = {}
        for message in unread_messages:
            if message.sender_id not in grouped_messages:
                grouped_messages[message.sender_id] = []
            grouped_messages[message.sender_id].append(message)

        return grouped_messages

    except Exception as e:
        # Handle the exception as needed
        logging.error(f"Exception: {str(e)}")
        return None

    finally:
        # Close the session
        db.close()
    