from sqlmodel import select 
from functools import wraps
from db.models import ReservationCreate, Reservation, ReservationUpdate
from fastapi import status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session


def validate_room_disponibility(func):

    @wraps(func)
    async def wrapper(reservation_data: ReservationCreate, session: AsyncSession = Depends(get_async_session)): 

        result = await session.execute(select(Reservation).where(Reservation.room_id == reservation_data.room_id))
        room_reservations = result.scalars().all()

        if not room_reservations: 
            return await func(reservation_data, session)

        reservation_date_start = str(reservation_data.start)
        reservation_date_end = str(reservation_data.end) 

        for reservation in room_reservations:
           
           date_start_reservation = str(reservation.start)
           date_end_reservation = str(reservation.end)

           if reservation_date_start[:7] == date_start_reservation[:7]: 

                dates_reservation_ocuppied = [date for date in range(int(date_start_reservation[-2:]), int(date_end_reservation[-2:]) + 1)]
                dates_new_reservation = [date for date in range(int(reservation_date_start[-2:]), int(reservation_date_end[-2:]) + 1)]

                print("ocuppied", dates_reservation_ocuppied[-1])
                print("new", dates_new_reservation)

                for date in dates_new_reservation: 

                    if date in dates_reservation_ocuppied and not date == dates_reservation_ocuppied[-1]:

                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                        detail="You select a ocuppied date, please try with another date") 
                    
        return await func(reservation_data, session)
    return wrapper

        

          

        
             


        
        