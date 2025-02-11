from fastapi import status, APIRouter, HTTPException, Query
from db.models.rooms import Room, RoomCreate, RoomUpdate
from sqlmodel import select 
from db.db import SessionDep

router = APIRouter()

@router.get("/rooms", response_model=list[Room], tags=["Rooms"])
async def get_all_rooms(session: SessionDep,
        skip: int = Query(0, description="Reservations for omit"), 
        limit: int = Query(10, description="Reservationsfor show")): 

    rooms = session.exec(select(Room).offset(skip).limit(limit)).all()

    if not rooms: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return rooms

@router.get("/rooms/{room_id}", response_model=Room, tags=["Rooms"])
async def get_rooms_by_id(room_id: int, session: SessionDep): 

    room = session.get(Room, room_id)

    if not room: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return room

@router.post("/rooms/create", response_model=Room, tags=["Rooms"])
async def create_room(room_data: RoomCreate, session: SessionDep): 

    room = Room.model_validate(room_data.model_dump(exclude_unset=True))

    session.add(room)
    session.commit()
    session.refresh(room)

    return room 

@router.patch("/rooms/{room_id}", response_model=Room, tags=["Rooms"])
async def update_room(room_id: int, room_data: RoomUpdate, session: SessionDep): 

    room = session.get(Room, room_id)

    if not room: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    room_data_for_update = room_data.model_dump(exclude_unset=True)

    for key, value in room_data_for_update.items(): 

        setattr(room, key, value)

    session.add(room)
    session.commit()
    session.refresh(room)

    return room 

@router.delete("/rooms/{room_id}", tags=["Rooms"])
async def delete_room(room_id: int, session: SessionDep): 

    room = session.get(Room, room_id)

    if room.status == "ocuppied": 

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            description = "Room is occupied, you cant delete the room") 

    session.delete(room)
    session.commit()

    return {
        "message": f"Room with the id: {room_id} deleted sucesfully"
    }