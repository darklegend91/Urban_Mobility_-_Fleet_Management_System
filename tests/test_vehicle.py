from inspect import isabstract

import pytest

from vehicle import Vehicle

class ConcreteVehicle(Vehicle):

    def calculate_trip_cost(self, distance: float) -> float:
        return distance * self.rental_price


def make_vehicle(
    vehicle_id: str = "TEST-001",
    model: str = "Test Vehicle",
    battery_percentage: float = 50.0,
    maintenance_status: str = "Available",
    rental_price: float = 10.0,
) -> ConcreteVehicle:
    return ConcreteVehicle(
        vehicle_id=vehicle_id,
        model=model,
        battery_percentage=battery_percentage,
        maintenance_status=maintenance_status,
        rental_price=rental_price,
    )


def test_vehicle_is_abstract() -> None:
    assert isabstract(Vehicle)


def test_vehicle_class_updation() -> None:
    
    test_vehicle = make_vehicle()

    test_vehicle.vehicle_id = "TEST-002"
    test_vehicle.model = "Updated Model"
    test_vehicle.battery_percentage = 100.0
    test_vehicle.maintenance_status = "Under Maintenance"
    test_vehicle.rental_price = 0.0

    assert test_vehicle.vehicle_id == "TEST-002"
    assert test_vehicle.model == "Updated Model"
    assert test_vehicle.battery_percentage == 100.0
    assert test_vehicle.maintenance_status == "Under Maintenance"
    assert test_vehicle.rental_price == 0.0

@pytest.mark.parametrize("battery", [-0.01, 100.01])
def test_battery_percentage_rejects_values_outside_range(
    battery: float,
) -> None:
    with pytest.raises(ValueError, match="battery_percentage"):
        make_vehicle(battery_percentage=battery)


@pytest.mark.parametrize("battery , should_pass" , [
    (0.0 , True),
    (50.5 , True),
    (100.0 , True),
    (-1.1 , False),
    (101.0 , False)
])
def test_battery_precentage(battery:float , should_pass : bool) -> None:
    if should_pass:
        test_vehicle = make_vehicle(battery_percentage=battery)
        assert test_vehicle.battery_percentage == battery
    
    else:
        with pytest.raises(ValueError):
            make_vehicle(battery_percentage=battery)

# This test tell us what the value of maintance status should be passed
@pytest.mark.parametrize("status , should_pass",[
    ("Available" , True), 
    ("On Trip" , True), 
    ("Under Maintenance" , True),
    ("Not Avaialble" , False),
    ("Free" , False)],
)
def test_all_documented_maintenance_statuses_are_accepted(status: str , should_pass: bool) -> None:
    if should_pass:
        assert make_vehicle(maintenance_status=status).maintenance_status == status
    
    else:
        with pytest.raises(ValueError):
            make_vehicle(maintenance_status= status)

#This test tell us what the returned value of maintance status must be
def test_allowed_statuses_accessor_returns_expected_values() -> None:
    assert Vehicle.get_ALLOWED_STATUSES() == {
        "Available",
        "On Trip",
        "Under Maintenance",
    }

def test_negative_rental_price_is_rejected() -> None:
    vehicle = make_vehicle()

    with pytest.raises(ValueError, match="Negative"):
        vehicle.rental_price = -0.01

    assert vehicle.rental_price == 10.0


def test_vehicles_compare_by_vehicle_id() -> None:
    original = make_vehicle(vehicle_id="SAME-ID", model="First")
    same_id = make_vehicle(vehicle_id="SAME-ID", model="Second")
    other_id = make_vehicle(vehicle_id="OTHER-ID")

    assert original == same_id
    assert original != other_id
    assert original != "SAME-ID"


def test_common_string_and_dictionary_representations() -> None:
    vehicle = make_vehicle()

    assert str(vehicle) == (
        "Vehicle #TEST-001 Details:\n"
        "  Model: Test Vehicle\n"
        "  Battery: 50.00%\n"
        "  Status: Available\n"
        "  Rental Price: 10.00"
    )
    assert vehicle.to_dict() == {
        "vehicle_id": "TEST-001",
        "model": "Test Vehicle",
        "battery_percentage": 50.0,
        "maintenance_status": "Available",
        "rental_price": 10.0,
    }
