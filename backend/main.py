from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sct.election import Election
from sct.agent import Agent
from sct.candidates import Candidates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the voting backend!"}

@app.post("/vote/")
def vote(data: dict):
    # result = run_election(data)  # Replace with your actual logic
    # return {"result": result}
    pass