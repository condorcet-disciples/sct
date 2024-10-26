import numpy as np
from sct.candidates import Candidates

class Agent:
    def __init__(self, name=None, coef=1, prefs=None):
        """TODO: add docstrings
        
        """
        self.name = name
        self.coef = coef
        self.prefs = prefs # TODO: We don't need to init none in this case: unless we wan't this to be a way people set their preferences

    def set_preferences(self, candidates: Candidates, ranking: list):
        """
        Defines the preferences of an agent given a list of candidates.
        For now, we're not assigning these preferences to the candidates and an Agent can have only 1 set of preferences at a time.

        Returns
        __________
        np.array
        """

        pref = np.zeros((len(ranking),len(ranking)))
        
        for i,v in enumerate(ranking):
            pref[i,v] = 1
        
        self.prefs = pref

        return pref

