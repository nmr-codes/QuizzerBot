from typing import Callable

from app.file_processing.parsers.pdf_parser import extract_text_from_pdf
from app.file_processing.parsers.docx_parser import extract_text_from_docx
from app.file_processing.parsers.image_parser import extract_text_from_image


PARSER_MAP: dict[str, Callable[[str], str]] = {
    "pdf": extract_text_from_pdf,
    "docx": extract_text_from_docx,
    "doc": extract_text_from_docx,
    "png": extract_text_from_image,
    "jpg": extract_text_from_image,
    "jpeg": extract_text_from_image,
}


def parse_file(path: str, ext: str) -> str:
    parser = PARSER_MAP.get(ext.lower())
    if not parser:
        return ""
    return parser(path)
