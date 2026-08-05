from abc import ABC , abstractmethod

class Vehicle(ABC):
    
    ALLOWED_STATUSES = {"Maintained", "Need Service"}
    
    def __init__(self , vehicle_id: str , model: str , battery_percentage: float , maintenance_status : str , rental_price : float) -> None:
        
        #Private Attributes of the Vehicale Class and can be only accesed through getter and setters
        self.vehicle_id = vehicle_id
        self.model = model
        self.battery_percentage = battery_percentage
        self.maintenance_status = maintenance_status
        self.rental_price = rental_price
        
    def __str__(self) -> str:
        return f"Vehicle #{self.vehicle_id} Details:\nModel : {self.model}\nBattery Percentage : {self.battery_percentage:.2f}\nRental Price: {self.rental_price:.2f}\nMaintainance Status : {self.maintenance_status}"
    
    #utility Methods
    @staticmethod
    def get_ALLOWED_STATUSES() -> set[str]:
        return Vehicle.ALLOWED_STATUSES
    
    @property
    def vehicle_id(self) -> str:
        return self.__vehicle_id
    
    @vehicle_id.setter
    def vehicle_id(self , id : str) -> None:
        self.__vehicle_id = id
        
    @property
    def model(self) -> str:
        return self.__model
        
    @model.setter
    def model(self , model: str) -> None:
        self.__model = model
    
    @property
    def battery_percentage(self) -> float:
        return self.__battery_percentage
    
    @battery_percentage.setter
    def battery_percentage(self , value: float) -> None:
        if not 0 <= value <= 100:
                    raise ValueError("battery_percentage cannot be more than 100 or less than 0")
        self.__battery_percentage = value
        
    @property
    def maintenance_status(self) -> str:
        return self.__maintenance_status
        
    @maintenance_status.setter
    def maintenance_status(self , status : str) -> None:
        if status not in Vehicle.ALLOWED_STATUSES:
            raise ValueError("Status must be 'Maintained' or 'Need Service'")
        self.__maintenance_status = status
    
    @property
    def rental_price(self) -> float:
        return self.__rental_price
    
    @rental_price.setter
    def rental_price(self , value : float) -> None:
        if value < 0:
            raise ValueError("Price can not be Negative")
        self.__rental_price = value
        
    @abstractmethod
    def calculate_trip_cost(self , distance: float) -> float:
        pass