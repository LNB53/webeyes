from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
import hashlib

app = FastAPI()

# CORS middleware to allow requests from Nginx
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this if you need to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Form format for API handling from webpage form
class User(BaseModel):
    mail: str
    password: str

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="10.0.0.243",
            user="administrator",
            password="administrator",
            database="login_database"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha512(password.encode()).hexdigest()

# Test endpoint
@app.get("/")
def read_root():
    return {"message": "API is running!"}

# Endpoint to register a new user
@app.post("/register")
def register_user(user: User):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        cursor = connection.cursor()
        # Hash the password before storing it in the database
        hashed_password = hash_password(user.password)
        cursor.execute("INSERT INTO users (mail, password) VALUES (%s, %s)", (user.mail, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "User registered successfully"}
    except Error as e:
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")
    
# Endpoint to handle login
@app.post("/login")
def login_user(user: User):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        cursor = connection.cursor(dictionary=True)
        # Fetch user by email from the database
        cursor.execute("SELECT * FROM users WHERE mail = %s", (user.mail,))
        matched_user = cursor.fetchone()

        if matched_user:
            # Hash the provided password and compare it to the stored hashed password
            hashed_password = hash_password(user.password)
            if matched_user['password'] == hashed_password:
                cursor.close()
                connection.close()
                return {"message": "Login successful!", "user": matched_user}
            else:
                raise HTTPException(status_code=401, detail="Invalid email or password")
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Error as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Error during login")
