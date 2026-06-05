from datetime import datetime
import os
import asyncio
from uuid import UUID

from app.workers.celery_app import celery_app

from app.file_processing.parser_factory import parse_file


@celery_app.task(name="file.process_upload")
def process_upload(upload_id: str, storage_path: str, filename: str):
    """Celery task to extract text from an uploaded file and update the Upload record."""
    try:
        ext = os.path.splitext(filename)[1].lstrip(".").lower()
        text = parse_file(storage_path, ext)

        # write extracted text to sidecar for debugging
        try:
            with open(storage_path + ".extracted.txt", "w", encoding="utf-8") as f:
                f.write(text or "")
        except Exception:
            pass

        # update DB asynchronously
        async def _update():
            from app.db.session import AsyncSessionLocal
            from app.repositories.upload_repo import UploadRepository

            async with AsyncSessionLocal() as session:
                repo = UploadRepository(session)
                try:
                    wc = len((text or "").split())
                    await repo.update(UUID(upload_id), {"extracted_text": text, "word_count": wc, "processing_status": "done", "processing_ended_at": datetime.utcnow()})
                except Exception:
                    try:
                        await repo.update(UUID(upload_id), {"processing_status": "error"})
                    except Exception:
                        pass

        try:
            asyncio.run(_update())
        except Exception:
            pass

        # enqueue AI generation tasks
        try:
            # import here to avoid circular imports
            from app.workers.ai_tasks import generate_summary, generate_quiz

            generate_summary.delay(str(upload_id))
            generate_quiz.delay(str(upload_id))
        except Exception:
            pass

        return {"status": "ok", "chars": len(text or "")}
    except Exception as exc:
        return {"status": "error", "error": str(exc), "time": datetime.utcnow().isoformat()}
