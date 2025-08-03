import json
from typing import Any, Dict
import pandas as pd
from mcp.server import FastMCP
from .utils import workspace_path

def add_tools(mcp: FastMCP):
    @mcp.tool()
    def execute_code(file_path: str, code: str) -> Any:
        """Execute arbitrary python code on a dataset. The dataframe is available as `df`."""
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

    @mcp.tool()
    def handle_missing_values(file_path: str, strategy: str = 'mean', value: Any = None) -> Dict[str, Any]:
        """Handle missing values in a dataset."""
        try:
            full_path = workspace_path / file_path
            if full_path.suffix.lower() == '.csv':
                df = pd.read_csv(full_path)
            elif full_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(full_path)
            else:
                return {"error": "Unsupported file type"}

            if strategy == 'mean':
                df.fillna(df.mean(numeric_only=True), inplace=True)
            elif strategy == 'median':
                df.fillna(df.median(numeric_only=True), inplace=True)
            elif strategy == 'mode':
                df.fillna(df.mode().iloc[0], inplace=True)
            elif strategy == 'constant':
                if value is None:
                    return {"error": "Please provide a value for the 'constant' strategy."}
                df.fillna(value, inplace=True)
            else:
                return {"error": f"Invalid strategy: {strategy}"}

            # Save the modified dataframe to a new file
            new_file_path = full_path.parent / f"{full_path.stem}_processed.csv"
            df.to_csv(new_file_path, index=False)

            return {"message": f"Missing values handled successfully. The processed file is saved at {new_file_path}"}

        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def remove_duplicates(file_path: str) -> Dict[str, Any]:
        """Remove duplicate rows from a dataset."""
        try:
            full_path = workspace_path / file_path
            if full_path.suffix.lower() == '.csv':
                df = pd.read_csv(full_path)
            elif full_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(full_path)
            else:
                return {"error": "Unsupported file type"}

            df.drop_duplicates(inplace=True)

            # Save the modified dataframe to a new file
            new_file_path = full_path.parent / f"{full_path.stem}_processed.csv"
            df.to_csv(new_file_path, index=False)

            return {"message": f"Duplicates removed successfully. The processed file is saved at {new_file_path}"}

        except Exception as e:
            return {"error": str(e)}
