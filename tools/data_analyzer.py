from typing import Any, Dict, List
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from mcp.server import FastMCP
from .utils import workspace_path, get_headers

def add_tools(mcp: FastMCP):

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
