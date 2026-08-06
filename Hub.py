from vehicle import Vehicle
from ElectricCar import ElectricCar
from ElectricScooter import ElectricScooter

class Hub:
    
    def __init__(self , name : str) -> None:
        self.__name = name
        self.__vehicles = []
    
    @property
    def name(self) -> str:
        return self.__name
    
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

    
    def get_all_vehicles(self):
        """Display all vehicles in the hub."""
        if not self.__vehicles:
            print(f"No vehicles found in {self.name} hub")
            return
        
        print(f" Vehicles in {self.__name}:")
        for vehicle in self.__vehicles:
            vehicle_type = "Car" if isinstance(vehicle, ElectricCar) else "Scooter"
            print(f" - {vehicle.vehicle_id}: {vehicle.model} ({vehicle_type})")