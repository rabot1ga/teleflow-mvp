"""Pydantic schemas for Analytics API."""

from typing import Dict, List

from pydantic import BaseModel, Field


class OverviewResponse(BaseModel):
    """Overview dashboard response."""

    period: Dict
    totals: Dict
    daily: List[Dict]


class ContentStatsResponse(BaseModel):
    """Content statistics response."""

    period: Dict
    articles: Dict
    approval_rate: float
    daily: List[Dict]


class FunnelStatsResponse(BaseModel):
    """Funnel statistics response."""

    period: Dict
    funnel: Dict
    daily: List[Dict]


class BroadcastStatsResponse(BaseModel):
    """Broadcast statistics response."""

    period: Dict
    broadcasts: Dict
    daily: List[Dict]


class PromotionStatsResponse(BaseModel):
    """Promotion statistics response."""

    period: Dict
    promotion: Dict
    daily: List[Dict]
