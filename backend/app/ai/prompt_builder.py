def build_summary_prompt(text: str) -> str:
    return f"You are an expert tutor. Provide a concise, structured summary of the following content:\n\n{text}\n\nReturn JSON with keys: summary, key_concepts (list), definitions (list)."


def build_quiz_prompt(text: str, difficulty: str = "medium") -> str:
    return (
        f"You are an expert exam writer. From the content below, generate a {difficulty} quiz. "
        "Return JSON with keys: title, difficulty, questions (array). Each question should have: id, type, prompt, choices, correct_answer, explanation.\n\n"
        f"Content:\n{text}"
    )
