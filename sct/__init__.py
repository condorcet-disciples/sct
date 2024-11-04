"""
A voting system package grounded in principles from social choice theory, modeling agents, candidates, 
and diverse voting methods for election simulations.

Modules
-------
agent : Defines the `Agent` class, representing a voter with preferences in an election.
candidates : Defines the `Candidates` class, a collection of candidates with functionalities to manage them.
election : Contains classes for different voting methods, such as `Plurality` and `Borda`, 
           each inheriting from the `Election` base class.

Classes
-------
Agent
    Represents a voter with a specified number of votes and a preference list.
Candidates
    Manages a list of candidates, with methods to add or remove candidates.
Election
    The base class for an election with candidates and agents, to be subclassed for specific voting methods.
Plurality
    A subclass of `Election` implementing a plurality voting system where the candidate with the most votes wins.
Borda
    A subclass of `Election` implementing a Borda count voting system, where points are assigned based on rank.

Usage
-----
The package can be used to set up an election, add agents and candidates, and run different voting methods 
to see outcomes based on plurality or Borda count rules. It allows for customization of election rules, 
such as allowing ties or setting different weight increments in the Borda method.
"""

from .agent import *
from .candidates import *
from .election import *