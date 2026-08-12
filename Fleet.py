import csv
import json
from collections import defaultdict
from pathlib import Path

from Hub import Hub
from ElectricCar import ElectricCar
from ElectricScooter import ElectricScooter
from vehicle import Vehicle


class FleetManager:
    CSV_FILE_NAME = "vehicle_data.csv"
    JSON_FILE_NAME = "fleet_data.json"
    # Kept as an alias for code written before JSON support was added.
    file_name = CSV_FILE_NAME
    CSV_FIELDS = (
        "hub_name",
        "vehicle_type",
        "vehicle_id",
        "model",
        "battery_percentage",
        "maintenance_status",
        "rental_price",
        "seating_capacity",
        "max_speed_limit",
    )

    def __init__(self):
        self.__hubs = []
        self.__vehicle_dict: defaultdict[str, list[Vehicle]] = defaultdict(
            list,
            {
                "Electric Car": [],
                "Electric Scooter": [],
            },
        )

    @staticmethod
    def _get_vehicle_type(vehicle: Vehicle) -> str:
        """Return the dictionary key for a supported vehicle object."""
        if isinstance(vehicle, ElectricCar):
            return "Electric Car"
        if isinstance(vehicle, ElectricScooter):
            return "Electric Scooter"
        raise TypeError("Only ElectricCar and ElectricScooter objects are supported")

    @property
    def vehicle_dict(self) -> defaultdict[str, list[Vehicle]]:
        """Map each vehicle type to the vehicle objects of that type."""
        return self.__vehicle_dict

    @vehicle_dict.setter
    def vehicle_dict(self, vehicle: Vehicle) -> None:
        vehicle_type = self._get_vehicle_type(vehicle)
        vehicles = self.__vehicle_dict[vehicle_type]
        if not any(existing is vehicle for existing in vehicles):
            vehicles.append(vehicle)

    
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

        # Validate before changing the hub, so both collections stay in sync.
        self._get_vehicle_type(vehicle)
        hub.add_vehicle(vehicle)
        self.vehicle_dict = vehicle
        return True

    def remove_vehicle_from_hub(self, hub_name, vehicle_id):
        """Remove a vehicle from a hub and its vehicle-type collection."""
        hub = self.find_hub(hub_name)
        if not hub:
            print(f"Hub '{hub_name}' not found!")
            return None

        removed_vehicle = hub.remove_vehicle(vehicle_id)
        vehicle_type = self._get_vehicle_type(removed_vehicle)
        exists_in_another_hub = any(
            vehicle is removed_vehicle
            for other_hub in self.__hubs
            for vehicle in other_hub.vehicles
        )
        if not exists_in_another_hub:
            self.__vehicle_dict[vehicle_type] = [
                vehicle
                for vehicle in self.__vehicle_dict[vehicle_type]
                if vehicle is not removed_vehicle
            ]
        return removed_vehicle

    def to_dict(self) -> dict:
        """Return the complete nested fleet in a JSON-serializable form."""
        return {"hubs": [hub.to_dict() for hub in self.__hubs]}

    def save_to_csv(self, file_path=None) -> int:
        """Save every vehicle and its hub to a CSV file."""
        csv_path = file_path if file_path is not None else self.file_name
        vehicle_count = 0

        with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.CSV_FIELDS)
            writer.writeheader()

            for hub in self.__hubs:
                for vehicle in hub.vehicles:
                    vehicle_type = self._get_vehicle_type(vehicle)
                    row = {
                        "hub_name": hub.name,
                        "vehicle_type": vehicle_type,
                        "vehicle_id": vehicle.vehicle_id,
                        "model": vehicle.model,
                        "battery_percentage": vehicle.battery_percentage,
                        "maintenance_status": vehicle.maintenance_status,
                        "rental_price": vehicle.rental_price,
                        "seating_capacity": "",
                        "max_speed_limit": "",
                    }

                    if isinstance(vehicle, ElectricCar):
                        row["seating_capacity"] = vehicle.seating_capacity
                    else:
                        row["max_speed_limit"] = vehicle.max_speed_limit

                    writer.writerow(row) #type:ignore
                    vehicle_count += 1

        print(f"Saved {vehicle_count} vehicle(s) to {csv_path}.")
        return vehicle_count

    def load_from_csv(self, file_path=None) -> int:
        """Load fleet data from CSV, replacing the manager's current data."""
        csv_path = file_path if file_path is not None else self.file_name

        loaded_hubs = []
        loaded_vehicle_dict: defaultdict[str, list[Vehicle]] = defaultdict(
            list,
            {
                "Electric Car": [],
                "Electric Scooter": [],
            },
        )
        vehicle_count = 0

        try:
            csv_file = open(csv_path, "r", newline="", encoding="utf-8")
        except FileNotFoundError:
            print(f"No saved fleet data found at {csv_path}.")
            return 0

        with csv_file:
            reader = csv.DictReader(csv_file)
            available_fields = set(reader.fieldnames or [])
            missing_fields = set(self.CSV_FIELDS) - available_fields
            if missing_fields:
                missing = ", ".join(sorted(missing_fields))
                raise ValueError(f"CSV file is missing required column(s): {missing}")

            for row_number, row in enumerate(reader, start=2):
                if not any(
                    str(value).strip()
                    for value in row.values()
                    if value is not None
                ):
                    continue

                def required_value(field_name):
                    value = (row.get(field_name) or "").strip()
                    if not value:
                        raise ValueError(
                            f"CSV row {row_number} has no value for {field_name}"
                        )
                    return value

                try:
                    hub_name = required_value("hub_name")
                    vehicle_type = required_value("vehicle_type")
                    common_values = {
                        "vehicle_id": required_value("vehicle_id"),
                        "model": required_value("model"),
                        "battery_percentage": float(
                            required_value("battery_percentage")
                        ),
                        "maintenance_status": required_value(
                            "maintenance_status"
                        ),
                        "rental_price": float(required_value("rental_price")),
                    }

                    if vehicle_type == "Electric Car":
                        vehicle = ElectricCar(
                            **common_values,
                            seating_capacity=int(
                                required_value("seating_capacity")
                            ),
                        )
                    elif vehicle_type == "Electric Scooter":
                        vehicle = ElectricScooter(
                            **common_values,
                            max_speed_limit=float(
                                required_value("max_speed_limit")
                            ),
                        )
                    else:
                        raise ValueError(
                            f"unsupported vehicle type '{vehicle_type}'"
                        )

                    hub = next(
                        (hub for hub in loaded_hubs if hub.name == hub_name),
                        None,
                    )
                    if hub is None:
                        hub = Hub(hub_name)
                        loaded_hubs.append(hub)

                    hub.add_vehicle(vehicle)
                    loaded_vehicle_dict[vehicle_type].append(vehicle)
                    vehicle_count += 1
                except (TypeError, ValueError) as error:
                    raise ValueError(
                        f"Invalid fleet data in CSV row {row_number}: {error}"
                    ) from error

        # Replace the live collections only after the entire file is valid.
        self.__hubs = loaded_hubs
        self.__vehicle_dict = loaded_vehicle_dict
        print(f"Loaded {vehicle_count} vehicle(s) from {csv_path}.")
        return vehicle_count

    def save_to_json(self, file_path=None) -> int:
        """Save hubs and their custom vehicle objects as nested JSON data."""
        json_path = file_path if file_path is not None else self.JSON_FILE_NAME
        vehicle_count = sum(len(hub.vehicles) for hub in self.__hubs)

        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(self.to_dict(), json_file, indent=4)

        print(f"Saved {vehicle_count} vehicle(s) to {json_path}.")
        return vehicle_count

    @staticmethod
    def _vehicle_from_json(vehicle_data: dict) -> Vehicle:
        """Recreate the correct custom vehicle type from one JSON object."""
        common_values = {
            "vehicle_id": vehicle_data["vehicle_id"],
            "model": vehicle_data["model"],
            "battery_percentage": vehicle_data["battery_percentage"],
            "maintenance_status": vehicle_data["maintenance_status"],
            "rental_price": vehicle_data["rental_price"],
        }

        vehicle_type = vehicle_data["type"]
        if vehicle_type == "ElectricCar":
            return ElectricCar(
                **common_values,
                seating_capacity=vehicle_data["seating_capacity"],
            )
        if vehicle_type == "ElectricScooter":
            return ElectricScooter(
                **common_values,
                max_speed_limit=vehicle_data["max_speed_limit"],
            )
        raise ValueError(f"Unsupported vehicle type '{vehicle_type}'")

    def load_from_json(self, file_path=None) -> int:
        """Load nested JSON data, replacing the manager's current fleet."""
        json_path = file_path if file_path is not None else self.JSON_FILE_NAME

        try:
            with open(json_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print(f"No saved fleet data found at {json_path}.")
            return 0

        if not isinstance(data, dict) or not isinstance(data.get("hubs"), list):
            raise ValueError("JSON data must contain a 'hubs' list")

        loaded_hubs = []
        loaded_vehicle_dict: defaultdict[str, list[Vehicle]] = defaultdict(
            list,
            {
                "Electric Car": [],
                "Electric Scooter": [],
            },
        )
        vehicle_count = 0

        try:
            for hub_number, hub_data in enumerate(data["hubs"], start=1):
                if not isinstance(hub_data, dict):
                    raise ValueError(f"hub {hub_number} must be a JSON object")

                hub_name = hub_data["name"]
                vehicle_data_list = hub_data["vehicles"]
                if not isinstance(hub_name, str) or not hub_name.strip():
                    raise ValueError(f"hub {hub_number} has an invalid name")
                if not isinstance(vehicle_data_list, list):
                    raise ValueError(
                        f"vehicles for hub '{hub_name}' must be a list"
                    )
                if any(hub.name == hub_name for hub in loaded_hubs):
                    raise ValueError(f"duplicate hub name '{hub_name}'")

                hub = Hub(hub_name)
                loaded_hubs.append(hub)

                for vehicle_data in vehicle_data_list:
                    if not isinstance(vehicle_data, dict):
                        raise ValueError(
                            f"vehicle data in hub '{hub_name}' must be an object"
                        )
                    vehicle = self._vehicle_from_json(vehicle_data)
                    hub.add_vehicle(vehicle)
                    vehicle_type = self._get_vehicle_type(vehicle)
                    loaded_vehicle_dict[vehicle_type].append(vehicle)
                    vehicle_count += 1
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Invalid fleet data in JSON: {error}") from error

        # Do not replace valid live data unless the whole JSON file is valid.
        self.__hubs = loaded_hubs
        self.__vehicle_dict = loaded_vehicle_dict
        print(f"Loaded {vehicle_count} vehicle(s) from {json_path}.")
        return vehicle_count

    @staticmethod
    def view_file(file_path: str) -> str:
        """Print and return the contents of a saved CSV or JSON file."""
        with open(file_path, "r", encoding="utf-8") as data_file:
            contents = data_file.read()

        print(f"\nContents of {file_path}")
        print("=" * 60)
        print(contents.rstrip() if contents else "The file is empty.")
        print("=" * 60)
        return contents
    
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

    def display_vehicles_by_type(self):
        """Display full car details separately from scooter details."""
        if not any(self.__vehicle_dict.values()):
            print("No vehicles in system!")
            return

        print("\n" + "=" * 50)
        print("ALL VEHICLES BY TYPE")
        print("=" * 50)

        headings = {
            "Electric Car": "ELECTRIC CARS",
            "Electric Scooter": "ELECTRIC SCOOTERS",
        }
        for vehicle_type, vehicles in self.__vehicle_dict.items():
            print(f"\n{headings[vehicle_type]}")
            print("-" * 50)
            if not vehicles:
                print("No vehicles found")
                continue

            for vehicle in vehicles:
                print(vehicle)
                print("-" * 50)

    def search_by_hub(self, hub_name):
        hub = self.find_hub(hub_name)

        if not hub:
            print("Hub not found")
            return

        if not hub.vehicles:
            print("No vehicles found")
            return

        hub.get_all_vehicles()

    def search_by_battery(self):
        vehicles = [
            vehicle
            for hub in self.__hubs
            for vehicle in filter(
                lambda vehicle: vehicle.battery_percentage > 80,
                hub.vehicles,
            )
        ]

        if not vehicles:
            print("No vehicles found with battery above 80%")
            return

        for vehicle in vehicles:
            print(vehicle)

    def get_status(self) -> dict[str, int]:
        """Return and display the number of vehicles in each current status."""
        status_counts = {
            "Available": 0,
            "On Trip": 0,
            "Under Maintenance": 0,
        }

        for vehicles in self.__vehicle_dict.values():
            for vehicle in vehicles:
                status_counts[vehicle.maintenance_status] += 1

        print("\n" + "=" * 45)
        print("VEHICLE STATUS SUMMARY")
        print("=" * 45)
        for status, count in status_counts.items():
            print(f"{status:<20}: {count}")
        print("-" * 45)
        print(f"{'Total Vehicles':<20}: {sum(status_counts.values())}")
        print("=" * 45)

        return status_counts

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


def _choose_data_file() -> tuple[str, str] | None: # type:ignore
    """Ask for CSV or JSON and return its format and selected filename."""
    print("\nFile format:")
    print("1. CSV")
    print("2. JSON")
    file_choice = input("Choose a format: ").strip()

    file_options = {
        "1": ("csv", FleetManager.CSV_FILE_NAME, ".csv"),
        "2": ("json", FleetManager.JSON_FILE_NAME, ".json"),
    }
    if file_choice not in file_options:
        print("Invalid file format.")
        return None

    file_format, default_name, required_suffix = file_options[file_choice]
    entered_name = input(
        f"File name (press Enter to use '{default_name}'): "
    ).strip()
    if not entered_name:
        return file_format, default_name

    selected_path = Path(entered_name)
    if selected_path.suffix.casefold() != required_suffix:
        selected_path = selected_path.with_suffix(required_suffix)
        print(f"Using file name '{selected_path}'.")

    return file_format, str(selected_path)


def _build_vehicle():
    """Prompt the user for details and build an ElectricCar or ElectricScooter."""
    print("\nVehicle type:")
    print("1. Electric Car")
    print("2. Electric Scooter")
    vehicle_type = input("Choose an option: ").strip()

    vehicle_id = input("Vehicle ID: ").strip()
    model = input("Model: ").strip()
    battery_percentage = _prompt_float("Battery percentage (0-100): ")
    maintenance_status = input(
        "Maintenance status ('Available', 'On Trip', or 'Under Maintenance'): "
    ).strip()
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
        "4. Search Vehicles by Hub\n"
        "5. Search Vehicles with Battery Above 80%\n"
        "6. Display All Vehicles by Type\n"
        "7. Get Status of all vehicles by their Current status\n"
        "8. Save Fleet Data\n"
        "9. Load Fleet Data\n"
        "10. View a CSV or JSON File\n"
        "11. Exit\n"
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
            hub_name = input("Enter hub name: ").strip()
            manager.search_by_hub(hub_name)

        elif choice == "5":
            manager.search_by_battery()

        elif choice == "6":
            manager.display_vehicles_by_type()

        elif choice == "7":
            manager.get_status()

        elif choice == "8":
            selected_file = _choose_data_file()
            if selected_file is None:
                continue
            file_format, file_path = selected_file
            try:
                if file_format == "csv":
                    manager.save_to_csv(file_path)
                else:
                    manager.save_to_json(file_path)
            except (OSError, csv.Error, TypeError) as error:
                print(f"Could not save fleet data: {error}")

        elif choice == "9":
            selected_file = _choose_data_file()
            if selected_file is None:
                continue
            file_format, file_path = selected_file
            try:
                if file_format == "csv":
                    manager.load_from_csv(file_path)
                else:
                    manager.load_from_json(file_path)
            except (OSError, csv.Error, ValueError) as error:
                print(f"Could not load fleet data: {error}")

        elif choice == "10":
            selected_file = _choose_data_file()
            if selected_file is None:
                continue
            _, file_path = selected_file
            try:
                manager.view_file(file_path)
            except OSError as error:
                print(f"Could not view data file: {error}")

        elif choice == "11":
            print("Exiting Fleet Management System.")
            break

        else:
            print("Invalid choice, please try again.")
