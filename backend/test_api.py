import requests

pdf_path = "uploads/random_3page_report.pdf"

with open(pdf_path, "rb") as pdf:
    response = requests.post(
        "http://127.0.0.1:8000/upload",
        files={"file": pdf}
    )

print("Status:", response.status_code)
print(response.json())