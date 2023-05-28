from typing import List, Optional

from lsprotocol.types import Location, ReferenceParams
from pygls.server import LanguageServer


def references(server: LanguageServer, params: ReferenceParams) -> Optional[List[Location]]:
    return None
