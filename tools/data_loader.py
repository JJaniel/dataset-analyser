from typing import Any, Dict, List
import pandas as pd
from mcp.server import FastMCP
from .utils import workspace_path

def add_tools(mcp: FastMCP):
    @mcp.tool()
    def list_datasets() -> List[str]:
        """List all available datasets."""
        datasets = []
        for dataset_path in workspace_path.glob("**/*.csv"):
            if dataset_path.is_file():
                datasets.append(str(dataset_path.name))
        return datasets

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
