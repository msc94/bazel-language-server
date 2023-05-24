import ast
import enum
import logging


class BazelFileContextType(enum.Enum):
    FILE = 1


class BazelFileContext:
    def __init__(self, text: str, type: BazelFileContextType):
        self.text = text
        self.type = type


class BazelFile:
    def __init__(self, contents):
        self._ast = ast.parse(contents)
        logging.debug(f"Bazel file AST:\n{ast.dump(self._ast, indent=4)}")

    def get_context(self, row, column) -> BazelFileContext:
        nodes = self._find_nodes(row, column)

        if not nodes:
            logging.info(f"No nodes at {row}, {column}")
            return None

        # Check if we have a ast.Constant node
        node = next(x for x in nodes if isinstance(x, ast.Constant))

        if node is None:
            logging.info(f"Cursor not over string at {row}, {column}")
            return None

        return BazelFileContext(node.value, BazelFileContextType.FILE)

    def _find_nodes(self, row, column):
        nodes = []
        for node in ast.walk(self._ast):
            # Add information about parent node to children
            for child in ast.iter_child_nodes(node):
                node.parent = child

            if hasattr(node, "lineno") and hasattr(node, "col_offset"):
                if node.lineno == row and (
                    column >= node.col_offset and column < node.end_col_offset
                ):
                    nodes.append(node)

        return nodes
