import csv
from collections import defaultdict
from contextlib import redirect_stdout
from io import StringIO
from tempfile import TemporaryDirectory

from ElectricCar import ElectricCar
from ElectricScooter import ElectricScooter
from Fleet import FleetManager, run_console
from Hub import Hub
from vehicle import Vehicle


def test_electric_car() -> None:
    print("\n========== ELECTRIC CAR TEST ==========")

    car = ElectricCar(
        vehicle_id="CAR-101",
        model="Tesla Model 3",
        battery_percentage=85.5,
        maintenance_status="Available",
        rental_price=2500.0,
        seating_capacity=5,
    )

    print("\nInitial car details:")
    print(car)

    print("\nTesting inheritance:")
    print("Is ElectricCar a Vehicle?", isinstance(car, Vehicle))

    print("\nTesting individual properties:")
    print("Vehicle ID:", car.vehicle_id)
    print("Model:", car.model)
    print("Battery:", car.battery_percentage)
    print("Maintenance status:", car.maintenance_status)
    print("Rental price:", car.rental_price)
    print("Seating capacity:", car.seating_capacity)

    print("\nUpdating car properties...")
    car.battery_percentage = 72.25
    car.maintenance_status = "Under Maintenance"
    car.rental_price = 2200.0
    car.seating_capacity = 4

    print("\nUpdated car details:")
    print(car)
    
    # Test calculate_trip_cost for car
    print("\nTesting trip cost calculation for car:")
    distance = 100
    cost = car.calculate_trip_cost(distance)
    print(f"Trip cost for {distance} km: ${cost:.2f}")


def test_electric_scooter() -> None:
    print("\n========== ELECTRIC SCOOTER TEST ==========")

    scooter = ElectricScooter(
        vehicle_id="SCOOTER-201",
        model="Ather 450X",
        battery_percentage=90.0,
        maintenance_status="Available",
        rental_price=500.0,
        max_speed_limit=80.0,
    )

    print("\nInitial scooter details:")
    print(scooter)

    print("\nTesting inheritance:")
    print("Is ElectricScooter a Vehicle?", isinstance(scooter, Vehicle))

    print("\nTesting individual properties:")
    print("Vehicle ID:", scooter.vehicle_id)
    print("Model:", scooter.model)
    print("Battery:", scooter.battery_percentage)
    print("Maintenance status:", scooter.maintenance_status)
    print("Rental price:", scooter.rental_price)
    print("Maximum speed:", scooter.max_speed_limit)

    print("\nUpdating scooter properties...")
    scooter.battery_percentage = 65.5
    scooter.maintenance_status = "Under Maintenance"
    scooter.rental_price = 450.0
    scooter.max_speed_limit = 75.0

    print("\nUpdated scooter details:")
    print(scooter)
    
    # Test calculate_trip_cost for scooter
    print("\nTesting trip cost calculation for scooter:")
    time = 30  # minutes
    cost = scooter.calculate_trip_cost(time)
    print(f"Trip cost for {time} minutes: ${cost:.2f}")


def test_allowed_statuses() -> None:
    print("\n========== ALLOWED STATUS TEST ==========")
    print("Allowed statuses:", Vehicle.get_ALLOWED_STATUSES())


def test_invalid_values() -> None:
    print("\n========== VALIDATION TESTS ==========")

    test_cases = [
        (
            "Battery percentage greater than 100",
            lambda: ElectricCar(
                "CAR-102",
                "Invalid Car",
                120.0,
                "Available",
                1000.0,
                4,
            ),
        ),
        (
            "Battery percentage below 0",
            lambda: ElectricScooter(
                "SCOOTER-202",
                "Invalid Scooter",
                -10.0,
                "Available",
                300.0,
                60.0,
            ),
        ),
        (
            "Invalid maintenance status",
            lambda: ElectricCar(
                "CAR-103",
                "Invalid Car",
                50.0,
                "Broken",
                1000.0,
                4,
            ),
        ),
        (
            "Negative rental price",
            lambda: ElectricCar(
                "CAR-104",
                "Invalid Car",
                50.0,
                "Available",
                -500.0,
                4,
            ),
        ),
        (
            "Invalid seating capacity",
            lambda: ElectricCar(
                "CAR-105",
                "Invalid Car",
                50.0,
                "Available",
                1000.0,
                0,
            ),
        ),
        (
            "Invalid scooter speed",
            lambda: ElectricScooter(
                "SCOOTER-203",
                "Invalid Scooter",
                50.0,
                "Available",
                300.0,
                0.0,
            ),
        ),
    ]

    for description, test_function in test_cases:
        try:
            test_function()
            print(f"[FAILED] {description}: No exception was raised")
        except ValueError as error:
            print(f"[PASSED] {description}: {error}")


