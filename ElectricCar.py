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
        return super().__str__() + f"\nSeating Capacity : {self.seating_capacity}"
        
        
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