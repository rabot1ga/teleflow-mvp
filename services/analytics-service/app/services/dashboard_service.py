"""
Dashboard data service.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analytics import AnalyticsDaily, AnalyticsEvent


class DashboardService:
    """Service for dashboard data."""

    async def get_overview(
        self,
        session: AsyncSession,
        project_id: str,
        days: int = 7,
    ) -> Dict:
        """Get overview statistics."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        # Get daily stats
        result = await session.execute(
            select(AnalyticsDaily).where(
                AnalyticsDaily.project_id == project_id,
                AnalyticsDaily.date >= start_date,
                AnalyticsDaily.date <= end_date,
            )
        )
        daily_stats = result.scalars().all()

        # Aggregate totals
        total_articles = sum(s.articles_created for s in daily_stats)
        total_published = sum(s.articles_published for s in daily_stats)
        total_funnel_entries = sum(s.funnel_entries for s in daily_stats)
        total_broadcasts = sum(s.broadcasts_sent for s in daily_stats)

        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days,
            },
            "totals": {
                "articles_created": total_articles,
                "articles_published": total_published,
                "funnel_entries": total_funnel_entries,
                "funnel_completions": sum(s.funnel_completions for s in daily_stats),
                "broadcasts_sent": total_broadcasts,
                "messages_delivered": sum(s.messages_delivered for s in daily_stats),
                "users_parsed": sum(s.users_parsed for s in daily_stats),
                "users_invited": sum(s.users_invited for s in daily_stats),
            },
            "daily": [
                {
                    "date": stat.date.isoformat(),
                    "articles_created": stat.articles_created,
                    "articles_published": stat.articles_published,
                    "funnel_entries": stat.funnel_entries,
                    "broadcasts_sent": stat.broadcasts_sent,
                }
                for stat in daily_stats
            ],
        }

    async def get_content_stats(
        self,
        session: AsyncSession,
        project_id: str,
        days: int = 30,
    ) -> Dict:
        """Get content statistics."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        result = await session.execute(
            select(AnalyticsDaily).where(
                AnalyticsDaily.project_id == project_id,
                AnalyticsDaily.date >= start_date,
                AnalyticsDaily.date <= end_date,
            )
        )
        daily_stats = result.scalars().all()

        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days,
            },
            "articles": {
                "created": sum(s.articles_created for s in daily_stats),
                "approved": sum(s.articles_approved for s in daily_stats),
                "rejected": sum(s.articles_rejected for s in daily_stats),
                "published": sum(s.articles_published for s in daily_stats),
            },
            "approval_rate": (
                sum(s.articles_approved for s in daily_stats) /
                sum(s.articles_created for s in daily_stats) * 100
                if sum(s.articles_created for s in daily_stats) > 0
                else 0
            ),
            "daily": [
                {
                    "date": stat.date.isoformat(),
                    "created": stat.articles_created,
                    "approved": stat.articles_approved,
                    "rejected": stat.articles_rejected,
                    "published": stat.articles_published,
                }
                for stat in daily_stats
            ],
        }

    async def get_funnel_stats(
        self,
        session: AsyncSession,
        project_id: str,
        days: int = 30,
    ) -> Dict:
        """Get funnel statistics."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        result = await session.execute(
            select(AnalyticsDaily).where(
                AnalyticsDaily.project_id == project_id,
                AnalyticsDaily.date >= start_date,
                AnalyticsDaily.date <= end_date,
            )
        )
        daily_stats = result.scalars().all()

        total_entries = sum(s.funnel_entries for s in daily_stats)
        total_completions = sum(s.funnel_completions for s in daily_stats)

        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days,
            },
            "funnel": {
                "entries": total_entries,
                "completions": total_completions,
                "conversion_rate": (
                    total_completions / total_entries * 100 if total_entries > 0 else 0
                ),
            },
            "daily": [
                {
                    "date": stat.date.isoformat(),
                    "entries": stat.funnel_entries,
                    "completions": stat.funnel_completions,
                }
                for stat in daily_stats
            ],
        }

    async def get_broadcast_stats(
        self,
        session: AsyncSession,
        project_id: str,
        days: int = 30,
    ) -> Dict:
        """Get broadcast statistics."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        result = await session.execute(
            select(AnalyticsDaily).where(
                AnalyticsDaily.project_id == project_id,
                AnalyticsDaily.date >= start_date,
                AnalyticsDaily.date <= end_date,
            )
        )
        daily_stats = result.scalars().all()

        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days,
            },
            "broadcasts": {
                "sent": sum(s.broadcasts_sent for s in daily_stats),
                "delivered": sum(s.messages_delivered for s in daily_stats),
            },
            "daily": [
                {
                    "date": stat.date.isoformat(),
                    "sent": stat.broadcasts_sent,
                    "delivered": stat.messages_delivered,
                }
                for stat in daily_stats
            ],
        }

    async def get_promotion_stats(
        self,
        session: AsyncSession,
        project_id: str,
        days: int = 30,
    ) -> Dict:
        """Get promotion statistics."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        result = await session.execute(
            select(AnalyticsDaily).where(
                AnalyticsDaily.project_id == project_id,
                AnalyticsDaily.date >= start_date,
                AnalyticsDaily.date <= end_date,
            )
        )
        daily_stats = result.scalars().all()

        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days,
            },
            "promotion": {
                "users_parsed": sum(s.users_parsed for s in daily_stats),
                "users_invited": sum(s.users_invited for s in daily_stats),
                "userbot_actions": sum(s.userbot_actions for s in daily_stats),
            },
            "daily": [
                {
                    "date": stat.date.isoformat(),
                    "parsed": stat.users_parsed,
                    "invited": stat.users_invited,
                }
                for stat in daily_stats
            ],
        }
