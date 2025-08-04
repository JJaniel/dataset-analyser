# Dataset Analyzer MCP

<div align="center">

*Author: JJaniel*
*License: MIT*
*Contact: [GitHub Issues](https://github.com/JJaniel/dataset-analyser/issues)*

</div>

---


This project is a Model Context Protocol (MCP) server designed for intelligent dataset analysis. It provides a suite of tools to help you understand, clean, and process your datasets.

See the [NEWS.md](NEWS.md) file for a log of project updates.

## How to Use This Project

This guide will walk you through setting up and running the Dataset Analyzer MCP server on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed on your system:
*   **Git:** [https://git-scm.com/downloads](https://git-scm.com/downloads)
*   **Python:** (Version 3.8 or higher) [https://www.python.org/downloads/](https://www.python.org/downloads/)
*   **uv:** (A fast Python package installer) You can install it with `pip`:
    ```bash
    pip install uv
    ```

---

### Part 1: For a User (Running the Project)

Follow these steps if you just want to use the server to analyze your own datasets.

**Step 1: Get the Code**

Clone the repository to your local machine using `git`. Open your terminal or command prompt and run:

```bash
# Use this command for HTTPS (easiest)
git clone https://github.com/JJaniel/dataset-analyser.git

# Or use this command for SSH (if you have SSH keys set up with GitHub)
git clone git@github.com:JJaniel/dataset-analyser.git
```
This will create a new folder named `dataset-analyser`. Navigate into it:
```bash
cd dataset-analyser
```

**Step 2: Set Up the Python Environment**

It's best practice to create a virtual environment to keep project dependencies isolated.

```bash
# Create a virtual environment using uv
uv venv

# Activate the environment
# On Windows:
source .venv/Scripts/activate
# On macOS/Linux:
source .venv/bin/activate

# Install the required Python packages
uv pip install -r requirements.txt
```

**Step 3: Configure the Dataset Directory**

This server loads datasets from a specific folder. You need to tell it where your datasets are by setting an environment variable named `DATASETS_DIR`.

*   **On Windows (in Command Prompt):**
    ```cmd
    set DATASETS_DIR=C:\path\to\your\datasets
    ```
*   **On Windows (in PowerShell):**
    ```powershell
    $env:DATASETS_DIR="C:\path\to\your\datasets"
    ```
*   **On macOS/Linux:**
    ```bash
    export DATASETS_DIR=/path/to/your/datasets
    ```
Replace `C:\path\to\your\datasets` with the actual, absolute path to the folder containing your `.csv` files.

**Step 4: Run the Server**

Now you can start the MCP server:
```bash
python main.py
```
The server is now running and ready to accept connections from an MCP-compatible client.

---

### Part 2: For a Contributor (Making Changes)

Follow these steps if you want to modify the code and contribute your changes back to the main project.

**Step 1: Fork the Repository**

Go to the project's GitHub page: [https://github.com/JJaniel/dataset-analyser](https://github.com/JJaniel/dataset-analyser)
Click the "**Fork**" button in the top-right corner. This creates a personal copy of the repository under your own GitHub account.

**Step 2: Clone Your Fork**

Clone the repository from *your* account, not the original. Replace `<your-username>` with your GitHub username.

```bash
git clone https://github.com/<your-username>/dataset-analyser.git
cd dataset-analyser
```

**Step 3: Create a New Branch**

It's crucial to make your changes on a new branch to keep them organized.

```bash
# Create a branch and switch to it
git checkout -b my-awesome-feature
```
Replace `my-awesome-feature` with a short, descriptive name for your change (e.g., `add-parquet-support`).

**Step 4: Make Your Changes**

Set up the environment as described in "Part 1" and make your desired code changes using your favorite editor.

**Step 5: Commit and Push Your Changes**

Once you are happy with your changes, commit them with a clear message and push them to *your fork*.

```bash
# Stage your changes
git add .

# Commit them with a descriptive message
git commit -m "feat: Add support for Parquet files"

# Push the changes to your fork on GitHub
git push origin my-awesome-feature
```

**Step 6: Create a Pull Request**

Go to your forked repository on GitHub. You will see a prompt to "**Compare & pull request**". Click it. This will take you to a page where you can describe your changes and submit them to the original project for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
