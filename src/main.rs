use chemfst::{build_fst_set, load_fst_set, prefix_search, substring_search};
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input_path = "chemical_names.txt";
    let fst_path = "chemical_names.fst";

    // Step 1: Create the index (do this weekly after updates).
    build_fst_set(input_path, fst_path)?;
    println!("FST index built and saved to disk.");

    // Step 2: Load memory-mapped index.
    let set = load_fst_set(fst_path)?;
    println!("FST index loaded into memory.");

    // Example prefix search
    let prefix = "acet";
    let prefix_results = prefix_search(&set, prefix, 10);
    println!("Prefix search results for '{}':", prefix);
    for name in prefix_results {
        println!("  {}", name);
    }

    // Example substring search
    let substring = "benz";
    let substring_results = substring_search(&set, substring, 10)?;
    println!("Substring search results for '{}':", substring);
    for name in substring_results {
        println!("  {}", name);
    }

    Ok(())
}