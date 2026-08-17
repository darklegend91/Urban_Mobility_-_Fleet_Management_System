# Pytest Folder Guide

This Folder is made to test the Urban Fleet Mobility mini oops project using **Pytest** 3rd party library of python.

This folder has 7 files one guide(readme) and 6 test files for tetsing each file and its methods.

## Folder structure

```
tests/
├── README.md
├── __pycache__                 # folder for .pyc files for faster import of the module
├── test_electric_car.py        # file to test electric_car methods
├── test_electric_scooter.py    # file to test electric_scooter methods
├── test_fleet.py               # file to test fleet methods
├── test_hub.py                 # file to test hub methods
├── test_main.py                # file to test main file methods
└── test_vehicle.py             # file to test vehicle methods
```

##  fixtures

Each test  file has fixtures which are functions that run before a test function to provide the necessary setup and isolate environment for each test case.

- `car`: an available `ElectricCar` with 92.5% battery.
- `scooter`: an `ElectricScooter` currently on a trip with 85% battery.
- `populated_manager`: a `FleetManager` containing a populated Central Hub and an Empty Hub.

##  Parameterized

Some tests has properties like ```@pytest.mark.parametrize()```  which helps us define multiple calulative test cases to test multiple test using single function logic.

- `@pytest.mark.parametrize("battery", [-0.01, 100.01])`: used in test_vehicle.py

## Tests included

### `test_vehicle.py` — 18 collected cases

- `test_vehicle_is_abstract()` checks whether `Vehicle` is an abstract class.
- `test_vehicle_class_updation()` checks whether all common vehicle properties can be updated.
- `test_battery_percentage_rejects_values_outside_range()` checks that battery percentages below 0 and above 100 raise a `ValueError`.
- `test_battery_precentage()` checks that valid battery percentages are accepted and invalid percentages are rejected.
- `test_all_documented_maintenance_statuses_are_accepted()` checks that the three documented maintenance statuses are accepted and unsupported statuses are rejected.
- `test_allowed_statuses_accessor_returns_expected_values()` checks that the allowed-status accessor returns the documented status values.
- `test_negative_rental_price_is_rejected()` checks that a negative rental price is rejected without changing the existing price.
- `test_vehicles_compare_by_vehicle_id()` checks equality by vehicle ID and inequality with vehicles having different IDs or unrelated objects.
- `test_common_string_and_dictionary_representations()` checks the common string and dictionary representations of a vehicle.

### `test_electric_car.py` — 10 collected cases

- `test_car_inherits_vehicle_and_exposes_car_data()` checks that an  ectricCar` inherits from `Vehicle` and exposes its car-specific data.
- `test_car_seating_capacity_can_be_updated()` checks that the seating capacity   be updated.
- `test_car_rejects_non_positive_seating_capacity()` checks that zero and  ative seating capacities raise a `ValueError`.
- `test_car_trip_cost_uses_distance()` checks trip-cost calculations for zero,  eger, and decimal distances.
- `test_car_string_adds_seating_capacity()` checks that the string  resentation includes the seating capacity.
- `test_car_dictionary_adds_type_and_seating_capacity()` checks that dictionary  ialization includes the car type and seating capacity.

### `test_electric_scooter.py` — 10 collected cases

- `test_scooter_inherits_vehicle_and_exposes_scooter_data()` checks that an  ectricScooter` inherits from `Vehicle` and exposes its scooter-specific  a.
- `test_scooter_speed_limit_can_be_updated()` checks that the maximum speed  it can be updated.
- `test_scooter_rejects_non_positive_speed_limit()` checks that zero and  ative speed limits raise a `ValueError`.
- `test_scooter_trip_cost_uses_duration()` checks trip-cost calculations for  o, integer, and decimal durations.
- `test_scooter_string_adds_speed_limit()` checks that the string  resentation includes the maximum speed limit.
- `test_scooter_dictionary_adds_type_and_speed_limit()` checks that dictionary  ialization includes the scooter type and maximum speed limit.

### `test_hub.py` — 12 collected cases

- `test_new_hub_has_a_name_and_no_vehicles()` checks that a new hub has the  en name, contains no vehicles, and displays an empty-hub message.
- `test_add_and_find_vehicle()` checks that a vehicle can be added to and found  a hub.
- `test_duplicate_vehicle_id_is_rejected()` checks that a hub rejects a vehicle  se ID is already present.
- `test_remove_vehicle_returns_removed_object()` checks that removing a vehicle returns that vehicle and removes it from the hub.
- `test_remove_missing_vehicle_raises_error()` checks that removing an unknown vehicle raises a `ValueError`.
- `test_sort_vehicles_supports_all_options_without_mutating()` checks sorting by model, battery, and fare without changing insertion order.
- `test_model_sorting_is_case_insensitive()` checks that vehicle models are sorted without considering letter case.
- `test_invalid_sort_option_is_rejected()` checks that an unsupported sorting option raises a `ValueError`.
- `test_hub_string_sorts_full_vehicle_details()` checks that the hub string contains full vehicle details sorted by model.
- `test_hub_dictionary_contains_nested_vehicle_data()` checks that dictionary serialization includes the hub name and nested vehicle data.
- `test_grouped_vehicle_display()` checks that cars and scooters are displayed in their respective groups.
- `test_empty_hub_display()` checks that displaying an empty hub prints the expected message.

