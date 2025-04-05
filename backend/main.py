from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sct.election import Election, ScoreVoting, Plurality, Borda
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

# Pydantic model to accept raw input
class ElectionRequest(BaseModel):
    candidates: list[str]
    ballots: list[tuple[str, int, list[str]]]  # Each tuple contains voter name, number of votes, and ranked preferences
    method: str
    num_winners: int = 1  # Default to 1 winner if not specified

@app.post("/vote/")
def run_election(data: ElectionRequest):
    candidate_objs = Candidates(names=data.candidates)
    agents = []
    for ballot in data.ballots:
        voter_name, num_votes, preferences = ballot
        agent = Agent(name=voter_name, num_votes=num_votes, choices=preferences)
        agents.append(agent)

    if data.method == "plurality":
        election = Plurality(candidates=candidate_objs, agents=agents, num_winners=data.num_winners)
    elif data.method == "borda":
        election = Borda(candidates=candidate_objs, agents=agents, num_winners=data.num_winners)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported voting method: {data.method}")
    
    full_results = election.calculate_results()
    winners = election.winners()
    # Convert winners to a list of names
    winners = list(winners.keys())

    return {
        "full_results": full_results,
        "winners": winners,
    }