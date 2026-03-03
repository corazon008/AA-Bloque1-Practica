from enum import Enum
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List

from src.service import Service, SERVICE_TYPE, COST_TYPE


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
        cost: float = None,
        status: STATUS = STATUS.pending,
    ):
        """
        Initializes a new reservation.
        Args:
            ID (int): Unique identifier for the reservation.
            name (str): Name of the reservation.
            service (Service): Service associated with the reservation.
            date (datetime): Date and time of the reservation.
            duration (float): Duration of the reservation in hours or number of sessions, depending on the service's cost type.
            cost (float, optional): Cost of the reservation. If not provided, it will be calculated based on the service and duration. Only use for restoring from CSV. Defaults to None.
            status (STATUS, optional): Status of the reservation. Defaults to STATUS.pending.
        """
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
        if cost is None:
            self.cost = service.price * duration
        else:
            self.cost = cost
        self.status = status

    def change_status(self, new_status: STATUS):
        if not isinstance(new_status, STATUS):
            raise ValueError(f"New status must be one of {STATUS}")
        self.status = new_status

        # If cancellation happens less than 24 hours before the reservation, apply a penalty of 20%
        if new_status == STATUS.cancelled and (
            self.date - datetime.now() < pd.Timedelta(hours=24)
        ):
            self.cost *= 0.2
        else:
            self.cost = 0

    def to_dict(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "service_name": self.service.name,
            "service_type": self.service.type.name,
            "service_price": self.service.price,
            "service_cost_type": self.service.cost_type.name,
            "date": self.date.strftime("%Y-%m-%d"),
            "duration": self.duration,
            "cost": self.cost,
            "status": self.status.name,
        }

    @staticmethod
    def from_dict(data: dict) -> "Reservation":
        return Reservation(
            ID=data["ID"],
            name=data["name"],
            service=Service(
                name=data["service_name"],
                type=SERVICE_TYPE[data["service_type"]],
                price=data["service_price"],
                cost_type=COST_TYPE[data["service_cost_type"]],
            ),
            date=datetime.strptime(data["date"], "%Y-%m-%d"),
            duration=data["duration"],
            cost=data["cost"],
            status=STATUS[data["status"]],
        )

    def __str__(self):
        return f"ID: {self.ID}, Name: {self.name}, Service: {self.service.name}, Date: {self.date.strftime('%Y-%m-%d')}, Duration: {self.duration}, Cost: {self.cost}, Status: {self.status.name}"
