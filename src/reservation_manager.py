from enum import Enum
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List

from src.services import Service, SERVICE_TYPE
from src.reservation import Reservation, STATUS

DB_PATH = Path(__file__).parent / "reservations.csv"


class ReservationManager:
    def __init__(self):
        self.reservations: List[Reservation] = []
        self.load_reservations()

    def new_reservation(self, reservation: Reservation):
        self.reservations.append(reservation)
        self.save_reservations()

    def get_all_reservations(self):
        return self.reservations

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
                    ),
                    date=datetime.strptime(row["date"], "%Y-%m-%d"),
                    duration=row["duration"],
                    status=STATUS[row["status"]],
                )
                self.reservations.append(reservation)

    def save_reservations(self):
        data = []
        for reservation in self.reservations:
            data.append(
                {
                    "ID": reservation.ID,
                    "name": reservation.name,
                    "service_name": reservation.service.name,
                    "service_type": reservation.service.type.name,
                    "service_price": reservation.service.price,
                    "date": reservation.date.strftime("%Y-%m-%d"),
                    "duration": reservation.duration,
                    "status": reservation.status.name,
                }
            )
        df = pd.DataFrame(data)
        df.to_csv(DB_PATH, index=False)
