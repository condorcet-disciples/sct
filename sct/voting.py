import numpy as np
from sct.agent import Agent
from sct.candidates import Candidates


class Election:
    '''
    Contains voting methods
    '''

    def __init__(self):
        pass

    def plurality(self, candidates: Candidates, agents: list, num_winners=1):
        '''
        Implementation of the plurality voting methods

        Inputs:
        candidates: Candidates object
        agents: List of Agent objects

        Returns:
        name of winner
        '''

        all_prefs = [agent.prefs * agent.coef for agent in agents] # Creating a list of matrices of preferences from the candidates weighted by the coefficient ascribed
        results = sum(all_prefs) # Summing preferences
        tie_flag = np.full(results.shape[0], False)
        winners = []
        i=0
        while len(winners)<num_winners:
            winner_idx = np.where(results[i]==max(results[i])) # Selecting the candidate that had the best score for the first row - #TODO: Adapt for multi-winners & ties 
            if len(winner_idx[0])>1:
                tie_flag[i]=True
            for idx in winner_idx[0]:
                winners.append(candidates.names[idx]) # Accessing the name of the winner
            i+=1

        return winners, results, tie_flag
    
    def borda(self, candidates: Candidates, agents: list, score_type='asymmetric'):
        '''
        Implementation of the Borda scoring method

        Inputs:
        candidates: Candidates object
        agents: List of Agent objects

        Returns:
        name of winner
        '''

        vector_score = np.array(list(reversed(range(len(candidates.names.values())))))
        all_prefs = [(vector_score @ agent.prefs) * agent.coef for agent in agents] # Creating a list of matrices of preferences from the candidates weighted by the coefficient ascribed
        results = sum(all_prefs) # Summing preferences
        winner_idx = np.argmax(results) # Selecting the candidate that had the best score for the first row - #TODO: Adapt for multi-winners & ties 
        winner = candidates.names[winner_idx] # Accessing the name of the winner

        return winner, results
    
    
class Plurality:
    def __init__(self, agents, candidates, winners=1):
        pass
