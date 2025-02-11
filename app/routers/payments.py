from fastapi import status, APIRouter, HTTPException, Query
from db.models.payments import Payment, PaymentCreate, PaymentUpdate
from sqlmodel import select 
from db.db import SessionDep

router = APIRouter()


@router.get("/payments", response_model=list[Payment], tags=["Payments"])
async def get_all_payments(

    session: SessionDep,
    skip: int = Query(0, description="Payments for omit"),
    limit: int = Query(10, description="Payments for show")): 

    payments = session.exec(select(Payment).offset(skip).limit(limit)).all()

    if not payments: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return payments 

@router.get("/payments/{payment_id}", response_model=Payment, tags=["Payments"])
async def get_payment_by_id(payment_id: int, session: SessionDep):

    payment = session.get(Payment, payment_id)

    if not payment: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return payment 

@router.post("/payments/create", response_model=Payment, tags=["Payments"])
async def create_payment(payment_data: PaymentCreate, session: SessionDep):

    payment = Payment.model_validate(payment_data)
    session.add(payment)
    session.commit()
    session.refresh(payment)

    return payment

@router.patch("/payments/{payment_id}", response_model=Payment, tags=["Payments"])
async def update_payment(payment_id: int, payment_data: PaymentUpdate, session: SessionDep): 

    payment = session.get(Payment, payment_id)

    if not payment: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    payment_data_for_update = payment_data.model_dump(exclude_unset=True)

    for key, value in payment_data_for_update.items(): 

        setattr(payment, key, value)

    session.add(payment)
    session.commit()
    session.refresh(payment)

    return payment

@router.delete("/payments/{payment_id}", response_model=Payment, tags=["Payments"])
async def delete_payment(payment_id: int, session: SessionDep): 

    try: 
        payment = session.get(Payment, payment_id)
    
        if not payment: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        session.delete(payment)
        session.commit()

        return {
            "message":f"Payment with the id: {payment_id} removed sucessfully"
        }
    
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Details: {e}")
