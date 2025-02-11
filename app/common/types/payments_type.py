from enum import Enum 

class ReservationsTypesEnum(str, Enum):

    BASIC="basic"
    PREMIUM="premium"
    LUXURY="luxury"


class RoomStatusEnum(str, Enum): 

    OCUPPIED="ocuppied"
    AVAILABLE="available"
    CLEANING="cleaning"


class PaymentMethodsEnum(str, Enum): 

    CASH="cash"
    DEBIT="debit"
    CREDIT="credit"


