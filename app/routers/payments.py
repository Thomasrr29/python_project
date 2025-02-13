from fastapi import status, APIRouter, HTTPException, Query, Depends
from db.models.payments import Payment, PaymentCreate, PaymentUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from sqlmodel import select 

router = APIRouter()


@router.get("/payments", response_model=list[Payment], tags=["Payments"])
async def get_all_payments(

    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, description="Payments for omit"),
    limit: int = Query(10, description="Payments for show")): 

    result = await session.execute(select(Payment).offset(skip).limit(limit))
    payments = result.scalars().all()

    if not payments: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return payments 

@router.get("/payments/{payment_id}", response_model=Payment, tags=["Payments"])
async def get_payment_by_id(payment_id: int, session: AsyncSession = Depends(get_async_session)):

    payment = await session.get(Payment, payment_id)

    if not payment: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return payment 

@router.post("/payments/create", response_model=Payment, tags=["Payments"])
async def create_payment(payment_data: PaymentCreate, session: AsyncSession = Depends(get_async_session)):

    customer = await session.get(Customer, payment_data.customer_id)

    if not customer: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"The customer with the id: {payment_data.customer_id} wasnt found")

    payment = Payment.model_validate(payment_data)
    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    return payment

@router.patch("/payments/{payment_id}", response_model=Payment, tags=["Payments"])
async def update_payment(payment_id: int, payment_data: PaymentUpdate, session: AsyncSession = Depends(get_async_session)): 

    payment = await session.get(Payment, payment_id)

    if not payment: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    payment_data_for_update = payment_data.model_dump(exclude_unset=True)

    for key, value in payment_data_for_update.items(): 

        setattr(payment, key, value)

    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    return payment

@router.delete("/payments/{payment_id}", response_model=dict, tags=["Payments"])
async def delete_payment(payment_id: int, session: AsyncSession = Depends(get_async_session)): 

    try: 
        payment = await session.get(Payment, payment_id)
    
        if not payment: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The payment with the id: {payment_id} wasn't found" )
        
        await session.delete(payment)
        await session.commit()

        return { "message": f"Payment with the id: {payment_id} removed sucessfully" }
    
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Details: {e}")
    
from db.models.customers import Customer
