from fastapi import FastAPI
import uvicorn
from routers.notes_router import router as notes_router
from routers.user_router import router as user_router
from  routers.course_units_router import router as course_units_router
from routers.curriculum_units import router as curriculum_units_router
from routers.assesments_router import router as assesment_router
import os

app=FastAPI()

app.include_router(user_router)
app.include_router(notes_router)
app.include_router(curriculum_units_router)
app.include_router(course_units_router)
app.include_router(assesment_router)


if __name__=="__main__":
    port=int(os.environ.get("PORT",8000))
    uvicorn.run("app:app",host="0.0.0.0",port=port)