import os
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

# Use environment variable for datasets directory, with a default
datasets_dir = os.environ.get("DATASETS_DIR", "datasets")
workspace_path = Path(datasets_dir)
# Caching just the headers to save memory
headers_cache: Dict[str, List[str]] = {}

def get_headers(file_path: str) -> Optional[List[str]]:
    """Get headers of a CSV or Excel file without loading the whole file."""
    if file_path in headers_cache:
        return headers_cache[file_path]
    
    try:
        full_path = workspace_path / file_path
        if not full_path.is_absolute():
            full_path = workspace_path / file_path

        if full_path.suffix.lower() == '.csv':
            df_header = pd.read_csv(full_path, nrows=0)
            headers_cache[file_path] = list(df_header.columns)
            return list(df_header.columns)
        elif full_path.suffix.lower() in ['.xlsx', '.xls']:
            df_header = pd.read_excel(full_path, nrows=0)
            headers_cache[file_path] = list(df_header.columns)
            return list(df_header.columns)
        return None
    except Exception as e:
        print(f"Error loading headers for {file_path}: {e}")
        return None
