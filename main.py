from src.reservation_manager import ReservationManager
from src.reservation import Reservation, STATUS
from src.services import Service, SERVICE_TYPE
from datetime import datetime

if __name__ == "__main__":
    manager = ReservationManager()
    print("Current reservations:", manager.get_all_reservations())

    # Create a new reservation
    new_reservation = Reservation(
        ID=1,
        name="John Doe",
        service=Service(name="Yoga", type=SERVICE_TYPE.GroupClass, price=20.0),
        date=datetime.strptime("2024-07-01", "%Y-%m-%d"),
        duration=3.0,
    )
    manager.new_reservation(new_reservation)
