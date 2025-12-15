# LLM-Orchestrated-Data-Exploration-Tool
An interactive, AI-powered data analysis application that allows users to upload CSV files and explore their data using natural language. The app converts user questions into executable Python or SQL, runs the analysis automatically, and displays results such as tables, metrics, and charts in a conversational interface.

---

## 🚀 Key Features

- Upload and analyze CSV files instantly
- Ask questions in plain English
- Automatic Python or SQL code generation using an LLM
- Safe execution of AI-generated analysis code
- Interactive charts and tables
- Automatic data profiling and health report
- Chat-style interface with conversation memory
- Export full analysis as an HTML report

---

## 🧠 Tech Stack

- **Frontend / App Framework**: Streamlit  
- **Data Processing**: Pandas  
- **Visualization**: Matplotlib, Seaborn  
- **SQL Engine**: DuckDB  
- **LLM Integration**: OpenAI API  
- **Environment Management**: python-dotenv  

---

## 📁 Project Structure
```bash
├── app.py
├── requirements.txt
├── core/
│ ├── state.py
│ ├── data_loader.py
│ ├── profiler.py
│ ├── prompts.py
│ ├── llm_client.py
│ ├── code_runner.py
│ ├── sql_prompt.py
│ ├── sql_engine.py
│ ├── export_report.py
│ └── ui_components.py
```


---

## 🔄 End-to-End Application Workflow

### 1️⃣ Application Initialization

When the application starts:
- Environment variables are loaded
- The OpenAI client is initialized
- Streamlit page settings are configured
- Session state is initialized to persist data across reruns

Session state stores:
- Chat messages
- Uploaded DataFrame
- Dataset summary
- Column profiling results
- Selected analysis engine (Python or SQL)

This ensures that the user’s data and conversation are not lost during app refreshes.

---

### 2️⃣ CSV Upload and Data Storage

Users upload a CSV file through the sidebar.

Once uploaded:
- The file is read using Pandas
- The DataFrame is stored in `st.session_state.df`
- A dataset summary is created, including:
  - Number of rows and columns
  - Column names
  - Data types
  - Sample rows
  - Basic statistics

This summary is later injected into the AI prompt to provide dataset context efficiently.

---

### 3️⃣ Automatic Data Profiling

After loading the dataset, the app automatically profiles each column.

For every column, the profiler detects:
- Data type (Numeric, Text, Categorical, Datetime)
- Number of unique values
- Percentage of missing values
- Potential ID columns
- Possible date columns
- Sample values

This profiling is done using deterministic Python logic and does not rely on the LLM.

---

### 4️⃣ Data Health Report (Sidebar)

The profiling results are displayed in the sidebar as a **Data Health Report**.

It includes:
- Overview metrics (total columns, missing-value columns)
- Detailed column profiling table
- Potential issues such as high missing values or ID-like columns

This helps users understand data quality before performing analysis.

---

### 5️⃣ Analysis Engine Selection (Python vs SQL)

Users can choose the analysis engine from the sidebar:

#### 🐍 Python Mode
- Flexible data analysis
- Supports transformations, aggregations, and visualizations

#### 🧮 SQL Mode
- Structured queries using DuckDB
- Fast and safe SELECT-only analysis

This dual-engine design demonstrates multiple analytical approaches.

---

### 6️⃣ Chat Interface and Conversation Memory

The application uses a chat-style interface.

- User questions are stored in session state
- AI responses and outputs are preserved
- The entire conversation is re-rendered on each rerun

This allows multi-step analysis where each question builds on previous results.

---

## 🧩 Prompt Engineering Design

### Python Analysis Prompt

The system prompt dynamically includes:
- Dataset shape
- Column names
- Data types
- Sample values
- Summary statistics

Key prompt rules:
- Always return Python code for calculations or plots
- Use the preloaded DataFrame `df`
- Do not import libraries
- Place explanations after the code block

This ensures reliable and executable AI output.

---

### SQL Analysis Prompt

The SQL prompt strictly enforces:
- SELECT-only queries
- No explanations or comments
- DuckDB-compatible syntax
- Table reference as `df`

This reduces risk and ensures predictable SQL execution.

---

## 🤖 LLM Interaction

The app sends:
- System prompt (Python or SQL)
- User question
- Limited recent chat history

This helps control token usage while maintaining context.

The LLM returns either:
- Python code (for Python mode)
- A SQL query (for SQL mode)

---

## ⚙️ Python Code Execution Engine

If the AI response contains Python code:
- The code is extracted from the response
- Executed using `exec()` in a controlled environment
- Captures:
  - Printed output
  - Returned values (DataFrames, numbers)
  - Warnings
  - Matplotlib figures

Results are displayed inline in the chat, creating a notebook-like experience.

---

## 🧮 SQL Execution Engine

In SQL mode:
- Generated SQL is validated to block unsafe commands
- DuckDB executes the query on the Pandas DataFrame
- Results are returned as a DataFrame and displayed

This enables fast, structured data analysis.

---

## 📄 Exporting Analysis Reports

The app allows users to export the entire analysis as an HTML report.

The report includes:
- Dataset metadata
- User questions
- AI-generated analysis
- Code blocks

The HTML file can be printed or shared for documentation purposes.

---

## ⚠️ Error Handling and User Feedback

The app includes basic error handling for:
- Missing or incorrect column names
- Type errors
- Invalid SQL queries
- Execution failures

Helpful messages are shown to guide the user instead of crashing.

---

## 🎓 Learning Outcomes

Through this project, I learned:
- End-to-end AI application design
- Prompt engineering for structured tasks
- Executing and validating AI-generated code
- Combining Python, SQL, and LLMs
- Building user-friendly data analysis tools

---

## 📝 Project Scope and Disclaimer

This project is a **personal learning and portfolio project**.
It is not intended for production use.

The goal is to demonstrate understanding of:
- AI integration
- Data analysis workflows
- Software engineering principles

---

## ✅ Conclusion

This project showcases how natural language, AI models, and traditional data tools can be combined into a single interactive system. It highlights practical skills in AI-assisted analytics, application architecture, and user experience design.

---

## 📌 Setup Instructions

```bash
pip install -r requirements.txt
streamlit run app.py
```
Make sure to add your OpenAI API key to a .env file:
```bash
OPENAI_API_KEY=your_api_key_here
```
