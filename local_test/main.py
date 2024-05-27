# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
import hashlib  # Import hashlib for password hashing

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

# Endpoint to register a new user
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
            # Check if the hashed password matches the provided password
            hashed_password = hashlib.sha512(user.password.encode()).hexdigest()
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