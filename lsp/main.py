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

logging.basicConfig(level=logging.DEBUG, filename="/tmp/lsp.log")
server = LanguageServer("bazel-language-server", "v0.1")

# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition


def extract_target(line: str, cursor_pos: int) -> str:
    logging.info(f"Extracting target from {line}, pos {cursor_pos}")

    start = cursor_pos
    while line[start] != '"':
        start -= 1
        if start == -1:
            return None

    end = cursor_pos
    while line[end] != '"':
        end += 1
        if end == len(line) - 1:
            return None

    return line[start + 1 : end]


@server.feature(TEXT_DOCUMENT_DEFINITION)
def definitions(params: DefinitionParams) -> Definition:
    logging.info("Handling definition request")

    document = server.workspace.get_document(params.text_document.uri)

    current_line = document.lines[params.position.line]
    logging.debug(f"Current line: {current_line}")

    # TODO: Handle UTF-16 -> UTF-32
    cursor_pos = params.position.character
    target = extract_target(current_line, cursor_pos)

    logging.debug(f"Target: {target}")

    return None


logging.info("Starting bazel LSP")
server.start_io()
