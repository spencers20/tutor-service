# connection to db logic
from psycopg_pool import ConnectionPool
from contextlib import contextmanager
import asyncio

try:
    pool=ConnectionPool(
        conninfo="postgresql://admin:admin001@localhost:5432/lexi"
      )
except Exception as e:
    print('error in connection to db,',e)

@contextmanager
def get_db():
    conn=pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)
    
    # with  pool.connection() as conn:
    #     with conn.cursor() as cur:

            # cur.execute("SELECT * FROM profileinfo")
            # data=cur.fetchall()
            # print('data..',data)

def release_db(conn):
    pool.putconn(conn)

async def main():
    with get_db() as con:
        with con.cursor() as cur:
            cur.execute('SELECT * FROM profileinfo')
            results=cur.fetchall()
        
            print('query results...',results)
    
 

    

if __name__=="__main__":
    asyncio.run(main())