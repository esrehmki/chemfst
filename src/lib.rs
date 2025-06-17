//! # `ChemFST`
//!
//! `ChemFST` is a high-performance chemical name search library using Finite State Transducers (FSTs)
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
//!     let input_path = "data/chemical_names.txt";
//!     let fst_path = "data/chemical_names.fst";
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
//!     let substring_results = substring_search(&set, "enz", 10)?;
//!     println!("Found {} chemicals containing 'enz'", substring_results.len());
//!
//!     Ok(())
//! }
//! ```

use fst::{IntoStreamer, Set, SetBuilder, Streamer};
use log::{debug, error, info};
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
/// # Errors
///
/// This function will return an error if:
/// * The input file cannot be found or read
/// * The output file cannot be created or written to
/// * There is an issue building the FST index
///
/// # Example
///
/// ```no_run
/// use chemfst::build_fst_set;
///
/// let result = build_fst_set("data/chemical_names.txt", "data/chemical_names.fst");
/// assert!(result.is_ok());
/// ```
pub fn build_fst_set(input_path: &str, fst_path: &str) -> Result<(), Box<dyn Error>> {
    info!("Building FST from input file: {}", input_path);
    debug!("Output FST file: {}", fst_path);

    let file = File::open(input_path).map_err(|e| {
        error!("Failed to open input file '{}': {}", input_path, e);
        e
    })?;
    let reader = BufReader::new(file);

    let mut names: Vec<String> = reader.lines().filter_map(Result::ok).collect();
    info!("Read {} chemical names from input file", names.len());

    // The fst crate requires sorted input.
    debug!("Sorting and deduplicating chemical names");
    names.sort_unstable();
    let original_count = names.len();
    names.dedup();
    let deduplicated_count = names.len();

    if original_count != deduplicated_count {
        info!(
            "Removed {} duplicate entries, {} unique names remaining",
            original_count - deduplicated_count,
            deduplicated_count
        );
    }

    debug!("Creating FST builder");
    let wtr = File::create(fst_path).map_err(|e| {
        error!("Failed to create output file '{}': {}", fst_path, e);
        e
    })?;
    let mut builder = SetBuilder::new(wtr)?;

    debug!("Inserting {} names into FST", names.len());
    for (i, name) in names.iter().enumerate() {
        if i > 0 && i % 10000 == 0 {
            debug!("Inserted {} / {} names", i, names.len());
        }
        builder.insert(name)?;
    }

    debug!("Finalizing FST");
    builder.finish()?;
    info!(
        "Successfully built FST with {} entries at: {}",
        deduplicated_count, fst_path
    );
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
/// # Errors
///
/// This function will return an error if:
/// * The FST file cannot be found or opened
/// * The file cannot be memory-mapped
/// * The file is not a valid FST index
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
/// build_fst_set("data/chemical_names.txt", "data/chemical_names.fst").unwrap();
///
/// // Then load it
/// let set = load_fst_set("data/chemical_names.fst").unwrap();
/// ```
pub fn load_fst_set(fst_path: &str) -> Result<Set<Mmap>, Box<dyn Error>> {
    info!("Loading FST from: {}", fst_path);

    let file = OpenOptions::new().read(true).open(fst_path).map_err(|e| {
        error!("Failed to open FST file '{}': {}", fst_path, e);
        e
    })?;

    debug!("Memory mapping FST file");
    let mmap = unsafe {
        Mmap::map(&file).map_err(|e| {
            error!("Failed to memory map FST file '{}': {}", fst_path, e);
            e
        })?
    };

    debug!("Creating FST set from memory map");
    let set = Set::new(mmap).map_err(|e| {
        error!("Failed to create FST set from file '{}': {}", fst_path, e);
        e
    })?;

    info!("Successfully loaded FST from: {}", fst_path);
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
/// let set = load_fst_set("data/chemical_names.fst").unwrap();
/// let results = prefix_search(&set, "acet", 10);
/// for chemical in results {
///     println!("Found: {}", chemical);
/// }
/// ```
#[must_use]
pub fn prefix_search(set: &Set<Mmap>, prefix: &str, max_results: usize) -> Vec<String> {
    debug!(
        "Starting prefix search for '{}' with max_results={}",
        prefix, max_results
    );

    let mut results = Vec::new();
    let mut stream = set
        .range()
        .ge(prefix)
        .lt(format!("{}{}", prefix, char::MAX))
        .into_stream();

    let mut checked_count = 0;
    while let Some(key) = stream.next() {
        checked_count += 1;
        if results.len() >= max_results {
            debug!("Reached max_results limit of {}", max_results);
            break;
        }
        if let Ok(s) = String::from_utf8(key.to_vec()) {
            debug!("Found match: {}", s);
            results.push(s);
        }
    }

    info!(
        "Prefix search for '{}' found {} results (checked {} entries)",
        prefix,
        results.len(),
        checked_count
    );
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
/// # Errors
///
/// This function will return an error if:
/// * There's an issue with UTF-8 encoding while processing strings
///
/// # Example
///
/// ```no_run
/// use chemfst::{load_fst_set, substring_search};
///
/// let set = load_fst_set("data/chemical_names.fst").unwrap();
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
    debug!(
        "Starting substring search for '{}' with max_results={}",
        substring, max_results
    );

    // We'll do this manually instead of using fst-regex
    // No need for regex pattern as we're doing direct substring matching
    let substring_lower = substring.to_lowercase();

    let mut results = Vec::new();
    let mut stream = set.stream().into_stream();
    let mut checked_count = 0;

    while let Some(key) = stream.next() {
        checked_count += 1;
        if checked_count % 10000 == 0 {
            debug!(
                "Checked {} entries, found {} matches so far",
                checked_count,
                results.len()
            );
        }

        if results.len() >= max_results {
            debug!("Reached max_results limit of {}", max_results);
            break;
        }

        if let Ok(s) = String::from_utf8(key.to_vec()) {
            // Manually check if the string contains our substring
            if s.to_lowercase().contains(&substring_lower) {
                debug!("Found match: {}", s);
                results.push(s);
            }
        }
    }

    info!(
        "Substring search for '{}' found {} results (checked {} entries)",
        substring,
        results.len(),
        checked_count
    );
    Ok(results)
}

/// Forces the operating system to load all pages of the FST into memory.
///
/// This function traverses the entire FST, causing all pages of the memory-mapped file
/// to be loaded into the operating system's page cache. This can significantly improve
/// the performance of subsequent searches by eliminating page faults.
///
/// # Arguments
///
/// * `set` - The FST Set to preload
///
/// # Returns
///
/// * `Ok(usize)` - The number of keys preloaded from the FST
/// * `Err(Box<dyn Error>)` if an error occurs during preloading
///
/// # Errors
///
/// This function will return an error if:
/// * There's an issue with iterating through the FST entries
///
/// # Example
///
/// ```no_run
/// use chemfst::{load_fst_set, preload_fst_set};
///
/// let set = load_fst_set("data/chemical_names.fst").unwrap();
/// let count = preload_fst_set(&set).unwrap();
/// println!("Preloaded {} chemical names into memory", count);
/// ```
pub fn preload_fst_set(set: &Set<Mmap>) -> Result<usize, Box<dyn Error>> {
    info!("Starting FST preload to load all pages into memory");

    // Force the OS to load parts of the FST into memory by performing a traversal
    let mut stream = set.stream().into_stream();
    let mut count = 0;

    // Just iterate through the set to touch all pages
    while stream.next().is_some() {
        count += 1;
        if count % 10000 == 0 {
            debug!("Preloaded {} entries", count);
        }
    }

    info!("Successfully preloaded {} entries into memory", count);
    Ok(count)
}
