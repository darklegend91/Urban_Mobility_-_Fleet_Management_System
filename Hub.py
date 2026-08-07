from vehicle import Vehicle
from ElectricCar import ElectricCar
from ElectricScooter import ElectricScooter

class Hub:

    def __init__(self , name : str) -> None:
        self.__name = name
        self.__vehicles = []

    def __str__(self) -> str:
        """Return all hub vehicles sorted alphabetically by model."""
        heading = f"Hub: {self.__name}"
        if not self.__vehicles:
            return f"{heading}\nNo vehicles found"

        divider = "-" * 45
        vehicle_details = f"\n{divider}\n".join(
            str(vehicle) for vehicle in self.sort_vehicles()
        )
        return (
            f"{heading}\n"
            f"Vehicles sorted by model\n"
            f"{divider}\n"
            f"{vehicle_details}\n"
            f"{divider}"
        )
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def vehicles(self):
        return self.__vehicles
    
    def find_vehicle(self, vehicle_id: str):
        """Find vehicle by ID using list comprehension."""
        found = [v for v in self.__vehicles if v.vehicle_id == vehicle_id]
        return found[0] if found else None


    def add_vehicle(self ,vehicle ) -> None:

        if self.find_vehicle(vehicle.vehicle_id):
            raise ValueError(f"Vehicle with {vehicle.vehicle_id} is already in {self.name}")

        self.__vehicles.append(vehicle)
        print(f"{vehicle.vehicle_id} is added to {self.name}")


    def remove_vehicle(self , vehicle_id):
        for vehicle in self.__vehicles:
            if vehicle.vehicle_id == vehicle_id:
                self.__vehicles.remove(vehicle)
                print(f"Vehicle {vehicle_id} removed from {self.__name}")
                return vehicle

        raise ValueError(f"Vehicle {vehicle_id} not found in {self.__name}")

    
    def sort_vehicles_aplhabetical(self) -> list[Vehicle]:
        """Return vehicles sorted alphabetically by model name."""
        return sorted(
            self.__vehicles,
            key=lambda vehicle: vehicle.model.lower(),
        )

    def sort_vehicles(self, sort_by: str = "model") -> list[Vehicle]:
      sort_options = {
          "model": (
              lambda vehicle: vehicle.model.casefold(),
              False,
          ),
          "battery": (
              lambda vehicle: vehicle.battery_percentage,
              True,
          ),
          "fare": (
              lambda vehicle: vehicle.rental_price,
              True,
          ),
      }

      if sort_by not in sort_options:
          raise ValueError("Sort option must be 'model', 'battery', or 'fare'")

      sort_key, descending = sort_options[sort_by]

      return sorted(
          self.__vehicles,
          key=sort_key,
          reverse=descending,
      )

    def get_all_vehicles(self):
        """Display full car details separately from scooter details."""
        if not self.__vehicles:
            print(f"No vehicles found in {self.name} hub")
            return

        cars = [
            vehicle for vehicle in self.__vehicles
            if isinstance(vehicle, ElectricCar)
        ]
        scooters = [
            vehicle for vehicle in self.__vehicles
            if isinstance(vehicle, ElectricScooter)
        ]

        print(f" Vehicles in {self.__name}:")
        for heading, vehicles in (
            ("ELECTRIC CARS", cars),
            ("ELECTRIC SCOOTERS", scooters),
        ):
            print(f"\n {heading}")
            print(" " + "-" * 40)
            if not vehicles:
                print(" No vehicles found")
                continue

            for vehicle in vehicles:
                for detail_line in str(vehicle).splitlines():
                    print(f" {detail_line}")
                print(" " + "-" * 40)
