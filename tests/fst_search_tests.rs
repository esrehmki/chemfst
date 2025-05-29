use fast_search::{build_fst_set, load_fst_set, prefix_search, substring_search};
use std::io::Write;
use std::path::PathBuf;
use tempfile::NamedTempFile;

// Helper function to create test data files
fn create_test_data() -> (PathBuf, PathBuf) {
    // Create a temporary file for input data
    let mut input_file = NamedTempFile::new().unwrap();
    writeln!(input_file, "acetone").unwrap();
    writeln!(input_file, "acetaminophen").unwrap();
    writeln!(input_file, "benzene").unwrap();
    writeln!(input_file, "benzaldehyde").unwrap();
    writeln!(input_file, "chloroform").unwrap();
    writeln!(input_file, "methanol").unwrap();

    let input_path = input_file.path().to_path_buf();

    // Create a temporary file for the FST
    let fst_file = NamedTempFile::new().unwrap();
    let fst_path = fst_file.path().to_path_buf();

    // Don't close the files yet to keep them alive
    std::mem::forget(input_file);
    std::mem::forget(fst_file);

    (input_path, fst_path)
}

#[test]
fn test_build_and_load_fst() {
    let (input_path, fst_path) = create_test_data();

    // Build the FST set
    let result = build_fst_set(input_path.to_str().unwrap(), fst_path.to_str().unwrap());
    assert!(result.is_ok());

    // Load the FST set
    let set_result = load_fst_set(fst_path.to_str().unwrap());
    assert!(set_result.is_ok());
}

#[test]
fn test_prefix_search() {
    let (input_path, fst_path) = create_test_data();

    // Build the FST set
    build_fst_set(input_path.to_str().unwrap(), fst_path.to_str().unwrap()).unwrap();

    // Load the FST set
    let set = load_fst_set(fst_path.to_str().unwrap()).unwrap();

    // Test prefix search
    let results = prefix_search(&set, "acet", 10);
    assert_eq!(results.len(), 2);
    assert!(results.contains(&"acetone".to_string()));
    assert!(results.contains(&"acetaminophen".to_string()));

    // Test prefix with no matches
    let empty_results = prefix_search(&set, "xyz", 10);
    assert_eq!(empty_results.len(), 0);

    // Test limit
    let limited_results = prefix_search(&set, "a", 1);
    assert_eq!(limited_results.len(), 1);
}

#[test]
fn test_substring_search() {
    let (input_path, fst_path) = create_test_data();

    // Build the FST set
    build_fst_set(input_path.to_str().unwrap(), fst_path.to_str().unwrap()).unwrap();

    // Load the FST set
    let set = load_fst_set(fst_path.to_str().unwrap()).unwrap();

    // Test substring search
    let results = substring_search(&set, "enz", 10).unwrap();
    assert_eq!(results.len(), 2);
    assert!(results.contains(&"benzene".to_string()));
    assert!(results.contains(&"benzaldehyde".to_string()));

    // Test substring with no matches
    let empty_results = substring_search(&set, "xyz", 10).unwrap();
    assert_eq!(empty_results.len(), 0);

    // Test case insensitivity
    let case_results = substring_search(&set, "BENZ", 10).unwrap();
    assert_eq!(case_results.len(), 2);

    // Test limit
    let limited_results = substring_search(&set, "e", 2).unwrap();
    assert_eq!(limited_results.len(), 2);
}
