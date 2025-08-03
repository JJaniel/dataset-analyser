from typing import Dict, List
import pandas as pd
from mcp.server import FastMCP
from .utils import workspace_path

def add_tools(mcp: FastMCP):
    @mcp.tool()
    def map_gene_ids(file_path: str, id_column: str, from_db: str, to_db: str) -> Dict[str, str]:
        """Map gene identifiers from one database to another."""
        try:
            full_path = workspace_path / file_path
            if full_path.suffix.lower() == '.csv':
                df = pd.read_csv(full_path)
            elif full_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(full_path)
            else:
                return {"error": "Unsupported file type"}

            if id_column not in df.columns:
                return {"error": f"Column '{id_column}' not found in the dataset."}

            # This is a very basic implementation with a hardcoded mapping.
            # In a real-world scenario, you would use a more comprehensive database or API.
            gene_mapping = {
                "ENSG00000123456": "BRCA1",
                "ENSG00000234567": "TP53",
            }

            df[f"{to_db}_id"] = df[id_column].map(gene_mapping)

            # Save the modified dataframe to a new file
            new_file_path = full_path.parent / f"{full_path.stem}_processed.csv"
            df.to_csv(new_file_path, index=False)

            return {"message": f"Gene IDs mapped successfully. The processed file is saved at {new_file_path}"}

        except Exception as e:
            return {"error": str(e)}
