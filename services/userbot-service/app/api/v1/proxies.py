"""API routers for proxies."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session
from app.models.proxy import Proxy
from app.schemas.userbot import (
    ProxyCreate,
    ProxyResponse,
    ProxyUpdate,
    ProxyCheckResponse,
)
from teleflow_common.schemas.responses import StandardResponse

router = APIRouter(prefix="/proxies", tags=["Proxies"])


@router.post("", response_model=StandardResponse[ProxyResponse])
async def create_proxy(
    proxy_data: ProxyCreate,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[ProxyResponse]:
    """Create a new proxy for account."""
    proxy = Proxy(**proxy_data.model_dump())
    session.add(proxy)
    await session.commit()
    await session.refresh(proxy)

    return StandardResponse[ProxyResponse](
        success=True,
        data=ProxyResponse.model_validate(proxy),
    )


@router.get("", response_model=StandardResponse[list[ProxyResponse]])
async def list_proxies(
    account_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[list[ProxyResponse]]:
    """List all proxies for an account."""
    result = await session.execute(
        select(Proxy).where(Proxy.account_id == account_id)
    )
    proxies = result.scalars().all()
    
    return StandardResponse[list[ProxyResponse]](
        success=True,
        data=[ProxyResponse.model_validate(p) for p in proxies],
    )


@router.get("/{proxy_id}", response_model=StandardResponse[ProxyResponse])
async def get_proxy(
    proxy_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[ProxyResponse]:
    """Get proxy by ID."""
    result = await session.execute(
        select(Proxy).where(Proxy.id == proxy_id)
    )
    proxy = result.scalar_one_or_none()
    
    if not proxy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proxy not found",
        )
    
    return StandardResponse[ProxyResponse](
        success=True,
        data=ProxyResponse.model_validate(proxy),
    )


@router.patch("/{proxy_id}", response_model=StandardResponse[ProxyResponse])
async def update_proxy(
    proxy_id: str,
    proxy_data: ProxyUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[ProxyResponse]:
    """Update proxy."""
    result = await session.execute(
        select(Proxy).where(Proxy.id == proxy_id)
    )
    proxy = result.scalar_one_or_none()
    
    if not proxy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proxy not found",
        )
    
    update_data = proxy_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(proxy, field, value)
    
    await session.commit()
    await session.refresh(proxy)
    
    return StandardResponse[ProxyResponse](
        success=True,
        data=ProxyResponse.model_validate(proxy),
    )


@router.delete("/{proxy_id}", response_model=StandardResponse[dict])
async def delete_proxy(
    proxy_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Delete proxy."""
    result = await session.execute(
        select(Proxy).where(Proxy.id == proxy_id)
    )
    proxy = result.scalar_one_or_none()
    
    if not proxy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proxy not found",
        )
    
    await session.delete(proxy)
    await session.commit()
    
    return StandardResponse[dict](
        success=True,
        data={"message": "Proxy deleted"},
    )


@router.post("/{proxy_id}/check", response_model=StandardResponse[ProxyCheckResponse])
async def check_proxy(
    proxy_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[ProxyCheckResponse]:
    """Check if proxy is working."""
    # TODO: Implement proxy check
    return StandardResponse[ProxyCheckResponse](
        success=True,
        data=ProxyCheckResponse(
            is_working=False,
            error="Not implemented",
        ),
    )
