import pytest
from sct.election import Election, ScoreVoting
from sct.candidates import Candidates
from sct.agent import Agent

# Test Election initialization
def test_election_initialization_candidates_object():
    assert 1==1