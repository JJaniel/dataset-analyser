from mcp.server import FastMCP
from tools import data_loader, data_analyzer, data_preprocessor, data_visualizer, feature_engineer, biomedical_tools

# Create an MCP server instance
mcp = FastMCP(
    "dataset-analyzer",
    "A tool for analyzing datasets and finding similar columns.",
)

# Add tools from the different modules
data_loader.add_tools(mcp)
data_analyzer.add_tools(mcp)
data_preprocessor.add_tools(mcp)
data_visualizer.add_tools(mcp)
feature_engineer.add_tools(mcp)
biomedical_tools.add_tools(mcp)

if __name__ == "__main__":
    mcp.run()