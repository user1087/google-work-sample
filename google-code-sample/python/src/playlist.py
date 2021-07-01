"""A playlist class."""

class Playlist:

    def __init__(self, name):
        """The Playlist class is initialized."""
        self._name = name
        self._videos = []

    def __lt__(self, other):
        return self._name < other._name

    def __gt__(self, other):
       return self._name > other._name

    def __le__(self, other):
       return self._name <= other._name

    def __ge__(self, other):
       return self._name >= other._name

    def __eq__(self, other):
       return self._name == other._name

    def __ne__(self, other):
       return self._name != other._name