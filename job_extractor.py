
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

import os
os.environ["GROQ_API_KEY"] = "********"

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

PROMPT = PromptTemplate.from_template(
"""
You are a data extraction engine.

STRICT RULES:
- Output ONLY valid JSON
- Do NOT explain anything
- Do NOT include markdown
- Do NOT include code
- Do NOT include comments
- Do NOT include extra text

TASK:
From the text below, extract job postings.

Each job must be an object with EXACT keys:
- company (string)
- title (string)
- date_posted (string, or "Unknown")

Only include real job roles.
Ignore internships, SEO, sales, marketing, business roles.

If no jobs are found, return an empty JSON list: []

TEXT:
{text}

OUTPUT:
"""
)


import ast
import json

def extract_jobs(text):
    response = llm.invoke(
        PROMPT.format(text=text[:12000])
    )

    raw = response.content.strip()

    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
        return []
    except Exception as e:
        print("⚠️ Failed to parse LLM output")
        print(raw)
        return []
