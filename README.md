# Excel Worksheet Analyzer

This project is a Proof of Concept (PoC) demonstrating how to use LangChain and OpenAI to analyze multiple Excel Worksheet files. It showcases the ReAct approach, wherein a “Grand Agent” determines which DataFrame-specific agent (tool) to invoke based on the user’s query.

---

## Overview

### Files:

- **main.py**: The main Python script containing the logic to:
  - Load two Excel files.
  - Create separate agents for each DataFrame using `create_pandas_dataframe_agent`.
  - Wrap those agents as tools.
  - Combine these tools under a grand “ReAct” agent to handle questions about both files.

- **requirements.txt**: Lists the Python dependencies.

### Sample Excel files:

- `EIS Billing Detail - FEB 2025 - HHS EIS PMO 75P00120F80177 2025.2.25-1.xlsx`
- `EIS Billing Detail - MAR 2025 - HHS EIS PMO 75P00120F80177.xlsx`

> **Note:** These files are examples and may not be included for confidentiality reasons.

---

## Key Components

- **LangChain**: A library for building language-model-powered applications.
- **ReAct Approach**: A structured reasoning process that follows a cycle of Thought → Action → Action Input → Observation → Final Answer.
- **create_pandas_dataframe_agent**: A specialized LangChain feature that generates Python code to query and manipulate a pandas DataFrame.
- **Agent-Tool Framework**: Each Excel file has its own agent, wrapped as a tool. A higher-level agent decides which tool to invoke based on user queries.

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Joelfranklin96/Excel-Worksheet-Analyzer.git
cd Excel-Worksheet-Analyzer
```

### Install Dependencies

Use `requirements.txt` to install the necessary Python libraries.

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Ensure you have a `.env` file (or environment variables set) containing your OpenAI API key.

For example, inside `.env`:

```bash
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

### Place Your Excel Files

By default, the script expects the following file paths in the same directory:

- `EIS Billing Detail - FEB 2025 - HHS EIS PMO 75P00120F80177 2025.2.25-1.xlsx`
- `EIS Billing Detail - MAR 2025 - HHS EIS PMO 75P00120F80177.xlsx`

> If your files have different names or locations, update the file paths in `main.py` accordingly.

---

## Run the Code

```bash
python main.py
```

You should see the script load the Excel files, create agents, and respond to sample user queries.

---

## How It Works

### Loading the Data

The script reads two Excel files into pandas DataFrames: one for February and one for March data.

### Creating Agents

For each DataFrame, `create_pandas_dataframe_agent` creates a LangChain agent capable of running queries on that DataFrame.

### Wrapping Agents as Tools

Each agent is then wrapped as a tool with a descriptive name and function.

### Grand Agent (ReAct)

A higher-level ReAct agent is given the tools for both February and March.

When a user query is provided, the agent decides:

- Which tool(s) to use.
- What query to run on the DataFrame.

It executes the query, gathers observations, and then produces a final answer.

---

## Sample Queries

- "How many unique values in the column 'agency hierarchy code' in the Billing file for the month of March?"
- "How many unique values in the column 'agency hierarchy code' in the Billing file for the month of February?"
- "In the March file, how many records with 'contractor invoice level account number' as SF000706?"

---

## Customizing

### Additional Excel Files

Create a new agent for each additional Excel file, wrap it as a tool, and supply it to the grand agent.

### Complex Queries

The ReAct agent is capable of iteratively generating code for complex tasks such as grouping, aggregating, filtering, and more.

### Prompt Engineering

The `instructions` variable in `main.py` can be modified to provide the agent with more detailed domain-specific guidance.

---

## Troubleshooting

- If you encounter file path errors, confirm that the filenames and locations match what you’ve set in `main.py`.
- If you get authentication errors, double-check your `.env` for the correct OpenAI API key.
- If you need to debug the chain’s behavior, you can set `verbose=True` (already set) in relevant agent calls to see the agent’s thought process.

---

## License

```csharp
This project is licensed under the MIT License - see the LICENSE file for details.
```

---

## Contact

**Author**: Joel Franklin 
**LinkedIn**: https://www.linkedin.com/in/joel-franklin-stalin-vijayakumar-89289a223/

For any questions or clarifications, feel free to open an issue or reach out directly.
