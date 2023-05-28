import logging
from pathlib import Path
from typing import Optional

import pygls.uris as uris
from lsprotocol.types import Definition, DefinitionParams, Location
from pygls.server import LanguageServer

import utils.paths as paths
from bazel.file import BazelFile, BazelFileContext, BazelFileContextType
from bazel.query import BazelQuery
from bazel.workspace import get_workspace_root
from utils.file import FilePathAndPosition, FilePosition


def definition(server: LanguageServer, params: DefinitionParams) -> Optional[Definition]:
    # https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition
    document_uri = params.text_document.uri
    document_path = Path(uris.to_fs_path(document_uri))
    document_parent_dir = paths.get_file_parent_path(document_path)

    document = server.workspace.get_document(params.text_document.uri)
    source = document.source
    bazel_file = BazelFile(source)

    position = FilePosition.from_lsp_position(params.position)
    logging.debug(f"Trying to find context at {position}")

    context = bazel_file.get_context(position)
    if context is None:
        logging.warning(
            f"No context found in file {document_path} at {position}\n  Relevant line: {document.lines[position.row]}")
        return None

    logging.debug(f"Context: {context.text}, Type: {context.type}")

    if context.type == BazelFileContextType.FILE:
        document_path = document_path.parent.joinpath(context.text)
        logging.debug(f"Go to file {document_path}")

        file_path_and_position = FilePathAndPosition(document_path, FilePosition(0, 0))
        location = file_path_and_position.to_lsp_location()

        logging.debug(f"Go to position {file_path_and_position}, location {location}")
        return location
    if context.type == BazelFileContextType.DEPENDENCY:
        target = context.text
        logging.debug(f"Go to target {target} relative to {document_parent_dir}")

        query = BazelQuery(document_parent_dir)
        file_path_and_position = query.get_target_location(target)
        location = file_path_and_position.to_lsp_location()

        if file_path_and_position is None:
            logging.error(f"Could not get location for target {target} relative to {document_parent_dir}")
            return None

        logging.debug(f"Go to position {file_path_and_position}, location {location}")
        return location
    else:
        logging.error(f"Unhandled context type {context.type}")
        return None

    return None
