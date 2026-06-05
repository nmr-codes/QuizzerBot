from typing import Any

from app.integrations.gemini import GeminiClient


class GeminiGenerator:
    def __init__(self, api_key: str | None = None):
        self.client = GeminiClient(api_key=api_key)

    def run_prompt(self, prompt: str) -> dict[str, Any]:
        resp = self.client.generate(prompt)
        # Try to parse JSON from the response; fallback to raw text
        text = resp.text
        try:
            import json

            return json.loads(text)
        except Exception:
            return {"text": text}
