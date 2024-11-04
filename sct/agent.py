import numpy as np
from sct.candidates import Candidates

class Agent:
    """Represents an agent (or voter) in a voting system, with the ability to set preferences
    for a list of candidates based on choice order.

    The `Agent` class is designed to manage individual voting preferences, allowing each agent
    to define and update their preferred order of candidates. It can be used in various voting 
    systems where voter preferences play a role in determining outcomes.

    Parameters
    ----------
    name : str, optional
        The name of the agent, which can be used to identify them uniquely. Defaults to None if not specified.
    num_votes : int, optional
        The number of votes the agent possesses, with a default of 1.
    choices : list of str, optional
        A list of preferred candidates in the agent's order of choice, represented as strings.
        Each choice is converted to lowercase to ensure standardization.

    Attributes
    ----------
    name : str
        The name of the agent.
    num_votes : int
        The number of votes assigned to the agent.
    choices : list of str
        An ordered list of the agent's preferred candidates, stored in lowercase.

    Methods
    -------
    set_preferences(choices)
        Defines or updates the agent's candidate preferences based on the provided list.
    """
    def __init__(self, name=None, num_votes=1, choices=None):
        self.name = name
        self.num_votes = num_votes
        self.choices = [choice.lower() for choice in choices]

    def set_preferences(self, choices: list):
        """ Defines or updates the preference order for the agent based on a list of candidate choices.

        Parameters
        ----------
        choices : list of str
            A list of candidate choices representing the agent's preferred order. 
            Each choice is converted to lowercase for standardization.

        Returns
        -------
        list of str
            The updated list of candidate preferences in lowercase.
        """
        self.choices = [choice.lower() for choice in choices]

        return self.choices
