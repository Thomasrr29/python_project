from fastapi import status, APIRouter, HTTPException, Query, Depends
from db.models.rooms import Room, RoomCreate, RoomUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select 
from db.db import get_async_session

router = APIRouter()

@router.get("/rooms", response_model=list[Room], tags=["Rooms"])
async def get_all_rooms(session: AsyncSession = Depends(get_async_session),
        skip: int = Query(0, description="Reservations for omit"), 
        limit: int = Query(10, description="Reservationsfor show")): 

    result = await session.execute(select(Room).offset(skip).limit(limit))
    rooms = result.scalars().all()

    if not rooms: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return rooms

@router.get("/rooms/{room_id}", response_model=Room, tags=["Rooms"])
async def get_rooms_by_id(room_id: int, session: AsyncSession = Depends(get_async_session)): 

    room = await session.get(Room, room_id)

    if not room: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return room

@router.post("/rooms/create", response_model=Room, tags=["Rooms"])
async def create_room(room_data: RoomCreate, session: AsyncSession = Depends(get_async_session)): 

    room = Room.model_validate(room_data.model_dump(exclude_unset=True))

    session.add(room)
    await session.commit()
    await session.refresh(room)

    return room 

@router.patch("/rooms/{room_id}", response_model=Room, tags=["Rooms"])
async def update_room(room_id: int, room_data: RoomUpdate, session: AsyncSession = Depends(get_async_session)): 

    room = await session.get(Room, room_id)

    if not room: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    room_data_for_update = room_data.model_dump(exclude_unset=True)

    for key, value in room_data_for_update.items(): 

        setattr(room, key, value)

    session.add(room)
    await session.commit()
    await session.refresh(room)

    return room 

@router.delete("/rooms/{room_id}", response_model=dict, tags=["Rooms"])
async def delete_room(room_id: int, session: AsyncSession = Depends(get_async_session)): 

    room = await session.get(Room, room_id)

    if not room: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Room with the id: {room_id} wasnt found") 

    if room.status == "ocuppied": 

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail = "Room is occupied, you cant delete the room") 

    await session.delete(room)
    await session.commit()

    return {
        "message": f"Room with the id: {room_id} deleted sucesfully"
    }