from typing import Optional
from fastapi import APIRouter, File, Form, UploadFile
from schemas.notes_schema import Get_Notes, Upload_Notes
from services.notes_service import get_notes, upload_notes

router=APIRouter(prefix="/notes",tags=["notes"])

@router.post('/upload_notes')
async def upload_note(
    file:UploadFile=File(...),
    # file_name:Optional[str]=Form(...),
    notes_for:str=Form(...),
    unit_id:Optional[str]=Form(None),
    subject_id:Optional[str]=Form(None)
):
    return await upload_notes(notes_for,file,unit_id,subject_id)

@router.get("/get_notes")
def get_notess(notes:Get_Notes):
    return get_notes(notes)

