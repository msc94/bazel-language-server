import subprocess
from pathlib import Path

from utils.directory import DirectoryChanger


def get_workspace_root(path: Path) -> Path:
    if not path.is_dir():
        dir = path.parent
    else:
        dir = path

    with DirectoryChanger(dir):
        raw_workspace = subprocess.check_output(["bazel", "info", "workspace"]).decode("utf-8").strip()
        path = Path(raw_workspace)
        if not path.exists() or not path.is_dir():
            raise RuntimeError(f"Failed getting workspace root from {path}")
        return path