def test_polymorphism() -> None:
    """UC 5: Polymorphism in Action - Demonstrates dynamic behavior with mixed vehicle types"""
    print("\n========== POLYMORPHISM TEST ==========")
    print("Demonstrating dynamic behavior with mixed vehicle types...\n")
    
    # Create a mixed list of vehicles
    vehicles = [
        ElectricCar(
            vehicle_id="CAR-101",
            model="Tesla Model 3",
            battery_percentage=85.5,
            maintenance_status="Available",
            rental_price=2500.0,
            seating_capacity=5,
        ),
        ElectricScooter(
            vehicle_id="SCOOTER-201",
            model="Ather 450X",
            battery_percentage=90.0,
            maintenance_status="On Trip",
            rental_price=500.0,
            max_speed_limit=80.0,
        ),
        ElectricCar(
            vehicle_id="CAR-102",
            model="Nissan Leaf",
            battery_percentage=75.0,
            maintenance_status="Under Maintenance",
            rental_price=1800.0,
            seating_capacity=4,
        ),
        ElectricScooter(
            vehicle_id="SCOOTER-202",
            model="Ola S1 Pro",
            battery_percentage=95.0,
            maintenance_status="Available",
            rental_price=600.0,
            max_speed_limit=90.0,
        ),
        ElectricCar(
            vehicle_id="CAR-103",
            model="BMW i3",
            battery_percentage=60.0,
            maintenance_status="On Trip",
            rental_price=2200.0,
            seating_capacity=4,
        ),
        ElectricScooter(
            vehicle_id="SCOOTER-203",
            model="Bajaj Chetak",
            battery_percentage=70.0,
            maintenance_status="Under Maintenance",
            rental_price=400.0,
            max_speed_limit=65.0,
        ),
    ]
    
    # Define trip parameters (km for cars, minutes for scooters)
    trip_parameters = {
        "CAR-101": {"distance": 100, "unit": "km"},
        "SCOOTER-201": {"distance": 30, "unit": "minutes"},
        "CAR-102": {"distance": 150, "unit": "km"},
        "SCOOTER-202": {"distance": 45, "unit": "minutes"},
        "CAR-103": {"distance": 200, "unit": "km"},
        "SCOOTER-203": {"distance": 20, "unit": "minutes"},
    }
    
    print("Processing rentals for mixed vehicle types...")
    print("=" * 60)
    
    total_revenue = 0.0
    vehicle_count = 0
    
    for vehicle in vehicles:
        vehicle_count += 1
        vehicle_id = vehicle.vehicle_id
        trip_info = trip_parameters[vehicle_id]
        distance = trip_info["distance"]
        unit = trip_info["unit"]
        
        # Calculate trip cost - POLYMORPHISM IN ACTION!
        # The SAME method call produces DIFFERENT results based on vehicle type
        cost = vehicle.calculate_trip_cost(distance)
        total_revenue += cost
        
        # Determine vehicle type dynamically
        vehicle_type = "Car" if isinstance(vehicle, ElectricCar) else "Scooter"
        
        # Display results
        print(f"\n{vehicle_count}. {vehicle_type}: {vehicle.model}")
        print(f"   Vehicle ID: {vehicle_id}")
        print(f"   Battery: {vehicle.battery_percentage:.1f}%")
        print(f"   Maintenance: {vehicle.maintenance_status}")
        print(f"   Trip Distance/Time: {distance} {unit}")
        print(f"   Trip Cost: ${cost:.2f}")
        print(f"   Object Type: {type(vehicle).__name__}")
        print("-" * 40)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Total vehicles processed: {vehicle_count}")
    print(f"Total revenue generated: ${total_revenue:.2f}")
    print(f"Average trip cost: ${total_revenue / vehicle_count:.2f}")
    
    # Demonstrate polymorphism with a simple loop
    print("\n" + "=" * 60)
    print("Demonstrating polymorphism with the same method call:")
    print("for vehicle in vehicles:")
    print("    cost = vehicle.calculate_trip_cost(distance)")
    print("\nThe SAME method name produces DIFFERENT results based on vehicle type!")
    print("This is dynamic polymorphism in action.")


