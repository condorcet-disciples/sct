import pytest
from sct.candidates import Candidates

def test_initialization_sorts_and_lowercases():
    c = Candidates(names=["Curie", "Feynman", "Einstein"])
    print(c.names)
    assert c.names == ["curie", "einstein", "feynman"]

def test_initialization_raises_type_error_on_nonstring():
    with pytest.raises(TypeError):
        Candidates(names=["Bohr", 42, "Planck"])

def test_add_candidate_successfully():
    c = Candidates(names=["Tesla", "Bohr"])
    c.add_candidate("Newton")
    assert c.names == ["bohr", "newton", "tesla"]

def test_add_duplicate_candidate_raises_value_error():
    c = Candidates(names=["Darwin", "Galileo"])
    with pytest.raises(ValueError):
        c.add_candidate("galileo")  # should be case-insensitive

def test_remove_candidate_successfully():
    c = Candidates(names=["Lovelace", "Turing", "Hopper"])
    c.remove_candidate("Turing")
    assert c.names == ["hopper", "lovelace"]

def test_remove_nonexistent_candidate_raises_value_error():
    c = Candidates(names=["Fermi", "Heisenberg"])
    with pytest.raises(ValueError):
        c.remove_candidate("Hawking")
