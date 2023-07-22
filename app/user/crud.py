from user.models import UserSchema
from sqlalchemy.orm import Session
from user.schemas import User
from sqlalchemy.exc import IntegrityError
from fastapi import  HTTPException
import logging


async def add_user_to_db(request:UserSchema,db:Session):
    try:
        # Check if the email is already registered
        user = db.query(User).filter(User.email == request.email).first()
        if user:
            return {"message": "Email already registered"}

        # Create a new User instance based on the received data
        new_user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone_number=request.phone_number,
            bio=request.bio,
            chat_status=request.chat_status,
            user_status=request.user_status,
            user_role=request.user_role,
            profile_picture=request.profile_picture,
        )

        # Add the new user to the database
        db.add(new_user)
        db.commit()

        return {"message": "User added successfully"}

    except IntegrityError as e:
        # Handle database integrity errors (e.g., duplicate email due to unique constraint)
        db.rollback()  # Rollback the transaction to avoid partial changes
        raise HTTPException(status_code=400, detail=f"Database Integrity Error {e}")

    except Exception as e:
        # Handle other generic exceptions (e.g., server errors)
        detail=f"Internal Server Error {str(e)}"
        logging.error(detail)
        raise HTTPException(status_code=500, detail=detail)

