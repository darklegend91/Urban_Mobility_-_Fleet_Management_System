import pytest

from ElectricScooter import ElectricScooter
from vehicle import Vehicle


@pytest.fixture
def scooter() -> ElectricScooter:
    return ElectricScooter(
        vehicle_id="SCOOTER-001",
        model="Ather 450X",
        battery_percentage=85.0,
        maintenance_status="On Trip",
        rental_price=450.0,
        max_speed_limit=80.0,
    )


def test_scooter_inherits_vehicle_and_exposes_scooter_data(
    scooter: ElectricScooter,
) -> None:
    assert isinstance(scooter, Vehicle)
    assert scooter.vehicle_id == "SCOOTER-001"
    assert scooter.max_speed_limit == 80.0


def test_scooter_speed_limit_can_be_updated(scooter: ElectricScooter) -> None:
    scooter.max_speed_limit = 75.5
    assert scooter.max_speed_limit == 75.5


@pytest.mark.parametrize("speed", [0, -0.01])
def test_scooter_rejects_non_positive_speed_limit(speed: float) -> None:
    with pytest.raises(ValueError, match="Speed Must be greater than 0"):
        ElectricScooter(
            "SCOOTER-X", "Invalid", 50, "Available", 300, speed
        )


@pytest.mark.parametrize(
    ("duration", "expected_cost"),
    [(0, 1.0), (1, 1.15), (30, 5.5), (12.5, 2.875)],
)
def test_scooter_trip_cost_uses_duration(
    duration: float,
    expected_cost: float,
    scooter: ElectricScooter,
) -> None:
    assert scooter.calculate_trip_cost(duration) == pytest.approx(expected_cost)


def test_scooter_string_adds_speed_limit(scooter: ElectricScooter) -> None:
    output = str(scooter)
    assert "Vehicle #SCOOTER-001 Details:" in output
    assert "Model: Ather 450X" in output
    assert "Maximum Speed Limit: 80.00" in output


def test_scooter_dictionary_adds_type_and_speed_limit(
    scooter: ElectricScooter,
) -> None:
    assert scooter.to_dict() == {
        "vehicle_id": "SCOOTER-001",
        "model": "Ather 450X",
        "battery_percentage": 85.0,
        "maintenance_status": "On Trip",
        "rental_price": 450.0,
        "type": "ElectricScooter",
        "max_speed_limit": 80.0,
    }
