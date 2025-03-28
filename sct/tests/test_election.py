import pytest
from sct.election import Election, ScoreVoting
from sct.candidates import Candidates
from sct.agent import Agent

# Test Election initialization
def test_election_initialization_candidates_object():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    e = Election(candidates=c)
    assert e.candidates.names == ["curie", "einstein", "feynman"]

def test_election_initialization_candidates_list():
    c = ["Curie", "Feynman", "Einstein"]
    e = Election(candidates=c)
    assert e.candidates.names == ["curie", "einstein", "feynman"]

def test_election_initialization_candidates_int():
    c = 30
    e = Election(candidates=c)
    assert e.candidates.names == ["a", "aa", "ab", "ac", "ad", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def test_election_initialization_candidates_error():
    c = 1.5
    with pytest.raises(ValueError):
        e = Election(candidates=c)

def test_election_initialization_list_of_agents_object():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = [Agent(name="Alice", choices=["Curie", "Einstein"]), Agent(name="Bob", choices=["Feynman", "Curie"])]
    e = Election(candidates=c, agents=a)
    assert e.agents[0].name == "Alice"
    assert e.agents[1].name == "Bob"

def test_election_initialization_list_of_agents_object_invalid_agents():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = [Agent(name="Alice", choices=["Curie", "Einstein"]), Agent(name="Bob", choices=["Feynman", "Planck"])]
    e = Election(candidates=c, agents=a)
    assert e.agents[0].name == "Alice"
    assert e.invalid_agents[0].name == "Bob"

def test_election_initialization_agents_int():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = 5
    e = Election(candidates=c, agents=a)
    assert len(e.agents) <= 5
    assert sum([a.num_votes for a in e.agents]) == 5

def test_election_initialization_agents_error():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = 1.5
    with pytest.raises(ValueError):
        e = Election(candidates=c, agents=a)

# Test Election methods
def test_election_generate_candidates():
    e = Election()
    candidates = e.generate_candidates(5)
    candidates2 = e.generate_candidates(30)
    assert len(candidates.names) == 5
    assert candidates.names == ['a', 'b', 'c', 'd', 'e']
    assert len(candidates2.names) == 30
    assert candidates2.names == ['a', 'aa', 'ab', 'ac', 'ad', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def test_election_generate_agents():
    e = Election()
    agents = e.generate_agents(5)
    assert len(agents) <= 5
    assert sum([a.num_votes for a in agents]) == 5
    for agent in agents:
        assert agent.name is not None
        assert len(agent.choices) == len(set(agent.choices))

# Test ScoreVoting initialization
def scorevoting_initialization():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = [Agent(name="Alice", choices=["Curie", "Einstein"]), Agent(name="Bob", choices=["Feynman", "Curie"])]
    sv = ScoreVoting(candidates=c, agents=a, score_vector=[1,0,0])
    assert sv.score_vector == [1,0,0]

def test_scorevoting_initialization_error():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = [Agent(name="Alice", choices=["Curie", "Einstein"]), Agent(name="Bob", choices=["Feynman", "Curie"])]
    with pytest.raises(ValueError):
        sv = ScoreVoting(candidates=c, agents=a, score_vector=[1,0])

# Test ScoreVoting methods
def test_scorevoting_calculate_score():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = [Agent(name="Alice", choices=["Curie", "Einstein"]), Agent(name="Bob", choices=["Feynman", "Curie"])]
    sv = ScoreVoting(candidates=c, agents=a, score_vector=[1,0,0])
    scores = sv.calculate_results()
    print(scores)
    assert scores == {"curie": 1, "feynman": 1, "einstein": 0}

def test_scorevoting_calculate_winners():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = [Agent(name="Alice", choices=["Curie", "Einstein"]), Agent(name="Bob", choices=["Feynman", "Curie"])]
    sv = ScoreVoting(candidates=c, agents=a, score_vector=[1,0,0])
    winners = sv.winners()
    assert winners == {"curie": 1, "feynman": 1}

def test_scorevoting_calculate_winners():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    a = [Agent(name="Alice", choices=["Curie", "Einstein"]), Agent(name="Bob", choices=["Curie", "Feynman"])]
    sv = ScoreVoting(candidates=c, agents=a, score_vector=[1,0,0])
    winners = sv.winners()
    assert winners == {"curie": 2}