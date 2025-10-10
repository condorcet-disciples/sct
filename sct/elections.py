
import numpy as np
import itertools

class Candidate:
    def __init__(self, name: str):
        self.name = name
        # generate unique alphanumeric ID for large simulations
    
    def __lt__(self, other):
        # sort by score (ascending)
        return self.name < other.name


# in an election, generate multiple candidates
# - add, remove

class Agent:
    def __init__(self, preferences: list[Candidate]):
        self.preferences = preferences
        # checks to verify preference validity
        # - each candidate appears only once
        # - length of list == length of available candidates

    def top_choice(self):
        return self.preferences[0]

    # do not edit during an election to backtrack individual preferences

class Population:
    # default constructor = list of agents
    def __init__(self, candidates_list: list[Candidate], agents_list: list[Agent]):
        self.candidates_list = candidates_list
        self.candidates_idx = {candidate: idx for idx, candidate in enumerate(sorted(candidates_list))}
        self.agents_list = agents_list
        self.preference_list = [[self.candidates_idx[pref] for pref in agent.preferences] for agent in self.agents_list]
        self.pref_matrix = self.build_pref_matrix()
        self.overall_matrix = self.build_overall_matrix()

    def build_pref_matrix(self):
        n = len(self.candidates_list)
        matrix_size = (n,) * n
        prefs = np.zeros(matrix_size)
        for pref in self.preference_list:
            prefs[tuple(pref)] += 1
        return prefs
    
    def build_overall_matrix(self):
        return np.stack(
            [self.pref_matrix.sum(axis=axes) for axes in itertools.combinations(
                range(self.pref_matrix.ndim), self.pref_matrix.ndim - 1)][::-1]
        )

    # second constructor = from a population matrix
    @classmethod
    def from_matrix():
        return 0

    # third constructor = from list of agents and associated volume vector (default vector of ones)
    # @classmethod
    # def from_preferences(archetypes: list[Agent], volume_vector: list[int]):
    #     # check that length(volume_vector) == length(archetypes) 


# class VotingSystem:
#     def run_election(self, population: Population) -> Candidate:
#         return 0

# class PluralityVoting(VotingSystem):
#     def run_election(self, population: Population) -> Candidate:
#         return 0

# class BordaCount(VotingSystem):
#     def run_election(self, population: Population) -> Candidate:
#         return 0

# # implement other voting systems accordingly


# class Election:
#     def __init__(self, candidates: list[Candidate], population: Population, system: VotingSystem):
#         self.candidates = candidates
#         self.population = population
#         self.system = system
    
#     # at a later stage, need to deal with VotingSystems that output set of candidates and probability distributions

#     def run(self):
#         winner = self.system.run_election(self.population)
#         print(f"Winner: {winner.name}")
#         return winner