def _get_output(function, *args) -> str:
    """Run a display/search function and return everything it prints."""
    output = StringIO()
    with redirect_stdout(output):
        function(*args)
    return output.getvalue()


def _expect_value_error(description, function, *args) -> None:
    """Verify that an invalid hub operation raises ValueError."""
    try:
        function(*args)
    except ValueError as error:
        print(f"[PASSED] {description}: {error}")
    else:
        raise AssertionError(f"{description}: ValueError was not raised")


def test_vehicle_type_dictionary_and_display() -> None:
    """Test the vehicle-type defaultdict and grouped output without input."""
    manager = FleetManager()
    manager.add_hub("Test Hub")

    car = ElectricCar(
        "CAR-T01", "Test Electric Car", 90.0, "Available", 1500.0, 5
    )
    scooter = ElectricScooter(
        "SCOOTER-T01",
        "Test Electric Scooter",
        85.0,
        "On Trip",
        400.0,
        75.0,
    )

    manager.add_vehicle_to_hub("Test Hub", car)
    manager.add_vehicle_to_hub("Test Hub", scooter)

    vehicle_dict = manager.vehicle_dict
    assert isinstance(vehicle_dict, defaultdict)
    assert vehicle_dict.default_factory is list
    assert vehicle_dict["Electric Car"] == [car]
    assert vehicle_dict["Electric Scooter"] == [scooter]
    assert vehicle_dict["Electric Car"][0] is car
    assert vehicle_dict["Electric Scooter"][0] is scooter

    display_output = _get_output(manager.display_vehicles_by_type)
    assert "ELECTRIC CARS" in display_output
    assert "ELECTRIC SCOOTERS" in display_output
    assert display_output.index("ELECTRIC CARS") < display_output.index(
        "ELECTRIC SCOOTERS"
    )
    assert "Vehicle #CAR-T01 Details" in display_output
    assert "Vehicle #SCOOTER-T01 Details" in display_output

    print("[PASSED] Vehicle type defaultdict and separate display")


def test_hub_str_displays_sorted_vehicles() -> None:
    """Test that print(hub) shows complete details sorted by model."""
    hub = Hub("String Test Hub")
    empty_hub = Hub("Empty Test Hub")

    zeta_car = ElectricCar(
        "CAR-S01", "Zeta EV", 90.0, "Available", 1800.0, 5
    )
    alpha_scooter = ElectricScooter(
        "SCOOTER-S01", "Alpha Ride", 80.0, "On Trip", 400.0, 70.0
    )
    middle_car = ElectricCar(
        "CAR-S02", "Middle Motors", 65.0, "Under Maintenance", 1400.0, 4
    )

    hub.add_vehicle(zeta_car)
    hub.add_vehicle(alpha_scooter)
    hub.add_vehicle(middle_car)

    hub_output = str(hub)
    assert "Hub: String Test Hub" in hub_output
    assert "Vehicles sorted by model" in hub_output
    assert hub_output.index("Alpha Ride") < hub_output.index("Middle Motors")
    assert hub_output.index("Middle Motors") < hub_output.index("Zeta EV")
    assert hub_output.count("Vehicle #") == 3
    assert "Maximum Speed Limit: 70.00" in hub_output
    assert "Seating Capacity: 5" in hub_output

    # sorted() returns a new list, so displaying the hub must not change its
    # original insertion order.
    assert hub.vehicles == [zeta_car, alpha_scooter, middle_car]
    assert str(empty_hub) == "Hub: Empty Test Hub\nNo vehicles found"

    print("[PASSED] Hub __str__ displays all vehicles in sorted order")


