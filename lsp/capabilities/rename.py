import logging

from typing import List, Dict, Optional, Text

from lsprotocol.types import Location, Position, Range
from lsprotocol.types import (TEXT_DOCUMENT_RENAME, RenameOptions, RenameParams)
from lsprotocol.types import WorkspaceEdit
from external.buildozer.buildozer import BazelBuildozerWrapper

from lsprotocol.types import (
    CreateFile,
    CreateFileOptions,
    DeleteFile,
    DeleteFileOptions,
    OptionalVersionedTextDocumentIdentifier,
    Position,
    Range,
    RenameFile,
    RenameFileOptions,
    RenameOptions,
    RenameParams,
    ResourceOperationKind,
    TextDocumentEdit,
    TextDocumentIdentifier,
    TextEdit,
    WorkspaceEdit,
)

from utils.file import FilePathAndPosition, FilePosition, get_line_from_file, get_target_at_position
from bazel.workspace import get_workspace_root

from capabilities.references import references

def rename(file_path_and_position: FilePathAndPosition, new_name: str) -> Optional[Dict]:

    file = file_path_and_position.path
    position = file_path_and_position.position

    workspace = str(get_workspace_root(file))
    target_name = get_target_at_position(file, position.row, position.column)
    if target_name is None:
        return None

    package = '/' + str(file).replace(workspace, '').replace('/BUILD', '')
    full_target_new_name = package + ":" + new_name
    full_target_name = package + ":" + target_name

    logging.debug(f"workspace: {workspace}")
    logging.debug(f"package: {package}")
    logging.debug(f"target_name: {target_name}")
    logging.debug(f"full_target_name: {full_target_name}")
    logging.debug(f"full_target_new_name: {full_target_new_name}")

    refs = references(file_path_and_position)



    if refs is None:
        return None

    changes = {}

    workspace_edit = {
        "changes": changes
    }

    logging.info(workspace_edit)

    return workspace_edit

    # for d in refs:

    #     logging.debug(f"File: {d.path}:{d.position.row + 1}")

    #     line = get_line_from_file(d.path, d.position.row + 1)
    #     if line is None:
    #         continue

    #     line = line[d.position.column:]

    #     logging.debug("Line from file: " + line)

    #     line_num = d.position.row
    #     start = d.position.column
    #     end   = line.find('"')

    #     logging.debug(f"positions {line_num}:{start}:{end}")

    #     text_edit=TextEdit(range=Range(
    #         start=Position(line=line_num, character=start),
    #         end=Position(line=line_num, character=end)
    #         ),
    #         new_text=new_name)

    #     path = str(d.path)
    #     if path not in changes.keys():
    #         changes[path] = []
    #     changes[path].append(text_edit)
    # "changes": {
    #     "uri1": [
    #         TextEdit(
    #             range=Range(
    #                 start=Position(line=0, character=0),
    #                 end=Position(line=1, character=1),
    #             ),
    #             new_text="text1",
    #         ),
    #         TextEdit(
    #             range=Range(
    #                 start=Position(line=1, character=1),
    #                 end=Position(line=2, character=2),
    #             ),
    #             new_text="text2",
    #         ),
    #     ],
    # },
