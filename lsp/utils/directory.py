import os
from pathlib import Path


class DirectoryChanger:
    def __init__(self, directory: Path):
        # Save the current cwd
        self._oldpath = os.getcwd()
        os.chdir(directory)

    def revert(self):
        os.chdir(self._oldpath)
