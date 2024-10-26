class Candidates():
    '''
    Instantiate the list of candidates (alternatives) for an election
    '''

    def __init__(self,names: list):
        '''
        transform a list of (n) names into a dictionary with keys from 0 to n.
        '''
        self.names = {i:v for i,v in enumerate(names)}
