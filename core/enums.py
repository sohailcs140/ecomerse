import enum


class PaymentStatus(enum.Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"


class PaymentType(enum.Enum):
    COD = "COD"
    GATEWAY = "Gateway"


class OrderStatus(enum.Enum):
    PLACED = "Placed"
    ON_THE_WAY = "On The Way"
    DELIVERED = "Delivered"


class CouponType(enum.Enum):
    VALUE = "Value"
    PERCENTAGE = "Percentage"

