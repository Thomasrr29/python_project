from .customers import router as customer_router
from .payments import router as payments_router 
from .reservations import router as reservations_router
from .rooms import router as rooms_router 

__all__ = ["customer_router", "payments_router", "reservations_router", "rooms_router"]