
from fastapi import APIRouter,Query
from schemas.course_units_schema import Get_Units
from services.course_units import get_nodes, get_units


router=APIRouter(prefix="/course_units",tags=["course","units"])

@router.get("/allunits")
def call_units(course_id:str=Query(...)):
    print("all")
    response=get_units(course_id)
    if response:
        print(response)
        return response
    else:
        print ("no response returned ..")
        return []
    
@router.get("/get_nodes")
def milestone_nodes(unit_id:str=Query(...)):
    print("getting milestones...")
    response=get_nodes(unit_id)
    if response:
        return response
    else:
        print("no resposense found")
        return []