from sqlmodel import Field, SQLModel, Relationship 
from pydantic import BaseModel
from typing import Optional, List
from datetime import date 

class CustomerBase(BaseModel): 

    name: str
    identification: int

class CustomerCreate(CustomerBase): 

    date_birth: date
    
class Customer(SQLModel, table=True): 

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str 
    identification: int 
    date_birth: date
    payments: list['Payment'] = Relationship(back_populates="customer")  
    reservations: list['Reservation'] = Relationship(back_populates="customer")

class CustomerUpdate(BaseModel): 

    name: Optional[str] = None
    identification: Optional[int] = None
    date_birth: Optional[date] = None
   
    

from .reservations import Reservation
from .payments import Payment