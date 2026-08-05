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
        return super().__str__()+ f"\nMaximum Speed Limit : {self.max_speed_limit}"
    
    @property
    def max_speed_limit(self) ->float:
        return self.__max_speed_limit
    
    @max_speed_limit.setter
    def max_speed_limit(self , speed : float):
        if speed <=0:
                    raise ValueError("Speed Must be greater than 0.")
        self.__max_speed_limit = speed
        
    def calculate_trip_cost(self, distance: float) -> float:
            return distance * self.rental_price