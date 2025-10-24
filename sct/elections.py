
import numpy as np
import itertools
import copy

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
    def __init__(self, preferences: list[Candidate], num_votes = 1):
        self.preferences = preferences
        self.num_votes = num_votes
        # checks to verify preference validity
        # - each candidate appears only once
        # - length of list == length of available candidates

    def top_choice(self):
        return self.preferences[0]

    # do not edit during an election to backtrack individual preferences

class Population:
    # default constructor = list of agents
    def __init__(self, candidates_list: list[Candidate], agents_list: list[Agent]):
        self.candidates_list = sorted(candidates_list)
        self.candidates_idx = {candidate: idx for idx, candidate in enumerate(sorted(candidates_list))}
        self.agents_list = agents_list
        self.preference_list = [[self.candidates_idx[pref] for pref in agent.preferences if pref in candidates_list] for agent in self.agents_list]
        self.pref_matrix = self.build_pref_matrix()
        self.overall_matrix = self.build_overall_matrix()

    # def build_pref_matrix(self):
    #     n = len(self.candidates_list)
    #     matrix_size = (n,) * n
    #     prefs = np.zeros(matrix_size)
    #     for pref in self.preference_list:
    #         prefs[tuple(pref)] += 1
    #     return prefs
    
    # def build_overall_matrix(self):
    #     return np.stack(
    #         [self.pref_matrix.sum(axis=axes) for axes in itertools.combinations(
    #             range(self.pref_matrix.ndim), self.pref_matrix.ndim - 1)][::-1]
    #     )
    def copy(self):
        return copy.deepcopy(self)

    def build_pref_matrix(self):
        # building the matrix of all possible permutations
        permus = np.stack(list(itertools.permutations(range(len(self.candidates_list)))))

        # adding an axis to keep track of the number of people voting for that alternative
        permus = np.concatenate([permus[:, :, None], np.zeros_like(permus[:, :, None])], axis=2)

        # attribute the votes 
        for i, pref in enumerate(self.preference_list):
            idx = np.where((permus[:, :, 0] == pref).all(axis=1))[0]
            permus[idx, :, 1] += self.agents_list[i].num_votes # attributing the number of votes of the agent corresponding to that preference

        return permus
    
    def build_overall_matrix(self):
        n = len(self.candidates_list)
        overall_mat = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                overall_mat[i, j] = self.pref_matrix[self.pref_matrix[:, j, 0] == i][:, 0, 1].sum()
        return overall_mat

    # second constructor = from a population matrix
    @classmethod
    def from_matrix():
        return 0

    # third constructor = from list of agents and associated volume vector (default vector of ones)
    # @classmethod
    # def from_preferences(archetypes: list[Agent], volume_vector: list[int]):
    #     # check that length(volume_vector) == length(archetypes) 


class VotingSystem:
    def __init__(self, population: Population):
        self.population = population
        self.voting_vector = []

    def run_election(self) -> dict:
        results_vector = self.population.overall_matrix @ self.voting_vector
        results_dict = {}
        for candidate, score in zip(self.population.candidates_list,
                                    results_vector):
            results_dict[candidate] = score
        return dict(sorted(results_dict.items(), key=lambda item: item[1], reverse=True))

class PluralityVoting(VotingSystem):
    def __init__(self, population: Population):
        super().__init__(population)

        # Creating the plurality voting vector
        self.voting_vector = np.zeros(len(self.population.candidates_list))
        self.voting_vector[0] = 1

    # def run_election(self, population: Population) -> Candidate:
    #     return 0

class BordaVoting(VotingSystem):
    def __init__(self, population: Population):
        super().__init__(population)
        
        # Creating the plurality voting vector
        self.voting_vector = np.array(list(reversed(range(len(self.population.candidates_list)))))

class SMCVoting: #Sequential Majoriy Comparison
    def __init__(self, population: Population):
        self.population = population
    
    def run_election(self):
        idxes = [(self.population.pref_matrix[:,:,0] == i).argmax(axis=1) for i in range(len(self.population.candidates_list))]
        max_idx = 0
        for idx in range(1,len(idxes)):
            mask = idxes[max_idx] < idxes[idx]
            if self.population.pref_matrix[:,:,1][mask][:,0].sum() > self.population.pref_matrix[:,:,1][~mask][:,0].sum():
                continue
            else:
                max_idx = idx
        return {self.population.candidates_list[max_idx]:max_idx}

# # implement other voting systems accordingly

class InstantRunoff:
    def __init__(self, population: Population, num_elim_per_round = 1):
        self.population = population
        self.num_elim_per_round = min(num_elim_per_round, len(population.candidates_list) - 1)
    
    def run_election(self):
        pop_temp = self.population.copy()
        candidates = pop_temp.candidates_list
        agents = pop_temp.agents_list

        for _ in range(len(pop_temp.candidates_list) - self.num_elim_per_round):
            round_plurality = PluralityVoting(pop_temp)
            result = round_plurality.run_election()
            for _ in range(min(self.num_elim_per_round, len(pop_temp.candidates_list) - 1)):
                loser = min(result, key=result.get)
                candidates.remove(loser)
                del result[loser]
            pop_temp = Population(candidates, agents)
        
        del pop_temp
        
        return result

class Plurality_with_Runoff(InstantRunoff):
    def __init__(self, population: Population):
        super().__init__(population, num_elim_per_round = len(population.candidates_list) - 2)


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