#!/usr/bin/python

import logging
from pathlib import Path
from typing import List, Optional

import pygls.uris as uris
from lsprotocol.types import (TEXT_DOCUMENT_DEFINITION,
                              TEXT_DOCUMENT_DOCUMENT_SYMBOL,
                              TEXT_DOCUMENT_REFERENCES, TEXT_DOCUMENT_RENAME,
                              Definition, DefinitionParams, DocumentSymbol,
                              DocumentSymbolParams, Location, ReferenceParams,
                              RenameOptions, RenameParams, WorkspaceEdit)
from pygls.server import LanguageServer

from capabilities.definition import definition
from capabilities.references import references
from capabilities.rename import rename
from capabilities.symbols import symbols
from utils.config import get_config_file
from utils.file import FilePathAndPosition

logging.basicConfig(level=logging.DEBUG, filename="/tmp/lsp.log")
config = get_config_file()

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

    universe = config.get("references", "universe")
    result = references(file_path_and_position, universe=universe)

    if result is None:
        logging.warning("Failed handling request")
        return None

    return [x.to_lsp_location() for x in result]

# @server.feature(TEXT_DOCUMENT_PREPARE_RENAME)
# def rename(params: PrepareRenameParams) -> Optional[Union[Range, PrepareRenameResult]]:


@server.feature(TEXT_DOCUMENT_RENAME, RenameOptions(prepare_provider=False))
def lsp_rename(params: RenameParams) -> Optional[WorkspaceEdit]:
    logging.info("Handling rename request")
    uri = params.text_document.uri
    position = params.position
    file_path_and_position = FilePathAndPosition.from_lsp_uri_and_position(uri, position)
    result = rename(file_path_and_position, params.new_name)

    if result is None:
        logging.warning("Failed handling request")
        return None

    logging.info(result)
    return None


@server.feature(TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def lsp_symbols(params: DocumentSymbolParams) -> Optional[List[DocumentSymbol]]:
    uri = params.text_document.uri
    path = Path(uris.to_fs_path(uri))
    return symbols(path)


logging.info("Starting bazel LSP")
server.start_io()
