from dataclasses import dataclass
import os
import httpx

from app.core.config import settings


@dataclass(slots=True)
class GeminiResponse:
    text: str


class GeminiClient:
    def __init__(self, api_key: str | None = None):
        # support multiple keys; pick first by default
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = settings.gemini_api_keys[0] if settings.gemini_api_keys else None

    def generate(self, prompt: str) -> GeminiResponse:
        if not self.api_key:
            # fallback: return a deterministic placeholder for local dev
            return GeminiResponse(text=f"[DUMMY SUMMARY] {prompt[:500]}")

        # Example HTTP call - adapt to actual Gemini REST API
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"prompt": prompt}
        with httpx.Client(timeout=60.0) as client:
            resp = client.post("https://api.gemini.example/v1/generate", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        # Expecting data["text"] or similar from real API
        text = data.get("text") or data.get("output") or ""
        return GeminiResponse(text=text)
