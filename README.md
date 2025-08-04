# Dataset Analyzer MCP

This project is a Model Context Protocol (MCP) server designed for intelligent dataset analysis. It provides a suite of tools to help you understand, clean, and process your datasets, with a special focus on biomedical data.

## Features

*   **Dataset Exploration:** Get comprehensive information about your datasets, including column names, data types, missing values, and summary statistics.
*   **Data Visualization:** Generate histograms to visualize the distribution of numeric columns.
*   **Data Cleaning:** Handle missing values and remove duplicate rows.
*   **Feature Engineering:** Create new features from existing ones, such as interaction terms.
*   **Biomedical Tools:** Map gene identifiers between different databases.
*   **Code Execution:** Execute arbitrary Python code on your datasets.

## Getting Started

1.  **Installation:**

    ```bash
    uv run pip install -r requirements.txt
    uv run mcp install main.py
    ```

2.  **Usage:**

    Once the MCP server is installed, you can interact with it through the Claude desktop app or any other MCP-compatible client.

## Tools

### Data Loader

*   `list_datasets()`: List all available datasets.
*   `get_data_sample(file_path: str, n_rows: int = 5)`: Get a small sample of a dataset.

### Data Analyzer

*   `get_dataset_info(file_path: str)`: Get comprehensive information about a dataset.
*   `find_similar_columns(target_column: str, threshold: int = 80)`: Find similar column names across all datasets.
*   `get_column_patterns()`: Identify column patterns and potential matches from headers.

### Data Visualizer

*   `plot_histogram(file_path: str, column_name: str)`: Generate a histogram for a numeric column.

### Data Preprocessor

*   `execute_code(file_path: str, code: str)`: Execute arbitrary Python code on a dataset.
*   `handle_missing_values(file_path: str, strategy: str = 'mean', value: Any = None)`: Handle missing values in a dataset.
*   `remove_duplicates(file_path: str)`: Remove duplicate rows from a dataset.

### Feature Engineer

*   `create_interaction_terms(file_path: str, col1: str, col2: str)`: Create an interaction term between two numeric columns.

### Biomedical Tools

*   `map_gene_ids(file_path: str, id_column: str, from_db: str, to_db: str)`: Map gene identifiers from one database to another.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.