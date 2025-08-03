import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from mcp.server import FastMCP

# Create an MCP server instance
mcp = FastMCP(
    "dataset-analyzer",
    "A tool for analyzing datasets and finding similar columns.",
)

workspace_path = Path("datasets")
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

@mcp.tool()
def get_dataset_info(file_path: str) -> Dict[str, Any]:
    """Get comprehensive dataset information efficiently."""
    try:
        full_path = workspace_path / file_path
        if not full_path.is_absolute():
            full_path = workspace_path / file_path

        if full_path.suffix.lower() not in ['.csv', '.xlsx', '.xls']:
                return {"error": "Unsupported file type"}

        # Get basic info from headers
        headers = get_headers(str(file_path))
        if headers is None:
            return {"error": "Could not load dataset headers"}

        info = {
            "file_path": str(file_path),
            "columns": headers,
        }

        # For detailed info, we need to iterate
        if full_path.suffix.lower() == '.csv':
            chunk_iter = pd.read_csv(full_path, chunksize=10000, iterator=True)
        else: # excel
            chunk_iter = iter([pd.read_excel(full_path)])

        row_count = 0
        total_memory_usage = 0
        null_counts = pd.Series()
        duplicated_rows = 0
        
        # Process in chunks for memory efficiency
        for chunk in chunk_iter:
            row_count += len(chunk)
            total_memory_usage += chunk.memory_usage(deep=True).sum()
            if null_counts.empty:
                null_counts = chunk.isnull().sum()
            else:
                null_counts += chunk.isnull().sum()
            duplicated_rows += chunk.duplicated().sum()

        info["shape"] = (row_count, len(headers))
        info["memory_usage"] = int(total_memory_usage)
        info["null_counts"] = null_counts.to_dict()
        info["null_percentages"] = (null_counts / row_count * 100).round(2).to_dict()
        info["duplicated_rows"] = int(duplicated_rows)
        info["dtypes"] = chunk.dtypes.astype(str).to_dict() # Dtypes from the last chunk

        # For summary stats, we can take a sample to be efficient
        sample_df = pd.read_csv(full_path, n_rows=1000) if full_path.suffix.lower() == '.csv' else pd.read_excel(full_path, n_rows=1000)
        numeric_cols = sample_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            info["numeric_summary"] = sample_df[numeric_cols].describe().to_dict()
        
        categorical_cols = sample_df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            info["categorical_summary"] = {
                col: {
                    "unique_count": int(sample_df[col].nunique()),
                    "top_values": sample_df[col].value_counts().head(5).to_dict()
                }
                for col in categorical_cols
            }

        return info

    except Exception as e:
        return {"error": f"An error occurred: {e}"}

@mcp.tool()
def get_data_sample(file_path: str, n_rows: int = 5) -> Dict[str, Any]:
    """Get a small sample of the dataset."""
    try:
        full_path = workspace_path / file_path
        if not full_path.is_absolute():
            full_path = workspace_path / file_path
        
        if full_path.suffix.lower() == '.csv':
            df_sample = pd.read_csv(full_path, nrows=n_rows)
            return df_sample.to_dict(orient='records')
        elif full_path.suffix.lower() in ['.xlsx', '.xls']:
            df_sample = pd.read_excel(full_path, nrows=n_rows)
            return df_sample.to_dict(orient='records')
        return {"error": "Unsupported file type"}
    except Exception as e:
        return {"error": f"Error loading sample from {file_path}: {e}"}

@mcp.tool()
def find_similar_columns(target_column: str, threshold: int = 80) -> List[Dict[str, Any]]:
    """Find similar column names across all datasets by only reading headers."""
    all_columns = []
    
    for dataset_path in workspace_path.glob("**/*.csv"):
        if dataset_path.is_file():
            dataset_name = dataset_path.name
            headers = get_headers(str(dataset_path))
            if headers:
                for col in headers:
                    all_columns.append({
                        "dataset": dataset_name,
                        "column": col,
                        "full_path": str(dataset_path)
                    })
    
    similar_columns = []
    for col_info in all_columns:
        similarity = fuzz.ratio(target_column.lower(), col_info["column"].lower())
        if similarity >= threshold:
            col_info["similarity_score"] = similarity
            similar_columns.append(col_info)
    
    similar_columns.sort(key=lambda x: x["similarity_score"], reverse=True)
    return similar_columns

@mcp.tool()
def get_column_patterns() -> Dict[str, List[Dict[str, Any]]]:
    """Identify column patterns and potential matches from headers."""
    patterns = {}
    pattern_mappings = {
        "cell_line": ["cell_line", "cellline", "cell_line_name", "cell_line_id", "cellline_name", "cell"],
        "drug": ["drug", "compound", "treatment", "agent", "drug_name", "compound_name", "name"],
        "dose": ["dose", "concentration", "dosage", "amount", "conc", "ic50", "ec50"],
        "time": ["time", "duration", "hours", "days", "timepoint", "time_point"],
        "viability": ["viability", "response", "effect", "inhibition", "survival", "auc"],
        "gene": ["gene", "gene_symbol", "gene_name", "target", "gene_id", "symbol"],
        "expression": ["expression", "fpkm", "tpm", "counts", "read_count", "value"]
    }
    
    for dataset_path in workspace_path.glob("**/*.csv"):
        if dataset_path.is_file():
            dataset_name = dataset_path.name
            headers = get_headers(str(dataset_path))
            if headers:
                for col in headers:
                    for pattern, variants in pattern_mappings.items():
                        for variant in variants:
                            similarity = fuzz.ratio(variant.lower(), col.lower())
                            if similarity >= 70:
                                if pattern not in patterns:
                                    patterns[pattern] = []
                                patterns[pattern].append({
                                    "dataset": dataset_name,
                                    "column": col,
                                    "similarity": similarity
                                })
    return patterns

@mcp.tool()
def list_datasets() -> List[str]:
    """List all available datasets."""
    datasets = []
    for dataset_path in workspace_path.glob("**/*.csv"):
        if dataset_path.is_file():
            datasets.append(str(dataset_path.name))
    return datasets

@mcp.tool()
def execute_pandas_code(file_path: str, code: str) -> Any:
    """Execute arbitrary pandas code on a dataset. The dataframe is available as `df`."""
    try:
        # Load the full dataset for execution
        full_path = workspace_path / file_path
        if full_path.suffix.lower() == '.csv':
            df = pd.read_csv(full_path)
        elif full_path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(full_path)
        else:
            return {"error": "Unsupported file type"}

        # Execute the code
        # Make a copy so the original df is not modified in the exec context
        exec_globals = {"df": df.copy(), "pd": pd}
        exec(code, exec_globals)
        
        # The result of the execution should be in a variable named `result`
        result = exec_globals.get("result", "Code executed, but no `result` variable was found.")
        
        # Convert result to JSON
        if isinstance(result, (pd.DataFrame, pd.Series)):
            return json.loads(result.to_json(orient='records', default_handler=str))
        else:
            return result

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
