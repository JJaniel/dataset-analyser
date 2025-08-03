from typing import Dict
import pandas as pd
from mcp.server import FastMCP
from .utils import workspace_path

def add_tools(mcp: FastMCP):
    @mcp.tool()
    def create_interaction_terms(file_path: str, col1: str, col2: str) -> Dict[str, str]:
        """Create an interaction term between two numeric columns."""
        try:
            full_path = workspace_path / file_path
            if full_path.suffix.lower() == '.csv':
                df = pd.read_csv(full_path)
            elif full_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(full_path)
            else:
                return {"error": "Unsupported file type"}

            if col1 not in df.columns or col2 not in df.columns:
                return {"error": f"One or both columns not found in the dataset."}

            if not pd.api.types.is_numeric_dtype(df[col1]) or not pd.api.types.is_numeric_dtype(df[col2]):
                return {"error": f"One or both columns are not numeric."}

            df[f"{col1}*{col2}"] = df[col1] * df[col2]

            # Save the modified dataframe to a new file
            new_file_path = full_path.parent / f"{full_path.stem}_processed.csv"
            df.to_csv(new_file_path, index=False)

            return {"message": f"Interaction term created successfully. The processed file is saved at {new_file_path}"}

        except Exception as e:
            return {"error": str(e)}
