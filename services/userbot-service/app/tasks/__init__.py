from app.celery_app import celery_app

@celery_app.task
def warm_account(account_id: str) -> dict:
    return {"status": "not_implemented"}

@celery_app.task
def execute_userbot_action(action_type: str, params: dict) -> dict:
    return {"status": "not_implemented"}
