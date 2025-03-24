"""
Code Conversion App

This Streamlit application converts Snowflake stored procedures into PySpark code and calculates the accuracy of the generated PySpark code using different language models.

Modules:
    - dotenv: Loads environment variables from a .env file.
    - os: Provides a way of using operating system dependent functionality.
    - streamlit: A framework for creating interactive web applications.
    - agno.agent: Provides the Agent and RunResponse classes for interacting with language models.
    - agno.models.groq: Provides the Groq model for language processing.
    - requests: Allows sending HTTP requests.
    - json: Provides functions for working with JSON data.

Functions:
    - convert_snowflake_to_requirements(snowflake_procedure): Converts a Snowflake stored procedure into requirements in English using the Groq model.
    - convert_requirements_to_pyspark(requirements): Converts requirements in English into PySpark code using the Groq model.
    - calculate_pyspark_accuracy(pyspark_code): Calculates the accuracy of the generated PySpark code using the deepseek-r1-distill-llama-70b model.

Streamlit Components:
    - Text areas for inputting Snowflake stored procedures, displaying requirements, PySpark code, and metrics.
    - Buttons for reading Snowflake stored procedures, saving requirements, converting requirements to PySpark code, and calculating the accuracy of the PySpark code.

Session State Variables:
    - requirements: Stores the requirements in English.
    - pyspark_code: Stores the generated PySpark code.
    - pyspark_metrics: Stores the metrics for the PySpark code generation.
    - snowflake_metrics: Stores the metrics for the Snowflake to requirements conversion.
    - pyspark_accuracy: Stores the accuracy of the generated PySpark code.
    - accuracy_metrics: Stores the metrics for the PySpark code accuracy calculation.

Usage:
    1. Paste your Snowflake stored procedure in the provided text area.
    2. Click "Read Snowflake" to convert the stored procedure into requirements in English.
    3. Edit the requirements if necessary and click "Save Requirements".
    4. Click "Convert to PySpark" to generate PySpark code from the requirements.
    5. Click "Calculate Accuracy" to calculate the accuracy of the generated PySpark code.
    6. View the generated PySpark code, metrics, and accuracy in the respective text areas.
"""

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
    """
    Converts a Snowflake stored procedure into requirements in English using the Groq model.

    Args:
        snowflake_procedure (str): The Snowflake stored procedure to be converted.

    Returns:
        tuple: A tuple containing the requirements in English and the metrics for the conversion.
    """
    # Initialize the Groq agent
    agent = Agent(
        model=Groq(id="qwen-2.5-coder-32b"),
        markdown=True
    )

    # Get the response in a variable
    run: RunResponse = agent.run(f"Convert the following Snowflake stored procedure into requirements in English:\n\n{snowflake_procedure}")
    return run.content, run.metrics

def convert_requirements_to_pyspark(requirements):
    """
    Converts requirements in English into PySpark code using the Groq model.

    Args:
        requirements (str): The requirements in English to be converted.

    Returns:
        tuple: A tuple containing the generated PySpark code and the metrics for the conversion.
    """
    # Initialize the Agno agent
    agent = Agent(
        model=Groq(id="qwen-2.5-coder-32b"),
        markdown=True
    )
    # Get the response in a variable
    run: RunResponse = agent.run(f"Convert the following requirements into PySpark code:\n\n{requirements}")
    return run.content, run.metrics

def calculate_pyspark_accuracy(pyspark_code):
    """
    Calculates the accuracy of the generated PySpark code using the deepseek-r1-distill-llama-70b model.

    Args:
        pyspark_code (str): The generated PySpark code to be evaluated.

    Returns:
        tuple: A tuple containing the accuracy of the PySpark code and the metrics for the accuracy calculation.
    """
    # Initialize the accuracy agent
    agent = Agent(
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        markdown=True
    )
    # Get the response in a variable
    run: RunResponse = agent.run(f"Calculate the accuracy of the following PySpark code in %:\n\n{pyspark_code}")
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

if 'pyspark_accuracy' not in st.session_state:
    st.session_state.pyspark_accuracy = ""

if 'accuracy_metrics' not in st.session_state:
    st.session_state.accuracy_metrics = ""

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

# Button to calculate accuracy of PySpark code
if st.button("Calculate Accuracy"):
    if st.session_state.pyspark_code:
        st.session_state.pyspark_accuracy, st.session_state.accuracy_metrics = calculate_pyspark_accuracy(st.session_state.pyspark_code)
        st.session_state.accuracy_metrics = str(st.session_state.accuracy_metrics) if st.session_state.accuracy_metrics else ""
    else:
        st.error("Please convert the requirements to PySpark code first by clicking 'Convert to PySpark'.")

# Display the PySpark code and metrics if available
if st.session_state.pyspark_code:
    st.text_area("PySpark Code:", value=st.session_state.pyspark_code, key="pyspark_code")
    st.text_area("PySpark agent tokens:", value=st.session_state.pyspark_metrics, key="pyspark_metrics")
    st.text_area("Snowflake agent tokens:", value=st.session_state.snowflake_metrics, key="snowflake_metrics_display")

# Display the PySpark code accuracy and metrics if available
if st.session_state.pyspark_accuracy:
    st.text_area("PySpark Code Accuracy:", value=st.session_state.pyspark_accuracy, key="pyspark_accuracy")
    st.text_area("Accuracy agent tokens:", value=st.session_state.accuracy_metrics, key="accuracy_metrics")
