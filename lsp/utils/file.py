import sys
from dataclasses import dataclass
from pathlib import Path

import pygls.uris as uris
from lsprotocol.types import Location, Position, Range


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
                f"FilePathAndPosition: {self.path} is not an absolute path"
            )

        if not self.path.exists():
            raise RuntimeError(
                f"FilePathAndPosition: {self.path} does not exist"
            )

        if not self.path.is_file():
            raise RuntimeError(
                f"FilePathAndPosition: {self.path} is not a file"
            )

    @staticmethod
    def from_lsp_uri_and_position(uri: str, pos: Position):
        return FilePathAndPosition(Path(uris.to_fs_path(uri)), FilePosition.from_lsp_position(pos))

    def to_lsp_location(self) -> Location:
        start = self.position.to_lsp_position()
        # LSP works with ranges, we work only with a single cursor position...
        end = Position(start.line + 1, 0)
        range = Range(start, end)
        return Location(uris.from_fs_path(str(self.path)), range)


def read_text_file(file_path: Path) -> str:
    if not file_path.is_file():
        raise RuntimeError(f"read_file {file_path} is not a file")

    with open(file_path, "r") as f:
        return f.read()


def get_line_from_file(file_path, line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if 0 <= line < len(lines):
            return lines[line - 1]
    return None

import logging
import re

#TODO: this is really fragile and shity. It should be handeled when full bazel ast is made
def get_target_at_position(file_path, row, col):
    line = get_line_from_file(file_path, row)
    if line is None:
        return None

    pattern = r"[ ,\"'/]\[]"
    start = end = -1
    match = re.search(pattern, line[:col])
    if match:
        logging.debug(f"match: {match.group()[:-1]}")
        start = match.start()

    logging.debug(f"LINE: {line}")

    match = re.search(pattern, line[start:])
    if match:
        end = match.start()

    logging.debug(f"row: {row} col:{col}")
    logging.debug(f"start: {start} end:{end}")
    logging.debug(f"Found string {line[start:end]}")

    return line[start:end]

