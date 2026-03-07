from fastapi import FastAPI, HTTPException, Path, UploadFile, File, Form
from pydantic import BaseModel, Field, field_validator
from typing import Annotated
import mysql.connector
import os      

from passlib.context import CryptContext


app = FastAPI()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=os.getenv("MYSQLPORT")
    )

class Register(BaseModel):
    email : str
    year : Annotated[int, Field(..., description='This is for the Year of Birth', example=2006)]
    password : Annotated[str, Field(..., description='The password must be strong', example='atul@2006', min_length=8, max_length=64)]
    conf_password : Annotated[str, Field(..., description='The password must match to above password')]


    @field_validator("conf_password")
    def pass_match(cls, value, info):
        password = info.data.get('password')

        if password and value != password:
            raise ValueError("Password not match")
        
        return value

class Login(BaseModel):
    email : str
    password : str

class Reset(BaseModel):
    email : str
    year : int
    new_password : str

class Remove(BaseModel):
    email : str

@app.get("/")
def home():
    return {"Detail" : "Hello User!"}


pwd_context = CryptContext(schemes=["bcrypt"])

@app.post('/register')
def user_register(register: Register):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_register WHERE email = %s", (register.email,))

        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already exixts")
        
        hashed_pass = pwd_context.hash(register.password)
        
        query = """
            INSERT INTO user_register(email, year, password)
            VALUES(%s, %s, %s)
        """
        values = (
            register.email,
            register.year,
            hashed_pass
        )

        cursor.execute(query, values)
        conn.commit()

        return {"message" : "Registration Successfull!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/login')
def login(user : Login):
    try: 
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM user_register WHERE email=%s', (user.email,))
        rows = cursor.fetchone()

        if not rows:
            raise HTTPException(status_code=400, detail="Email not found")

        if pwd_context.verify(user.password, rows["password"]):
            return {"message" : "Login Successfull!"}
        
        # row = rows[0]
        # if row["email"] == user.email and row["password"] == user.password:
        #     return {"Status" : "Login successfull...!"}
            
        return {"message" : "Invalid Credential..! Check Your Password"}
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

@app.put('/reset_password/')
def reset_password(reset : Reset):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT * FROM user_register
            WHERE email = %s and year = %s;
        """

        value = (reset.email, reset.year)

        cursor.execute(query, value)
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail='Varification failed')
        
        query2 = """
            UPDATE user_register
            SET password = %s
            WHERE email = %s;
        """

        change_password = pwd_context.hash(reset.new_password)

        value2 = (change_password, reset.email)

        cursor.execute(query2, value2)
        conn.commit()

        return {'message' : 'Passwod is changed'}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete('/remove_acc')
def remove_acc(rem : Remove):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM user_register WHERE email=%s', (rem.email,))
        conn.commit()

        return {'message' : 'Account deleted'}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# class Resume(BaseModel):
#     email : str

UPLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.post('/upload')
async def upload_file(email: str = Form(...), file : UploadFile = File(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM user_register WHERE email = %s
            """, (email,)
            )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)

        cursor.execute(
            """
            UPDATE user_register
            SET file_path = %s
            WHERE email = %s
            """,
            (file_path, email)
            )

        conn.commit()

        return {"message": "File uploaded successfully", "path": file_path}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get('/check')
def check_conn():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT 1')
        return {"message" : "Database connected"}
    
    except:
        return {"message" : "Database did not connect"}
    

    


