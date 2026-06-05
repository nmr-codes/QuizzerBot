def extract_text_from_pdf(path: str) -> str:
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(path)
        texts = []
        for page in reader.pages:
            texts.append(page.extract_text() or "")
        return "\n".join(texts)
    except Exception:
        # Fallback: return empty string
        return ""