def test_advanced_vehicle_sorting() -> None:
    """Test descending battery and fare sorting without user input."""
    hub = Hub("Advanced Sorting Hub")
    empty_hub = Hub("Empty Sorting Hub")

    high_fare_car = ElectricCar(
        "CAR-A01", "City Premium", 45.0, "Available", 3000.0, 5
    )
    high_battery_scooter = ElectricScooter(
        "SCOOTER-A01", "Eco Sprint", 95.0, "On Trip", 500.0, 80.0
    )
    middle_car = ElectricCar(
        "CAR-A02", "Metro Drive", 70.0, "Under Maintenance", 1800.0, 4
    )

    hub.add_vehicle(high_fare_car)
    hub.add_vehicle(high_battery_scooter)
    hub.add_vehicle(middle_car)
    original_order = list(hub.vehicles)

    battery_sorted = hub.sort_vehicles("battery")
    assert battery_sorted == [high_battery_scooter, middle_car, high_fare_car]
    assert [vehicle.battery_percentage for vehicle in battery_sorted] == [
        95.0,
        70.0,
        45.0,
    ]

    fare_sorted = hub.sort_vehicles("fare")
    assert fare_sorted == [high_fare_car, middle_car, high_battery_scooter]
    assert [vehicle.rental_price for vehicle in fare_sorted] == [
        3000.0,
        1800.0,
        500.0,
    ]

    # Dynamic sorting returns new lists and does not mutate the hub.
    assert hub.vehicles == original_order
    assert empty_hub.sort_vehicles("battery") == []
    assert empty_hub.sort_vehicles("fare") == []
    _expect_value_error(
        "Unknown sorting option is rejected",
        hub.sort_vehicles,
        "unknown",
    )

    print("[PASSED] Advanced sorting by battery and fare")


