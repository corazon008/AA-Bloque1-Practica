from src.reservation_manager import ReservationManager
from src.services import Service, SERVICE_TYPE
from datetime import datetime

if __name__ == "__main__":
    manager = ReservationManager()
    print("Current reservations:", manager.get_all_reservations())

    # Create a new reservation
    manager.new_reservation(
        name="John Doe",
        service=Service(name="Yoga", type=SERVICE_TYPE.GroupClass, price=20.0),
        date=datetime.strptime("2024-07-01", "%Y-%m-%d"),
        duration=3.0,
    )
