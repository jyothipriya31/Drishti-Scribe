import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


class Element(BaseModel):
    type: str
    text: str
    description: str


class Page(BaseModel):
    page: int
    elements: list[Element]


class DocumentAnalysis(BaseModel):
    pages: list[Page]


def analyze_pdf(file_path: str):
    pdf_path = Path(file_path)

    uploaded_file = client.files.upload(file=pdf_path)

    prompt = """
Analyze this PDF for an accessibility system.

For every page, identify the major meaningful elements.

Possible element types include:
heading, paragraph, table, chart, diagram, flowchart, image, other.

For every element:
- type: what kind of element it is
- text: its title or important textual content
- description: a concise description suitable for text-to-speech

For charts, describe important values and trends.
For tables, preserve important information.
For diagrams and flowcharts, describe relationships, sequence, and decisions.
Do not omit important visual information.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            uploaded_file,
            prompt
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": DocumentAnalysis,
        },
    )

    return DocumentAnalysis.model_validate_json(response.text)