from services import Service, SERVICE_TYPE, ACTIVITIES


def test_service_creation():
    service = Service(name="Yoga", type=SERVICE_TYPE.GroupClass, price=20.0)

    assert service.name == "Yoga"
    assert service.type == SERVICE_TYPE.GroupClass
    assert service.price == 20.0


def test_invalid_service_name():
    try:
        Service(
            name="InvalidActivity", type=SERVICE_TYPE.GroupClass, price=20.0
        )
        assert False, "Expected ValueError for invalid activity name"
    except ValueError as e:
        assert (
            str(e)
            == f"Invalid activity name: InvalidActivity. Must be one of {ACTIVITIES}"
        )


def test_invalid_service_type():
    try:
        Service(name="Yoga", type="InvalidType", price=20.0)
        assert False, "Expected ValueError for invalid service type"
    except ValueError as e:
        assert (
            str(e)
            == f"Invalid service type: InvalidType. Must be one of {SERVICE_TYPE}"
        )


def test_negative_price():
    try:
        Service(name="Yoga", type=SERVICE_TYPE.GroupClass, price=-10.0)
        assert False, "Expected ValueError for negative price"
    except ValueError as e:
        assert str(e) == "Price cannot be negative"
