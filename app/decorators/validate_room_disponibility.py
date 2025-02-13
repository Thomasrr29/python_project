from sqlmodel import select 
from functools import wraps
from db.models import ReservationCreate, Reservation
from fastapi import status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session

def validate_room_disponibility(func):

    @wraps(func)
    async def wrapper(reservation_data: ReservationCreate, session: AsyncSession = Depends(get_async_session)): 

        result = await session.execute(select(Reservation).where(Reservation.room_id == reservation_data.room_id))
        room_reservations = result.scalars().all()


        for reservation in room_reservations:

            start_day = str(reservation.start)
            end_day =  str(reservation.end)

            

    return wrapper
        
             


        
        