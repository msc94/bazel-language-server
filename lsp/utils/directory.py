import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DirectoryChanger:
    directory: Path

    def __enter__(self):
        self._old = os.getcwd()
        os.chdir(self.directory)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._old)
