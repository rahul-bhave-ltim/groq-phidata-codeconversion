# groq-phidata-codeconversion

To setup this repository, you need following-

1. Access to Groq Cloud.
2. Get the API key from the Groq Cloud
3. Create python virtual environment
4. Setup GROQ_API_KEY on GitBash using command, echo $GROQ_API_KEY=YOUR_GROQ_API_KEY
5. Install requirements
6. Launch the streamlit app using command- streamlit run code_conversion_agent.py

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
