from typing import Any

import pandas as pd
from dotenv import load_dotenv

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.tools import Tool
from langchain import hub  # Import hub directly from langchain

load_dotenv()


def main():
    print("Start...")

    # 1) Prompt instructions for the ReAct agent
    instructions = """
You are a ReAct agent capable of using tools to answer user queries about billing details.
We have 2 Excel files:
1) EIS Billing Detail - FEB 2025 - HHS EIS PMO 75P00120F80177 2025.2.25-1.xlsx (sheet_name = 'Billing Invoice (BI) Detail')
2) EIS Billing Detail - MAR 2025 - HHS EIS PMO 75P00120F80177.xlsx (sheet_name = 'Billing Invoice (BI) Detail')

Whenever a user’s question requires analyzing or retrieving information 
from these files, you should use the appropriate tool:

- **Excel Agent - February** for the February file
- **Excel Agent - March** for the March file

Here is how you should structure your reasoning and responses:

- **Thought**: 
  Provide your internal, step-by-step reasoning about how to approach the user's question 
  (not shown to the user).

- **Action**: 
  If you need to consult the data, specify the name of the tool 
  (either “Excel Agent - February” or “Excel Agent - March”).

- **Action Input**:
  Provide the specific query or instructions you want to pass into the tool.

- **Observation**:
  The tool’s response to your query. This will inform your next steps.

- **Final Answer**:
  The concise, direct answer you provide to the user after integrating 
  all relevant information and your reasoning.

Remember:
1. Use "Excel Agent - February" or "Excel Agent - March" depending on which data you need.
2. Think carefully, plan your steps, and then provide the best final answer.
"""

    # 2) Create a ChatOpenAI model
    llm_feb = ChatOpenAI(temperature=0, model="gpt-4")
    llm_mar = ChatOpenAI(temperature=0, model="gpt-4")

    # 3) Load each Excel file into its own DataFrame
    feb_file_path = "EIS Billing Detail - FEB 2025 - HHS EIS PMO 75P00120F80177 2025.2.25-1.xlsx"
    mar_file_path = "EIS Billing Detail - MAR 2025 - HHS EIS PMO 75P00120F80177.xlsx"

    df_february = pd.read_excel(feb_file_path, sheet_name="Billing Invoice (BI) Detail")
    df_march = pd.read_excel(mar_file_path, sheet_name="Billing Invoice (BI) Detail")

    # 4) Create a Pandas DataFrame agent for each DataFrame
    excel_agent_executor_february = create_pandas_dataframe_agent(
        llm=llm_feb,
        df=df_february,
        verbose=True,
        allow_dangerous_code=True,  # Add this parameter
    )
    excel_agent_executor_march = create_pandas_dataframe_agent(
        llm=llm_mar,
        df=df_march,
        verbose=True,
        allow_dangerous_code=True,  # Add this parameter
    )

    # 5) Wrap each DataFrame agent in a Tool
    excel_agent_tool_february = Tool(
        name="Excel Agent - February",
        func=excel_agent_executor_february.invoke,
        description="""Use this tool to analyze:
EIS Billing Detail - FEB 2025 - HHS EIS PMO 75P00120F80177 2025.2.25-1.xlsx
Provide your query for data analysis.
""",
    )

    excel_agent_tool_march = Tool(
        name="Excel Agent - March",
        func=excel_agent_executor_march.invoke,
        description="""Use this tool to analyze:
EIS Billing Detail - MAR 2025 - HHS EIS PMO 75P00120F80177.xlsx
Provide your query for data analysis.
""",
    )

    # 6) Combine the instructions with the standard ReAct agent prompt
    #    If you have a custom prompt, you can load or define it here.
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    # 7) Create the ReAct agent and pass in both tools
    tools = [excel_agent_tool_february, excel_agent_tool_march]
    grand_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=tools,
    )

    grand_agent_executor = AgentExecutor(
        agent=grand_agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

    # 8) Ask a sample question that might involve either file
    query1 = "How many unique values in the column 'agency hierarchy code in the Billing file for the month of March?"
    print("=====================================================")
    print("User Query #1:", query1)
    response1 = grand_agent_executor.invoke({"input": query1})
    print("\nFinal Answer #1:", response1)
    print("=====================================================\n")

    query2 = "How many unique values in the column 'agency hierarchy code' in the Billing file for the month of February?"
    print("=====================================================")
    print("User Query #2:", query2)
    response2 = grand_agent_executor.invoke({"input": query2})
    print("\nFinal Answer #2:", response2)
    print("=====================================================\n")

    query3 = "In the March file, how many records with 'contractor invoice level account number' as SF000706?"
    print("=====================================================")
    print("User Query #3:", query3)
    response3 = grand_agent_executor.invoke({"input": query3})
    print("\nFinal Answer #3:", response3)
    print("=====================================================\n")


if __name__ == "__main__":
    main()
