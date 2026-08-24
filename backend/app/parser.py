import fitz


def extract_document_from_pdf(file_path: str):
    document = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        blocks = page.get_text("blocks")

        page_elements = []

        for block in blocks:
            x0, y0, x1, y1, text, block_number, block_type = block

            text = text.strip()

            if not text:
                continue

            page_elements.append({
                "type": "text",
                "text": text,
                "bbox": {
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1
                },
                "block_number": block_number,
                "block_type": block_type
            })

        pages.append({
            "page": page_number,
            "elements": page_elements
        })

    document.close()

    return pages