import logging
from typing import List, Optional

from lsprotocol.types import (TEXT_DOCUMENT_DEFINITION,
                              TEXT_DOCUMENT_REFERENCES, Definition,
                              DefinitionParams, Location, ReferenceParams)
from pygls.server import LanguageServer

import capabilities.definition
import capabilities.references
from utils.file import FilePathAndPosition

logging.basicConfig(level=logging.DEBUG, filename="/tmp/lsp.log")
server = LanguageServer("bazel-language-server", "v0.1")


@server.feature(TEXT_DOCUMENT_DEFINITION)
def definition(params: DefinitionParams) -> Optional[Definition]:
    logging.info("Handling definition request")
    uri = params.text_document.uri
    position = params.position
    file_path_and_position = FilePathAndPosition.from_lsp_uri_and_position(uri, position)
    return capabilities.definition.definition(file_path_and_position)


@server.feature(TEXT_DOCUMENT_REFERENCES)
def references(params: ReferenceParams) -> Optional[List[Location]]:
    logging.info("Handling references request")
    uri = params.text_document.uri
    position = params.position
    file_path_and_position = FilePathAndPosition.from_lsp_uri_and_position(uri, position)
    return capabilities.references.references(file_path_and_position)


logging.info("Starting bazel LSP")
server.start_io()
