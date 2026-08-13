import pytest

import main as application


def test_main_runs_demo_checks_then_starts_console(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls: list[str] = []
    demo_checks = [
        "test_electric_car",
        "test_electric_scooter",
        "test_allowed_statuses",
        "test_invalid_values",
        "test_polymorphism",
        "test_vehicle_type_dictionary_and_display",
        "test_hub_str_displays_sorted_vehicles",
        "test_advanced_vehicle_sorting",
        "test_fleet_manager_and_hubs",
        "test_csv_vehicle_persistence",
        "test_json_vehicle_persistence",
    ]

    for name in demo_checks:
        monkeypatch.setattr(
            application,
            name,
            lambda current_name=name: calls.append(current_name),
        )
    monkeypatch.setattr(application, "run_console", lambda: calls.append("console"))

    application.main()

    assert calls == [*demo_checks, "console"]
    output = capsys.readouterr().out
    assert "ALL TESTS COMPLETED SUCCESSFULLY!" in output
    assert "Starting Fleet Management System..." in output
