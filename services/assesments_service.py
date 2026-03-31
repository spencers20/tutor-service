import re
from typing import Optional
from fastapi import UploadFile
import vercel_blob
from database.db import get_db
from schemas.assesment_schema import Assesment_Data
import fitz
import requests
from datetime import datetime

token="vercel_blob_rw_3Pum5QwJd8qrCfRj_FMBAachsrpnpF9Qh1tD8ZpkyZJh4Io"

async def reg_assesment(
        file:UploadFile,
        eligible_for:str,
        assesment_type:str,
        assesment_name:Optional[str]=None,
        unit_id:Optional[str]=None,
        subject_id:Optional[str]=None
):
    file_contents=await file.read()
    file_name=file.filename

    try:
        pages=extract_file(file_contents)
        chunks=merge_short_pages(pages)
        store_file_res=vercel_blob.put(
            file_name,
            file_contents,
            {
                "access":"public",
                "token":token
            }
        )

        file_url=store_file_res["url"]
        if unit_id:
            query="INSERT INTO assesments(assesment_name,assesment_type, eligible_for,unit_id,file_path) VALUES (%s,%s,%s,%s,%s) RETURNING assesment_id"
            params=(file_name,assesment_type,eligible_for,unit_id,file_url)
        elif subject_id:
            query="INSERT INTO assesments(assesment_name,assesment_type, eligible_for,subject_id,file_path) VALUES (%s,%s,%s,%s,%s) RETURNING assesment_id"
            params=(file_name,assesment_type,eligible_for,subject_id,file_url)

        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query,params)
                assesment_id=cur.fetchone()[0]
                cur.commit()

                if assesment_id:
                    all_responses=[]
                    errors=[]
                    for i,chunk in enumerate(chunks):
                        print(f"processing chunk {i+1} out of {len(chunks)}")
                        url='https://untawed-overheady-tony.ngrok-free.dev/webhook-test/513e7382-0b44-4149-8fc8-3c1462626ffa'
                        data={
                           "chunk":chunk,
                           "assesment_id":assesment_id,
                           "date":datetime.now()
                        }
                        response=requests.post(url=url,json=data)
                        response_data=response.json()
                        if response.status_code==200:
                            print(f"✅ Chunk {i+1} processed successfully")
                            all_responses.append({
                                "chunk": i + 1,
                                "status": "success",
                                "data": response_data
                            })
                            
                        else:
                            print(f"❌ Chunk {i+1} failed: {response.status_code}")
                            errors.append({
                                "chunk": i + 1,
                                "status": "error",
                                "error": response_data
                            })
                        
                        all_responses.append({f"chunk {i+1}":response})
                    
                    # for res in all_responses:
                    #     print(res)

                    if len(all_responses) ==len(chunks):
                        print("all chunks processed successfully ")
                        return {"success":"all chunks processed successfully"}
                    else:
                        print("errors occurred")
                        return {
                            "errors":errors
                        }
    


    except Exception as e:
        return {"error":f"Error entering data on the assesment table ::{e}"}

    


def extract_file(file_contents):
    doc=fitz.open(stream=file_contents,filetype="pdf")
    pages=[]

    for i,page in enumerate(doc):
        text=page.get_text().strip()
        if text:
            pages.append({"page":i+1,"text":text})
    doc.close()
    return pages

# using regex for overlap, overlap the next question fully
question_pattern= r'(\d+\.\s|Q\d+\.\s|Question\s\d+)'

def get_overlap(next_chunk_text):
    matches=list(re.finditer(question_pattern,next_chunk_text))

    if len(matches)>0:
        # get the first 3 sentences instead 
        sentences = re.split(r'(?<=[.!?])\s+',next_chunk_text)
        return "".join(sentences[:3])
    
    elif len(matches)==1:
        return next_chunk_text[matches[0].start():]
    
    else:
        return next_chunk_text[matches[0].start():matches[1].start()].strip()

def merge_short_pages(pages, min_words=100):
    buffer=""
    merged=[]
    buffer_pages=[]

    for p in pages:
        word_count=len(p["text"].split())
        if word_count<min_words:
            buffer +=""+p["text"]
            buffer_pages.append(p["page"])
        else:
            if buffer:
                merged.append({"pages":buffer_pages,"text":buffer.strip()})
                buffer=""
                buffer_pages=[]
            merged.append({"pages":p["page"],"text":p["text"]})

    if buffer:
        merged.append({"pages":buffer_pages,"text":buffer.strip()})
    
    chunks=[]
    
    for i, chunk in enumerate (merged):
        if i+1 < len(merged):
            overlap=get_overlap(merged[i+1]["text"])
            text=chunk["text"] + "[OVERLAP]" +overlap
        else:
            text=chunk["text"]
        
        chunks.append({
            "pages":chunk["pages"],
            "text":text
        })
    
    return chunks

