from typing import List, Optional

from lsprotocol.types import Location, ReferenceParams
from pygls.server import LanguageServer

from utils.file import FilePathAndPosition, FilePosition


def references(file_path_and_position: FilePathAndPosition) -> Optional[List[FilePathAndPosition]]:
    return None
