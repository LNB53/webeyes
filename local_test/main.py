from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware to allow requests from Nginx
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://nginx"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# Define your API endpoints and OAuth authentication here
