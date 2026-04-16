import asyncio
import re
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
import vercel_blob
from database.db import get_db
from schemas.assesment_schema import Assesment_Data
import fitz
import requests
from datetime import datetime
import httpx

token="vercel_blob_rw_3Pum5QwJd8qrCfRj_FMBAachsrpnpF9Qh1tD8ZpkyZJh4Io"
class assesment_questions(BaseModel):
    assessment_id:str

async def fetch_querys(assessment_id:str):
    try:
        print("getting the questions....",assessment_id)
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM questions WHERE assessment_id=%s",(assessment_id,))

                all_questions=cur.fetchall()
                print("all_questions",all_questions)
                if (all_questions):
                    columns=[desc[0] for desc in cur.description]
                    questions_data=[dict(zip(columns,row))for row in all_questions]
                    return questions_data
                else:
                    return{"error":f"no questions_data...[]"}
    except Exception as e:
        print("error in getting the questions",e)


# Main service --store questions to db
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
                "addRandomSuffix":True,
                "token":token
            }
        )

        file_url=store_file_res["url"]
        questions,question_number=await get_questions(chunks,file_url)
        print(f"questions {len(questions)} , question_number {question_number}")
        print("questions...",questions)
        if unit_id:
            query="INSERT INTO resources(name,type,assesment_type, eligible_for,unit_id,url) VALUES (%s,%s,%s,%s,%s) RETURNING _id"
            params=(file_name,'assessments',assesment_type,eligible_for,unit_id,file_url)
        elif subject_id:
            query="INSERT INTO resources(name,type,assesment_type, eligible_for,subject_id,url) VALUES (%s,%s,%s,%s,%s) RETURNING _id"
            params=(file_name,'assessments',assesment_type,eligible_for,subject_id,file_url)

        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query,params)
                assesment_id=cur.fetchone()[0]
                question_inserting_count=0
                for n,question in enumerate(questions):
                    print(f"questions...{n}")
                    quizz=question.get("question")
                    answer=question.get("answer")
                    explanation=question.get("explanation")
                    created_at_time=datetime.now()
                    question_number=n

                    query_params=(assesment_id,quizz,answer,explanation,created_at_time,question_number)
                    
                    max_trial=3
                    inserted=False
                    for i in range (0,max_trial):
                        try:
                            print(f'entering with trial {i}')
                            cur.execute('INSERT INTO questions(assesment_id,question,answer,explanation,created_at,question_number) values (%s,%s,%s,%s,%s,%s)',query_params)
                            if cur.rowcount >0:
                                print(f'question {n} saved sucessfully')
                                question_inserting_count+=1
                                inserted=True
                                break
                            else:
                                print(f"question {n} failed..continuing")
                                continue
                        
                        except Exception as e:
                            print("error in inserting {i}",e)
                        if i<max_trial:
                            wait=i * 5
                            print(f"retrying in {wait}s ..")
                            await asyncio.sleep(wait)
                    
                    if not inserted:
                        print(f"❌ Question {n} failed all {max_trial} trials — rolling back")
                        conn.rollback()
                        return {"error":f"Failed to insert question {n} after {max_trial} attempts. All changes rolled back."}
                
                if question_inserting_count ==len(questions):
                    conn.commit()
                    print(f"✅ All {question_inserting_count} questions inserted successfully")
                    return {"success": 200, "assesment_id": assesment_id, "questions_saved": question_inserting_count}
                
                else:
                    conn.rollback()
                    return {"error": f"Only {question_inserting_count}/{len(questions)} questions inserted. All changes rolled back."}

                

                


    except Exception as e:
        delete_res=vercel_blob.delete(file_url,{
            "token":token
        })
        print('deleting file',delete_res)
        print("error in entering data",e)
        return {"error":f"Error entering data on the assesment table ::{e}"}

async def process_with_n_eight_n(url,data,max_retries,timeout=120):
    for attempt in range(0,max_retries):
        try:
            print(f"processing with attempt {attempt}/{max_retries}..")
            async with httpx.AsyncClient(timeout=timeout) as client:         
                response=await client.post(url,json=data)
                print(f"Status: {response.status_code}")
                print(f"Raw response: {response.text}")
                print(f"response....",response)
                if not response.text:
                    print("⚠️ Empty response body")
                    continue
                try:
                    response_data=response.json()
                    if len(response_data)>0:
                        print("response_data",response_data)
                    
                except Exception as e:
                    print(f"❌ Failed to parse JSON: {e} | Raw: {response.text}")
                    continue

                if response.status_code==200 and response_data:
                    print(f"processing success with attempt {attempt}")
                    return {"success":200,"data":response_data}
                else:
                    print(f"unexpected response")

        except httpx.TimeoutException:
            print(f"attempt {attempt} timedout")
        except httpx.ConnectError as e:
            print(f"attempt {attempt} connection error ::{e}")

        if attempt < max_retries:
            wait =attempt*5
            print(f"retrying in {wait}s ..")
            await asyncio.sleep(wait)
    return {"error": "error", "error": f"Failed after {max_retries} attempts"}

def process_queries(query_data, question_number, questions):
    for i, query in enumerate(query_data):
        print(f'inserting query {i} out of {len(query_data)}')
        question_number += 1                          # ✅ += not =+
        query["question_number"] = question_number    # ✅ set on the dict
        questions.append(query)
    
    return question_number, questions
async def get_questions(chunks,file_url):
    try:
        all_responses=[]
        questions=[]
        question_number=0
        for i,chunk in enumerate(chunks):
            print(f"processing chunk {i+1} out of {len(chunks)}")
            print(chunk['text'])
            url='https://untawed-overheady-tony.ngrok-free.dev/webhook/7a5caadc-920a-45a8-adcd-456409d91821'
            # url='https://untawed-overheady-tony.ngrok-free.dev/webhook-test/7a5caadc-920a-45a8-adcd-456409d91821'
            data={
                "chunk":chunk['text']
                            #   "assesment_id":assesment_id,
                            #   "date":datetime.now()
            }
            max_attempts=4
            process_res=await process_with_n_eight_n(url,data,max_attempts)
        #   process_res=requests.post(url,data)
            print(process_res['data'])
            query_data=process_res['data']

            question_number,questions=process_queries(query_data,question_number,questions)
            

        
        #   if process_res.get("success")==200:
        #       print("process_res", process_res.get("data"))

            all_responses.append({f"chunk {i+1}":process_res})
            # if len(all_responses) ==len(chunks):
            #     print("all chunks processed successfully ")
            #     return {"success":"all chunks processed successfully"}
            # else:
            #     print("errors occurred")
            #     return {
            #         "errors":errors
            #     }
        return questions,question_number          
    except Exception as e:
        vercel_blob.delete(file_url,{
            "token":token
        })
        print("error in processing chunks",e)
        return{"error":f"Error in processing chunks::{e}"}
   


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
# question_pattern= r'(\d+\.\s|Q\d+\.\s|Question\s\d+)'
question_pattern = r'(?=\n(?:\d+\.\s|Q\d+\.\s|Question\s\d+[\.\s]|[a-zA-Z][\.\)]\s))'

def get_overlap(next_chunk_text):
    matches=list(re.finditer(question_pattern,next_chunk_text))

    if len(matches)==0:
        # get the first 3 sentences instead 
        sentences = re.split(r'(?<=[.!?])\s+',next_chunk_text)
        return "".join(sentences[:3])
    
    elif len(matches)==1:
        return next_chunk_text[matches[0].start():]
    
    else:
        return next_chunk_text[matches[0].start():matches[1].start()].strip()

def merge_short_pages(pages, min_words=500):
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

