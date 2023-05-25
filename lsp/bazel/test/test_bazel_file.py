from bazel.bazel_file import BazelFile, BazelFileContextType

bzl_contents = """                  # Line 0
load("@rules_cc//cc:defs.bzl", "cc_binary", "cc_library")

cc_library(
    name = "hello-greet",           # Line 4
    srcs = ["hello-greet.cc"],
    hdrs = ["hello-greet.h"],
)

cc_binary(
    name = "hello-world",
    srcs = ["hello-world.cc"],
    deps = [
        ":hello-greet",
        "//lib:hello-time",         # Line 14
    ],
)"""


def test_name():
    file = BazelFile(bzl_contents)
    context = file.get_context(4, 15)
    assert context.text == "hello-greet"
    assert context.type == BazelFileContextType.NAME


def test_dep():
    file = BazelFile(bzl_contents)
    context = file.get_context(14, 19)
    assert context.text == "//lib:hello-time"
    assert context.type == BazelFileContextType.DEPENDENCY
