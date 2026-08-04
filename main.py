"""Use Case 1 
Define a class Vehicle with __init__ constructor.
Initialize attributes: vehicle_id, model, and battery_percentage.
"""

class Vehicle:
    
    def __init__(self , vehicle_id: str , model: str , battery_precentage: float) -> None:
        self.vehicle_id = vehicle_id
        self.model = model
        self.battery_precentage = battery_precentage