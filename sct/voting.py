import numpy as np
from sct.agent import Agent
from sct.candidates import Candidates

class Election():
    '''
    Contains voting methods
    '''

    def __init__(self):
        pass

    def plurality(self, candidates: Candidates, agents: list):
        '''
        Implementation of the plurality voting methods

        Inputs:
        candidates: Candidates object
        agents: List of Agent objects

        Returns:
        name of winner
        '''

        all_prefs = [agent.prefs for agent in agents]
        results = sum(all_prefs)
        winner_idx = np.argmax(results[0])
        winner = candidates.names[winner_idx]

        return winner