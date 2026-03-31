# function to get the units 
from database.db import get_db
from schemas.course_units_schema import Get_Units

# get the units linked to a certain course
def get_units(course:Get_Units):
    course_id=course.course_id
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM units WHERE course_id=%s",(course_id,))
                # conn.commit()
                units=cur.fetchall()

                if units:
                    columns=[desc[0] for desc in cur.description]
                    data=[dict(zip(columns,row)) for row in units]
                    # return {"units":data , "statuscode":200}
                    return data
                else:
                    return []
    except Exception as e:
        return{"errror":f"Exception error in getting the units for course {course_id} :: {e} "}
        


            
