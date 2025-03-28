class Candidates:
    """Represents a collection of candidates in a voting system, allowing for management of 
    candidate names including adding, removing, and organizing candidates.

    Parameters
    ----------
    names : list of str
        A list of candidate names to initialize the collection. Names are standardized to lowercase 
        and sorted alphabetically.

    Attributes
    ----------
    names : list of str
        An alphabetically sorted list of candidate names in lowercase for consistent reference.

    Methods
    -------
    add_candidate(name)
        Adds a new candidate to the collection, ensuring that the name is unique, standardized 
        to lowercase, and the list remains sorted.
    remove_candidate(name)
        Removes a candidate from the collection by name, if the name exists.
    """
    def __init__(self, names: list):
        if not all(isinstance(name, str) for name in names):
            raise TypeError("All candidate names must be strings.")
        self.names = [name.lower() for name in names]
        self.names.sort()

    def add_candidate(self, name):
        """Adds a new candidate to the collection.

        Parameters
        ----------
        name : str
            The name of the candidate to add.

        Raises
        ------
        ValueError
            If the candidate already exists in the collection.
        """
        if name.lower() in self.names:
            raise ValueError(f"Candidate '{name}' already exists.")
        self.names.append(name.lower())
        self.names.sort()

    def remove_candidate(self, name):
        """Removes a candidate from the collection.

        Parameters
        ----------
        name : str
            The name of the candidate to remove.

        Raises
        ------
        ValueError
            If the candidate is not in the collection.
        """
        if name.lower() not in self.names:
            raise ValueError(f"Candidate '{name}' not found.")
        self.names.remove(name.lower())