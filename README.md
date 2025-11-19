agent.py is a standalone script that reads text from a PDF file, uses an LLM (Groq + Open-Source Model) to extract structured information, converts that into a flat JSON object, and exports it to both JSON and Excel (XLSX) formats.

The LLM automatically understands patterns inside the PDF and returns normalized JSON fields.

🚀 Features

Extracts full text from any PDF using pypdf

Sends content to an LLM using Groq API

Standardizes output into flat JSON

Saves results to:

Output.json

Output2.xlsx

Automatically handles:

messy text

lists

nested JSON

missing values

📦 Project Structure
Project/
│-- agent.py
│-- Data_Input.pdf
│-- .env

🔧 Installation
1. Clone or copy project files
2. Install dependencies
pip install -r requirements.txt


(If you don’t have a requirements.txt, use the list below:)

pypdf
pandas
python-dotenv
langchain-core
langchain-groq
openpyxl

🔑 Environment Variables

Create a .env file in the project folder:

GROQ_API_KEY=your_groq_key_here


Get keys from: https://console.groq.com/

🗂️ Input File

Place your input PDF inside the project folder and set its name here:

PDF_FILE = "Data_Input.pdf"

▶️ How to Run
python agent.py

📤 Outputs

After execution, you will get:

✔ Output.json

Flat JSON with key → value pairs.

✔ Output2.xlsx

Excel file containing the same extracted fields in tabular form.

🧠 How It Works

Read PDF

Extracts text using pypdf

Prepare Prompt

Sends extracted text to the LLM

Instructs it to return strict flat JSON only

LLM Processing

Model: openai/gpt-oss-20b running on Groq

Parse & Normalize

Fixes invalid JSON

Flattens nested structures

Converts lists → single values

Writes clean dictionary

Export

Writes Output.json

Writes Output2.xlsx

📌 Customization
Change model:
MODEL_NAME = "openai/gpt-oss-20b"

Change output filenames:
OUTPUT_XLSX = "YourFileName.xlsx"
OUTPUT_JSON = "YourFileName.json"

Change extraction rules (in system prompt):
- JSON only
- Flat structure only
- One value per key
