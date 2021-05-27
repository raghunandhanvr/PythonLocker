
import sqlite3
import base64
import imageio
import cv2

PASSWORD = "Raghu"                                                 

connect = input("Password : \n")

while connect != PASSWORD:
    connect = input("Password : \n")
    
    if connect == "q":
        break

if connect == PASSWORD:
    conn = sqlite3.connect('safe.db')
    
    try:                                                                     
        conn.execute('''CREATE TABLE SAFE
            (FULL_NAME TEXT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''')
        print("Locker DB created! \n What would you like to add to DB?")
    except:
        print("You have a Locker, what would you like to do today?")
    
    
    while True:
        print("\n"+ "*"*15)                                                    
        print("Commands:")
        print("q = quit program")
        print("o = open file")
        print("s = store file")
        print("*"*15)
        input_ = input(":")

        if input_ == "q":
            break
        if input_ == "o":
            file_type = input("What is the filetype of the file you want to open? The Formats are txt, png, dart, java, jpg, jpeg\n")
            file_name = input("What is the name of the file you want to open?\n")
            FILE_ = file_name + "." + file_type

            cursor = conn.execute("SELECT * from SAFE WHERE FULL_NAME=" + '"' + FILE_ + '"')

            file_string = ""
            for row in cursor:
                file_string = row[3]
            with open(FILE_, 'wb') as f_output:
                print(file_string)
                f_output.write(base64.b64decode(file_string))




        if input_ == "s":
            PATH = raw_input("Type in the full path to the file you want to store.\nExample: /home/raghu/Desktop/file.py\n")

            FILE_TYPES = {                                                         
                "txt": "TEXT",
                "jpg": "IMAGE",
                "png": "IMAGE",
                "jpeg": "IMAGE"
            }

            file_name = PATH.split("/")
            file_name = file_name[len(file_name) - 1]
            file_string = ""

            NAME = file_name.split(".")[0]
            EXTENSION = file_name.split(".")[1]

            try:
                EXTENSION = FILE_TYPES[EXTENSION]
            except:
                Exception()


            if EXTENSION == "IMAGE":
                IMAGE = cv2.imread(PATH)
                file_string = base64.b64encode(cv2.imencode('.jpg', IMAGE)[1]).decode()

            elif EXTENSION == "TEXT":
                file_string = open(PATH, "r").read()
                file_string = base64.b64encode(file_string)

            EXTENSION = file_name.split(".")[1]
            
            command = 'INSERT INTO SAFE (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' %('"' + file_name +'"', '"' + NAME +'"', '"' + EXTENSION +'"', '"' + file_string +'"')
            
            conn.execute(command)
            conn.commit()
