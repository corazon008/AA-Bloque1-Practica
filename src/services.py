from enum import Enum


class SERVICE_TYPE(Enum):
    GroupClass = 1
    PersonalTraining = 2
    OpenGym = 3


class COST_TYPE(Enum):
    PerHour = 1
    PerSession = 2


ACTIVITIES = [
    "Yoga",
    "Rollerblading",
    "Boxing",
    "Crossfit",
    "Zumba",
    "Pilates",
    "Spinning",
]


class Service:
    def __init__(
        self,
        name: str,
        type: SERVICE_TYPE,
        price: float,
        cost_type: COST_TYPE = COST_TYPE.PerHour,
    ):
        # Check for valid data
        if name not in ACTIVITIES:
            raise ValueError(
                f"Invalid activity name: {name}. Must be one of {ACTIVITIES}"
            )
        if not isinstance(type, SERVICE_TYPE):
            raise ValueError(
                f"Invalid service type: {type}. Must be one of {SERVICE_TYPE}"
            )
        if price < 0:
            raise ValueError("Price cannot be negative")
        if not isinstance(cost_type, COST_TYPE):
            raise ValueError(
                f"Invalid cost type: {cost_type}. Must be one of {COST_TYPE}"
            )

        self.name = name
        self.type = type
        self.price = price
        self.cost_type = cost_type
