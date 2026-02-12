#!/usr/bin/env python3
"""
Run an election using the votes in the backend.
Outputs JSON with winners and disappointment indices.
"""

import sys
import os
import json
import argparse
from string import ascii_lowercase

# Add parent directory to path to import sct module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import sct


def dict_to_serializable(d):
    """Convert dict with Candidate keys to serializable format."""
    return {c.name: float(v) for c, v in d.items()}


def get_rank(scores_dict, winner_name):
    """Get the rank (1st, 2nd, 3rd, 4th) of a candidate in a scores dict."""
    # Sort by score descending
    sorted_candidates = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
    suffixes = ["1st", "2nd", "3rd", "4th", "5th", "6th"]
    for i, (name, _) in enumerate(sorted_candidates):
        if name == winner_name:
            return suffixes[i] if i < len(suffixes) else f"{i+1}th"
    return "N/A"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session-id', required=False, help='Session ID to process')
    args = parser.parse_args()

    # Read database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.json')
    with open(db_path, 'r') as f:
        data = json.load(f)

    # Get session ID
    if args.session_id:
        session_id = args.session_id
    else:
        # Fall back to latest session
        session_ids = list(data['sessions'].keys())
        if not session_ids:
            print(json.dumps({"error": "No sessions found"}))
            return
        session_id = session_ids[-1]

    # Check if session has votes
    votes = data.get('votes', {}).get(session_id, [])
    if not votes:
        print(json.dumps({"error": "No votes in session"}))
        return

    # Create candidates
    candidate_list = []
    for ii in range(4):
        globals()[ascii_lowercase[ii]] = sct.Candidate(f'candidate_{ii+1}')
        candidate_list.append(globals()[ascii_lowercase[ii]])

    a, b, c, d = candidate_list

    # Create agents from votes
    agent_list = []
    for vote in votes:
        agent_list.append(sct.Agent({
            a: vote.get('candidate_1', 2),
            b: vote.get('candidate_2', 2),
            c: vote.get('candidate_3', 2),
            d: vote.get('candidate_4', 2)
        }))

    # Run elections
    pop = sct.Population(candidate_list, agent_list)

    plurality = sct.PluralityVoting(pop)
    borda = sct.BordaVoting(pop)
    majority = sct.MajorityJudgment(pop)

    # Get scores for each system (serialized)
    plurality_scores = dict_to_serializable(plurality.run_election())
    borda_scores = dict_to_serializable(borda.run_election())
    majority_scores = dict_to_serializable(majority.run_election())

    # Get winners
    plurality_winner = plurality.get_winner()
    borda_winner = borda.get_winner()
    majority_winner = majority.get_winner()

    # Build results with cross-system rankings
    results = {
        "plurality": {
            "winner": plurality_winner,
            "scores": plurality_scores,
            "disappointment": dict_to_serializable(plurality.disappointment_index()),
            "winner_rank_in_borda": get_rank(borda_scores, plurality_winner),
            "winner_rank_in_majority": get_rank(majority_scores, plurality_winner)
        },
        "borda": {
            "winner": borda_winner,
            "scores": borda_scores,
            "disappointment": dict_to_serializable(borda.disappointment_index()),
            "winner_rank_in_plurality": get_rank(plurality_scores, borda_winner),
            "winner_rank_in_majority": get_rank(majority_scores, borda_winner)
        },
        "majority": {
            "winner": majority_winner,
            "scores": majority_scores,
            "disappointment": dict_to_serializable(majority.disappointment_index()),
            "winner_rank_in_plurality": get_rank(plurality_scores, majority_winner),
            "winner_rank_in_borda": get_rank(borda_scores, majority_winner)
        }
    }

    print(json.dumps(results))


if __name__ == "__main__":
    main()