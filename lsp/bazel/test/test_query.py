from bazel.query import BazelQuery
from utils.file import FilePathAndPosition, FilePosition
from utils.paths import get_bazel_example_workspace


def test_get_target_location():
    example_workspace = get_bazel_example_workspace()
    query = BazelQuery(example_workspace)

    target = "//main:hello-greet"
    location = query.get_target_location(target)

    expected_path = example_workspace.joinpath("main/BUILD")
    assert location.path == expected_path

    expected_position = FilePosition(3, 11)
    assert location.position == expected_position


def test_get_target_location_relative():
    build_file_path = get_bazel_example_workspace().joinpath("main")
    query = BazelQuery(build_file_path)

    target = ":hello-greet"
    location = query.get_target_location(target)

    expected_path = build_file_path.joinpath("BUILD")
    assert location.path == expected_path

    expected_position = FilePosition(3, 11)
    assert location.position == expected_position


def test_get_target_rdeps():
    example_workspace = get_bazel_example_workspace()
    query = BazelQuery(example_workspace)

    target = "//lib:hello-time"
    rdeps = query.get_target_rdeps(target, universe="//...", depth=1)

    assert len(rdeps) == 2

    first = FilePathAndPosition(example_workspace.joinpath("lib/BUILD"), FilePosition(3, 11))
    assert first in rdeps

    second = FilePathAndPosition(example_workspace.joinpath("main/BUILD"), FilePosition(9, 10))
    assert second in rdeps
