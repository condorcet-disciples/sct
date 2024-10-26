'''
    CLASS NOT IN USE FOR NOW.
    In this class, we could model all potential preference rankings for a specific set of candidates (or maybe we do this in the candidates class?)
'''


from sct.candidates import Candidates

class Preferences():

    def __init__(self,candidates: Candidates):
        self.candidates = candidates