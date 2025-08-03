# Dataset Analyzer MCP Server

An MCP server that provides intelligent dataset analysis capabilities including:
- Dataset information (shape, columns, null values, statistics)
- Similar column detection across datasets
- Column pattern recognition
- Dataset listing

## Features

1. **Dataset Information**: Get comprehensive details about any CSV or Excel file including shape, columns, data types, null value counts, and statistical summaries.

2. **Similar Column Detection**: Find similar column names across all datasets using fuzzy string matching, helpful when columns represent the same data but have different names.

3. **Column Pattern Recognition**: Identify common data patterns (like cell_line, drug, dose, etc.) even when they have different column names.

4. **Dataset Listing**: List all available CSV datasets in your workspace.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run python main.py
```

The server communicates over stdio and provides the following tools:

- `get_dataset_info`: Get comprehensive information about a dataset
- `find_similar_columns`: Find similar column names across datasets
- `get_column_patterns`: Identify column patterns and potential matches
- `list_datasets`: List all available datasets in the workspace