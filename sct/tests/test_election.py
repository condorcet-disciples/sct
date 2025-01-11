import sct.election as election

def test_generate_candidates():
    # Create an election object
    e = election.Election()
    # Generate 5 candidates
    e.generate_candidates(5)
    # Check that the number of candidates is 5
    assert len(e.candidates.names) == 5