import pytest
from sct.agent import Agent

def test_agent_initialization_with_choices():
    agent = Agent(name="Einstein", num_votes=2, choices=["Curie", "Feynman", "Turing"])
    
    assert agent.name == "Einstein"
    assert agent.num_votes == 2
    assert agent.choices == ["curie", "feynman", "turing"]

def test_agent_initialization_without_name_or_choices():
    agent = Agent()
    
    assert agent.name is None
    assert agent.num_votes == 1
    assert agent.choices == []

def test_set_preferences_updates_choices():
    agent = Agent(name="Newton", choices=["Galileo"])
    
    new_choices = ["Tesla", "Bohr"]
    updated = agent.set_preferences(new_choices)
    
    assert agent.choices == ["tesla", "bohr"]
    assert updated == ["tesla", "bohr"]

def test_set_preferences_case_insensitive():
    agent = Agent(name="Ada", choices=["EINSTEIN", "BoHR"])
    
    assert agent.choices == ["einstein", "bohr"]