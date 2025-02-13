from fastapi import FastAPI
from db.models import Customer, Reservation, Payment, Room
from routers import customer_router, payments_router, reservations_router, rooms_router
from db.db import create_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI): 

    print("Creando todas las tablas")
    await create_tables()

    yield
    print("Application closing.....")

app = FastAPI(lifespan=lifespan)

app.include_router(customer_router)
app.include_router(payments_router)
app.include_router(reservations_router)
app.include_router(rooms_router)

app.get("/")
def read_root(): 
    return {"Hello":"world"}