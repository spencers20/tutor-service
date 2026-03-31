
from pydantic import BaseModel

class curriculumcreate(BaseModel):
    country:str

class academiclevelcreate(BaseModel):
    level_name:str
    curriculum_id:str

class coursecreate(BaseModel):
    course_name:str
    academic_level:str

class unitscreate(BaseModel):
    unit_name:str
    course_id:str

class subjectcreate(BaseModel):
    subject_name:str
    academiclevel_id:str
