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
    def __init__(self, candidates: Candidates, agents: list):
        self.candidates = candidates
        self.agents = agents


class Plurailty(Election):
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
    def __init__(self, candidates, agents, allow_ties=True):
        super().__init__(candidates, agents)
        self.allow_ties = allow_ties

    def calculate_results(self):
        """Calculates the results of the plurality election.

        Each agent's top candidate preference is counted as a single vote. The candidate with the
        highest vote count is declared the winner. If `allow_ties` is True, multiple candidates can
        win in the case of a tie.

        Returns
        -------
        tuple
            A tuple containing the winner(s) and their respective vote count.
        """
        pass # shoudl reutrn winner and votes earned imo

    def show_full_results(self):
        """Displays the full results of the plurality election.

        This includes a summary of each candidate and the total votes they received.
        """
        pass


class Borda(Election):
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
    def __init__(self, candidates, agents, weight_increment=1):
        super().__init__(candidates, agents)
        self.weight_increment = weight_increment

    def calculate_results(self):
        """Calculates the results of the Borda count election.

        Each agent ranks candidates, and points are awarded incrementally based on rank position. 
        The candidate with the highest total score is declared the winner.

        Returns
        -------
        tuple
            A tuple containing the winner(s) and their respective scores.
        """
        pass # shoudl reutrn winner and votes earned imo

    def show_full_results(self):
        """Displays the full results of the Borda count election.

        This includes a summary of each candidate and the total points they received.
        """
        pass
