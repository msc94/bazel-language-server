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
    return {"references": {"universe": "//..."}}


def get_config_file() -> configparser.ConfigParser:
    path = _get_config_directory().joinpath("bazel-lsp").joinpath("config.ini")
    logging.info(f"Loading config from {path}")

    parser = configparser.ConfigParser()
    parser.read_dict(_get_default_config())

    if path.exists():
        with open(path, "r") as f:
            parser.read_file(f)
    else:
        logging.warning("Config file {path} does not exist, writing default...")

    # Write out config again, adding any new values from the default config
    with open(path, "w") as f:
        parser.write(f)

    return parser
