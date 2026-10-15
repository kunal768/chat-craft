from enum import Enum 

''' add as per requirement '''
class UpdateInterval(Enum):
    TIME_NONE = -1
    TIME_FIVE = 5 
    TIME_THIRTY = 30 
    TIME_HOUR = 60 
    TIME_DAY = 1440
    
    class Config:
        orm_mode = True
