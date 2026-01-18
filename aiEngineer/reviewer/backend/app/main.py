from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Reviewer API")

origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite default
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
