from sqlmodel import Field, SQLModel, Relationship 
from common.types.payments_type import ReservationStatusEnum, PaymentMethodsEnum, RoomsTypesEnum
from pydantic import BaseModel
from typing import Optional

class PaymentCreate(BaseModel):

    payment_method: PaymentMethodsEnum
    customer_id: int
    amount: int 

class Payment(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    payment_method: PaymentMethodsEnum
    amount: int 
    customer_id: int = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="payments")
    reservation: "Reservation" = Relationship(back_populates="payment")

class PaymentUpdate(BaseModel): 

    payment_method: Optional[int] 

from .customers import Customer
from .reservations import Reservation

 