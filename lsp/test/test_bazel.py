import bazel

bzl_contents = """
load("@rules_cc//cc:defs.bzl", "cc_binary", "cc_library")

cc_library(
    name = "hello-greet",
    srcs = ["hello-greet.cc"],
    hdrs = ["hello-greet.h"],
)

cc_binary(
    name = "hello-world",
    srcs = ["hello-world.cc"],
    deps = [
        ":hello-greet",
        "//lib:hello-time",
    ],
)
"""


def test_answer():
    file = bazel.BazelFile(bzl_contents)
    context = file.get_context(5, 15)
    assert context.type == bazel.BazelFileContextType.FILE
