from sqlmodel import SQLModel, Relationship, Field
from common.types.payments_type import ReservationsTypesEnum, RoomStatusEnum
from pydantic import BaseModel
from typing import Optional


class RoomCreate(BaseModel): 

    number: int 
    type_room: ReservationsTypesEnum
    status: RoomStatusEnum 

class Room(SQLModel, table=True): 

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    number: int 
    type_room: ReservationsTypesEnum
    status: RoomStatusEnum
    reservation: Optional["Reservation"] = Relationship(back_populates="room")

class RoomUpdate(BaseModel): 

    number: Optional[int] 
    type_room: Optional[ReservationsTypesEnum]
    status: Optional[RoomStatusEnum]


from .reservations import Reservation