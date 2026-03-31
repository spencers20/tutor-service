# define the API endpoints
from fastapi import APIRouter
from pydantic import BaseModel
from services.user_service import create_user
from schemas.user_schema import userCreate
import requests


router=APIRouter(prefix="/users",tags=["users"])

class TrialData(BaseModel):
    name:str
    age:int
    grade:str

@router.post("/create")
def register_user(user:userCreate):
    return create_user(user)

@router.post("/automate")
def automate_trial(trialdata:TrialData):
    name=trialdata.name
    age=trialdata.age
    grade=trialdata.grade

    insertingdata={
        name:name,
        age:age,
        grade:grade
    }

    response=requests.post(
        url="https://untawed-overheady-tony.ngrok-free.dev/webhook-test/2fa7d1ca-0672-4094-85ca-fb855770016f",
        json=insertingdata)

    print(response)

    