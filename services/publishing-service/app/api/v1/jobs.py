"""
Publish Jobs API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_async_session
from app.schemas.job import PublishJobCreate, PublishJobList, PublishJobResponse, PublishJobUpdate
from app.services.job_service import PublishJobService
from teleflow_common.auth.dependencies import get_current_user
from teleflow_common.schemas.responses import ResponseMeta, StandardResponse

router = APIRouter(prefix="/jobs", tags=["Publish Jobs"])


def get_job_service(db=Depends(get_async_session)) -> PublishJobService:
    """Get job service instance."""
    return PublishJobService(db)


@router.post(
    "",
    response_model=StandardResponse[PublishJobResponse],
    summary="Create publish job",
)
async def create_job(
    data: PublishJobCreate,
    job_service: PublishJobService = Depends(get_job_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishJobResponse]:
    """Create a new publish job."""
    job = await job_service.create_job(data)

    return StandardResponse(
        data=PublishJobResponse.model_validate(job),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "",
    response_model=StandardResponse[PublishJobList],
    summary="List publish jobs",
)
async def list_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status_filter: str | None = Query(None, alias="status"),
    article_id: str | None = None,
    job_service: PublishJobService = Depends(get_job_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishJobList]:
    """List publish jobs with pagination and filters."""
    skip = (page - 1) * per_page
    project_id = current_user.get("project_id", "test-project")
    
    jobs, total = await job_service.list_jobs(
        project_id=project_id,
        skip=skip,
        limit=per_page,
        status=status_filter,
        article_id=article_id,
    )

    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return StandardResponse(
        data=PublishJobList(
            items=[PublishJobResponse.model_validate(j) for j in jobs],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        ),
        meta=ResponseMeta(request_id=""),
    )


@router.get(
    "/{job_id}",
    response_model=StandardResponse[PublishJobResponse],
    summary="Get publish job by ID",
)
async def get_job(
    job_id: str,
    job_service: PublishJobService = Depends(get_job_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishJobResponse]:
    """Get publish job by ID."""
    job = await job_service.get_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return StandardResponse(
        data=PublishJobResponse.model_validate(job),
        meta=ResponseMeta(request_id=""),
    )


@router.patch(
    "/{job_id}",
    response_model=StandardResponse[PublishJobResponse],
    summary="Update publish job",
)
async def update_job(
    job_id: str,
    data: PublishJobUpdate,
    job_service: PublishJobService = Depends(get_job_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishJobResponse]:
    """Update publish job."""
    job = await job_service.get_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    updated_job = await job_service.update_job(job, data)

    return StandardResponse(
        data=PublishJobResponse.model_validate(updated_job),
        meta=ResponseMeta(request_id=""),
    )


@router.delete(
    "/{job_id}",
    response_model=StandardResponse[bool],
    summary="Delete publish job",
)
async def delete_job(
    job_id: str,
    job_service: PublishJobService = Depends(get_job_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[bool]:
    """Delete publish job."""
    job = await job_service.get_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    await job_service.delete_job(job)

    return StandardResponse(data=True, meta=ResponseMeta(request_id=""))


@router.post(
    "/{job_id}/publish",
    response_model=StandardResponse[PublishJobResponse],
    summary="Publish job now",
)
async def publish_job_now(
    job_id: str,
    job_service: PublishJobService = Depends(get_job_service),
    current_user: dict = Depends(get_current_user),
) -> StandardResponse[PublishJobResponse]:
    """Trigger immediate publishing."""
    job = await job_service.get_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Update status to trigger publishing
    job.status = "pending"
    await job_service.db.flush()

    # TODO: Trigger Celery task
    # from app.tasks import publish_article
    # publish_article.delay(job.id)

    return StandardResponse(
        data=PublishJobResponse.model_validate(job),
        meta=ResponseMeta(request_id=""),
    )
