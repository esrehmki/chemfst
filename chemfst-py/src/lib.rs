use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::exceptions::{PyFileNotFoundError, PyRuntimeError};
use std::path::Path;
use memmap2::Mmap;
use fst::Set;

/// Python module for ChemFST: A high-performance chemical name search library using Finite State Transducers
#[pymodule]
fn chemfst(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ChemicalFST>()?;
    m.add_function(wrap_pyfunction!(build_fst, m)?)?;
    m.add("__doc__", "ChemFST Python bindings for high-performance chemical name searching using Finite State Transducers (FSTs).")?;
    Ok(())
}

/// Creates an FST Set from a list of chemical names in a text file.
///
/// Args:
///     input_path: Path to a text file containing chemical names, one per line
///     fst_path: Path where the FST index file will be saved
///
/// Returns:
///     None
///
/// Raises:
///     FileNotFoundError: If the input file cannot be found
///     RuntimeError: If there's an error building the FST
#[pyfunction]
fn build_fst(input_path: &str, fst_path: &str) -> PyResult<()> {
    if !Path::new(input_path).exists() {
        return Err(PyFileNotFoundError::new_err(format!(
            "Input file not found: {}",
            input_path
        )));
    }

    ::chemfst::build_fst_set(input_path, fst_path).map_err(|e| {
        PyRuntimeError::new_err(format!("Failed to build FST: {}", e))
    })
}

/// ChemicalFST provides efficient searching of chemical names using Finite State Transducers.
///
/// This class provides methods for prefix-based autocomplete and substring searching
/// through large chemical name databases with high performance.
#[pyclass(name = "ChemicalFST")]
struct ChemicalFST {
    set: Set<Mmap>,
}

#[pymethods]
impl ChemicalFST {
    /// Create a new ChemicalFST instance by loading an FST file.
    ///
    /// Args:
    ///     fst_path: Path to the FST index file
    ///
    /// Returns:
    ///     ChemicalFST: A new ChemicalFST instance
    ///
    /// Raises:
    ///     FileNotFoundError: If the FST file cannot be found
    ///     RuntimeError: If there's an error loading the FST
    #[new]
    fn new(fst_path: &str) -> PyResult<Self> {
        if !Path::new(fst_path).exists() {
            return Err(PyFileNotFoundError::new_err(format!(
                "FST file not found: {}",
                fst_path
            )));
        }

        let set = ::chemfst::load_fst_set(fst_path).map_err(|e| {
            PyRuntimeError::new_err(format!("Failed to load FST: {}", e))
        })?;

        Ok(Self { set })
    }

    /// Find chemical names starting with a specified prefix.
    ///
    /// Args:
    ///     prefix: The prefix to search for
    ///     max_results: Maximum number of results to return (default: 100)
    ///
    /// Returns:
    ///     list: A list of chemical names that start with the given prefix
    fn prefix_search(&self, prefix: &str, max_results: Option<usize>) -> Vec<String> {
        ::chemfst::prefix_search(&self.set, prefix, max_results.unwrap_or(100))
    }

    /// Find chemical names containing a specified substring.
    ///
    /// Args:
    ///     substring: The substring to search for
    ///     max_results: Maximum number of results to return (default: 100)
    ///
    /// Returns:
    ///     list: A list of chemical names that contain the given substring
    ///
    /// Raises:
    ///     RuntimeError: If there's an error during the search
    fn substring_search(&self, substring: &str, max_results: Option<usize>) -> PyResult<Vec<String>> {
        ::chemfst::substring_search(&self.set, substring, max_results.unwrap_or(100))
            .map_err(|e| PyRuntimeError::new_err(format!("Search error: {}", e)))
    }

    /// Return a string representation of the ChemicalFST instance.
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("ChemicalFST(loaded=True)"))
    }

    /// Return a string representation of the ChemicalFST instance.
    fn __str__(&self) -> PyResult<String> {
        Ok("ChemicalFST - Chemical name search engine using Finite State Transducers".to_string())
    }

    /// Forces the operating system to load all pages of the FST into memory.
    ///
    /// This function traverses the entire FST, causing all pages to be loaded into
    /// the operating system's page cache. This improves the performance of subsequent
    /// searches by eliminating page faults.
    ///
    /// Args:
    ///     None
    ///
    /// Returns:
    ///     int: The number of keys preloaded from the FST
    ///
    /// Raises:
    ///     RuntimeError: If there's an error during preloading
    fn preload(&self) -> PyResult<usize> {
        ::chemfst::preload_fst_set(&self.set)
            .map_err(|e| PyRuntimeError::new_err(format!("Preload error: {}", e)))
    }
}
