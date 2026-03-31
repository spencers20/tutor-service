# this is the user services /logic
import logging
from database.db import get_db
from schemas.user_schema import userCreate

def create_user(user:userCreate):
    name=user.name
    email=user.email
    phone_number=user.phone_number
    curriculum=user.curriculum
    level=user.level

    try:
        print("inserting into db...")
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO profileinfo (name,user_email,phone_number,curriculum,level) VALUES (%s,%s,%s,%s,%s)",(name,email,phone_number,curriculum,level))
                conn.commit()

                if cur.rowcount>0:
                    print("inserted...")
                    return{
                        "message":"created user successfully",
                    },200
                else:
                    return {"error":"error in creating user"},500
    except Exception as e:
        print()
        return {"error":f"❌❌Exception in creating user {e}"}
    