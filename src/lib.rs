//! # ChemFST
//!
//! ChemFST is a high-performance chemical name search library using Finite State Transducers (FSTs)
//! to provide efficient searches of systematic and trivial names of chemical compounds in milliseconds.
//! It's particularly useful for autocomplete features and searching through large chemical databases.
//!
//! ## Features
//!
//! - Memory-efficient indexing using Finite State Transducers
//! - Extremely fast prefix-based searches (autocomplete)
//! - Case-insensitive substring searches
//! - Memory-mapped file access for optimal performance
//!
//! ## Example
//!
//! ```rust,no_run
//! use chemfst::{build_fst_set, load_fst_set, prefix_search, substring_search};
//! use std::error::Error;
//!
//! fn main() -> Result<(), Box<dyn Error>> {
//!     // Build an FST index from a list of chemical names
//!     let input_path = "chemical_names.txt";
//!     let fst_path = "chemical_names.fst";
//!     build_fst_set(input_path, fst_path)?;
//!
//!     // Load the index into memory efficiently
//!     let set = load_fst_set(fst_path)?;
//!
//!     // Perform prefix search (autocomplete)
//!     let prefix_results = prefix_search(&set, "acet", 10);
//!     println!("Found {} chemicals starting with 'acet'", prefix_results.len());
//!
//!     // Perform substring search
//!     let substring_results = substring_search(&set, "benz", 10)?;
//!     println!("Found {} chemicals containing 'benz'", substring_results.len());
//!
//!     Ok(())
//! }
//! ```

use fst::{IntoStreamer, Set, SetBuilder, Streamer};
use memmap2::Mmap;

use std::error::Error;
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader};

/// Creates an FST Set from a list of chemical names in a text file.
///
/// This function reads chemical names from a text file (one name per line), sorts them
/// (as required by the FST data structure), and builds an FST set index. The
/// index is saved to disk at the specified path.
///
/// # Arguments
///
/// * `input_path` - Path to a text file containing chemical names, one per line
/// * `fst_path` - Path where the FST index file will be saved
///
/// # Returns
///
/// * `Ok(())` on success
/// * `Err(Box<dyn Error>)` if an error occurs during file operations or index building
///
/// # Example
///
/// ```no_run
/// use chemfst::build_fst_set;
/// 
/// let result = build_fst_set("chemical_names.txt", "chemical_names.fst");
/// assert!(result.is_ok());
/// ```
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
///
/// This function loads an FST set from disk using memory mapping, which provides
/// efficient access to the index without loading the entire file into memory.
///
/// # Arguments
///
/// * `fst_path` - Path to the FST index file
///
/// # Returns
///
/// * `Ok(Set<Mmap>)` - The memory-mapped FST set
/// * `Err(Box<dyn Error>)` if the file cannot be opened or mapped
///
/// # Safety
///
/// This function uses `unsafe` to create a memory map of the file. It's safe as long as
/// the file is not modified while the memory map is active.
///
/// # Example
///
/// ```no_run
/// use chemfst::{build_fst_set, load_fst_set};
/// 
/// // First build the index
/// build_fst_set("chemical_names.txt", "chemical_names.fst").unwrap();
/// 
/// // Then load it
/// let set = load_fst_set("chemical_names.fst").unwrap();
/// ```
pub fn load_fst_set(fst_path: &str) -> Result<Set<Mmap>, Box<dyn Error>> {
    let file = OpenOptions::new().read(true).open(fst_path)?;
    let mmap = unsafe { Mmap::map(&file)? };
    let set = Set::new(mmap)?;
    Ok(set)
}

/// Performs prefix-based autocomplete search.
///
/// This function efficiently finds all chemical names in the FST set that start with the given prefix,
/// up to a specified maximum number of results.
///
/// # Arguments
///
/// * `set` - The FST Set to search in
/// * `prefix` - The prefix to search for
/// * `max_results` - Maximum number of results to return
///
/// # Returns
///
/// A vector of strings containing the matching chemical names
///
/// # Example
///
/// ```no_run
/// use chemfst::{load_fst_set, prefix_search};
/// 
/// let set = load_fst_set("chemical_names.fst").unwrap();
/// let results = prefix_search(&set, "acet", 10);
/// for chemical in results {
///     println!("Found: {}", chemical);
/// }
/// ```
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

/// Performs substring search using pattern matching on the FST set.
///
/// This function finds all chemical names in the FST set that contain the given substring,
/// up to a specified maximum number of results. The search is case-insensitive.
///
/// # Arguments
///
/// * `set` - The FST Set to search in
/// * `substring` - The substring to search for
/// * `max_results` - Maximum number of results to return
///
/// # Returns
///
/// * `Ok(Vec<String>)` - A vector of strings containing the matching chemical names
/// * `Err(Box<dyn Error>)` if an error occurs during search
///
/// # Example
///
/// ```no_run
/// use chemfst::{load_fst_set, substring_search};
/// 
/// let set = load_fst_set("chemical_names.fst").unwrap();
/// let results = substring_search(&set, "benz", 10).unwrap();
/// for chemical in results {
///     println!("Found: {}", chemical);
/// }
/// ```
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