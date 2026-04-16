# function to get the units 
from database.db import get_db
from schemas.course_units_schema import Get_Units

# get the units linked to a certain course
def get_units(course_id:str):
    # course_id=course.course_id
    params=(course_id,)
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # cur.execute("SELECT * FROM units WHERE course_id=%s",(course_id,))
                cur.execute("SELECT * FROM units")
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
        return{"error":f"Exception error in getting the units for course {course_id} :: {e} "}
        

def get_nodes(unit_id:str):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT _id,title,description,status,index FROM nodes WHERE unit_id=%s",(unit_id,))
                nodes=cur.fetchall()
                if nodes:
                    columns=[desc[0] for desc in cur.description]
                    data=[dict(zip(columns,row)) for row in nodes]
                    return data
                else:
                    return []
    except Exception as e:
        return {"error":f"exception error in getting the milestone nodes for {unit_id}::error {e}"}

            
