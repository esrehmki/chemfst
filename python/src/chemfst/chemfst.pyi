from typing import List, Optional

def build_fst(input_path: str, fst_path: str) -> None:
    """
    Creates an FST Set from a list of chemical names in a text file.

    Args:
        input_path: Path to a text file containing chemical names, one per line
        fst_path: Path where the FST index file will be saved

    Raises:
        FileNotFoundError: If the input file cannot be found
        RuntimeError: If there's an error building the FST
    """
    ...

class ChemicalFST:
    """
    ChemicalFST provides efficient searching of chemical names using Finite State Transducers.

    This class provides methods for prefix-based autocomplete and substring searching
    through large chemical name databases with high performance.
    """

    def __init__(self, fst_path: str) -> None:
        """
        Create a new ChemicalFST instance by loading an FST file.

        Args:
            fst_path: Path to the FST index file

        Raises:
            FileNotFoundError: If the FST file cannot be found
            RuntimeError: If there's an error loading the FST
        """
        ...

    def prefix_search(self, prefix: str, max_results: Optional[int] = None) -> List[str]:
        """
        Find chemical names starting with a specified prefix.

        Args:
            prefix: The prefix to search for
            max_results: Maximum number of results to return (default: 100)

        Returns:
            A list of chemical names that start with the given prefix
        """
        ...

    def substring_search(self, substring: str, max_results: Optional[int] = None) -> List[str]:
        """
        Find chemical names containing a specified substring.

        Args:
            substring: The substring to search for
            max_results: Maximum number of results to return (default: 100)

        Returns:
            A list of chemical names that contain the given substring

        Raises:
            RuntimeError: If there's an error during the search
        """
        ...

    def preload(self) -> int:
        """
        Forces the operating system to load all pages of the FST into memory.

        This function traverses the entire FST, causing all pages to be loaded into
        the operating system's page cache. This improves the performance of subsequent
        searches by eliminating page faults.

        Returns:
            The number of keys preloaded from the FST

        Raises:
            RuntimeError: If there's an error during preloading
        """
        ...

    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
