from sct.agent import Agent
from sct.candidates import Candidates

class Election:
    def __init__(self, candidates: Candidates, agents: list):
        self.candidates = candidates
        self.agents = agents


class Plurailty(Election):
    def __init__(self, candidates, agents, allow_ties=True):
        super().__init__(candidates, agents)
        self.allow_ties = allow_ties

    def calculate_results(self):
        pass # shoudl reutrn winner and votes earned imo

    def show_full_results(self):
        pass


class Borda(Election):
    def __init__(self, candidates, agents, weight_increment=1):
        super().__init__(candidates, agents)
        self.weight_increment = weight_increment

    def calculate_results(self):
        pass # shoudl reutrn winner and votes earned imo

    def show_full_results(self):
        pass
