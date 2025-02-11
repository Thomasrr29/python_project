from sqlmodel import Field, SQLModel, Relationship 
from common.types.payments_type import ReservationsTypesEnum, PaymentMethodsEnum
from pydantic import BaseModel
from typing import Optional


class PaymentBase(BaseModel): 

    reservation_type: ReservationsTypesEnum 
    amount: int 

class PaymentCreate(BaseModel):

    reservation_type: ReservationsTypesEnum 
    payment_method: PaymentMethodsEnum
    amount: int 

class Payment(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    reservation_type: ReservationsTypesEnum 
    payment_method: PaymentMethodsEnum
    amount: int 
    customer_id: int = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="payments")
    reservation: "Reservation" = Relationship(back_populates="payment")

class PaymentUpdate(BaseModel): 

    reservation_type: Optional[ReservationsTypesEnum] 
    amount: Optional[int] 

from .customers import Customer
from .reservations import Reservation

 