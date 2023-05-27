use anyhow::Result;

use rustpython_parser::ast::Mod;
use rustpython_parser::parser::{parse, Mode::Module};
use rustpython_parser::visitor::Visitor;

pub struct BazelFile {
    root_node: Mod,
}

impl BazelFile {
    pub fn new(contents: String) -> Result<BazelFile> {
        let root_node = parse(&contents, Module, "")?;
        dbg!(&root_node);
        Ok(BazelFile { root_node })
    }

    pub fn get_context(self, row: i32, column: i32) -> Result<String> {
        Ok("".to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn get_example_bazel_file() -> String {
        return r#"                              # Line 0
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
)"#
        .to_string();
    }

    #[test]
    fn test_my_function() -> anyhow::Result<()> {
        let file = BazelFile::new(get_example_bazel_file())?;
        assert_eq!(file.get_context(4, 28)?, "hello-greet");
        Ok(())
    }
}
