import asyncio
import sys
from pathlib import Path

# Add the current directory to the path so we can import main
sys.path.insert(0, str(Path(__file__).parent))

try:
    import main
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()