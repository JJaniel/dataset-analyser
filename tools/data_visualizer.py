import base64
from io import BytesIO
from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
from mcp.server import FastMCP
from .utils import workspace_path

def add_tools(mcp: FastMCP):
    @mcp.tool()
    def plot_histogram(file_path: str, column_name: str) -> Dict[str, str]:
        """Generate a histogram for a numeric column in a dataset."""
        try:
            full_path = workspace_path / file_path
            if full_path.suffix.lower() == '.csv':
                df = pd.read_csv(full_path)
            elif full_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(full_path)
            else:
                return {"error": "Unsupported file type"}

            if column_name not in df.columns:
                return {"error": f"Column '{column_name}' not found in the dataset."}

            if not pd.api.types.is_numeric_dtype(df[column_name]):
                return {"error": f"Column '{column_name}' is not numeric."}

            plt.figure()
            df[column_name].hist()
            plt.title(f"Histogram of {column_name}")
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            
            # Save the plot to a buffer and encode it as base64
            buf = BytesIO()
            plt.savefig(buf, format="png")
            plt.close()
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            return {"image": image_base64}

        except Exception as e:
            return {"error": str(e)}
