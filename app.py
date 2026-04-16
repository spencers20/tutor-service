from fastapi import FastAPI
import uvicorn
from routers.notes_router import router as notes_router
from routers.user_router import router as user_router
from  routers.course_units_router import router as course_units_router
from routers.curriculum_units import router as curriculum_units_router
from routers.assesments_router import router as assesment_router
from fastapi.middleware.cors import CORSMiddleware
from routers.resources_router import router as resource_router
import os

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://172.28.188.197:3000","http://0.0.0.0:3000"],
    # allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
    
)

app.include_router(resource_router)
app.include_router(user_router)
app.include_router(notes_router)
app.include_router(curriculum_units_router)
app.include_router(course_units_router)
app.include_router(assesment_router)


if __name__=="__main__":
    port=int(os.environ.get("PORT",8000))
    uvicorn.run("app:app",host="0.0.0.0",port=port)