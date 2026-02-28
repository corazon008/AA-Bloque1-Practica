import re
from enum import Enum
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List

from services import Service, SERVICE_TYPE, COST_TYPE
from reservation import Reservation, STATUS

DB_PATH = Path(__file__).parent / "reservations.csv"


class ReservationManager:
    def __init__(self):
        self.reservations: List[Reservation] = []
        self.load_reservations()

    def new_reservation(
        self,
        name: str,
        service: Service,
        date: datetime,
        duration: float,
    ) -> int:
        new_id = max((res.ID for res in self.reservations), default=0) + 1
        self.reservations.append(
            Reservation(new_id, name, service, date, duration)
        )
        self.save_reservations()
        return new_id

    def get_all_reservations(self) -> List[Reservation]:
        return self.reservations

    def get_reservation_by_id(self, reservation_id: int) -> Reservation:
        for reservation in self.reservations:
            if reservation.ID == reservation_id:
                return reservation
        return None

    def get_all_profit(self) -> float:
        return sum(
            reservation.cost
            for reservation in self.reservations
            if reservation.status == STATUS.confirmed
        )

    def change_reservation_status(
        self, reservation_id: int, new_status: STATUS
    ) -> bool:
        reservation = self.get_reservation_by_id(reservation_id)
        if reservation:
            reservation.change_status(new_status)
            self.save_reservations()
            return True
        return False

    def load_reservations(self):
        if DB_PATH.exists():
            df = pd.read_csv(DB_PATH)
            for _, row in df.iterrows():
                reservation = Reservation(
                    ID=row["ID"],
                    name=row["name"],
                    service=Service(
                        name=row["service_name"],
                        type=SERVICE_TYPE[row["service_type"]],
                        price=row["service_price"],
                        cost_type=COST_TYPE[row["service_cost_type"]],
                    ),
                    date=datetime.strptime(row["date"], "%Y-%m-%d"),
                    duration=row["duration"],
                    cost=row["cost"],
                    status=STATUS[row["status"]],
                )
                self.reservations.append(reservation)

    def save_reservations(self):
        data = []
        self.reservations.sort(key=lambda r: r.ID)  # Ensure consistent order
        for reservation in self.reservations:
            data.append(
                {
                    "ID": reservation.ID,
                    "name": reservation.name,
                    "service_name": reservation.service.name,
                    "service_type": reservation.service.type.name,
                    "service_price": reservation.service.price,
                    "service_cost_type": reservation.service.cost_type.name,
                    "date": reservation.date.strftime("%Y-%m-%d"),
                    "duration": reservation.duration,
                    "cost": reservation.cost,
                    "status": reservation.status.name,
                }
            )
        df = pd.DataFrame(data)
        df.to_csv(DB_PATH, index=False)
