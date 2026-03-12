from app.celery_app import celery_app

@celery_app.task
def parse_users(task_id: str) -> dict:
    return {"status": "not_implemented"}

@celery_app.task
def invite_users(task_id: str) -> dict:
    return {"status": "not_implemented"}

@celery_app.task
def masslook(task_id: str) -> dict:
    return {"status": "not_implemented"}