def test_fleet_manager_and_hubs() -> None:
    """Test every FleetManager and Hub operation with cars and scooters."""
    print("\n========== FLEET AND HUB TESTS ==========")

    manager = FleetManager()

    # Empty fleet cases
    assert "No hubs in system!" in _get_output(manager.display_all_hubs)
    assert "No vehicles found with battery above 80%" in _get_output(
        manager.search_by_battery
    )
    assert "No vehicles in system!" in _get_output(
        manager.display_vehicles_by_type
    )
    print("[PASSED] Empty fleet display and battery search")

    # Add hubs, find hubs, and reject duplicate hub names
    assert manager.add_hub("Central Hub") is True
    assert manager.add_hub("Airport Hub") is True
    assert manager.add_hub("Central Hub") is False

    central_hub = manager.find_hub("Central Hub")
    airport_hub = manager.find_hub("Airport Hub")
    assert central_hub is not None
    assert airport_hub is not None
    assert central_hub.name == "Central Hub"
    assert central_hub.vehicles == []
    assert manager.find_hub("Missing Hub") is None
    print("[PASSED] Add, find, and duplicate hub cases")

    # Empty and missing hub searches
    assert "No vehicles found" in _get_output(
        manager.search_by_hub, "Airport Hub"
    )
    assert "Hub not found" in _get_output(manager.search_by_hub, "Missing Hub")
    assert "No vehicles found in Airport Hub hub" in _get_output(
        airport_hub.get_all_vehicles
    )
    print("[PASSED] Empty and missing hub search cases")

    car = ElectricCar(
        "CAR-F01", "Tata Nexon EV", 92.0, "Available", 1800.0, 5
    )
    scooter = ElectricScooter(
        "SCOOTER-F01", "Ather 450X", 85.0, "On Trip", 450.0, 80.0
    )
    low_battery_car = ElectricCar(
        "CAR-F02", "MG Comet EV", 60.0, "Under Maintenance", 1200.0, 4
    )

    # Add both vehicle types through FleetManager. The manager automatically
    # stores each object under its vehicle type.
    assert manager.add_vehicle_to_hub("Central Hub", car) is True
    assert manager.add_vehicle_to_hub("Central Hub", scooter) is True
    assert manager.add_vehicle_to_hub("Central Hub", low_battery_car) is True
    assert manager.add_vehicle_to_hub("Missing Hub", car) is False
    assert central_hub.find_vehicle("CAR-F01") is car
    assert central_hub.find_vehicle("UNKNOWN") is None
    assert central_hub.vehicles == [car, scooter, low_battery_car]
    print("[PASSED] Add vehicles and find vehicles")

    sorted_vehicles = central_hub.sort_vehicles()
    assert sorted_vehicles == [scooter, low_battery_car, car]
    assert [vehicle.model for vehicle in sorted_vehicles] == [
        "Ather 450X",
        "MG Comet EV",
        "Tata Nexon EV",
    ]
    assert central_hub.vehicles == [car, scooter, low_battery_car]
    assert airport_hub.sort_vehicles() == []
    print("[PASSED] Sort hub vehicles alphabetically by model")

    assert manager.vehicle_dict == {
        "Electric Car": [car, low_battery_car],
        "Electric Scooter": [scooter],
    }
    assert manager.vehicle_dict["Electric Car"][0] is car
    assert manager.vehicle_dict["Electric Scooter"][0] is scooter
    print("[PASSED] Vehicle type-to-object dictionary")

    status_output = StringIO()
    with redirect_stdout(status_output):
        status_counts = manager.get_status()

    assert status_counts == {
        "Available": 1,
        "On Trip": 1,
        "Under Maintenance": 1,
    }
    summary = status_output.getvalue()
    assert "VEHICLE STATUS SUMMARY" in summary
    assert "Available           : 1" in summary
    assert "On Trip             : 1" in summary
    assert "Under Maintenance   : 1" in summary
    assert "Total Vehicles      : 3" in summary
    print("[PASSED] Vehicle counts by current status")

    _expect_value_error(
        "Duplicate vehicle is rejected",
        manager.add_vehicle_to_hub,
        "Central Hub",
        car,
    )

    # Display all hubs and all vehicles in a hub.
    hub_output = _get_output(central_hub.get_all_vehicles)
    assert "ELECTRIC CARS" in hub_output
    assert "ELECTRIC SCOOTERS" in hub_output
    assert hub_output.index("ELECTRIC CARS") < hub_output.index(
        "ELECTRIC SCOOTERS"
    )
    assert "Vehicle #CAR-F01 Details" in hub_output
    assert "Seating Capacity: 5" in hub_output
    assert "Vehicle #SCOOTER-F01 Details" in hub_output
    assert "Maximum Speed Limit: 80.00" in hub_output

    fleet_output = _get_output(manager.display_all_hubs)
    assert "Central Hub" in fleet_output
    assert "Airport Hub" in fleet_output
    assert "Vehicle #CAR-F02 Details" in fleet_output

    type_output = _get_output(manager.display_vehicles_by_type)
    assert type_output.index("ELECTRIC CARS") < type_output.index(
        "ELECTRIC SCOOTERS"
    )
    assert "Vehicle #CAR-F01 Details" in type_output
    assert "Vehicle #SCOOTER-F01 Details" in type_output
    print("[PASSED] Display cars separately from scooters")

    # Search by hub and battery percentage.
    search_output = _get_output(manager.search_by_hub, "Central Hub")
    assert "CAR-F01" in search_output
    assert "SCOOTER-F01" in search_output
    assert "CAR-F02" in search_output

    battery_output = _get_output(manager.search_by_battery)
    assert "CAR-F01" in battery_output
    assert "SCOOTER-F01" in battery_output
    assert "CAR-F02" not in battery_output
    print("[PASSED] Search vehicles by hub and battery above 80%")

    # Remove a vehicle, confirm it is gone, and test a missing removal.
    removed_vehicle = manager.remove_vehicle_from_hub("Central Hub", "CAR-F02")
    assert removed_vehicle is low_battery_car
    assert central_hub.find_vehicle("CAR-F02") is None
    assert low_battery_car not in central_hub.vehicles
    assert manager.vehicle_dict["Electric Car"] == [car]
    _expect_value_error(
        "Missing vehicle cannot be removed",
        manager.remove_vehicle_from_hub,
        "Central Hub",
        "UNKNOWN",
    )
    print("[PASSED] Remove vehicle from hub")


