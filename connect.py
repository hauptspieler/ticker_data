#!/usr/bin/python
from dis import Instruction
import psycopg2
import psycopg2.extras
from config import config

#def connection ():
 #   conn = None
  #  try:
   #     params = config()
    #    conn = psycopg2.connect(**params)	
     #   return conn
    #except (Exception, psycopg2.DatabaseError) as error:
     #
     #    print(error)
#connect(Instruction, params)
def connect( instruction, instructionParams):
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)	
      
        cur = conn.cursor()
        
        cur.execute(instruction, instructionParams)

        cursorData = cur.statusmessage
        
        conn.commit()

        return cursorData
       
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if cur is not None:
            cur.close()
            print('Cursor closed')
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def connect_multi( instruction, arrayInstructionParams):
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)	
      
        cur = conn.cursor()

        args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s)", element).decode("utf-8") for element in arrayInstructionParams)
       
        cur.execute(instruction + args_str) 
        
        cursorData = cur.statusmessage
        
        conn.commit()

        return cursorData
       
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if cur is not None:
            cur.close()
            print('Cursor closed')
        if conn is not None:
            conn.close()
            print('Database connection closed.')