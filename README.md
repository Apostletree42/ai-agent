# AI Agent

> **Note:** This is not a production-ready AI agent. It's a demonstration/learning project.

A simple AI agent built with Google's Gemini API that can interact with files and execute Python code within a constrained working directory. The agent uses function calls to perform various file operations and can help with code analysis, debugging, and execution.

## What it can do

- **File Operations**: List files, read file contents, and write new files
- **Code Execution**: Run Python files and capture their output
- **Code Analysis**: Analyze code structure, explain functionality, and identify bugs
- **Interactive Problem Solving**: Fix issues through iterative code analysis and execution
- **Directory Navigation**: Work within a specified working directory (defaults to `./calculator`)

## How to run

1. Set up environment variables in `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   SYSTEM_PROMPT=your_system_prompt
   MODEL_NAME=gemini-2.0-flash-001
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the agent:
   ```bash
   python main.py "Your prompt here"
   python main.py "Your prompt here" --verbose  # for detailed output
   ```

Example:
For this command, modify `pkg/calculator.py` and change the precedence of the + operator to 3.
```bash
python main.py "fix the bug in the calculator: 3 + 7 * 2 shouldn't be
```