
from sqlmodel import select 
from db.models import CustomerCreate, Customer
from functools import wraps 
from fastapi import HTTPException, status, Depends
from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

def validate_customer_existence(func): 

    @wraps(func)
    async def wrapper(customer_data: CustomerCreate, *args, session: AsyncSession = Depends(get_async_session)): 

        result = await session.execute(select(Customer)
        .where(Customer.identification == customer_data.identification))
        customer = result.one_or_none()
        
        print("The customer is: ", customer)

        if customer: 

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer with the identification: {customer.identification} already exists")
            
        print(f"✅ Executing function: {func.__name__} with customer_data: {customer_data}")
        return await func(customer_data, session)

        
    return wrapper