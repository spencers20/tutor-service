# define the request and response structure/types
from typing import Optional
from pydantic import BaseModel


class userCreate(BaseModel):
    name:str
    email:str
    phone_number:Optional[int]=None
    curriculum:Optional[str]=None #kenyan , american etc
    level:Optional[str]=None
    course:Optional[str]=None  #if university student