from dataclasses import dataclass
from pathlib import Path
import sys

print(sys.path)
from lsprotocol.types import Position

# TODO: Think hard about removing these and just use the LSP types...


@dataclass
class FilePosition:
    row: int
    column: int

    # @staticmethod
    # def from_lsp_position(pos: Position):
    #     return FilePosition(pos.line, pos.character)


@dataclass
class FilePathAndPosition:
    path: Path
    position: FilePosition

    def __post_init__(self):
        if not self.path.is_absolute():
            raise RuntimeError(
                f"FilePathAndPosition needs an absolute path, given {self.path}"
            )
