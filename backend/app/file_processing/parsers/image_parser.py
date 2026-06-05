def extract_text_from_image(path: str) -> str:
    try:
        from PIL import Image
        import pytesseract

        img = Image.open(path)
        return pytesseract.image_to_string(img)
    except Exception:
        return ""
