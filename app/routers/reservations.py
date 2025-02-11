from fastapi import status, APIRouter, HTTPException, Query
from db.models.reservations import Reservation, ReservationCreate, ReservationUpdate
from sqlmodel import select 
from db.db import SessionDep


router = APIRouter()


@router.get("/reservations", response_model=list[Reservation], tags=["Reservations"])
async def get_all_reservations(session: SessionDep,
        skip: int = Query(0, description="Reservations for omit"), 
        limit: int = Query(10, description="Reservationsfor show")): 

    reservations = session.exec(select(Reservation).offset(skip).limit(limit)).all()

    if not reservations: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return reservations

@router.get("/reservations/{reservation_id}", response_model=Reservation, tags=["Reservations"])
async def get_reservation_by_id(reservation_id: int, session: SessionDep): 

    reservation = session.get(Reservation, reservation_id)

    if not reservation: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return reservation

@router.post("/reservations", response_model=Reservation, tags=["Reservations"])
async def create_reservation(reservation_data: ReservationCreate, session: SessionDep): 

        customer = await get_customer_by_identification(reservation_data.customer.identification, session=session)

        if not customer: 

            customer = await create_customer(reservation_data.customer, session)

        payment_data = {
            **reservation_data.payment.model_dump(), 
            "customer_id":customer.id
        }
        
        payment_created = await create_payment(payment_data, session=session)

        print(f"Customer id: {customer.id}")
        print(f"Payment created id: {payment_created.id}")

        reservation = Reservation(
            start=reservation_data.start,
            end=reservation_data.end,
            customer_id=customer.id,
            payment_id=payment_created.id,
            room_id=reservation_data.room_id
        )

        session.add(reservation)
        session.commit()
        session.refresh(reservation)

        return reservation


    

@router.delete("/reservations/{reservation_id}", response_model=Reservation, tags=["Reservations"])
async def delete_reservations(reservation_id: int, session: SessionDep): 

    try: 

        reservation = session.get(Reservation, reservation_id)
        
        if not reservation: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        session.delete(reservation)
        session.commit()

        return {
            "message": f"Reservation with the id: {reservation_id} deleted sucesfully"
        }

    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message: {e}")


from .customers import get_customer_by_identification, create_customer
from .payments import create_payment