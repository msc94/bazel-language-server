import logging
from typing import Optional

from lsprotocol.types import Definition, DefinitionParams
from pygls.server import LanguageServer

from bazel.bazel_file import BazelFile
from utils.file import FilePathAndPosition


def goto_definition(server: LanguageServer, params: DefinitionParams) -> Optional[Definition]:
    # https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition

    document = server.workspace.get_document(params.text_document.uri)
    source = document.source
    bazel_file = BazelFile(source)

    row = params.position.line
    column = params.position.character

    logging.debug(f"Trying to find context at {row}, {column}")

    context = bazel_file.get_context(row, column)
    if context is None:
        return None

    logging.debug(f"Context: {context.text}, Type: {context.type}")
    return None
