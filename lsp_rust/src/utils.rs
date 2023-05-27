use anyhow::Result;
use std::{fs::File, io::Read, path::Path};

pub fn read_file(path: &Path) -> Result<String> {
    let mut contents = String::new();
    let mut file = File::open(path)?;
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
