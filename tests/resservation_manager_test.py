from reservation_manager import ReservationManager
from services import Service, SERVICE_TYPE
from datetime import datetime


def test_reservation_manager():
    manager = ReservationManager()
    initial_count = len(manager.get_all_reservations())

    service = Service(name="Yoga", type=SERVICE_TYPE.GroupClass, price=20.0)
    date = datetime.strptime("2024-07-01", "%Y-%m-%d")
    manager.new_reservation(
        name="John Doe",
        service=service,
        date=date,
        duration=3.0,
    )

    reservations = manager.get_all_reservations()
    assert len(reservations) == initial_count + 1
    assert reservations[-1].name == "John Doe"
    assert reservations[-1].service.name == "Yoga"
    assert reservations[-1].date == date
    assert reservations[-1].duration == 3.0
