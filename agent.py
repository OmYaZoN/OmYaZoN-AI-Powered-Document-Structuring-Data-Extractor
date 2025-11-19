#!/usr/bin/env python3
import os
import json
import pandas as pd
from pypdf import PdfReader
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --------------------------------------------------------
# SET YOUR PDF FILE NAME HERE
# --------------------------------------------------------
PDF_FILE = "Data_Input.pdf"
OUTPUT_XLSX = "Output2.xlsx"
OUTPUT_JSON = "Output.json"
MODEL_NAME = "openai/gpt-oss-20b"
# --------------------------------------------------------


def read_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n\n".join(pages).strip()


def safe_parse_json(text: str):
    text = text.strip()

    try:
        return json.loads(text)
    except:
        pass

    s = text.find("{")
    e = text.rfind("}")
    if s != -1 and e != -1:
        try:
            return json.loads(text[s:e+1])
        except:
            pass

    raise ValueError("Could not parse JSON output.")


def normalize_flat_json(obj: dict) -> dict:
    out = {}
    for k, v in obj.items():
        key = str(k).strip()

        if v is None:
            out[key] = None
            continue

        if isinstance(v, (str, int, float, bool)):
            out[key] = v
            continue

        if isinstance(v, (list, tuple)):
            out[key] = v[0] if v else None
            continue

        out[key] = json.dumps(v, ensure_ascii=False)

    return out


def write_xlsx(flat: dict, path: str):
    rows = [{"Key": k, "Value": flat[k]} for k in sorted(flat.keys())]
    df = pd.DataFrame(rows)
    df.to_excel(path, index=False)


def main():

    if not os.path.exists(PDF_FILE):
        raise FileNotFoundError(f"PDF not found: {PDF_FILE}")

    pdf_text = read_pdf_text(PDF_FILE)

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise RuntimeError("GROQ_API_KEY missing.")

    llm = ChatGroq(
        model=MODEL_NAME,
        api_key=groq_key,
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are an advanced information extraction engine.

Return EXACTLY one flat JSON object only.

Rules:
- JSON only, no markdown
- Flat structure only
- One value per key
- If unknown → null
- Keys must be human-readable
"""),
        ("user",
         """Extract structured data from the following text:

<<<
{pdf_text}
>>>
""")
    ])

    parser = StrOutputParser()

    # LCEL pipeline replaces LLMChain
    chain = prompt | llm | parser

    raw_output = chain.invoke({"pdf_text": pdf_text})

    parsed = safe_parse_json(raw_output)
    flat = normalize_flat_json(parsed)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(flat, f, ensure_ascii=False, indent=2)

    write_xlsx(flat, OUTPUT_XLSX)

    print(json.dumps(flat, ensure_ascii=False))


if __name__ == "__main__":
    main()
