class EmptyFileError(Exception):
    """Used when a confg file is empty"""

class InvalidConfigPathError(Exception):
    """Used when the inputted config path is invalid"""

class NoChangesMade(Exception):
    """Used when there's an error writing to file and no changes are made"""