import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)

pdf_path = Path("uploads/random_3page_report.pdf")

uploaded_file = client.files.upload(file=pdf_path)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[
        uploaded_file,
        """
Analyze this PDF as an accessibility assistant.

For every page, identify the major meaningful elements.

Possible element types include:
- heading
- paragraph
- table
- chart
- diagram
- flowchart
- image
- other

For each element:
1. Identify its type.
2. Give its relevant text or title.
3. Give a concise description suitable for conversion to speech.
4. Preserve the page number.

Return ONLY valid JSON.
"""
    ]
)

print(response.text)