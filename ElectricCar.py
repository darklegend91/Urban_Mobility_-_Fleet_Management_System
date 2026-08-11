from vehicle import Vehicle

class ElectricCar(Vehicle):
    """ This is Electric Car class inherited from vehicle class"""
    def __init__(self ,
                 vehicle_id: str , 
                 model: str , 
                 battery_percentage: float , 
                 maintenance_status : str , 
                 rental_price : float,
                 seating_capacity : int) -> None:
                
        super().__init__(vehicle_id , 
                         model , 
                         battery_percentage , 
                         maintenance_status , 
                         rental_price)
        
        self.seating_capacity = seating_capacity
        
    
    def __str__(self) -> str:
        """Return clean electric-car details for console output."""
        return super().__str__() + f"\n  Seating Capacity: {self.seating_capacity}"

    def to_dict(self) -> dict:
        """Add car-specific values to the serialized vehicle data."""
        data = super().to_dict()
        data.update(
            {
                "type": "ElectricCar",
                "seating_capacity": self.seating_capacity,
            }
        )
        return data
        
        
    @property
    def seating_capacity(self) -> int:
        return self.__seating_capacity
    
    @seating_capacity.setter
    def seating_capacity(self , value : int) -> None:
        if value<=0:
            raise ValueError("Seating capacity must be not 0 or negative.")
        self.__seating_capacity = value
        

    def calculate_trip_cost(self, distance: float) -> float:
        return 5.00 + (0.50 * distance)
