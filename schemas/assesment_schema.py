from typing import Optional
from pydantic import BaseModel

class Assesment_Data(BaseModel):
    assesment_name:str
    assesment_type:str
    eligible_for:str
    file_path:Optional[str]=None
    unit_id:Optional[str]=None
    subject_id:Optional[str]=None