def test_csv_vehicle_persistence() -> None:
    """Test saving vehicles to CSV and loading them into a new manager."""
    print("\n========== CSV VEHICLE PERSISTENCE TESTS ==========")

    with TemporaryDirectory() as temporary_directory:
        filename = f"{temporary_directory}/vehicle_data.csv"

        manager = FleetManager()
        assert manager.add_hub("CSV Test Hub") is True

        car = ElectricCar(
            "CAR-CSV01",
            "CSV Test Car",
            88.5,
            "Available",
            1750.0,
            5,
        )
        scooter = ElectricScooter(
            "SCOOTER-CSV01",
            "CSV Test Scooter",
            76.0,
            "Under Maintenance",
            350.0,
            72.5,
        )

        assert manager.add_vehicle_to_hub("CSV Test Hub", car) is True
        assert manager.add_vehicle_to_hub("CSV Test Hub", scooter) is True
        assert manager.save_to_csv(filename) == 2

        with open(filename, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)

        assert reader.fieldnames == list(FleetManager.CSV_FIELDS)
        assert len(rows) == 2

        car_row = next(row for row in rows if row["vehicle_id"] == "CAR-CSV01")
        assert car_row["hub_name"] == "CSV Test Hub"
        assert car_row["vehicle_type"] == "Electric Car"
        assert car_row["model"] == "CSV Test Car"
        assert car_row["battery_percentage"] == "88.5"
        assert car_row["maintenance_status"] == "Available"
        assert car_row["rental_price"] == "1750.0"
        assert car_row["seating_capacity"] == "5"
        assert car_row["max_speed_limit"] == ""

        scooter_row = next(
            row for row in rows if row["vehicle_id"] == "SCOOTER-CSV01"
        )
        assert scooter_row["hub_name"] == "CSV Test Hub"
        assert scooter_row["vehicle_type"] == "Electric Scooter"
        assert scooter_row["model"] == "CSV Test Scooter"
        assert scooter_row["battery_percentage"] == "76.0"
        assert scooter_row["maintenance_status"] == "Under Maintenance"
        assert scooter_row["rental_price"] == "350.0"
        assert scooter_row["seating_capacity"] == ""
        assert scooter_row["max_speed_limit"] == "72.5"
        print("[PASSED] Car and scooter records are written correctly to CSV")

        loaded_manager = FleetManager()
        assert loaded_manager.load_from_csv(filename) == 2

        loaded_hub = loaded_manager.find_hub("CSV Test Hub")
        assert loaded_hub is not None

        loaded_car = loaded_hub.find_vehicle("CAR-CSV01")
        loaded_scooter = loaded_hub.find_vehicle("SCOOTER-CSV01")
        assert isinstance(loaded_car, ElectricCar)
        assert isinstance(loaded_scooter, ElectricScooter)
        assert loaded_car.seating_capacity == 5
        assert loaded_car.battery_percentage == 88.5
        assert loaded_scooter.max_speed_limit == 72.5
        assert loaded_scooter.maintenance_status == "Under Maintenance"
        assert loaded_manager.vehicle_dict["Electric Car"] == [loaded_car]
        assert loaded_manager.vehicle_dict["Electric Scooter"] == [
            loaded_scooter
        ]
        print("[PASSED] Vehicle records are loaded back from CSV")


def main() -> None:
    """Run all test cases, then start the fleet management console."""
    print("=" * 60)
    print("VEHICLE MANAGEMENT SYSTEM - COMPLETE TEST SUITE")
    print("=" * 60)
    
    try:
        # UC 1-3: Basic functionality tests
        test_electric_car()
        test_electric_scooter()
        
        # Validation tests
        test_allowed_statuses()
        test_invalid_values()
        
        # UC 5: Polymorphism test
        test_polymorphism()

        # UC 6-9: Fleet manager, hubs, and their vehicles
        test_vehicle_type_dictionary_and_display()
        test_hub_str_displays_sorted_vehicles()
        test_advanced_vehicle_sorting()
        test_fleet_manager_and_hubs()
        test_csv_vehicle_persistence()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as error:
        print(f"\n" + "=" * 60)
        print(f"UNEXPECTED ERROR OCCURRED: {error}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return

    print("\nStarting Fleet Management System...")
    run_console()

if __name__ == "__main__":
    main()
