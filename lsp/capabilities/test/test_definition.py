from capabilities.definition import definition
from utils.file import FilePathAndPosition, FilePosition
from utils.paths import get_bazel_example_workspace


def test_definition():
    workspace = get_bazel_example_workspace()
    file_path_and_position = FilePathAndPosition(workspace.joinpath("main/BUILD"), FilePosition(13, 19))
    definition_file_path_and_position = definition(file_path_and_position)

    assert definition_file_path_and_position.path == workspace.joinpath("lib/BUILD")
    assert definition_file_path_and_position.position == FilePosition(3, 11)
