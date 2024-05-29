from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
import hashlib
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# CORS middleware to allow requests from Nginx
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this if you need to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT secret key (change this to a secure value)
SECRET_KEY = "your-secret-key"

# Token expiration time (change this according to your needs)
TOKEN_EXPIRATION = timedelta(minutes=30)

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

# Generate JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + TOKEN_EXPIRATION
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

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
        hashed_password = hashlib.sha512(user.password.encode()).hexdigest()
        cursor = connection.cursor()
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
            # Check if the hashed password matches the provided password
            hashed_password = hashlib.sha512(user.password.encode()).hexdigest()
            if matched_user['password'] == hashed_password:
                # Generate token
                access_token = create_access_token(data={"mail": matched_user["mail"]})
                cursor.close()
                connection.close()
                return {"message": "Login successful!", "user": access_token}
            else:
                raise HTTPException(status_code=401, detail="Invalid email or password")
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Error as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Error during login")

# Endpoint to handle account deletion
@app.post("/yeetus-deletus")
def delete_account(email: str = Header(..., alias="Authorization")):
    try:
        # Decode JWT token to get user email
        token = email.split(" ")[1]  # Assuming the token is sent as "Bearer <token>"
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_email = decoded_token.get("mail")

        # Check if the email exists
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Delete the user's account from the database
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Failed to connect to the database")

        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE mail = %s", (user_email,))
        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Account deleted successfully"}

    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    except Error as e:
        print(f"Error during account deletion: {e}")
        raise HTTPException(status_code=500, detail="Error during account deletion")
    
# Endpoint to handle password change
@app.post("/change-password")
def change_password(password_change: PasswordChange, email: str = Header(..., alias="Authorization")):
    try:
        # Decode JWT token to get user email
        token = email.split(" ")[1]  # Assuming the token is sent as "Bearer <token>"
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_email = decoded_token.get("mail")

        # Check if the email exists
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Verify if the old password matches
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Failed to connect to the database")

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE mail = %s", (user_email,))
        matched_user = cursor.fetchone()

        if not matched_user:
            raise HTTPException(status_code=401, detail="User not found")

        hashed_old_password = hashlib.sha512(password_change.old_password.encode()).hexdigest()
        if matched_user['password'] != hashed_old_password:
            raise HTTPException(status_code=401, detail="Incorrect old password")

        # Update the user's password in the database
        hashed_new_password = hashlib.sha512(password_change.new_password.encode()).hexdigest()
        cursor.execute("UPDATE users SET password = %s WHERE mail = %s", (hashed_new_password, user_email))
        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Password changed successfully"}

    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    except Error as e:
        print(f"Error during password change: {e}")
        raise HTTPException(status_code=500, detail="Error during password change")