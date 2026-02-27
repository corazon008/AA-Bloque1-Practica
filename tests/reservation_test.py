from datetime import datetime
from reservation import Reservation, STATUS
from services import Service, SERVICE_TYPE

service = Service(name="Yoga", type=SERVICE_TYPE.GroupClass, price=20.0)
date = datetime.strptime("2024-07-01", "%Y-%m-%d")


def test_reservation_creation():
    reservation = Reservation(
        ID=1,
        name="John Doe",
        service=service,
        date=date,
        duration=3.0,
    )

    assert reservation.ID == 1
    assert reservation.name == "John Doe"
    assert reservation.duration == 3.0
    assert reservation.status == STATUS.pending
    assert reservation.cost == 60.0


def test_invalid_reservation_ID():
    try:
        Reservation(
            ID=-1,
            name="John Doe",
            service=service,
            date=date,
            duration=3.0,
        )
        assert False, "Expected ValueError for negative ID"
    except ValueError as e:
        assert str(e) == "ID must be a positive integer"


def test_invalid_reservation_name():
    try:
        Reservation(
            ID=1,
            name="",
            service=service,
            date=date,
            duration=3.0,
        )
        assert False, "Expected ValueError for empty name"
    except ValueError as e:
        assert str(e) == "Name must be a non-empty string"


def test_invalid_reservation_service():
    try:
        Reservation(
            ID=1,
            name="John Doe",
            service="InvalidService",
            date=date,
            duration=3.0,
        )
        assert False, "Expected ValueError for invalid service"
    except ValueError as e:
        assert str(e) == "Service must be an instance of Service class"


def test_invalid_reservation_date():
    try:
        Reservation(
            ID=1,
            name="John Doe",
            service=service,
            date="2024-07-01",
            duration=3.0,
        )
        assert False, "Expected ValueError for invalid date"
    except ValueError as e:
        assert str(e) == "Date must be a datetime object"


def test_invalid_reservation_duration():
    try:
        Reservation(
            ID=1,
            name="John Doe",
            service=service,
            date=date,
            duration=-1.0,
        )
        assert False, "Expected ValueError for negative duration"
    except ValueError as e:
        assert str(e) == "Duration must be a positive number"


def test_invalid_reservation_status():
    try:
        Reservation(
            ID=1,
            name="John Doe",
            service=service,
            date=date,
            duration=3.0,
            status="InvalidStatus",
        )
        assert False, "Expected ValueError for invalid status"
    except ValueError as e:
        assert str(e) == f"Status must be one of {STATUS}"
