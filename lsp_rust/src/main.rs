mod bazel_file;
mod language_server;
mod utils;

use language_server::start_lsp;
use log::LevelFilter;
use log4rs::append::file::FileAppender;
use log4rs::config::{Appender, Config, Root};
use log4rs::encode::pattern::PatternEncoder;

#[tokio::main]
async fn main() {
    let filepath = "/tmp/rust_lsp.log";
    let pattern = "{d(%Y-%m-%d %H:%M:%S%.3f)} - {l} - {m}\n";

    let logfile = FileAppender::builder()
        .encoder(Box::new(PatternEncoder::new(pattern)))
        .build(filepath)
        .expect("Failed to create FileAppender");

    let config = Config::builder()
        .appender(Appender::builder().build("logfile", Box::new(logfile)))
        .build(
            Root::builder()
                .appender("logfile")
                .build(LevelFilter::Debug),
        )
        .expect("Failed to create logging configuration");

    log4rs::init_config(config).unwrap();

    start_lsp().await;
}
