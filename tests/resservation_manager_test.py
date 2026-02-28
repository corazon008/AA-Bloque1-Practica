from reservation_manager import ReservationManager
from services import Service, SERVICE_TYPE, COST_TYPE
from reservation import STATUS
from datetime import datetime
import pandas as pd
import pytest


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


def test_penalty_on_cancellation():
    manager = ReservationManager()
    service = Service(name="Yoga", type=SERVICE_TYPE.GroupClass, price=20.0)
    date = datetime.now() + pd.Timedelta(hours=23)  # Less than 24 hours away
    r_id = manager.new_reservation(
        name="Jane Doe",
        service=service,
        date=date,
        duration=2.0,
    )

    manager.change_reservation_status(r_id, STATUS.cancelled)

    assert (
        manager.get_reservation_by_id(r_id).cost == 8.0
    )  # 20% of original cost (40.0)

    del manager

    # Check that the penalty is applied correctly even after reloading reservations
    new_manager = ReservationManager()
    loaded_reservation = new_manager.get_reservation_by_id(r_id)
    assert loaded_reservation is not None
    assert loaded_reservation.cost == 8.0  # Penalty should persist after reload


if __name__ == "__main__":
    pytest.main([__file__])
    print("All tests passed!")
