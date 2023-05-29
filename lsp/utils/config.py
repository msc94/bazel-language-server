import configparser
import logging
import os
from pathlib import Path


def _get_config_directory() -> Path:
    # TODO: That's not really platform agnostic...
    dir = os.environ.get("XDG_CONFIG_HOME")
    if dir is None:
        path = Path("~/.config").expanduser()
    else:
        path = Path(dir)
    return path


def _get_default_config() -> dict:
    return {
        "references": {
            "universe": "//...",
        },
    }


def get_config_file() -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    parser.read_dict(_get_default_config())

    path = _get_config_directory().joinpath("bazel-lsp").joinpath("config.ini")
    if path.exists():
        logging.info(f"Loading config from {path}")
        with open(path, "r") as f:
            parser.read_file(f)
    else:
        logging.warning(f"Config file {path} does not exist, writing default...")

    # Create the directory path if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Write out config again, adding any new values from the default config
    with open(path, "w") as f:
        parser.write(f)

    return parser
