from abc import ABC, abstractmethod

class Sensor(ABC): 
    def __init__(self): 
        self.units = "mm"

    @abstractmethod
    def setup(self) -> bool: 
        print("Please implement setup setting")
        return True 

    @abstractmethod
    def read(self): 
        print("Please implement read setting")
        pass 
    
    @abstractmethod
    def available(self): 
        print("Please implement configuration setting")
        pass 


        
