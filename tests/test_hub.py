import pytest

from ElectricCar import ElectricCar
from ElectricScooter import ElectricScooter
from Hub import Hub


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


def test_new_hub_has_a_name_and_no_vehicles() -> None:
    hub = Hub("Central")
    assert hub.name == "Central"
    assert hub.vehicles == []
    assert str(hub) == "Hub: Central\nNo vehicles found"


def test_add_and_find_vehicle(
    car: ElectricCar,
    capsys: pytest.CaptureFixture[str],
) -> None:
    hub = Hub("Central")
    hub.add_vehicle(car)

    assert hub.find_vehicle("CAR-001") is car
    assert hub.find_vehicle("UNKNOWN") is None
    assert "CAR-001 is added to Central" in capsys.readouterr().out


def test_duplicate_vehicle_id_is_rejected(car: ElectricCar) -> None:
    hub = Hub("Central")
    duplicate = ElectricCar(
        "CAR-001", "Different Model", 75, "Available", 1000, 4
    )
    hub.add_vehicle(car)

    with pytest.raises(ValueError, match="already in Central"):
        hub.add_vehicle(duplicate)

    assert hub.vehicles == [car]


def test_remove_vehicle_returns_removed_object(
    car: ElectricCar,
    capsys: pytest.CaptureFixture[str],
) -> None:
    hub = Hub("Central")
    hub.add_vehicle(car)
    capsys.readouterr()

    assert hub.remove_vehicle("CAR-001") is car
    assert hub.vehicles == []
    assert "Vehicle CAR-001 removed from Central" in capsys.readouterr().out


def test_remove_missing_vehicle_raises_error() -> None:
    hub = Hub("Central")
    with pytest.raises(ValueError, match="Vehicle UNKNOWN not found"):
        hub.remove_vehicle("UNKNOWN")


def test_sort_vehicles_supports_all_options_without_mutating(
    car: ElectricCar,
    scooter: ElectricScooter,
) -> None:
    middle = ElectricCar(
        "CAR-002", "MG Comet", 70, "Under Maintenance", 1200, 4
    )
    hub = Hub("Central")
    for vehicle in (car, scooter, middle):
        hub.add_vehicle(vehicle)
    insertion_order = list(hub.vehicles)

    assert hub.sort_vehicles("model") == [scooter, middle, car]
    assert hub.sort_vehicles("battery") == [car, scooter, middle]
    assert hub.sort_vehicles("fare") == [car, middle, scooter]
    assert hub.sort_vehicles_aplhabetical() == [scooter, middle, car]
    assert hub.vehicles == insertion_order


def test_model_sorting_is_case_insensitive(
    car: ElectricCar,
    scooter: ElectricScooter,
) -> None:
    car.model = "zebra"
    scooter.model = "Alpha"
    hub = Hub("Central")
    hub.add_vehicle(car)
    hub.add_vehicle(scooter)

    assert hub.sort_vehicles() == [scooter, car]


def test_invalid_sort_option_is_rejected() -> None:
    with pytest.raises(ValueError, match="Sort option must be"):
        Hub("Central").sort_vehicles("speed")


def test_hub_string_sorts_full_vehicle_details(
    car: ElectricCar,
    scooter: ElectricScooter,
) -> None:
    hub = Hub("Central")
    hub.add_vehicle(car)
    hub.add_vehicle(scooter)

    output = str(hub)
    assert output.index("Ather 450X") < output.index("Tata Nexon EV")
    assert output.count("Vehicle #") == 2
    assert "Vehicles sorted by model" in output


def test_hub_dictionary_contains_nested_vehicle_data(
    car: ElectricCar,
    scooter: ElectricScooter,
) -> None:
    hub = Hub("Central")
    hub.add_vehicle(car)
    hub.add_vehicle(scooter)

    data = hub.to_dict()
    assert data["name"] == "Central"
    assert [item["type"] for item in data["vehicles"]] == [
        "ElectricCar",
        "ElectricScooter",
    ]


def test_grouped_vehicle_display(
    car: ElectricCar,
    scooter: ElectricScooter,
    capsys: pytest.CaptureFixture[str],
) -> None:
    hub = Hub("Central")
    hub.add_vehicle(car)
    hub.add_vehicle(scooter)
    capsys.readouterr()

    hub.get_all_vehicles()
    output = capsys.readouterr().out

    assert output.index("ELECTRIC CARS") < output.index("ELECTRIC SCOOTERS")
    assert "Vehicle #CAR-001 Details" in output
    assert "Vehicle #SCOOTER-001 Details" in output


def test_empty_hub_display(capsys: pytest.CaptureFixture[str]) -> None:
    Hub("Empty").get_all_vehicles()
    assert "No vehicles found in Empty hub" in capsys.readouterr().out
