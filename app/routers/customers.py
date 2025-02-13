from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.customers import Customer, CustomerCreate, CustomerUpdate
from db.db import get_async_session
from decorators import validate_customer_existence



router = APIRouter()

@router.get("/customer", tags=["Customers"])
async def get_customers(
        session: AsyncSession = Depends(get_async_session),
        skip: int = Query(0, description="Registers for omit"),
        limit: int = Query(10, description="Registers number")): 

    customers = await session.execute(select(Customer).offset(skip).limit(limit))
    result = customers.scalars().all()
    
    return result 

@router.get("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def get_customer_by_id(
        customer_id: int, 
        session: AsyncSession = Depends(get_async_session)): 

    customer = await session.get(Customer, customer_id)

    if not customer: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return customer 

@router.get("/customers/identification/{identification}", response_model=Customer, tags=["Customers"])
async def get_customer_by_identification(
            identification: int, 
            session: AsyncSession = Depends(get_async_session)): 

    result = await session.execute(select(Customer).where(Customer.identification == identification))
    customer = result.scalars().first()

    if customer is None: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Customer not found by identification: {identification}") 
    
    return customer 

@router.post("/customers/create", tags=['Customers'])
@validate_customer_existence
async def create_customer(
    customer_data:CustomerCreate, 
    session: AsyncSession = Depends(get_async_session)): 

    customer = Customer.model_validate(customer_data.model_dump(exclude_unset=True))

    session.add(customer)
    await session.commit()
    await session.refresh(customer)

    return customer

@router.patch("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def update_customer(
            customer_id: int,
            customer_update_data: CustomerUpdate, 
            session: AsyncSession = Depends(get_async_session)): 

    customer = await session.get(Customer, customer_id)

    if not customer: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The customer by the id: {customer_id} wasnt found")

    update_data = customer_update_data.model_dump(exclude_unset=True)

    for key, value in update_data.items(): 

        setattr(customer, key, value)
    
    session.add(customer)
    await session.commit()
    await session.refresh(customer)

    return customer

@router.delete("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def delete_customer(
            customer_id: int, 
            session: AsyncSession = Depends(get_async_session)): 

    customer = await session.get(Customer, customer_id)

    if not customer: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Customer with the id: {customer_id} wasnt found")

    await session.delete(customer)
    await session.commit()

    return {

        "message": f"The customer with the id: {customer_id} was removed sucessfully"
    }