from typing import List, Optional

from lsprotocol.types import Location
from lsprotocol.types import (TEXT_DOCUMENT_RENAME, RenameOptions, RenameParams)
from lsprotocol.types import WorkspaceEdit

from pygls.server import LanguageServer
from utils.file import FilePathAndPosition, FilePosition


def rename(params: RenameParams) -> Optional[WorkspaceEdit]:
    return None
