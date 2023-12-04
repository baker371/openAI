#!pip install langchain openai psycopg2-binary streamlit

import streamlit as st
import os
import sys
import warnings
import constant
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.utilities import SQLDatabase

warnings.filterwarnings('ignore')

os.environ["OPENAI_API_KEY"] = constant.APIKEY



st.set_page_config(page_title="Query Executor", page_icon=":robot:")

# Function to create SQL agent
def create_sql_agent_executor():
    return create_sql_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        toolkit=SQLDatabaseToolkit(
            db=SQLDatabase.from_uri("postgresql://username:password@server:port2/database"),
            llm=OpenAI(temperature=0)
        ),
        verbose=False,
        agent_type=AgentType.OPENAI_FUNCTIONS
    )

def main():
    st.title("Interactive Query Executor")

    # User input field
    user_input = st.text_input("Enter your query here:")

    # Submit button
    if st.button("Submit"):
        # Check if user input is not empty
        if user_input:
            # Creating the SQL agent
            agent_executor = create_sql_agent_executor()

            # Execute the query
            result = agent_executor.run(user_input)

            # Displaying the result
            st.subheader("Result:")
            st.write(result)

            # Store query and response in a history list
            history = st.session_state.get("history", [])
            history.append({"question": user_input, "response": result})
            st.session_state["history"] = history

    # Display history of queries and responses
    if "history" in st.session_state:
        st.subheader("History:")
        for idx, item in enumerate(reversed(st.session_state["history"])):
            st.markdown(f"**{len(st.session_state['history']) - idx}. Question:** {item['question']}")
            st.markdown(f"**Response:** {item['response']}")
            st.markdown("---")

if __name__ == "__main__":
    main()