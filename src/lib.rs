use fst::{IntoStreamer, Set, SetBuilder, Streamer};
use memmap2::Mmap;

use std::error::Error;
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader};

/// Creates an FST Set from a list of chemical names in a text file.
pub fn build_fst_set(input_path: &str, fst_path: &str) -> Result<(), Box<dyn Error>> {
    let file = File::open(input_path)?;
    let reader = BufReader::new(file);

    let mut names: Vec<String> = reader.lines().filter_map(Result::ok).collect();

    // The fst crate requires sorted input.
    names.sort_unstable();
    names.dedup();

    let wtr = File::create(fst_path)?;
    let mut builder = SetBuilder::new(wtr)?;

    for name in names {
        builder.insert(name)?;
    }

    builder.finish()?;
    Ok(())
}

/// Memory maps an FST set from disk.
pub fn load_fst_set(fst_path: &str) -> Result<Set<Mmap>, Box<dyn Error>> {
    let file = OpenOptions::new().read(true).open(fst_path)?;
    let mmap = unsafe { Mmap::map(&file)? };
    let set = Set::new(mmap)?;
    Ok(set)
}

/// Performs prefix-based autocomplete search.
pub fn prefix_search(set: &Set<Mmap>, prefix: &str, max_results: usize) -> Vec<String> {
    let mut results = Vec::new();
    let mut stream = set
        .range()
        .ge(prefix)
        .lt(format!("{}{}", prefix, char::MAX))
        .into_stream();
    
    while let Some(key) = stream.next() {
        if results.len() >= max_results {
            break;
        }
        if let Ok(s) = String::from_utf8(key.to_vec()) {
            results.push(s);
        }
    }
    
    results
}

/// Performs substring search using regex pattern matching on the FST set.
pub fn substring_search(
    set: &Set<Mmap>,
    substring: &str,
    max_results: usize,
) -> Result<Vec<String>, Box<dyn Error>> {
    // We'll do this manually instead of using fst-regex
    // No need for regex pattern as we're doing direct substring matching
    
    let mut results = Vec::new();
    let mut stream = set.stream().into_stream();
    
    while let Some(key) = stream.next() {
        if results.len() >= max_results {
            break;
        }
        
        if let Ok(s) = String::from_utf8(key.to_vec()) {
            // Manually check if the string contains our substring
            if s.to_lowercase().contains(&substring.to_lowercase()) {
                results.push(s);
            }
        }
    }
    
    Ok(results)
}