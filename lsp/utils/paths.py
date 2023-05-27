from pathlib import Path


def get_module_root_path() -> Path:
    # If this file is moved, make it point to the root again
    return Path(__file__).parent.parent


def get_bazel_example_workspace() -> Path:
    return get_module_root_path().parent.joinpath("example")
