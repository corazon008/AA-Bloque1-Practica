import re
from enum import Enum
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List

from src.service import Service, SERVICE_TYPE, COST_TYPE
from src.reservation import Reservation, STATUS

DB_PATH = Path(__file__).parent / "reservations.csv"
DB_PATH_TEST = Path(__file__).parent / "reservations_test.csv"


class ReservationManager:
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.db_path = DB_PATH_TEST if test_mode else DB_PATH
        self.reservations: List[Reservation] = []
        self.load_reservations()

    def new_reservation(
        self,
        name: str,
        service: Service,
        date: datetime,
        duration: float,
    ) -> int:
        """
        Creates a new reservation and saves it to the CSV file.
        Args:
            name (str): Name of the reservation.
            service (Service): Service associated with the reservation.
            date (datetime): Date and time of the reservation.
            duration (float): Duration of the reservation in hours or number of sessions, depending on the service's cost type.
        Returns:
            int: The ID of the newly created reservation.
        """
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
        if self.db_path.exists():
            df = pd.read_csv(self.db_path)
            for _, row in df.iterrows():
                reservation = Reservation.from_dict(row)
                self.reservations.append(reservation)

    def save_reservations(self):
        data = []
        self.reservations.sort(key=lambda r: r.ID)  # Ensure consistent order
        for reservation in self.reservations:
            data.append(reservation.to_dict())
        df = pd.DataFrame(data)
        df.to_csv(self.db_path, index=False)
