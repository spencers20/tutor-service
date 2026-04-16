
from database.db import get_db
from schemas.curriculum_units_schema import academiclevelcreate, coursecreate, curriculumcreate, subjectcreate, unitscreate


def create_curriculum(curriculum:curriculumcreate):
    try:
        country=curriculum.country
        print("creating curriculum...")
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO  curriculum (country) VALUES (%s) RETURNING curriculum_id',(country))
                conn.commit()

                if cur.rowcount>0:
                    print("inserted successfullyy...✔✔")
                    return {
                        "message","curriculum created successfully"
                    }
                else:
                    return {"error":"error in creating curriculum"}
                
    except Exception as e:
        print('error e❌❌0',e)
        return {"error":f"❌❌Exception in creating curriculum {e}"}


def create_academiclevel(academic_level:academiclevelcreate):
    try:
        level_name=academic_level.level_name
        curriculum_id=academic_level.curriculum_id

        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute ('INSERT INTO academiclevel (level_name,curriculum_id) VALUES (%s)',(level_name,curriculum_id))
                conn.commit()

                if cur.rowcount>0:
                    print('academic level  inserted successfully')
                    return {"message":"academic level created successfully"},200
                
                else:
                    return{"error":"inserting curriculum failed"}
    except Exception as e:
        print("error in creating academic level❌❌",e)


def create_course(course:coursecreate):
    try:
        course_name=course.course_name
        academic_level=course.academic_level
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO course(course_name,academiclevel_id) VALUES (%s,%s)",(course_name,academic_level))
                conn.commit()

                if cur.rowcount>0:
                    return{"success":"success in inserting course"}
                
                else:
                    return {"error", "errorr in inserting course"}
                    # throw new 
    except Exception as e:
        return{"errror":f"exception error in inserting course {e}"}

def create_units(units:unitscreate):
    try:
        unit_name=units.unit_name
        course_id=units.course_id
        what_to_learn=[]
        prerequisites=[]
        
        with get_db() as conn:
            with conn.cursor() as cur:
          
                cur.execute("INSERT INTO units (unit_name, course_id,what_to_learn,prerequisites) VALUES (%s,%s) ",(unit_name, course_id,what_to_learn,prerequisites))
                conn.commit()

                if cur.rowcount>0:
                    return {"success":"success in creating unit"},200
                    
                else:
                    return {"error":"error in creating units"},500
    except Exception as e:
         return{"errror":f"exception error in inserting units {e}"}
    

def create_subject(subject:subjectcreate):
    try:
        subject_name=subject.subject_name
        academic_id=subject.academiclevel_id
        
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO subject (subject_name, academiclevel_id) VALUES (%s,%s) ",(subject_name, academic_id))
                conn.commit()

                if cur.rowcount>0:
                    return {"success":"success in creating subject"}
                    
                else:
                    return {"error":"error in creating subject"}
    except Exception as e:
         return{"errror":f"exception error in inserting subject {e}"}
        