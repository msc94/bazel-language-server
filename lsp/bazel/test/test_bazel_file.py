from bazel.bazel_file import BazelFile, BazelFileContextType

bzl_contents = """
load("@rules_cc//cc:defs.bzl", "cc_binary", "cc_library")

cc_library(
    name = "hello-greet",           # Line 5
    srcs = ["hello-greet.cc"],
    hdrs = ["hello-greet.h"],
)

cc_binary(
    name = "hello-world",
    srcs = ["hello-world.cc"],
    deps = [
        ":hello-greet",
        "//lib:hello-time",         # Line 15
    ],
)"""


def test_name():
    file = BazelFile(bzl_contents)
    context = file.get_context(5, 15)
    assert context.text == "hello-greet"
    assert context.type == BazelFileContextType.NAME


def test_dep():
    file = BazelFile(bzl_contents)
    context = file.get_context(15, 19)
    assert context.text == "//lib:hello-time"
    assert context.type == BazelFileContextType.DEPENDENCY
