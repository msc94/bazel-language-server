import logging
from pathlib import Path


def get_file_parent_path(file_path: Path) -> Path:
    if file_path.is_dir():
        logging.info(f"get_file_parent_path: {file_path} is already a directory?")
        return file_path
    return file_path.parent


def get_module_root_path() -> Path:
    # If this file is moved, make it point to the root again
    return Path(__file__).parent.parent


def get_bazel_example_workspace() -> Path:
    return get_module_root_path().parent.joinpath("example")
