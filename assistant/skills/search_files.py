import os
import fnmatch
from typing import Optional

from assistant.skills.decorator import skill

# Map natural names to absolute folder paths
KNOWN_FOLDERS = {
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
}

def resolve_directory(name: Optional[str]) -> str:
    if name is None:
        return os.path.expanduser("~")  # default: user home
    name = name.strip().lower()
    return KNOWN_FOLDERS.get(name, name)  # use mapped folder or raw path

@skill
def search_files(
    query: str,
    directory: Optional[str] = None,
    file_type: Optional[str] = None,
    max_results: int = 10,
    recursive: bool = True
) -> list[str]:
    """
    Searches for files matching the query within a specified directory.

    Args:
        query (str): Keyword or partial filename to search for.
        directory (Optional[str]): Folder name or path to search in. Defaults to user home.
        file_type (Optional[str]): Limit to files with a given extension (e.g., 'pdf').
        max_results (int): Maximum number of file paths to return.
        recursive (bool): Whether to search subdirectories recursively.

    Returns:
        list[str]: List of file paths matching the query.
    """
    dir_path = resolve_directory(directory)
    if not os.path.isdir(dir_path):
        print("Assistant: Found no such file.")
        return []

    results = []
    query = query.lower()

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if query in file.lower():
                if file_type and not fnmatch.fnmatch(file.lower(), f"*.{file_type.lower()}"):
                    continue
                full_path = os.path.join(root, file)
                results.append(full_path)
                if len(results) >= max_results:
                    print(f"Assistant: Here are the results {results}", results)
                    return results
        if not recursive:
            break

    print(f"Assistant: Here are the results {results}", results)
    return results
