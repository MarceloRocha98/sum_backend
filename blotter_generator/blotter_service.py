import os
from unittest import skip
import requests

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os.path

import sqlalchemy
import pandas as pd

   

watch_file = "./blotters.txt"
user_id = 1 # user id do cliente em que as informações serão adicionadas. Para simplificação, passado de forma Hard Coded
cursor_filename = "cursor.txt" # Arquivo em que a variável cursor será armazenada


def create_mysql_engine():
     dbEngine=sqlalchemy.create_engine("sqlite:///D:/sum/backend/db.sqlite3") 
     return dbEngine 

def appendBlotter(array, table_name="blotter"):
    df = pd.DataFrame(array)
    df = df[['ticker', 'price', 'volume','user_id']]
    sql_engine = create_mysql_engine()
    dbConnection = sql_engine.connect()
    df.to_sql(table_name, dbConnection, if_exists='append', index=False, chunksize=1000)
    dbConnection.close()
    return 'OK'


class BlotterHandler():
    def __init__(self, watch_file, cursor_filename):
        self.path = watch_file
        self.data = []
        self.cursor = 1
        self.cursor_filename = cursor_filename

    def get_cursor(self, cursor_filename, cursor=1):
        if(not os.path.exists(cursor_filename)):
            open(cursor_filename, "a").write(str(cursor))
            return 1
        else:
            with open(cursor_filename) as f:
                cursor = f.read().splitlines()[0]
                # print(cursor)
        self.cursor = int(cursor)

    def set_cursor(self, cursor_filename, value):
        raw = open(cursor_filename, "r+")
        raw.seek(0)                        
        raw.truncate()
        raw.write(str(value))

    def get_data(self):
        self.get_cursor(self.cursor_filename)
    

        with open(self.path) as f:
            lines = f.readlines()
            # print(lines[self.cursor:])
            lines = lines[self.cursor:]
            tmp = []
            for idx, line in enumerate(lines):
                data = line[:-1].split(",") # eliminando o caracter de quebra de linha e transformando em array
                # print(data)               
      
                if(len(data)):
                    tmp.append({
                        "ticker":data[0],
                        "volume":data[1],
                        "price":data[2],
                        "user_id": user_id,
                    })
            self.data = tmp
            f.close()
            # print(self.cursor+len(lines))
            self.set_cursor(cursor_filename, self.cursor+len(lines)) # verificar


    def post_data(self):
        data = self.data

        try:
            r = appendBlotter(data, table_name="blotter")
            print(r)
        except:
            print("error on update")


        
        


class EventHandler(FileSystemEventHandler):
    global cursor

    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')

        if(event.src_path == watch_file):
            blotter_handler = BlotterHandler(watch_file, cursor_filename)
            blotter_handler.get_data()
            blotter_handler.post_data()
        

if __name__ == "__main__":
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()