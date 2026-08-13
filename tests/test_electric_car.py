import pytest

from ElectricCar import ElectricCar
from vehicle import Vehicle

@pytest.fixture
def car() -> ElectricCar:
    return ElectricCar(
        vehicle_id="CAR-001",
        model="Tata Nexon EV",
        battery_percentage=92.5,
        maintenance_status="Available",
        rental_price=1800.0,
        seating_capacity=5,
    )

def test_car_inherits_vehicle_and_exposes_car_data(car: ElectricCar) -> None:
    assert isinstance(car, Vehicle)
    assert car.vehicle_id == "CAR-001"
    assert car.seating_capacity == 5


def test_car_seating_capacity_can_be_updated(car: ElectricCar) -> None:
    car.seating_capacity = 4
    assert car.seating_capacity == 4


@pytest.mark.parametrize("capacity", [0, -1])
def test_car_rejects_non_positive_seating_capacity(capacity: int) -> None:
    with pytest.raises(ValueError, match="Seating capacity"):
        ElectricCar("CAR-X", "Invalid", 50, "Available", 1000, capacity)


@pytest.mark.parametrize(
    ("distance", "expected_cost"),
    [(0, 5.0), (1, 5.5), (100, 55.0), (12.5, 11.25)],
)
def test_car_trip_cost_uses_distance(
    distance: float,
    expected_cost: float,
    car: ElectricCar,
) -> None:
    assert car.calculate_trip_cost(distance) == pytest.approx(expected_cost)


def test_car_string_adds_seating_capacity(car: ElectricCar) -> None:
    output = str(car)
    assert "Vehicle #CAR-001 Details:" in output
    assert "Model: Tata Nexon EV" in output
    assert "Seating Capacity: 5" in output


def test_car_dictionary_adds_type_and_seating_capacity(car: ElectricCar) -> None:
    assert car.to_dict() == {
        "vehicle_id": "CAR-001",
        "model": "Tata Nexon EV",
        "battery_percentage": 92.5,
        "maintenance_status": "Available",
        "rental_price": 1800.0,
        "type": "ElectricCar",
        "seating_capacity": 5,
    }
