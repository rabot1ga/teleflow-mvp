"""
Celery tasks for Promotion Service.
"""

import asyncio
from datetime import datetime

from celery import Task

from app.celery_app import celery_app
from app.database import async_session_factory
from app.models.promotion import PromotionTask, PromotionTaskStatus, PromotionTaskType
from app.services.promotion_executor import PromotionExecutor


class DatabaseTask(Task):
    """Base task with database session."""

    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = async_session_factory
        return self._db


@celery_app.task(base=DatabaseTask, bind=True, max_retries=3)
def execute_promotion_task(self, task_id: str) -> dict:
    """
    Execute promotion task.
    
    Args:
        task_id: UUID of the promotion task
        
    Returns:
        dict: Task execution result
    """
    import asyncio
    
    async def _execute():
        async with async_session_factory() as session:
            # Get task
            from sqlalchemy import select
            result = await session.execute(
                select(PromotionTask).where(PromotionTask.id == task_id)
            )
            task = result.scalar_one_or_none()

            if not task:
                return {"success": False, "error": "Task not found"}

            try:
                executor = PromotionExecutor(task, session)
                
                if task.task_type == PromotionTaskType.PARSE:
                    result = await executor.execute_parse()
                elif task.task_type == PromotionTaskType.INVITE:
                    result = await executor.execute_invite()
                elif task.task_type == PromotionTaskType.MASSLOOK:
                    result = await executor.execute_masslook()
                elif task.task_type == PromotionTaskType.COMMENT:
                    result = await executor.execute_comment()
                else:
                    raise ValueError(f"Unknown task type: {task.task_type}")

                # Update task status
                task.status = PromotionTaskStatus.COMPLETED
                task.completed_at = datetime.utcnow()
                task.processed_count = result.get("processed", 0)
                task.success_count = result.get("success", 0)
                task.failed_count = result.get("failed", 0)
                await session.commit()

                return {
                    "success": True,
                    "task_id": task_id,
                    "processed": result.get("processed", 0),
                    "success": result.get("success", 0),
                    "failed": result.get("failed", 0),
                }

            except Exception as e:
                # Update task status
                task.status = PromotionTaskStatus.FAILED
                task.error_message = str(e)
                await session.commit()

                return {
                    "success": False,
                    "error": str(e),
                }

    return asyncio.run(_execute())
