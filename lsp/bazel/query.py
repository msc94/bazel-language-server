import logging
import subprocess
from pathlib import Path
from typing import List, Optional

from utils.directory import DirectoryChanger
from utils.file import FilePathAndPosition, FilePosition

# NOTE: We can also implement a simpler version of this class that does not use bazel but does simple directory
# manipulations. That could be much faster.


class BazelQuery:
    def __init__(self, root_path: Path):
        self._root_path = root_path

    def get_target_location(self, target: str) -> Optional[FilePathAndPosition]:
        logging.debug(f"Querying location of target {target} in {self._root_path}")

        locations = self._execute_query(target, "location")
        logging.debug(f"Locations: {locations}")

        if len(locations) == 0:
            logging.warning(f"Could not get location for {target} in {self._root_path}")
            return None

        if len(locations) > 1:
            logging.warning(f"Got more than one location for {target} in {self._root_path}")
            return None

        return self._parse_location(locations[0])

    def get_target_rdeps(self, target: str, universe: str, depth: Optional[int] = None) -> Optional[List[FilePathAndPosition]]:
        logging.debug(
            f"Querying rdeps of target {target} in {self._root_path}, universe {universe}, depth of {depth}")

        # rdeps(universe, x, depth)
        if depth is None:
            query = f"rdeps({universe}, {target})"
        else:
            query = f"rdeps({universe}, {target}, {depth})"

        rdeps = self._execute_query(query, "location")
        logging.debug(f"Reverse dependencies: {rdeps}")

        if len(rdeps) == 0:
            logging.warning(f"Failed to get rdeps for {target} in {self._root_path}")
            return None

        return [self._parse_location(x) for x in rdeps]

    def _parse_location(self, location: str) -> FilePathAndPosition:
        parts = location.split(":")
        return FilePathAndPosition(Path(parts[0]), FilePosition(int(parts[1]), int(parts[2])))

    def _execute_query(self, target: str, output_type: str) -> List[str]:
        with DirectoryChanger(self._root_path):
            locations = subprocess.check_output(["bazel", "query", f"--output={output_type}", target])
            return [x for x in locations.decode("utf-8").split("\n") if x]
