from app.celery_app import celery_app

@celery_app.task
def rewrite_text(text: str, prompt: str) -> dict:
    return {"status": "not_implemented"}

@celery_app.task
def summarize_text(text: str, max_words: int) -> dict:
    return {"status": "not_implemented"}

@celery_app.task
def classify_text(text: str, categories: list) -> dict:
    return {"status": "not_implemented"}
