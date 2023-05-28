import logging
from typing import List, Optional

from bazel.file import BazelFile, BazelFileContextType
from bazel.query import BazelQuery
from utils.file import FilePathAndPosition, read_text_file


def references(file_path_and_position: FilePathAndPosition, universe: str) -> Optional[List[FilePathAndPosition]]:
    logging.info(f"Getting references at {file_path_and_position}")

    file_path = file_path_and_position.path
    directory_path = file_path.parent

    contents = read_text_file(file_path)
    bazel_file = BazelFile(contents)

    context = bazel_file.get_context(file_path_and_position.position)
    if context is None:
        logging.warning(
            f"No context found at {file_path_and_position}")
        return None

    logging.debug(f"Context: {context.text}, type: {context.type}")

    if context.type == BazelFileContextType.NAME:
        target = f":{context.text}"
        query = BazelQuery(directory_path)
        rdeps = query.get_target_rdeps(target, universe=universe, depth=1)
        return rdeps
    if context.type == BazelFileContextType.DEPENDENCY:
        query = BazelQuery(directory_path)
        rdeps = query.get_target_rdeps(context.text, universe=universe, depth=1)
        return rdeps
    else:
        logging.error(f"Unhandled context type {context.type}")
        return None
