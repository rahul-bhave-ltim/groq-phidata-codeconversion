
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
from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
import requests
import json

# Load environment variables from .env file
load_dotenv()

# Set the Groq API key from the environment variable
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
api_key = os.getenv("GROQ_API_KEY")

# Title of the app
st.title("Code Conversion App")

# Text area for input Snowflake stored procedure
snowflake_input = st.text_area("Paste your Snowflake stored procedure here:", key="snowflake_input")

def convert_snowflake_to_requirements(snowflake_procedure):
    # Initialize the Groq agent
    agent = Agent(
        model=Groq(id="qwen-2.5-coder-32b"),
        markdown=True
    )

    # Get the response in a variable
    run: RunResponse = agent.run(f"Convert the following Snowflake stored procedure into requirements in English:\n\n{snowflake_procedure}")
    return run.content, run.metrics

def convert_requirements_to_pyspark(requirements):
    # Initialize the Agno agent
    agent = Agent(
        model=Groq(id="qwen-2.5-coder-32b"),
        markdown=True
    )
    # Get the response in a variable
    run: RunResponse = agent.run(f"Convert the following requirements into PySpark code:\n\n{requirements}")
    return run.content, run.metrics

# Initialize a session state for requirements and metrics to persist between button clicks
if 'requirements' not in st.session_state:
    st.session_state.requirements = ""

if 'pyspark_code' not in st.session_state:
    st.session_state.pyspark_code = ""

if 'pyspark_metrics' not in st.session_state:
    st.session_state.pyspark_metrics = ""

if 'snowflake_metrics' not in st.session_state:
    st.session_state.snowflake_metrics = ""

if st.button("Read Snowflake"):
    st.session_state.requirements, st.session_state.snowflake_metrics = convert_snowflake_to_requirements(snowflake_input)
    st.session_state.snowflake_metrics = str(st.session_state.snowflake_metrics) if st.session_state.snowflake_metrics else ""

# Editable text area for requirements
edited_requirements = st.text_area("Requirements in English:", value=st.session_state.requirements, key="requirements")
st.text_area("Snowflake agent tokens:", value=st.session_state.snowflake_metrics, key="snowflake_metrics")

# Button to save the edited requirements
if st.button("Save Requirements"):
    st.session_state.requirements = edited_requirements
    st.success("Requirements saved successfully!")

# Button to convert requirements to PySpark code
if st.button("Convert to PySpark"):
    if st.session_state.requirements:
        st.session_state.pyspark_code, st.session_state.pyspark_metrics = convert_requirements_to_pyspark(st.session_state.requirements)
        st.session_state.pyspark_metrics = str(st.session_state.pyspark_metrics) if st.session_state.pyspark_metrics else ""
    else:
        st.error("Please generate the requirements first by clicking 'Read Snowflake'.")

# # Display the PySpark code and metrics if available
# if st.session_state.pyspark_code:
#     st.text_area("PySpark Code:", value=st.session_state.pyspark_code, key="pyspark_code")
#     st.text_area("PySpark agent tokens:", value=st.session_state.pyspark_metrics, key="pyspark_metrics")
#     st.text_area("Snowflake agent tokens:", value=st.session_state.snowflake_metrics, key="snowflake_metrics_display")


# Display the PySpark code and metrics if available
if st.session_state.pyspark_code:
    st.text_area("PySpark Code:", value=st.session_state.pyspark_code, key="pyspark_code")
    
    # Extract and format PySpark agent tokens
    pyspark_metrics = st.session_state.pyspark_metrics
    
    # Debugging: Print the entire pyspark_metrics dictionary
    print("pyspark_metrics:", pyspark_metrics)
    
    # Check if the metrics are in the expected format
    if isinstance(pyspark_metrics, dict):
        try:
            input_tokens = pyspark_metrics['input_tokens'][0]
            output_tokens = pyspark_metrics['output_tokens'][0]
            total_tokens = pyspark_metrics['total_tokens'][0]
            
            # Debugging: Print the extracted token values
            print("input_tokens:", input_tokens)
            print("output_tokens:", output_tokens)
            print("total_tokens:", total_tokens)
            
            # Display the formatted tokens
            formatted_tokens = f"input_tokens={input_tokens}, output_tokens={output_tokens}, total_tokens={total_tokens}"
            print("formatted_tokens:", formatted_tokens)
            st.text_area("PySpark agent tokens:", value=formatted_tokens, key="pyspark_metrics_display")
        except (KeyError, IndexError, TypeError) as e:
            print("Error extracting metrics:", e)
            st.text_area("PySpark agent tokens:", value="Metrics data is not in the expected format.", key="pyspark_metrics_display_error_1")
    else:
        print("Metrics data is not in the expected format.")
        st.text_area("PySpark agent tokens:", value="Metrics data is not in the expected format.", key="pyspark_metrics_display_error_2")
    
    # Display Snowflake agent tokens
    st.text_area("Snowflake agent tokens:", value=st.session_state.snowflake_metrics, key="snowflake_metrics_display")
