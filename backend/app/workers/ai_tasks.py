from datetime import datetime
from uuid import UUID
import asyncio

from app.workers.celery_app import celery_app


@celery_app.task(name="ai.generate_summary")
def generate_summary(upload_id: str):
    """Generate a summary for the given upload using AIService and persist it."""
    try:
        from app.db.session import AsyncSessionLocal
        from app.repositories.upload_repo import UploadRepository
        from app.repositories.summary_repo import SummaryRepository
        from app.repositories.ai_usage_repo import AIUsageRepository
        from app.services.ai import AIService

        async def _run():
            async with AsyncSessionLocal() as session:
                upload_repo = UploadRepository(session)
                upload = await upload_repo.get(UUID(upload_id))
                if not upload or not upload.extracted_text:
                    return {"status": "no_text"}

                ai = AIService()
                resp = ai.summarize(upload.extracted_text)

                # Create summary record
                summary_repo = SummaryRepository(session)
                summary_text = resp.get("summary") if isinstance(resp, dict) else str(resp)
                await summary_repo.create({
                    "upload_id": upload.id,
                    "user_id": upload.user_id,
                    "summary_text": summary_text or "",
                    "key_concepts": resp.get("key_concepts", []),
                    "definitions": resp.get("definitions", []),
                    "word_count": len((summary_text or "").split()),
                })

                # Log AI usage (best-effort)
                ai_repo = AIUsageRepository(session)
                await ai_repo.create({
                    "user_id": upload.user_id,
                    "upload_id": upload.id,
                    "operation": "summarize",
                    "model": "gemini",
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "latency_ms": None,
                    "success": True,
                })

                return {"status": "ok"}

        asyncio.run(_run())
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "error", "error": str(exc), "time": datetime.utcnow().isoformat()}


@celery_app.task(name="ai.generate_quiz")
def generate_quiz(upload_id: str):
    """Generate a quiz for the given upload using AIService and persist it."""
    try:
        from app.db.session import AsyncSessionLocal
        from app.repositories.upload_repo import UploadRepository
        from app.repositories.quiz_repo import QuizRepository
        from app.repositories.ai_usage_repo import AIUsageRepository
        from app.services.ai import AIService

        async def _run():
            async with AsyncSessionLocal() as session:
                upload_repo = UploadRepository(session)
                upload = await upload_repo.get(UUID(upload_id))
                if not upload or not upload.extracted_text:
                    return {"status": "no_text"}

                ai = AIService()
                resp = ai.generate_quiz(upload.extracted_text)

                # Create quiz record
                quiz_repo = QuizRepository(session)
                questions = resp.get("questions") if isinstance(resp, dict) else {}
                await quiz_repo.create({
                    "upload_id": upload.id,
                    "user_id": upload.user_id,
                    "title": resp.get("title") or upload.original_filename,
                    "difficulty": resp.get("difficulty", "medium"),
                    "question_count": len(questions) if isinstance(questions, list) else 0,
                    "question_types": [q.get("type") for q in questions] if isinstance(questions, list) else [],
                    "questions": questions,
                })

                # Log AI usage (best-effort)
                ai_repo = AIUsageRepository(session)
                await ai_repo.create({
                    "user_id": upload.user_id,
                    "upload_id": upload.id,
                    "operation": "generate_quiz",
                    "model": "gemini",
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "latency_ms": None,
                    "success": True,
                })

                return {"status": "ok"}

        asyncio.run(_run())
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "error", "error": str(exc), "time": datetime.utcnow().isoformat()}
