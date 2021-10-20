"""
This exceptions were introduces as a mechanism to cancel tasks if main page gives 404 or
data is already collected in order to trim a number of requests.

NOT USED IN A FINAL VERSION
"""


class PageNotFoundException(Exception):
    pass


class DataAlreadyCollectedException(Exception):
    pass
