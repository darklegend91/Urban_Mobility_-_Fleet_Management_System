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
            maintenance_status="Maintained",
            rental_price=2500.0,
            seating_capacity=5,
        ),
        ElectricScooter(
            vehicle_id="SCOOTER-201",
            model="Ather 450X",
            battery_percentage=90.0,
            maintenance_status="Maintained",
            rental_price=500.0,
            max_speed_limit=80.0,
        ),
        ElectricCar(
            vehicle_id="CAR-102",
            model="Nissan Leaf",
            battery_percentage=75.0,
            maintenance_status="Need Service",
            rental_price=1800.0,
            seating_capacity=4,
        ),
        ElectricScooter(
            vehicle_id="SCOOTER-202",
            model="Ola S1 Pro",
            battery_percentage=95.0,
            maintenance_status="Maintained",
            rental_price=600.0,
            max_speed_limit=90.0,
        ),
        ElectricCar(
            vehicle_id="CAR-103",
            model="BMW i3",
            battery_percentage=60.0,
            maintenance_status="Maintained",
            rental_price=2200.0,
            seating_capacity=4,
        ),
        ElectricScooter(
            vehicle_id="SCOOTER-203",
            model="Bajaj Chetak",
            battery_percentage=70.0,
            maintenance_status="Need Service",
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


def main() -> None:
    """Main function to run all tests"""
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
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as error:
        print(f"\n" + "=" * 60)
        print(f"UNEXPECTED ERROR OCCURRED: {error}")
        print("=" * 60)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()