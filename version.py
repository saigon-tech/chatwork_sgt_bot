import os

__version__ = os.getenv("GIT_REV", "")[:7]
