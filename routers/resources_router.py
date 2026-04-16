from typing import Optional
from fastapi import APIRouter, File, Form, Query, UploadFile
from pydantic import BaseModel
from services.assesments_service import reg_assesment
from services.resources_service import pull_resources

router=APIRouter(prefix="/resources",tags=["assesments","questions"])
# class Resources(BaseModel):
#     unit_id:str=Query(...)
@router.get("/all_resources")
async def get_resources(unit_id:str=Query(...)):
    try:
        if unit_id:
            return await pull_resources(unit_id)
    except Exception as e:
        print("error in getting resources",e)
        return {"error":"errror in getting resources::{e}"},500



@router.post("/upload_assesments")
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


@router.post('/upload_notes')
async def upload_note(
    file:UploadFile=File(...),
    # file_name:Optional[str]=Form(...),
    notes_for:str=Form(...),
    unit_id:Optional[str]=Form(None),
    subject_id:Optional[str]=Form(None)
):
    return await upload_notes(notes_for,file,unit_id,subject_id)
