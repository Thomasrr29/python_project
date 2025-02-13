from enum import Enum 

class RoomsTypesEnum(str, Enum):

    BASIC="basic"
    PREMIUM="premium"
    LUXURY="luxury"

class ReservationStatusEnum(str, Enum): 

    CANCELLED = "cancelled"
    VALID = "valid"

class RoomStatusEnum(str, Enum): 

    OCUPPIED="ocuppied"
    AVAILABLE="available"
    CLEANING="cleaning"

class PaymentMethodsEnum(str, Enum): 

    CASH="cash"
    DEBIT="debit"
    CREDIT="credit"


