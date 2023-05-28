import sys
from dataclasses import dataclass
from pathlib import Path

import pygls.uris as uris
from lsprotocol.types import Location, Position, Range

print(sys.path)

# TODO: Think hard about removing these and just use the LSP types...


@dataclass
class FilePosition:
    # 0-indexed
    row: int

    # TODO: Take a look at character encoding
    column: int

    def to_lsp_position(self) -> Position:
        return Position(self.row, self.column)

    @staticmethod
    def from_lsp_position(pos: Position):
        return FilePosition(pos.line, pos.character)


@dataclass
class FilePathAndPosition:
    path: Path
    position: FilePosition

    def __post_init__(self):
        if not self.path.is_absolute():
            raise RuntimeError(
                f"FilePathAndPosition needs an absolute path, given {self.path}"
            )

    def to_lsp_location(self) -> Location:
        start = self.position.to_lsp_position()
        end = Position(start.line + 1, 0)
        range = Range(start, end)
        return Location(uris.from_fs_path(str(self.path)), range)
