# 🌉 DBridger

**The Secure Enterprise AI Gateway.** DBridger is a standalone native desktop application that allows users to query complex local databases in plain English. It bridges the gap between old-world relational databases and modern AI Agents (Google Gemini), ensuring strict data privacy and local execution.

## 🚀 Features

* **Native Desktop Interface**: A professional, responsive dark-mode UI built with PyQt6. No browser tabs, no web uploads—just native OS file pickers and local memory.
* **Autonomous AI Agent**: Powered by Google's modern `genai` SDK. The agent is capable of multi-step reasoning, automatically navigating foreign keys, and executing complex "joins" across multiple tables.
* **Automated PII Masking**: A built-in security moat intercepts raw database rows and redacts sensitive info (SSNs, Credit Cards, Emails) *before* the data is ever sent to the LLM.
* **Dynamic Schema Mapping**: Automatically introspects the connected SQLite database and injects a complete topological map into the AI's context, drastically reducing API quota and preventing hallucination loops.
* **Asynchronous Execution**: Utilizes background threading (`QThread`) to keep the UI buttery smooth while the Agent performs heavy sequential tool calls.

---

## 📂 Project Structure

* `src/app.py`: The PyQt6 Desktop Application (UI, Tabs, and Threading).
* `src/agent.py`: The AI Brain (Gemini configuration, tool injection, and strict System Prompts).
* `src/server.py`: The secure local tool execution layer (searches and schema parsing).
* `src/security.py`: The PII redaction logic ("The Moat").
* `setup_database.py`: Generates the `example.db` mock enterprise database for testing.

---

## 🛠️ Quick Start (Developer Mode)

### 1. Installation

Install the required Python frameworks (no Node.js required):

```bash
# Install UI and AI SDKs
pip install -r requirements.txt

```

### 2. Generate the Test Database

Run the setup script to generate a complex, 8-table relational e-commerce database packed with mock PII:

```bash
python setup_database.py

```

### 3. Run the App

Launch the desktop application:

```bash
python -m src.app

```

*Note: In the UI, open your local `.db` file, paste your Gemini API key into the Agent tab, and start asking questions!*

---

## 🛡️ The DBridger Architecture (How it protects data)

DBridger operates on a strict **"Local First, Context Second"** architecture:

1. **Introspection**: The user connects a local database. DBridger maps the schema natively.
2. **Context Injection**: The Agent is handed the database map, but *no actual row data*.
3. **Execution**: The user asks a question. The Agent plans its search and requests local tool execution (`search_records`).
4. **The Moat**: The Python backend runs the SQL locally, intercepts the result, and physically scrubs the PII.
5. **Synthesis**: The AI receives only the masked data snippet to formulate its final, human-readable answer.
