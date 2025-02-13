from sqlmodel import Field, SQLModel, Relationship 
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from common.types.payments_type import ReservationStatusEnum
from datetime import date 

class ReservationCreate(BaseModel): 

    start: date 
    end: date 
    room_id: int
    status: ReservationStatusEnum
    customer: "CustomerCreate"
    payment: "PaymentCreate"
    
class Reservation(SQLModel, table=True): 

    id: int = Field(default=None, unique=True, primary_key=True)
    start: date 
    end: date
    customer_id: int = Field(foreign_key="customer.id") 
    payment_id:  int = Field(foreign_key="payment.id")
    room_id: int = Field(foreign_key="room.id")
    status: ReservationStatusEnum
    customer: "Customer" = Relationship(back_populates="reservations")
    payment: "Payment" = Relationship(back_populates="reservation")
    room: "Room" = Relationship(back_populates="reservation") 

class ReservationUpdate(BaseModel): 

    start: Optional[date] = None
    end: Optional[date] = None 
    status: Optional[ReservationStatusEnum] = None

from .customers import Customer, CustomerCreate
from .payments import Payment, PaymentCreate
from .rooms import Room

ReservationCreate.model_rebuild()