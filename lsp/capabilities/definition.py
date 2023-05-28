import logging
from pathlib import Path
from typing import Optional

from lsprotocol.types import Definition, DefinitionParams, Location

import utils.paths as paths
from bazel.file import BazelFile, BazelFileContext, BazelFileContextType
from bazel.query import BazelQuery
from bazel.workspace import get_workspace_root
from utils.file import FilePathAndPosition, FilePosition, read_text_file


def definition(file_path_and_position: FilePathAndPosition) -> Optional[FilePathAndPosition]:
    # https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition
    logging.info(f"Getting definition at {file_path_and_position}")

    file_path = file_path_and_position.path
    directory_path = file_path.parent

    contents = read_text_file(file_path)
    bazel_file = BazelFile(contents)

    context = bazel_file.get_context(file_path_and_position.position)
    if context is None:
        logging.warning(
            f"No context found at {file_path_and_position}")
        return None

    logging.debug(f"Context: {context.text}, Type: {context.type}")

    if context.type == BazelFileContextType.FILE:
        document_path = directory_path.joinpath(context.text)
        logging.debug(f"Go to file {document_path}")

        file_path_and_position = FilePathAndPosition(document_path, FilePosition(0, 0))

        logging.debug(f"Go to position {file_path_and_position}")
        return file_path_and_position
    if context.type == BazelFileContextType.DEPENDENCY:
        target = context.text
        logging.debug(f"Go to target {target} relative to {directory_path}")

        query = BazelQuery(directory_path)
        query_result = query.get_target_location(target)

        if query_result is None:
            logging.error(f"Could not get location for target {target} relative to {directory_path}")
            return None

        logging.debug(f"Go to position {file_path_and_position}")
        return query_result
    else:
        logging.error(f"Unhandled context type {context.type}")
        return None

    return None
