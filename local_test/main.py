# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# CORS middleware to allow requests from Nginx
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this if you need to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# form format for API handling from webpage form
class User(BaseModel):
    mail: str
    password: str

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql",
            user="administrator",
            password="administrator",
            database="login_database"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Test endpoint
@app.get("/")
def read_root():
    return {"message": "API is running!"}

# Endpoint to test database connection and retrieve users
@app.get("/users")
def get_users():
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users
    except Error as e:
        print(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching users from the database")

# Endpoint to register a new user
@app.post("/register")
def register_user(user):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        cursor = connection.cursor()
        hashed_password = sha256(user.password.encode('utf-8')).hexdigest()
        cursor.execute(
            "INSERT INTO users (mail, password) VALUES (%s, %s)",
            (user.email, user.confirm_password)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "User registered successfully"}
    except Error as e:
        print(f"Error inserting user: {e}")
        raise HTTPException(status_code=500, detail="Error registering user")
    

@app.post("/register")
def register_user(user: User):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (mail, password) VALUES (%s, %s)", (user.mail, user.password))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "User registered successfully"}
    except Error as e:
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Error registering user")