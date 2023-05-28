from capabilities.references import references
from utils.file import FilePathAndPosition, FilePosition
from utils.paths import get_bazel_example_workspace


def test_references_on_name():
    # NOTE: There is a little bit of code duplication between this and the unit test of BazelQuery... what to do?
    workspace = get_bazel_example_workspace()
    file_path_and_position = FilePathAndPosition(workspace.joinpath("lib/BUILD"), FilePosition(3, 16))
    references_file_path_and_positions = references(file_path_and_position)

    first = FilePathAndPosition(workspace.joinpath("lib/BUILD"), FilePosition(3, 11))
    assert first in references_file_path_and_positions

    second = FilePathAndPosition(workspace.joinpath("main/BUILD"), FilePosition(9, 10))
    assert second in references_file_path_and_positions


def test_references_on_target():
    workspace = get_bazel_example_workspace()
    file_path_and_position = FilePathAndPosition(workspace.joinpath("main/BUILD"), FilePosition(13, 18))
    references_file_path_and_positions = references(file_path_and_position)

    first = FilePathAndPosition(workspace.joinpath("lib/BUILD"), FilePosition(3, 11))
    assert first in references_file_path_and_positions
