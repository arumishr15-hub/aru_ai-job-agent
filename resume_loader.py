
from io import BytesIO

import pymupdf
from docx import Document


def load_resume(uploaded_file) -> str:
    """Read text from an uploaded PDF or DOCX resume."""

    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if filename.endswith(".pdf"):
        with pymupdf.open(
            stream=file_bytes,
            filetype="pdf"
        ) as document:
            text = "\n".join(
                page.get_text()
                for page in document
            )

    elif filename.endswith(".docx"):
        document = Document(BytesIO(file_bytes))

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        # Also capture text inside tables
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += "\n" + cell.text

    else:
        raise ValueError("Only PDF and DOCX are supported.")

    return text.strip()
