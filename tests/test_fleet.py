import csv
import json
from collections.abc import Callable
from pathlib import Path
import pytest
import Fleet
from ElectricCar import ElectricCar
from ElectricScooter import ElectricScooter
from Fleet import FleetManager


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
        model="Ola",
        battery_percentage=85.0,
        maintenance_status="On Trip",
        rental_price=450.0,
        max_speed_limit=80.0,
    )


@pytest.fixture
def populated_manager( car: ElectricCar, scooter: ElectricScooter ) -> FleetManager:
    manager = FleetManager()
    manager.add_hub("Central Hub")
    manager.add_hub("Empty Hub")
    manager.add_vehicle_to_hub("Central Hub", car)
    manager.add_vehicle_to_hub("Central Hub", scooter)
    return manager


def test_new_manager_initializes_vehicle_type_dictionary() -> None:
    manager = FleetManager()
    assert manager.vehicle_dict == {
        "Electric Car": [],
        "Electric Scooter": [],
    }


def test_add_find_and_reject_duplicate_hub(
    capsys: pytest.CaptureFixture[str],
) -> None:
    manager = FleetManager()
    assert manager.add_hub("Central") is True
    central_hub = manager.find_hub("Central")
    assert central_hub is not None
    assert central_hub.name == "Central"
    assert manager.find_hub("Missing") is None
    assert manager.add_hub("Central") is False

    output = capsys.readouterr().out
    assert "Hub 'Central' created!" in output
    assert "Hub 'Central' already exists!" in output


def test_add_vehicle_keeps_hub_and_type_dictionary_in_sync(
    car: ElectricCar,
    scooter: ElectricScooter,
    capsys: pytest.CaptureFixture[str],
) -> None:
    manager = FleetManager()
    manager.add_hub("Central")

    assert manager.add_vehicle_to_hub("Central", car) is True
    assert manager.add_vehicle_to_hub("Central", scooter) is True
    central_hub = manager.find_hub("Central")
    assert central_hub is not None
    assert central_hub.vehicles == [car, scooter]
    assert manager.vehicle_dict["Electric Car"] == [car]
    assert manager.vehicle_dict["Electric Scooter"] == [scooter]

    assert manager.add_vehicle_to_hub("Missing", car) is False
    assert "Hub 'Missing' not found!" in capsys.readouterr().out


def test_unsupported_vehicle_is_rejected_before_hub_changes() -> None:
    manager = FleetManager()
    manager.add_hub("Central")

    with pytest.raises(TypeError, match="Only ElectricCar and ElectricScooter"):
        manager.add_vehicle_to_hub("Central", object())

    assert manager.find_hub("Central").vehicles == [] # type:ignore


def test_remove_vehicle_updates_hub_and_dictionary(
    populated_manager: FleetManager,
    car: ElectricCar,
) -> None:
    removed = populated_manager.remove_vehicle_from_hub("Central Hub", "CAR-001")

    assert removed is car
    central_hub = populated_manager.find_hub("Central Hub")
    assert central_hub is not None
    assert central_hub.find_vehicle("CAR-001") is None
    assert populated_manager.vehicle_dict["Electric Car"] == []