### `test_fleet.py` — 30 collected cases

- `test_new_manager_initializes_vehicle_type_dictionary()` checks that a new fleet manager initializes empty car and scooter collections.
- `test_add_find_and_reject_duplicate_hub()` checks that hubs can be added and found and that duplicate hub names are rejected.
- `test_add_vehicle_keeps_hub_and_type_dictionary_in_sync()` checks that adding vehicles updates both the hub and the vehicle-type dictionary.
- `test_unsupported_vehicle_is_rejected_before_hub_changes()` checks that an unsupported object raises a `TypeError` without changing the hub.
- `test_remove_vehicle_updates_hub_and_dictionary()` checks that removing a vehicle updates both its hub and the vehicle-type dictionary.
- `test_removing_from_missing_hub_returns_none()` checks that removal from an unknown hub returns `None` and displays the expected message.
- `test_same_object_remains_indexed_while_present_in_another_hub()` checks that a shared vehicle remains indexed until it is removed from every hub.
- `test_fleet_dictionary_and_status_summary()` checks nested fleet serialization and vehicle-status totals.
- `test_display_and_search_operations()` checks hub displays, vehicle-type displays, hub searches, and battery searches.
- `test_empty_and_missing_search_messages()` checks the messages shown for empty fleet data and missing search results.
- `test_csv_round_trip_preserves_both_vehicle_types()` checks that cars and scooters can be saved to and loaded from CSV.
- `test_csv_missing_file_returns_zero()` checks that loading a missing CSV file returns zero and displays the expected message.
- `test_csv_missing_columns_is_rejected()` checks that a CSV file missing required columns raises a `ValueError`.
- `test_invalid_csv_does_not_replace_current_fleet()` checks that invalid CSV data does not replace the current fleet.
- `test_json_round_trip_preserves_hubs_and_vehicle_types()` checks that hubs, cars, and scooters can be saved to and loaded from JSON.
- `test_json_missing_file_returns_zero()` checks that loading a missing JSON file returns zero and displays the expected message.
- `test_invalid_json_structures_are_rejected()` checks that five invalid JSON structures, including duplicate hubs and unsupported vehicle types, raise a `ValueError`.
- `test_invalid_json_does_not_replace_current_fleet()` checks that invalid JSON data does not replace the current fleet.
- `test_view_file_prints_and_returns_contents()` checks that file viewing both prints and returns the file contents.
- `test_numeric_prompt_helpers_retry()` checks that numeric input helpers retry after invalid input and return valid numeric values.
- `test_choose_data_file()` checks CSV/JSON file selection, default names, automatic suffixes, and cancellation.
- `test_build_vehicle_creates_selected_type()` checks that interactive input constructs the selected vehicle type with the entered data.
- `test_console_can_exit_immediately()` checks that the interactive console can exit normally.

### `test_main.py` — 1 collected case

- `test_main_runs_demo_checks_then_starts_console()` checks that the demo checks run in order and that the console starts after they succeed. The real interactive console is replaced so the automated test never waits for input.
  
## Set up the test environment

```bash
source .venv/bin/activate
pip3 install pytest pytest-cov
```

## Run the tests

Run the complete suite:

```bash
python -m pytest
```

Show every test name:

```bash
python -m pytest -v
```

Run one module:

```bash
python -m pytest tests/test_hub.py -v
```

Run one specific test:

```bash
python -m pytest tests/test_hub.py::test_add_and_find_vehicle -v
```

## Check code coverage uding HTML

Coverage reports show which production lines and branches were executed by the tests. Install the optional coverage plugin first:

```bash
python -m pip install pytest-cov
```
Display missing lines and branch coverage in the terminal:

```bash
python -m pytest \
  --cov=vehicle \
  --cov=ElectricCar \
  --cov=ElectricScooter \
  --cov=Hub \
  --cov=Fleet \
  --cov=main \
  --cov-branch \
  --cov-report=term-missing
```

Generate a browsable HTML report:

```bash
python -m pytest \
  --cov=vehicle \
  --cov=ElectricCar \
  --cov=ElectricScooter \
  --cov=Hub \
  --cov=Fleet \
  --cov=main \
  --cov-branch \
  --cov-report=html
```

Open `htmlcov/index.html` in a browser. Green lines were executed; red lines were missed. A high percentage is useful, but important behavior and failure cases matter more than reaching 100% mechanically.