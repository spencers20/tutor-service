from typing import Optional
from fastapi import APIRouter,UploadFile,File,Form
from database.db import get_db
from schemas.notes_schema import Get_Notes, Upload_Notes
import vercel_blob
import os


token="vercel_blob_rw_3Pum5QwJd8qrCfRj_FMBAachsrpnpF9Qh1tD8ZpkyZJh4Io"



async def upload_notes(
        notes_for:str,
        file:UploadFile,
        # file_name:Optional[str]=None,
        unit_id:Optional[str]=None,
        subject_id:Optional[str]=None

):
    # notes_name:Optional[str]=Form(...),
    # notes_for:str=Form(...),
    # file:UploadFile=File(...)
    # ):
    print("entereed upload notes...")
    file_contents=await file.read()
    file_name= file.filename
    notes_for=notes_for
    unit_id=unit_id
    subject_id=subject_id

    print("storing the file on vercel",file_name)
    storefile_res=vercel_blob.put(
        file_name,
        file_contents,
        {
            "access":"public",
            "token":token
        }
    )

    file_url=storefile_res["url"]

    print('file_url:..',file_url)
    
    if not file_url:
        print('file_url..not created')
        return {
            "error":"no file_url"
        }
    
    if unit_id:
        query="INSERT INTO resources (name,type,eligible_for,unit_id,url) VALUES (%s,%s,%s,%s)"
        params=(file_name,'notes',notes_for,unit_id,file_url)
    else:
        query="INSERT INTO resources (name,type,eligible_for,subject_id,url) VALUES (%s,%s,%s,%s)"
        params=(file_name,'notes',notes_for,subject_id,file_url)
    
    try:
        # get the unit_id pk-to be used as fk
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute (query,params)
                conn.commit()
                if cur.rowcount>0:
                    print("inserted...")
                    return{
                        "message":"created notes successfully",
                    },200
                else:
                    return {"error":"error in creating notes"},500

            
            
    except Exception as e:
        return {"error":"error in uploading the notes"}

# get all notes for a specific course
def get_notes(notes:Get_Notes):
    try:
        unit_id=notes.unit_id
        subject_id=notes.subject_id

        if unit_id:
            query='SELECT * FROM notes WHERE unit_id=%s'
            params=(unit_id,)
    
        else:
            query='SElECT * FROM notes WHERE subject_id=%s'
            params=(subject_id,)
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query,params)

                data_res=cur.fetchall()
                if data_res:
                    columns=[desc[0] for desc in cur.description]
                    data=[zip(columns,row) for row in data_res]

                    return data
                else:
                    return []

    except Exception as e:
        return {"error":f"Exception error in getting the notes for id {unit_id} //{subject_id} errror::{e}"}



   