import logging

from lsprotocol.types import TEXT_DOCUMENT_DEFINITION, Definition, DefinitionParams
from pygls.server import LanguageServer

from capabilities.goto_definition import goto_definition

logging.basicConfig(level=logging.DEBUG, filename="/tmp/lsp.log")
server = LanguageServer("bazel-language-server", "v0.1")


@server.feature(TEXT_DOCUMENT_DEFINITION)
def definitions(params: DefinitionParams) -> Definition:
    logging.info("Handling definition request")
    return goto_definition(server, params)


logging.info("Starting bazel LSP")
server.start_io()
