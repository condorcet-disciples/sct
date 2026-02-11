#!/usr/bin/env python3
"""
Run an election using the votes in the backend.
"""

import sys
import os
import json
from string import ascii_lowercase

# Add parent directory to path to import sct module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import sct

def main():
    # read database
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'database.json'), 'r') as f:
        data = json.load(f)

        # get latest session ID
        # TODO: do this with the creation datetime instead of assuming the last is latest
        session_IDs = data['sessions'].keys()
        latest_session = list(session_IDs)[-1]
    
    # create candidates
    # TODO: create this from the agents data instead of hardcoding 4 candidates
    # candidate_list = [
    #     sct.Candidate(f'candidate_{str(ii)}') for ii in range(1,5)
    # ]
    candidate_list = []
    for ii in range(4):
        globals()[ascii_lowercase[ii]] = sct.Candidate(f'candidate_{str(ii+1)}')
        candidate_list.append(globals()[ascii_lowercase[ii]])

    # create agents
    agents = data['votes'][latest_session]
    agent_list = []
    for agent in agents:
        agent_list.append(sct.Agent({
            a: agent.get('candidate_1', 2),
            b: agent.get('candidate_2', 2),
            c: agent.get('candidate_3', 2),
            d: agent.get('candidate_4', 2)
            }))
        
    # run election
    pop = sct.Population(candidate_list, agent_list)

    plurality = sct.PluralityVoting(pop)
    borda = sct.BordaVoting(pop)
    majority = sct.MajorityJudgment(pop)
    
    print("Plurality winner:", plurality.get_winner())
    print("Borda winner:", borda.get_winner())
    print("Majority Judgment winner:", majority.get_winner())

if __name__ == "__main__":
    main()