import logging

from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DEFINITION,
    CompletionItem,
    CompletionList,
    CompletionParams,
    Definition,
    DefinitionParams,
    Location,
)
from pygls.server import LanguageServer

logging.basicConfig(level=logging.DEBUG)
server = LanguageServer("bazel-language-server", "v0.1")


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition
@server.feature(TEXT_DOCUMENT_DEFINITION)
def definitions(params: DefinitionParams) -> Definition:
    logging.info("Handling definition request")

    document = server.workspace.get_document(params.text_document.uri)
    logging.info(f"Document: {document}")

    current_line = document.lines[params.position.line].strip()
    logging.debug(f"Current line: {current_line}")

    return None


logging.info("Starting bazel LSP")
server.start_io()
