from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from typing import Optional


class Upload_Notes():
    notes_name:Optional[str]=Form(...)
    notes_for:str=Form(...)
    file:UploadFile=File(...)
    unit_id:Optional[str]=Form(...)
    subject_id:Optional[str]=Form(...)

# getting notes for certain course
class Get_Notes(BaseModel):
    unit_id:Optional[str]=None
    subject_id:Optional[str]=None