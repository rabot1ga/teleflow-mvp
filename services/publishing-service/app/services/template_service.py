"""
PublishTemplate service.
"""

from typing import List, Optional, Tuple

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.template import PublishTemplate
from app.schemas.template import PublishTemplateCreate, PublishTemplateUpdate

logger = structlog.get_logger()


class PublishTemplateService:
    """PublishTemplate business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_template(self, data: PublishTemplateCreate) -> PublishTemplate:
        """Create a new publish template."""
        template = PublishTemplate(
            project_id=data.project_id,
            name=data.name,
            body=data.body,
            description=data.description,
            parse_mode=data.parse_mode,
            disable_preview=data.disable_preview,
            buttons=data.buttons,
            scope=data.scope,
            scope_value=data.scope_value,
            is_active=data.is_active,
        )

        self.db.add(template)
        await self.db.flush()

        logger.info(
            "publish_template_created",
            template_id=template.id,
            name=template.name,
        )

        return template

    async def get_by_id(self, template_id: str) -> Optional[PublishTemplate]:
        """Get template by ID."""
        result = await self.db.execute(
            select(PublishTemplate).where(PublishTemplate.id == template_id)
        )
        return result.scalar_one_or_none()

    async def list_templates(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None,
    ) -> Tuple[List[PublishTemplate], int]:
        """List templates with pagination."""
        query = select(PublishTemplate).where(PublishTemplate.project_id == project_id)

        if is_active is not None:
            query = query.where(PublishTemplate.is_active == is_active)

        # Get total count
        count_query = select(PublishTemplate.id).where(PublishTemplate.project_id == project_id)
        if is_active is not None:
            count_query = count_query.where(PublishTemplate.is_active == is_active)
        total_result = await self.db.execute(count_query)
        total = len(total_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(PublishTemplate.created_at.desc())
        result = await self.db.execute(query)
        templates = result.scalars().all()

        return list(templates), total

    async def update_template(
        self,
        template: PublishTemplate,
        data: PublishTemplateUpdate,
    ) -> PublishTemplate:
        """Update template."""
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(template, field, value)

        await self.db.flush()

        logger.info(
            "publish_template_updated",
            template_id=template.id,
            fields=list(update_data.keys()),
        )

        return template

    async def delete_template(self, template: PublishTemplate) -> None:
        """Delete template."""
        await self.db.delete(template)

        logger.info(
            "publish_template_deleted",
            template_id=template.id,
        )
