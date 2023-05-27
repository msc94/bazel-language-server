import logging
import subprocess
from pathlib import Path
from typing import List, Optional

from utils.directory import DirectoryChanger
from utils.file import FilePathAndPosition, FilePosition

# NOTE: We can also implement a simpler version of this class that does not use bazel but does simple directory
# manipulations. That could be much faster.


class BazelQuery:
    def __init__(self, workspace_root: Path):
        self._workspace_root = workspace_root

    def get_target_location(self, target: str) -> Optional[FilePathAndPosition]:
        logging.debug(f"Querying location of target {target} in {self._workspace_root}")

        locations = self._execute_query(target, "location")
        logging.debug(f"Locations: {locations}")

        if len(locations) == 0:
            logging.warning(f"Could not get location of Bazel target {target} in {self._workspace_root}")
            return None

        if len(locations) > 1:
            logging.warning(f"Got more than one location for Bazel target {target} in {self._workspace_root}")
            return None

        return self._parse_location(locations[0])

    def _parse_location(self, location: str) -> FilePathAndPosition:
        parts = location.split(":")
        return FilePathAndPosition(Path(parts[0]), FilePosition(int(parts[1]), int(parts[2])))

    def _execute_query(self, target: str, output_type: str) -> List[str]:
        try:
            changer = DirectoryChanger(self._workspace_root)
            locations = subprocess.check_output(["bazel", "query", f"--output={output_type}", target])
            return [x for x in locations.decode("utf-8").split("\n") if x]
        finally:
            changer.revert()
