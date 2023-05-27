from external.buildozer.buildozer import BazelBuildozerWrapper
from utils.paths import get_bazel_example_workspace


def test_buildozer():
    workspace = get_bazel_example_workspace()
    wrapper = BazelBuildozerWrapper(workspace, "buildozer")

    # target = "//main:BUILD"

    target = "//main:hello-greet"
    # wrapper.add_load_statement(target, "//path/to/load_file", "symbol1, symbol2")
    wrapper.add_attribute_value(target, "srcs", "file1.py")
    wrapper.replace_attribute_value(target, "srcs", "file1.py", "file2.py")
    wrapper.remove_attribute_value(target, "srcs", "file2.py")
    attributes = ["srcs", "hdrs"]
    wrapper.print_attribute(target, attributes)
    # wrapper.remove_attribute(target, "hdrs")
    wrapper.rename_attribute(target, "hdrs", "headers")
    wrapper.set_attribute(target, "special_data_attr", 1)

    target = "//main"
    path = "//path/to/load_file"
    symbols = "symbol1 symbol2"
    wrapper.add_load_statement(target, path, symbols)
    wrapper.replace_load_statement(target, path + "2", "symbol1")


test_buildozer()
