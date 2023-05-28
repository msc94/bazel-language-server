#!/usr/bin/python

import logging
from typing import List, Optional

from lsprotocol.types import (Location, WorkspaceEdit)
from lsprotocol.types import (TEXT_DOCUMENT_DEFINITION, Definition, DefinitionParams)
from lsprotocol.types import (TEXT_DOCUMENT_REFERENCES, ReferenceParams)
from lsprotocol.types import (TEXT_DOCUMENT_RENAME, RenameOptions, RenameParams)

from pygls.server import LanguageServer

from capabilities.definition import definition
from capabilities.references import references
from capabilities.rename import rename
from utils.file import FilePathAndPosition


logging.basicConfig(level=logging.DEBUG, filename="/tmp/lsp.log")
server = LanguageServer("bazel-language-server", "v0.1")


@server.feature(TEXT_DOCUMENT_DEFINITION)
def lsp_definition(params: DefinitionParams) -> Optional[Definition]:
    logging.info("Handling definition request")
    uri = params.text_document.uri
    position = params.position
    file_path_and_position = FilePathAndPosition.from_lsp_uri_and_position(uri, position)

    result = definition(file_path_and_position)
    if result is None:
        logging.warning("Failed handling request")
        return None

    return result.to_lsp_location()


@server.feature(TEXT_DOCUMENT_REFERENCES)
def lsp_references(params: ReferenceParams) -> Optional[List[Location]]:
    logging.info("Handling references request")
    uri = params.text_document.uri
    position = params.position
    file_path_and_position = FilePathAndPosition.from_lsp_uri_and_position(uri, position)
    result = references(file_path_and_position)

    if result is None:
        logging.warning("Failed handling request")
        return None

    return [x.to_lsp_location() for x in result]


@server.feature(TEXT_DOCUMENT_RENAME, RenameOptions(prepare_provider=True))
def lsp_rename(params: RenameParams) -> Optional[WorkspaceEdit]:
    return None #return WorkspaceEdit(**workspace_edit)

logging.info("Starting bazel LSP")
server.start_io()
