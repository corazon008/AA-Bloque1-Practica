from enum import Enum
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List

from services import Service, SERVICE_TYPE, COST_TYPE


class STATUS(Enum):
    confirmed = 1
    pending = 2
    cancelled = 3
    completed = 4


class Reservation:
    def __init__(
        self,
        ID: int,
        name: str,
        service: Service,
        date: datetime,
        duration: float,
        status: STATUS = STATUS.pending,
    ):
        # Check for valid data
        if ID <= 0:
            raise ValueError("ID must be a positive integer")
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")
        if not isinstance(service, Service):
            raise ValueError("Service must be an instance of Service class")
        if not isinstance(date, datetime):
            raise ValueError("Date must be a datetime object")
        if duration <= 0:
            raise ValueError("Duration must be a positive number")
        if not isinstance(status, STATUS):
            raise ValueError(f"Status must be one of {STATUS}")

        self.ID = ID
        self.name = name
        self.service = service
        self.date = date
        self.duration = duration
        if service.cost_type == COST_TYPE.PerHour:
            self.cost = service.price * duration
        else:
            self.cost = service.price
        self.status = status

    def change_status(self, new_status: STATUS):
        if not isinstance(new_status, STATUS):
            raise ValueError(f"New status must be one of {STATUS}")
        self.status = new_status
