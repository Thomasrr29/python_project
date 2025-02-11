from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db.models.customers import Customer, CustomerCreate, CustomerUpdate
from db.db import SessionDep 


router = APIRouter()

@router.get("/customer", response_model=list[Customer], tags=["Customers"])
async def get_customers(
        session: SessionDep,
        skip: int = Query(0, description="Registers for omit"),
        limit: int = Query(10, description="Registers number")): 

    customers = session.exec(select(Customer).offset(skip).limit(limit)).all()
    return customers 

@router.get("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def get_customer_by_id(customer_id: int, session: SessionDep): 

    customer = session.get(Customer, customer_id)

    if not customer: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return customer 

@router.get("/customers/identification/{identification}", response_model=Customer, tags=["Customers"])
async def get_customer_by_identification(identification: int, session: SessionDep): 

    customer = session.exec(select(Customer).where(Customer.identification == identification)).first()

    if customer is None: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Customer not found by identification: {identification}") 
    
    return customer 

@router.post("/customers/create", tags=['Customers'])
async def create_customer(customer_data:CustomerCreate, session: SessionDep): 

    customer = Customer.model_validate(customer_data.model_dump(exclude_unset=True))

    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer

@router.patch("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def update_customer(customer_id: int, customer_update_data: CustomerUpdate, session: SessionDep): 

    customer = session.get(Customer, customer_id)

    if not customer: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The customer by the id: {customer_id} wasnt found")

    update_data = customer_update_data.model_dump(exclude_unset=True)

    for key, value in update_data.items(): 

        setattr(customer, key, value)
    
    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer

@router.delete("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def delete_customer(customer_id: int, session:SessionDep): 

    customer = session.get(Customer, customer_id)

    if not customer: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            description=f"Customer with the id: {customer_id} wasnt found")

    session.delete(customer)
    session.commit()

    return {

        "message": f"The customer with the id: {customer_id} was removed sucessfully"
    }