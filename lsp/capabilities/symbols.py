import logging
from pathlib import Path
from typing import List, Optional

from lsprotocol.types import DocumentSymbol

from utils.file import read_text_file


def symbols(path: Path) -> Optional[List[DocumentSymbol]]:
    logging.info(f"Getting symbols from {path}")
    contents = read_text_file(path)
