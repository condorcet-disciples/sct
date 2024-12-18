import numpy as np
import itertools
import string
import random
from collections import Counter
from sct.agent import Agent
from sct.candidates import Candidates

class Election:
    """Base class for conducting an election among candidates with a list of agents (voters).

    The `Election` class provides a framework for different voting systems, using a list of 
    agents and a set of candidates. Specific voting methods inherit from this class to implement 
    their unique calculation and display methods.

    Parameters
    ----------
    candidates : Candidates
        An instance of the `Candidates` class containing the list of candidates.
    agents : list of Agent
        A list of `Agent` instances representing the voters in the election.

    Attributes
    ----------
    candidates : Candidates
        The collection of candidates participating in the election.
    agents : list of Agent
        The list of agents (voters) participating in the election.
    """
    def __init__(self, candidates: Candidates = [], agents: list = []):
        self.candidates = candidates
        self.agents = agents

    def generate_candidates(self, n):
        '''
        Function to generate a candidates object with an arbitrary number of candidates
        '''

        # Create a list to store the results
        result = []
        
        # Single characters (first 26 letters)
        alphabet = string.ascii_lowercase  # 'a' to 'z'
        
        # Use a counter for the length of the string
        length = 1
        
        while len(result) < n:
            # Generate combinations for the current length
            for combination in itertools.product(alphabet, repeat=length):
                result.append(''.join(combination))
                # Stop when we reach the desired length
                if len(result) == n:
                    break
            length += 1

        self.candidates = Candidates(result)
        return Candidates(result)
    
    def generate_agents(self, n):
        '''
        Function to generate an arbitrary number of agents with random preferences
        '''

        # Creating a list of all permutations of candidates
        perms = list(itertools.permutations(self.candidates.names))

        # Probability of each permutation (uniform distribution)       
        probabilities = [1 / len(perms)] * len(perms)

        # Randomly sample n permutations based on the probabilities
        random_sampling = random.choices(perms, probabilities, k=n)

        # Creating an object containing the choices
        agents_choices = Counter(random_sampling)

        agents = []
        i = 0
        for choix in agents_choices.items():
            agents.append(Agent(name=f'Agent_{i}', choices=choix[0], num_votes=choix[1]))
            i += 1
        
        self.agents = agents
        return agents

class ScoreVoting(Election):
    def __init__(self, candidates, agents, score_vector, allow_ties=True, num_winners=1):
        super().__init__(candidates, agents)
        self.score_vector = score_vector
        self.allow_ties = allow_ties
        self.num_winners = num_winners

    def calculate_results(self):
        results = {c: 0 for c in (self.candidates.names)}

        # Run the election
        for agent in self.agents:
            i = 0
            for choice in agent.choices:
                results[choice] += self.score_vector[i] * agent.num_votes
                i += 1

        # Sorting the results
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

        return results

    def winners(self):
        """Returns only the winners of the plurality method.

        Returns
        -------
        dict
            A sorted dictionary containing the winners and their respective vote count.
        """

        results = self.calculate_results()

        # Save the results
        max_value = max(results.values())
        winners = {key:value for key, value in results.items() if value == max_value}

        return winners

class Plurality(ScoreVoting):
    """Represents a plurality (or first-past-the-post) voting system where the candidate with the most votes wins.

    Each agent's top candidate preference is counted as a single vote. The candidate with the 
    highest vote count is declared the winner.
    
    Parameters
    ----------
    candidates : Candidates
        An instance of the `Candidates` class containing the list of candidates.
    agents : list of Agent
        A list of `Agent` instances representing the voters in the election.
    allow_ties : bool, optional
        A flag indicating whether ties are permitted, by default True.

    Attributes
    ----------
    allow_ties : bool
        Indicates whether ties are allowed in the voting results.

    Methods
    -------
    calculate_results()
        Calculates and returns the winning candidate(s) and their vote count.
    show_full_results()
        Displays a summary of the full voting results, including each candidate's vote count.
    """
    def __init__(self, candidates, agents, allow_ties=True, num_winners=1):
        score_vector = np.zeros(len(candidates.names))
        score_vector[0] = 1
        super().__init__(candidates, agents, score_vector)
        self.allow_ties = allow_ties
        self.num_winners = num_winners
    
    def update_score_vector(self):
        score_vector = np.zeros(len(self.candidates.names))
        score_vector[0] = 1
        self.score_vector = score_vector


class Borda(ScoreVoting):
    """Represents a Borda count voting system where candidates are ranked and points are awarded 
    based on their rank order.

    In the Borda count, agents assign rankings to candidates, and each rank is assigned a point
    value, with higher ranks earning more points. The candidate with the highest cumulative 
    score wins the election.

    Parameters
    ----------
    candidates : Candidates
        An instance of the `Candidates` class containing the list of candidates.
    agents : list of Agent
        A list of `Agent` instances representing the voters in the election.
    weight_increment : int, optional
        The increment by which points are awarded based on rank order, by default 1.

    Attributes
    ----------
    weight_increment : int
        The point increment for each rank position in the Borda count.

    Methods
    -------
    calculate_results()
        Calculates and returns the winning candidate(s) and their total score.
    show_full_results()
        Displays a summary of the full voting results, including each candidate's score.
    """
    def __init__(self, candidates, agents, allow_ties=True, num_winners=1):
        score_vector = list(range(len(candidates.names)))
        score_vector.reverse()
        super().__init__(candidates, agents, score_vector)
        self.allow_ties = allow_ties
        self.num_winners = num_winners
    
    def update_score_vector(self):
        score_vector = list(range(len(self.candidates.names)))
        score_vector.reverse()
        self.score_vector = score_vector
