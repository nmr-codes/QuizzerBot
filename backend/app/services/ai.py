from typing import Any

from app.ai.prompt_builder import build_summary_prompt, build_quiz_prompt
from app.ai.generator import GeminiGenerator


class AIService:
    def __init__(self, api_key: str | None = None):
        self.generator = GeminiGenerator(api_key=api_key)

    def summarize(self, text: str) -> dict[str, Any]:
        prompt = build_summary_prompt(text)
        return self.generator.run_prompt(prompt)

    def generate_quiz(self, text: str, difficulty: str = "medium") -> dict[str, Any]:
        prompt = build_quiz_prompt(text, difficulty=difficulty)
        return self.generator.run_prompt(prompt)
