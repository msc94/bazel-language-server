import logging
import re

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

from bazel.bazel_file import BazelFile

logging.basicConfig(level=logging.DEBUG, filename="/tmp/lsp.log")
server = LanguageServer("bazel-language-server", "v0.1")


@server.feature(TEXT_DOCUMENT_DEFINITION)
def definitions(params: DefinitionParams) -> Definition:
    # https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition
    logging.info("Handling definition request")

    document = server.workspace.get_document(params.text_document.uri)
    source = document.source
    bazel_file = BazelFile(source)

    row = params.position.line
    column = params.position.character

    logging.debug(f"Trying to find context at {row}, {column}")

    context = bazel_file.get_context(row, column)
    logging.debug(f"Context: {context.text}, Type: {context.type}")

    return None


logging.info("Starting bazel LSP")
server.start_io()
