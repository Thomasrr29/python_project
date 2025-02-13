from fastapi import status, APIRouter, HTTPException, Query, Depends
from db.models.reservations import Reservation, ReservationCreate, ReservationUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from decorators import validate_room_disponibility
from sqlmodel import select 
from db.db import get_async_session


router = APIRouter()

@router.get("/reservations", response_model=list[Reservation], tags=["Reservations"])
async def get_all_reservations(session: AsyncSession = Depends(get_async_session),
        skip: int = Query(0, description="Reservations for omit"), 
        limit: int = Query(10, description="Reservationsfor show")): 

    result = await session.execute(select(Reservation).offset(skip).limit(limit))
    reservations = result.scalars().all()

    if not reservations: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return reservations

@router.get("/reservations/{reservation_id}", response_model=Reservation, tags=["Reservations"])
async def get_reservation_by_id(reservation_id: int, session: AsyncSession = Depends(get_async_session)): 

    reservation = await session.get(Reservation, reservation_id)

    if not reservation: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return reservation

@router.post("/reservations", tags=["Reservations"])
async def create_reservation(reservation_data: ReservationCreate, session: AsyncSession = Depends(get_async_session)): 

    try: 
        customer = await get_customer_by_identification(reservation_data.customer.identification, session)
        
        if not customer: 

            customer = await create_customer(reservation_data.customer, session)

        session.refresh(customer)

        payment_data = {
            **reservation_data.payment.model_dump(), 
            "customer_id":customer.id
        }
        
        payment_created = await create_payment(PaymentCreate.model_validate(payment_data), session)

        reservation = Reservation(
            start=reservation_data.start,
            end=reservation_data.end,
            status=reservation_data.status,
            customer_id=customer.id,
            payment_id=payment_created.id,
            room_id=reservation_data.room_id
        )

        print("Customer_id: ", reservation_data.payment.customer_id)

        session.add(reservation)
        await session.commit()
        await session.refresh(reservation)

        return reservation
    
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{e}")

@router.patch("/reservations/{reservation_id}", response_model=Reservation, tags=["Reservations"])
async def update_reservation(reservation_id: int, reservation_data: ReservationUpdate, session: AsyncSession = Depends(get_async_session)):

    reservation = await session.get(Reservation, reservation_id)

    if not reservation: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The reservation with the id: {reservation_id} wasnt found")

    reservation_for_update = reservation_data.model_dump(exclude_unset=True)

    for key, value in reservation_for_update.items(): 

        setattr(key, value, reservation)

    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)

    return reservation 

@router.delete("/reservations/{reservation_id}", response_model=Reservation, tags=["Reservations"])
async def delete_reservations(reservation_id: int, session: AsyncSession = Depends(get_async_session)): 

    try: 

        reservation = await session.get(Reservation, reservation_id)
        
        if not reservation: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(reservation)
        await session.commit()

        return {
            "message": f"Reservation with the id: {reservation_id} deleted sucesfully"
        }

    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message: {e}")

@router.post("/reservations/verification", tags=["Reservations"])                 
async def wrapper(reservation_data: ReservationCreate, session: AsyncSession = Depends(get_async_session)): 

        result = await session.execute(select(Reservation).where(Reservation.room_id == reservation_data.room_id))
        room_reservations = result.scalars().all()

        reservation_date_start = str(reservation_data.start)
        reservation_date_end = str(reservation_data.end) 

        for reservation in room_reservations:
           
           date_start_reservation = str(reservation.start)
           date_end_reservation = str(reservation.end)

           if reservation_date_start[:7] == date_start_reservation[:7]: 

                dates_reservation_ocuppied = [date for date in range(int(date_start_reservation[-2:]), int(date_end_reservation[-2:]) + 1)]
                dates_new_reservation = [date for date in range(int(reservation_date_start[-2:]), int(reservation_date_end[-2:]) + 1)]

                for date in dates_reservation_ocuppied: 

                    if not date in dates_new_reservation or date == dates_new_reservation[-1:]:

                        return "Bien mi pana"

                    else: 

                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                        detail="You select a ocuppied date, please try with another date") 

        return room_reservations

from .customers import get_customer_by_identification, create_customer
from .payments import create_payment
from .rooms import update_room
from db.models import PaymentCreate