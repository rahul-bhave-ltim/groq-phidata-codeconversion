
'''
1. **Frameworks and Libraries Used**:
   - `dotenv`: Used to load environment variables from a `.env` file.
   - `os`: Used to interact with the operating system.
   - `streamlit`: Used to create a web application.
   - `phi.agent` and `phi.model.groq`: Used to initialize and run agents for converting Snowflake stored procedures to requirements in English and then to PySpark code.

2. **Environment Variables**:
   - The code loads environment variables from a `.env` file using the `load_dotenv()` function.
   - The `GROQ_API_KEY` environment variable is set using the value from the `.env` file.

3. **Streamlit Application**:
   - The title of the Streamlit app is set to "Code Conversion App".
   - A text area is created for the user to paste their Snowflake stored procedure.

4. **Agent Functions**:
   - `convert_snowflake_to_requirements(snowflake_procedure)`: 
     - Initializes a Groq agent with a specific model (`qwen-2.5-coder-32b`).
     - Runs the agent to convert the Snowflake stored procedure into requirements in English.
     - Returns the response content.
   
   - `convert_requirements_to_pyspark(requirements)`:
     - Initializes a Phidata agent with a specific model (`qwen-2.5-coder-32b`).
     - Runs the agent to convert the requirements into PySpark code.
     - Returns the response content.
'''
from dotenv import load_dotenv
import os
import streamlit as st
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq

# Load environment variables from .env file
load_dotenv()

# Set the Groq API key from the environment variable in case you are going save key in the .env file
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Title of the app
st.title("Code Conversion App")

# Text area for input Snowflake stored procedure
snowflake_input = st.text_area("Paste your Snowflake stored procedure here:")

def convert_snowflake_to_requirements(snowflake_procedure):
    # Initialize the Groq agent
    agent = Agent(
        model=Groq(id="qwen-2.5-coder-32b"),
        markdown=True
    )

    # Get the response in a variable
    run: RunResponse = agent.run(f"Convert the following Snowflake stored procedure into requirements in English:\n\n{snowflake_procedure}")
    return run.content

def convert_requirements_to_pyspark(requirements):
    # Initialize the Phidata agent
    agent = Agent(
        model=Groq(id="qwen-2.5-coder-32b"),
        markdown=True
    )
    # Get the response in a variable
    run: RunResponse = agent.run(f"Convert the following requirements into PySpark code:\n\n{requirements}")
    return run.content

# Initialize a session state for requirements to persist between button clicks
if 'requirements' not in st.session_state:
    st.session_state.requirements = ""

# Button to convert Snowflake stored procedure to requirements
if st.button("Read Snowflake"):
    st.session_state.requirements = convert_snowflake_to_requirements(snowflake_input)
    st.text_area("Requirements in English:", st.session_state.requirements)

# Button to convert requirements to PySpark code
if st.button("Convert to PySpark"):
    if st.session_state.requirements:
        pyspark_code = convert_requirements_to_pyspark(st.session_state.requirements)
        st.text_area("PySpark Code:", pyspark_code)
    else:
        st.error("Please generate the requirements first by clicking 'Read Snowflake'.")
