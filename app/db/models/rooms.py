from sqlmodel import SQLModel, Relationship, Field
from common.types.payments_type import RoomsTypesEnum, RoomStatusEnum
from pydantic import BaseModel
from typing import Optional


class RoomCreate(BaseModel): 

    number: int 
    type_room: RoomsTypesEnum
    status: RoomStatusEnum 

class Room(SQLModel, table=True): 

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    number: int 
    type_room: RoomsTypesEnum
    status: RoomStatusEnum
    reservation: Optional["Reservation"] = Relationship(back_populates="room")

class RoomUpdate(BaseModel): 

    number: Optional[int] = None
    type_room: Optional[RoomsTypesEnum] = None 
    status: Optional[RoomStatusEnum] = None


from .reservations import Reservation