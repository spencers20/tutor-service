from fastapi import APIRouter
from schemas.curriculum_units_schema import academiclevelcreate, coursecreate, curriculumcreate, subjectcreate, unitscreate
from services.curriculum_units import create_academiclevel, create_course, create_curriculum, create_subject, create_units

router=APIRouter(prefix="/curriculum",tags=["curriculum","course","unit","subject"])

@router.post("/create_curriculum")
def create_curric(curriculum:curriculumcreate):
    response= create_curriculum(curriculum)
    return response

@router.post("/create_academiclevel")
def make_academiclevel(academic_level:academiclevelcreate):
    response=create_academiclevel(academic_level)
    return response

@router.post("/create_course")
def make_course(course:coursecreate):
    response=create_course(course)
    return response

@router.post("/create_units")
def make_units(units:unitscreate):
    response=create_units(units)
    print(f"inserting units response {response}")
    return response

@router.post("/create_subject")
def make_subjects(subjects:subjectcreate):
    response=create_subject(subjects)
    return response