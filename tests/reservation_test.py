from datetime import datetime
import pandas as pd
from reservation import Reservation, STATUS
from services import Service, SERVICE_TYPE
import pytest

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


def test_change_status():
    reservation = Reservation(
        ID=1,
        name="John Doe",
        service=service,
        date=date,
        duration=3.0,
    )
    reservation.change_status(STATUS.confirmed)
    assert reservation.status == STATUS.confirmed

    try:
        reservation.change_status("InvalidStatus")
        assert False, "Expected ValueError for invalid new status"
    except ValueError as e:
        assert str(e) == f"New status must be one of {STATUS}"


def test_penalty_on_cancellation():
    reservation = Reservation(
        ID=1,
        name="John Doe",
        service=service,
        date=datetime.now() + pd.Timedelta(hours=23),  # Less than 24 hours away
        duration=3.0,
    )
    reservation.change_status(STATUS.cancelled)
    assert reservation.cost == 60.0 * 0.2  # 20% penalty applied

    reservation = Reservation(
        ID=2,
        name="Jane Doe",
        service=service,
        date=datetime.now() + pd.Timedelta(hours=25),  # More than 24 hours away
        duration=3.0,
    )
    reservation.change_status(STATUS.cancelled)
    assert reservation.cost == 0.0  # No penalty applied