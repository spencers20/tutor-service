
from fastapi import APIRouter
from schemas.course_units_schema import Get_Units
from services.course_units import get_units


router=APIRouter(prefix="/course_units",tags=["course","units"])

@router.get("/get_units")
def call_units(course:Get_Units):
    response=get_units(course)
    if response:
        print(response)
        return response
    else:
        
        return {"response":response},500