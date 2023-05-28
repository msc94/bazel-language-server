import ast
import enum
import logging
from collections import deque
from dataclasses import dataclass
from typing import Optional

from utils.file import FilePosition


class BazelFileContextType(enum.Enum):
    UNKNOWN = 0
    NAME = 1
    DEPENDENCY = 2
    VISBILITY = 3
    FILE = 4


@dataclass
class BazelFileContext:
    text: str
    type: BazelFileContextType


class BazelFile:
    def __init__(self, contents):
        self._ast = ast.parse(contents)

    def get_context(self, position: FilePosition) -> Optional[BazelFileContext]:
        # Note that ast lines are 1-indexed, we take 0-indexed line numbers
        node_under_cursor = self._find_deepest_node_at_position(position.row + 1, position.column)

        if not node_under_cursor:
            logging.info(f"No nodes at {position}")
            return None

        if not isinstance(node_under_cursor, ast.Constant):
            logging.info(f"Cursor not over string at {position}")
            return None

        keyword = self._get_node_keyword(node_under_cursor)
        context_type = self._keyword_to_type(keyword)

        return BazelFileContext(node_under_cursor.value, context_type)

    def _find_deepest_node_at_position(self, row, column):
        nodes = deque()
        nodes.append(self._ast)

        while nodes:
            node = nodes.popleft()

            children = list(ast.iter_child_nodes(node))

            for child in children:
                # Add information about parent
                child.parent = node
                # Visit children next
                nodes.append(child)

            if hasattr(node, "lineno") and hasattr(node, "col_offset"):
                if self._position_over_node(node, row, column) and len(children) == 0:
                    # We have a node under the cursor and it has no children -> return
                    return node

        return None

    def _position_over_node(self, node, row, column):
        if row < node.lineno or row > node.end_lineno:
            return False
        if column < node.col_offset or column >= node.end_col_offset:
            return False
        return True

    def _keyword_to_type(self, type):
        if type == "name":
            return BazelFileContextType.NAME
        elif type == "srcs" or type == "hdrs":
            return BazelFileContextType.FILE
        elif type == "deps":
            return BazelFileContextType.DEPENDENCY
        else:
            logging.warning(f"Unknown type {type}")
            return BazelFileContextType.UNKNOWN

    def _get_node_keyword(self, node):
        current = node
        while current is not None:
            if isinstance(current, ast.keyword):
                return current.arg
            current = getattr(current, "parent", None)
        return None
