"""API routers for promotion tasks."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session
from app.models.promotion import PromotionTask, PromotionTaskStatus, PromotionTaskType
from app.schemas.promotion import (
    PromotionTaskCreate,
    PromotionTaskResponse,
    PromotionTaskUpdate,
)
from teleflow_common.schemas.responses import StandardResponse

router = APIRouter(prefix="/tasks", tags=["Promotion Tasks"])


@router.post("", response_model=StandardResponse[PromotionTaskResponse])
async def create_task(
    task_data: PromotionTaskCreate,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[PromotionTaskResponse]:
    """Create a new promotion task."""
    task = PromotionTask(
        project_id=task_data.project_id,
        name=task_data.name,
        task_type=PromotionTaskType(task_data.task_type.value),
        target_chat_id=task_data.target_chat_id,
        target_chat_username=task_data.target_chat_username,
        source_chat_id=task_data.source_chat_id,
        source_chat_username=task_data.source_chat_username,
        parse_filters=task_data.parse_filters,
        config=task_data.config,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return StandardResponse[PromotionTaskResponse](
        success=True,
        data=PromotionTaskResponse.model_validate(task),
    )


@router.get("", response_model=StandardResponse[list[PromotionTaskResponse]])
async def list_tasks(
    project_id: str,
    task_type: str | None = Query(None),
    status: str | None = Query(None),
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[list[PromotionTaskResponse]]:
    """List all promotion tasks for a project."""
    query = select(PromotionTask).where(PromotionTask.project_id == project_id)

    if task_type:
        query = query.where(PromotionTask.task_type == task_type)
    if status:
        query = query.where(PromotionTask.status == status)

    result = await session.execute(query.order_by(PromotionTask.created_at.desc()))
    tasks = result.scalars().all()

    return StandardResponse[list[PromotionTaskResponse]](
        success=True,
        data=[PromotionTaskResponse.model_validate(task) for task in tasks],
    )


@router.get("/{task_id}", response_model=StandardResponse[PromotionTaskResponse])
async def get_task(
    task_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[PromotionTaskResponse]:
    """Get task by ID."""
    result = await session.execute(
        select(PromotionTask).where(PromotionTask.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return StandardResponse[PromotionTaskResponse](
        success=True,
        data=PromotionTaskResponse.model_validate(task),
    )


@router.delete("/{task_id}", response_model=StandardResponse[dict])
async def delete_task(
    task_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Delete task by ID."""
    result = await session.execute(
        select(PromotionTask).where(PromotionTask.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    await session.delete(task)
    await session.commit()

    return StandardResponse[dict](
        success=True,
        data={"message": "Task deleted"},
    )


@router.post("/{task_id}/start", response_model=StandardResponse[dict])
async def start_task(
    task_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Start promotion task."""
    from datetime import datetime
    from app.tasks.promotion import execute_promotion_task
    
    result = await session.execute(
        select(PromotionTask).where(PromotionTask.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.status not in [PromotionTaskStatus.PENDING, PromotionTaskStatus.FAILED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task cannot be started. Current status: {task.status.value}",
        )

    task.status = PromotionTaskStatus.RUNNING
    task.started_at = datetime.utcnow()
    await session.commit()

    # Start Celery task
    execute_promotion_task.delay(str(task.id))

    return StandardResponse[dict](
        success=True,
        data={
            "message": "Task started",
            "task_id": task_id,
        },
    )


@router.post("/{task_id}/cancel", response_model=StandardResponse[dict])
async def cancel_task(
    task_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Cancel promotion task."""
    result = await session.execute(
        select(PromotionTask).where(PromotionTask.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.status != PromotionTaskStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task cannot be cancelled. Current status: {task.status.value}",
        )

    task.status = PromotionTaskStatus.CANCELLED
    await session.commit()

    return StandardResponse[dict](
        success=True,
        data={
            "message": "Task cancelled",
            "task_id": task_id,
        },
    )