def test_removing_from_missing_hub_returns_none(
    populated_manager: FleetManager,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert populated_manager.remove_vehicle_from_hub("Missing", "CAR-001") is None
    assert "Hub 'Missing' not found!" in capsys.readouterr().out


def test_same_object_remains_indexed_while_present_in_another_hub(
    car: ElectricCar,
) -> None:
    manager = FleetManager()
    manager.add_hub("One")
    manager.add_hub("Two")
    manager.add_vehicle_to_hub("One", car)
    manager.add_vehicle_to_hub("Two", car)

    manager.remove_vehicle_from_hub("One", car.vehicle_id)
    assert manager.vehicle_dict["Electric Car"] == [car]

    manager.remove_vehicle_from_hub("Two", car.vehicle_id)
    assert manager.vehicle_dict["Electric Car"] == []


def test_fleet_dictionary_and_status_summary(
    populated_manager: FleetManager,
    capsys: pytest.CaptureFixture[str],
) -> None:
    capsys.readouterr()
    data = populated_manager.to_dict()
    counts = populated_manager.get_status()

    assert [hub["name"] for hub in data["hubs"]] == ["Central Hub", "Empty Hub"]
    assert counts == {
        "Available": 1,
        "On Trip": 1,
        "Under Maintenance": 0,
    }
    assert "Total Vehicles      : 2" in capsys.readouterr().out


def test_display_and_search_operations(
    populated_manager: FleetManager,
    capsys: pytest.CaptureFixture[str],
) -> None:
    capsys.readouterr()
    populated_manager.display_all_hubs()
    all_hubs_output = capsys.readouterr().out
    assert "ALL HUBS IN SYSTEM" in all_hubs_output
    assert "Central Hub" in all_hubs_output
    assert "Vehicle #CAR-001 Details" in all_hubs_output

    populated_manager.display_vehicles_by_type()
    type_output = capsys.readouterr().out
    assert type_output.index("ELECTRIC CARS") < type_output.index(
        "ELECTRIC SCOOTERS"
    )

    populated_manager.search_by_hub("Central Hub")
    assert "SCOOTER-001" in capsys.readouterr().out

    populated_manager.search_by_battery()
    battery_output = capsys.readouterr().out
    assert "CAR-001" in battery_output
    assert "SCOOTER-001" in battery_output


def test_empty_and_missing_search_messages(
    capsys: pytest.CaptureFixture[str],
) -> None:
    manager = FleetManager()
    manager.display_all_hubs()
    manager.display_vehicles_by_type()
    manager.search_by_hub("Missing")
    manager.search_by_battery()

    output = capsys.readouterr().out
    assert "No hubs in system!" in output
    assert "No vehicles in system!" in output
    assert "Hub not found" in output
    assert "No vehicles found with battery above 80%" in output


def test_csv_round_trip_preserves_both_vehicle_types(
    populated_manager: FleetManager,
    tmp_path: Path,
) -> None:
    path = tmp_path / "fleet.csv"
    assert populated_manager.save_to_csv(path) == 2

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert reader.fieldnames == list(FleetManager.CSV_FIELDS)
    assert rows[0]["vehicle_type"] == "Electric Car"
    assert rows[0]["seating_capacity"] == "5"
    assert rows[0]["max_speed_limit"] == ""
    assert rows[1]["vehicle_type"] == "Electric Scooter"
    assert rows[1]["max_speed_limit"] == "80.0"

    loaded = FleetManager()
    assert loaded.load_from_csv(path) == 2
    hub = loaded.find_hub("Central Hub")
    assert hub is not None
    assert isinstance(hub.find_vehicle("CAR-001"), ElectricCar)
    assert isinstance(hub.find_vehicle("SCOOTER-001"), ElectricScooter)
    assert loaded.find_hub("Empty Hub") is None


def test_csv_missing_file_returns_zero(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    missing = tmp_path / "missing.csv"
    assert FleetManager().load_from_csv(missing) == 0
    assert "No saved fleet data found" in capsys.readouterr().out


def test_csv_missing_columns_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "invalid.csv"
    path.write_text("hub_name,vehicle_id\nCentral,CAR-1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required column"):
        FleetManager().load_from_csv(path)


def test_invalid_csv_does_not_replace_current_fleet(
    populated_manager: FleetManager,
    tmp_path: Path,
) -> None:
    path = tmp_path / "invalid.csv"
    path.write_text(
        ",".join(FleetManager.CSV_FIELDS)
        + "\nCentral,Electric Car,BAD,Invalid,101,Available,1000,4,\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid fleet data in CSV row 2"):
        populated_manager.load_from_csv(path)

    assert populated_manager.find_hub("Central Hub") is not None
    assert populated_manager.find_hub("Central") is None


def test_json_round_trip_preserves_hubs_and_vehicle_types(
    populated_manager: FleetManager,
    tmp_path: Path,
) -> None:
    path = tmp_path / "fleet.json"
    assert populated_manager.save_to_json(path) == 2

    saved = json.loads(path.read_text(encoding="utf-8"))
    assert [hub["name"] for hub in saved["hubs"]] == [
        "Central Hub",
        "Empty Hub",
    ]
    assert [item["type"] for item in saved["hubs"][0]["vehicles"]] == [
        "ElectricCar",
        "ElectricScooter",
    ]

    loaded = FleetManager()
    assert loaded.load_from_json(path) == 2
    empty_hub = loaded.find_hub("Empty Hub")
    central_hub = loaded.find_hub("Central Hub")
    assert empty_hub is not None
    assert central_hub is not None
    assert empty_hub.vehicles == []
    assert isinstance(
        central_hub.find_vehicle("CAR-001"),
        ElectricCar,
    )


def test_json_missing_file_returns_zero(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    missing = tmp_path / "missing.json"
    assert FleetManager().load_from_json(missing) == 0
    assert "No saved fleet data found" in capsys.readouterr().out


@pytest.mark.parametrize(
    "data",
    [
        [],
        {},
        {"hubs": "not-a-list"},
        {"hubs": [{"name": "Central", "vehicles": [{"type": "Bicycle"}]}]},
        {
            "hubs": [
                {"name": "Repeated", "vehicles": []},
                {"name": "Repeated", "vehicles": []},
            ]
        },
    ],
)
def test_invalid_json_structures_are_rejected(data: object, tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError):
        FleetManager().load_from_json(path)


def test_invalid_json_does_not_replace_current_fleet(
    populated_manager: FleetManager,
    tmp_path: Path,
) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps({"hubs": [{"name": "Broken"}]}), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid fleet data in JSON"):
        populated_manager.load_from_json(path)

    assert populated_manager.find_hub("Central Hub") is not None
    assert populated_manager.find_hub("Broken") is None


def test_view_file_prints_and_returns_contents(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    path = tmp_path / "data.json"
    path.write_text('{"hubs": []}\n', encoding="utf-8")

    contents = FleetManager.view_file(path) # type:ignore
    assert contents == '{"hubs": []}\n'
    assert 'Contents of' in capsys.readouterr().out


@pytest.mark.parametrize(
    ("helper", "answers", "expected", "error_message"),
    [
        (Fleet._prompt_float, ["wrong", "12.5"], 12.5, "valid number"),
        (Fleet._prompt_int, ["wrong", "4"], 4, "valid whole number"),
    ],
)
def test_numeric_prompt_helpers_retry(
    helper: Callable[[str], float | int],
    answers: list[str],
    expected: float | int,
    error_message: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    responses = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    assert helper("Value: ") == expected
    assert error_message in capsys.readouterr().out


@pytest.mark.parametrize(
    ("answers", "expected"),
    [
        (["1", ""], ("csv", FleetManager.CSV_FILE_NAME)),
        (["2", "backup"], ("json", "backup.json")),
        (["3"], None),
    ],
)
def test_choose_data_file(
    answers: list[str],
    expected: tuple[str, str] | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    assert Fleet._choose_data_file() == expected


def test_build_vehicle_creates_selected_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = iter(["1", "CAR-9", "City Car", "80", "Available", "900", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    vehicle = Fleet._build_vehicle()
    assert isinstance(vehicle, ElectricCar)
    assert vehicle.to_dict()["seating_capacity"] == 4


def test_console_can_exit_immediately(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "11")
    Fleet.run_console()
    assert "Exiting Fleet Management System." in capsys.readouterr().out
