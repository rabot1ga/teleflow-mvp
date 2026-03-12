from app.celery_app import celery_app

@celery_app.task
def aggregate_daily_stats(project_id: str, date: str) -> dict:
    return {"status": "not_implemented"}

@celery_app.task
def process_event(event_type: str, payload: dict) -> dict:
    return {"status": "not_implemented"}
