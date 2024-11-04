def set_preferences(self, candidates: Candidates, ranking: list, by='order'):
    """
    Defines the preferences of an agent given a list of candidates.
    For now, we're not assigning these preferences to the candidates and an Agent can have only 1 set of preferences at a time.

    Returns
    __________
    np.array
    """

    #Make sure that the agents indicate only one vote per candidate i.e. that there are no duplicates
    if len(ranking) != len(set(ranking)):
        raise ValueError('Please vote for all candidates and ascribe only one vote per candidate')

    if by == 'name':
        ranking = [list(candidates.names.keys())[list(candidates.names.values()).index(r)] for r in ranking]

    pref = np.zeros((len(candidates.names.values()),len(candidates.names.values())))
    
    for i,v in enumerate(ranking):
        pref[i,v] = 1
    
    self.choices = pref

    return pref
