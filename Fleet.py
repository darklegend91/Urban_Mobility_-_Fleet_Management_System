from Hub import Hub
from ElectricCar import ElectricCar
from ElectricScooter import ElectricScooter

class FleetManager:
    def __init__(self):
        self.__hubs = []
    
    def add_hub(self, name):
        """Add a new hub"""
        if self.find_hub(name):
            print(f"Hub '{name}' already exists!")
            return False
        
        new_hub = Hub(name)
        self.__hubs.append(new_hub)
        print(f"Hub '{name}' created!")
        return True
    
    def find_hub(self, name):
        """Find hub by name"""
        for hub in self.__hubs:
            if hub.name == name:
                return hub
        return None
    
    def add_vehicle_to_hub(self, hub_name, vehicle):
        """Add vehicle to specific hub"""
        hub = self.find_hub(hub_name)
        if not hub:
            print(f"Hub '{hub_name}' not found!")
            return False
        
        hub.add_vehicle(vehicle)
        return True
    
    def display_all_hubs(self):
        """Display all hubs"""
        if not self.__hubs:
            print("No hubs in system!")
            return
        
        print("\n" + "="*50)
        print("ALL HUBS IN SYSTEM")
        print("="*50)
        for hub in self.__hubs:
            print(f"\n{hub.name}")
            hub.get_all_vehicles()


def _prompt_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def _prompt_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")


def _build_vehicle():
    """Prompt the user for details and build an ElectricCar or ElectricScooter."""
    print("\nVehicle type:")
    print("1. Electric Car")
    print("2. Electric Scooter")
    vehicle_type = input("Choose an option: ").strip()

    vehicle_id = input("Vehicle ID: ").strip()
    model = input("Model: ").strip()
    battery_percentage = _prompt_float("Battery percentage (0-100): ")
    maintenance_status = input("Maintenance status ('Maintained' or 'Need Service'): ").strip()
    rental_price = _prompt_float("Rental price: ")

    if vehicle_type == "1":
        seating_capacity = _prompt_int("Seating capacity: ")
        return ElectricCar(
            vehicle_id, model, battery_percentage, maintenance_status,
            rental_price, seating_capacity,
        )
    elif vehicle_type == "2":
        max_speed_limit = _prompt_float("Maximum speed limit: ")
        return ElectricScooter(
            vehicle_id, model, battery_percentage, maintenance_status,
            rental_price, max_speed_limit,
        )
    else:
        print("Invalid vehicle type.")
        return None


def run_console() -> None:
    """Console menu for managing hubs and vehicles."""
    manager = FleetManager()

    menu = (
        "\n" + "=" * 50 + "\n"
        "FLEET MANAGEMENT SYSTEM\n"
        + "=" * 50 + "\n"
        "1. Add Hub\n"
        "2. Add Vehicle to Hub\n"
        "3. Display All Hubs\n"
        "4. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Hub name: ").strip()
            manager.add_hub(name)

        elif choice == "2":
            hub_name = input("Hub name: ").strip()
            if not manager.find_hub(hub_name):
                print(f"Hub '{hub_name}' not found!")
                continue
            try:
                vehicle = _build_vehicle()
            except ValueError as error:
                print(f"Could not create vehicle: {error}")
                continue
            if vehicle is not None:
                try:
                    manager.add_vehicle_to_hub(hub_name, vehicle)
                except ValueError as error:
                    print(f"Could not add vehicle: {error}")

        elif choice == "3":
            manager.display_all_hubs()

        elif choice == "4":
            print("Exiting Fleet Management System.")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    run_console()