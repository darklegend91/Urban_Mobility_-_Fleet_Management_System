from vehicle import Vehicle

class ElectricScooter(Vehicle):
    """ This is Electric Scooter class inherited from vehicle class"""
    def __init__(self ,
                     vehicle_id: str , 
                     model: str , 
                     battery_percentage: float , 
                     maintenance_status : str , 
                     rental_price : float,
                     max_speed_limit : float) -> None:
            
        super().__init__(vehicle_id , model , battery_percentage , maintenance_status , rental_price)
        
        self.max_speed_limit = max_speed_limit
    
    def __str__(self) -> str:
        """Return clean electric-scooter details for console output."""
        return super().__str__() + (
            f"\n  Maximum Speed Limit: {self.max_speed_limit:.2f}"
        )

    def to_dict(self) -> dict:
        """Add scooter-specific values to the serialized vehicle data."""
        data = super().to_dict()
        data.update(
            {
                "type": "ElectricScooter",
                "max_speed_limit": self.max_speed_limit,
            }
        )
        return data
    
    @property
    def max_speed_limit(self) ->float:
        return self.__max_speed_limit
    
    @max_speed_limit.setter
    def max_speed_limit(self , speed : float):
        if speed <=0:
                    raise ValueError("Speed Must be greater than 0.")
        self.__max_speed_limit = speed
        
    def calculate_trip_cost(self, distance: float) -> float:
            return  1.0 + (distance * 0.15)
