from ElectricCar import ElectricCar
from ElectricScooter import ElectricScooter
from vehicle import Vehicle


def test_electric_car() -> None:
    print("\n========== ELECTRIC CAR TEST ==========")

    car = ElectricCar(
        vehicle_id="CAR-101",
        model="Tesla Model 3",
        battery_percentage=85.5,
        maintenance_status="Maintained",
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
    car.maintenance_status = "Need Service"
    car.rental_price = 2200.0
    car.seating_capacity = 4

    print("\nUpdated car details:")
    print(car)


def test_electric_scooter() -> None:
    print("\n========== ELECTRIC SCOOTER TEST ==========")

    scooter = ElectricScooter(
        vehicle_id="SCOOTER-201",
        model="Ather 450X",
        battery_percentage=90.0,
        maintenance_status="Maintained",
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
    scooter.maintenance_status = "Need Service"
    scooter.rental_price = 450.0
    scooter.max_speed_limit = 75.0

    print("\nUpdated scooter details:")
    print(scooter)


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
                "Maintained",
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
                "Maintained",
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
                "Maintained",
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
                "Maintained",
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
                "Maintained",
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


def main() -> None:
    print("Starting vehicle management system tests...")

    try:
        test_electric_car()
        test_electric_scooter()
        test_allowed_statuses()
        test_invalid_values()

    except Exception as error:
        print(f"\nUnexpected error occurred: {error}")


if __name__ == "__main__":
    main()