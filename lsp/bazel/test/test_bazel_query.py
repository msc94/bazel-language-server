from bazel.bazel_query import BazelQuery
from utils.file import FilePosition
from utils.paths import get_bazel_example_workspace


def test_bazel_query():
    example_workspace = get_bazel_example_workspace()
    query = BazelQuery(example_workspace)

    target = "//main:hello-greet"
    location = query.get_target_location(target)

    expected_path = example_workspace.joinpath("main/BUILD")
    assert location.path == expected_path

    expected_position = FilePosition(3, 11)
    assert location.position == expected_position
