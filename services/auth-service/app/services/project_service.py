"""
Project service.
"""

import json
from typing import Optional

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project, ProjectMember
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectMemberAdd

logger = structlog.get_logger()


class ProjectService:
    """Project business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(
        self,
        data: ProjectCreate,
        owner_id: str,
    ) -> Project:
        """Create a new project."""
        # Check if slug exists
        result = await self.db.execute(
            select(Project).where(Project.slug == data.slug)
        )
        if result.scalar_one_or_none():
            raise ValueError("Project with this slug already exists")

        # Create project
        project = Project(
            name=data.name,
            slug=data.slug,
            owner_id=owner_id,
        )

        # Add owner as admin member
        member = ProjectMember(
            project_id=project.id,
            user_id=owner_id,
            role="admin",
        )

        self.db.add(project)
        self.db.add(member)
        await self.db.flush()

        logger.info(
            "project_created",
            project_id=project.id,
            slug=project.slug,
            owner_id=owner_id,
        )

        return project

    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """Get project by ID."""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_user_projects(self, user_id: str) -> list[Project]:
        """Get all projects for a user."""
        result = await self.db.execute(
            select(Project)
            .join(ProjectMember)
            .where(ProjectMember.user_id == user_id)
            .where(Project.is_active == True)
        )
        return list(result.scalars().all())

    async def add_member(
        self,
        project: Project,
        data: ProjectMemberAdd,
    ) -> ProjectMember:
        """Add member to project."""
        # Check if user exists
        user_result = await self.db.execute(
            select(User).where(User.id == data.user_id)
        )
        if not user_result.scalar_one_or_none():
            raise ValueError("User not found")

        # Check if already member
        existing = await self.db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == data.user_id,
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("User is already a member of this project")

        # Add member
        member = ProjectMember(
            project_id=project.id,
            user_id=data.user_id,
            role=data.role,
        )

        self.db.add(member)
        await self.db.flush()

        logger.info(
            "project_member_added",
            project_id=project.id,
            user_id=data.user_id,
            role=data.role,
        )

        return member

    async def remove_member(
        self,
        project: Project,
        user_id: str,
    ) -> None:
        """Remove member from project."""
        result = await self.db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == user_id,
            )
        )
        member = result.scalar_one_or_none()

        if not member:
            raise ValueError("User is not a member of this project")

        await self.db.delete(member)

        logger.info(
            "project_member_removed",
            project_id=project.id,
            user_id=user_id,
        )

    async def update_member_role(
        self,
        project: Project,
        user_id: str,
        new_role: str,
    ) -> ProjectMember:
        """Update member role."""
        result = await self.db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == user_id,
            )
        )
        member = result.scalar_one_or_none()

        if not member:
            raise ValueError("User is not a member of this project")

        member.role = new_role
        await self.db.flush()

        logger.info(
            "project_member_role_updated",
            project_id=project.id,
            user_id=user_id,
            role=new_role,
        )

        return member
