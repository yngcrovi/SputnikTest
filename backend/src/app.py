from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.route import file, alert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file)
app.include_router(alert)




