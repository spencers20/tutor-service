from typing import Optional
from fastapi import APIRouter, File, Form, Query, UploadFile
from services.assesments_service import fetch_querys,  reg_assesment

router=APIRouter(prefix="/assesments",tags=["assesments","questions"])

@router.post("/create")
async def create_assesment(
    file:UploadFile=File(...),
    eligible_for:str=Form(...),
    assesment_type:str=Form(...),
    unit_id:Optional[str]=Form(None),
    subject_id:Optional[str]=Form(None)

):
    results=await reg_assesment(
        file=file,
        eligible_for=eligible_for,
        assesment_type=assesment_type,
        unit_id=unit_id,
        subject_id=subject_id
    )

    return results

@router.get("/get_question")
async def fetch_questions(assessment_id:str=Query(...)):
    try:
        if assessment_id:
            return await fetch_querys(assessment_id)

    except Exception as e:
        print(f"error in getting questions :: {e}")
        return []
    