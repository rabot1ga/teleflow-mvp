"""
AI Service with caching and usage tracking.
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

import redis.asyncio as redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai import AIProvider, AIRequest, AIUsage
from app.services.ai_providers import (
    AIProviderBase,
    OpenAIProvider,
    AnthropicProvider,
    OllamaProvider,
)


class AIService:
    """Main AI service with caching and tracking."""

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        ollama_base_url: str = "http://localhost:11434",
        redis_url: str = "redis://redis:6379/0",
        cache_ttl: int = 86400,  # 24 hours
    ):
        self.providers: Dict[str, AIProviderBase] = {}
        
        if openai_api_key:
            self.providers["openai"] = OpenAIProvider(openai_api_key)
        
        if anthropic_api_key:
            self.providers["anthropic"] = AnthropicProvider(anthropic_api_key)
        
        self.providers["ollama"] = OllamaProvider(ollama_base_url)
        
        self.redis = redis.from_url(redis_url)
        self.cache_ttl = cache_ttl

    def _get_cache_key(
        self,
        operation: str,
        text: str,
        parameters: Optional[Dict] = None,
    ) -> str:
        """Generate cache key for request."""
        key_data = {
            "operation": operation,
            "text": text,
            "parameters": parameters or {},
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return f"ai:{operation}:{hashlib.sha256(key_str.encode()).hexdigest()}"

    async def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Get result from cache."""
        try:
            cached = await self.redis.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception:
            pass
        return None

    async def _save_to_cache(
        self,
        cache_key: str,
        result: Dict,
    ) -> None:
        """Save result to cache."""
        try:
            await self.redis.setex(
                cache_key,
                self.cache_ttl,
                json.dumps(result),
            )
        except Exception:
            pass

    async def _save_request(
        self,
        session: AsyncSession,
        project_id: str,
        provider: str,
        model: str,
        operation: str,
        input_text: str,
        output_text: Optional[str],
        parameters: Optional[Dict],
        input_tokens: Optional[int],
        output_tokens: Optional[int],
        latency_ms: Optional[int],
        status: str,
        error_message: Optional[str],
        is_cached: bool,
        cache_key: Optional[str],
    ) -> AIRequest:
        """Save AI request to database."""
        request = AIRequest(
            project_id=project_id,
            provider=AIProvider(provider),
            model=model,
            operation=operation,
            input_text=input_text,
            output_text=output_text,
            parameters=parameters,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            status=status,
            error_message=error_message,
            is_cached=is_cached,
            cache_key=cache_key,
        )
        session.add(request)
        await session.commit()
        await session.refresh(request)
        return request

    async def _update_usage(
        self,
        session: AsyncSession,
        project_id: str,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: int,
        is_cached: bool,
        is_success: bool,
    ) -> None:
        """Update daily usage statistics."""
        today = datetime.utcnow().date()
        
        result = await session.execute(
            select(AIUsage).where(
                AIUsage.project_id == project_id,
                AIUsage.date == today,
                AIUsage.provider == AIProvider(provider),
                AIUsage.model == model,
            )
        )
        usage = result.scalar_one_or_none()
        
        if not usage:
            usage = AIUsage(
                project_id=project_id,
                date=today,
                provider=AIProvider(provider),
                model=model,
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                cached_requests=0,
                total_input_tokens=0,
                total_output_tokens=0,
            )
            session.add(usage)
        
        usage.total_requests += 1
        if is_success:
            usage.successful_requests += 1
        else:
            usage.failed_requests += 1
        if is_cached:
            usage.cached_requests += 1
        
        usage.total_input_tokens += input_tokens or 0
        usage.total_output_tokens += output_tokens or 0
        
        # Update average latency
        total_req = usage.total_requests
        if total_req > 0:
            usage.avg_latency_ms = (
                (usage.avg_latency_ms or 0) * (total_req - 1) + latency_ms
            ) // total_req
            usage.max_latency_ms = max(usage.max_latency_ms or 0, latency_ms)
        
        await session.commit()

    def _get_provider(self, provider_name: Optional[str] = None) -> AIProviderBase:
        """Get AI provider by name or best available."""
        if provider_name:
            if provider_name not in self.providers:
                raise ValueError(f"Unknown provider: {provider_name}")
            return self.providers[provider_name]
        
        # Return best available provider
        if "openai" in self.providers:
            return self.providers["openai"]
        if "anthropic" in self.providers:
            return self.providers["anthropic"]
        if "ollama" in self.providers:
            return self.providers["ollama"]
        
        raise ValueError("No AI providers available")

    async def rewrite(
        self,
        text: str,
        project_id: str,
        session: AsyncSession,
        style: str = "neutral",
        tone: str = "formal",
        provider: Optional[str] = None,
    ) -> Dict:
        """Rewrite text in different style."""
        start_time = time.time()
        cache_key = self._get_cache_key("rewrite", text, {"style": style, "tone": tone})
        
        # Check cache
        cached_result = await self._get_from_cache(cache_key)
        if cached_result:
            latency_ms = int((time.time() - start_time) * 1000)
            await self._save_request(
                session=session,
                project_id=project_id,
                provider=provider or "openai",
                model="cached",
                operation="rewrite",
                input_text=text,
                output_text=cached_result.get("text"),
                parameters={"style": style, "tone": tone},
                input_tokens=0,
                output_tokens=0,
                latency_ms=latency_ms,
                status="completed",
                error_message=None,
                is_cached=True,
                cache_key=cache_key,
            )
            return {**cached_result, "is_cached": True}
        
        # Generate
        ai_provider = self._get_provider(provider)
        try:
            result = await ai_provider.rewrite(text, style, tone)
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Save to cache
            await self._save_to_cache(cache_key, result)
            
            # Save to database
            await self._save_request(
                session=session,
                project_id=project_id,
                provider=provider or "openai",
                model=result.get("model", "unknown"),
                operation="rewrite",
                input_text=text,
                output_text=result.get("text"),
                parameters={"style": style, "tone": tone},
                input_tokens=result.get("input_tokens"),
                output_tokens=result.get("output_tokens"),
                latency_ms=latency_ms,
                status="completed",
                error_message=None,
                is_cached=False,
                cache_key=cache_key,
            )
            
            # Update usage
            await self._update_usage(
                session=session,
                project_id=project_id,
                provider=provider or "openai",
                model=result.get("model", "unknown"),
                input_tokens=result.get("input_tokens", 0),
                output_tokens=result.get("output_tokens", 0),
                latency_ms=latency_ms,
                is_cached=False,
                is_success=True,
            )
            
            return {**result, "is_cached": False}
            
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            await self._save_request(
                session=session,
                project_id=project_id,
                provider=provider or "openai",
                model="unknown",
                operation="rewrite",
                input_text=text,
                output_text=None,
                parameters={"style": style, "tone": tone},
                input_tokens=0,
                output_tokens=0,
                latency_ms=latency_ms,
                status="failed",
                error_message=str(e),
                is_cached=False,
                cache_key=cache_key,
            )
            raise

    async def summarize(
        self,
        text: str,
        project_id: str,
        session: AsyncSession,
        max_length: int = 100,
        provider: Optional[str] = None,
    ) -> Dict:
        """Summarize text."""
        start_time = time.time()
        cache_key = self._get_cache_key("summarize", text, {"max_length": max_length})
        
        # Check cache
        cached_result = await self._get_from_cache(cache_key)
        if cached_result:
            latency_ms = int((time.time() - start_time) * 1000)
            await self._save_request(
                session=session,
                project_id=project_id,
                provider=provider or "openai",
                model="cached",
                operation="summarize",
                input_text=text,
                output_text=cached_result.get("text"),
                parameters={"max_length": max_length},
                input_tokens=0,
                output_tokens=0,
                latency_ms=latency_ms,
                status="completed",
                error_message=None,
                is_cached=True,
                cache_key=cache_key,
            )
            return {**cached_result, "is_cached": True}
        
        # Generate
        ai_provider = self._get_provider(provider)
        try:
            result = await ai_provider.summarize(text, max_length)
            latency_ms = int((time.time() - start_time) * 1000)
            
            await self._save_to_cache(cache_key, result)
            
            await self._save_request(
                session=session,
                project_id=project_id,
                provider=provider or "openai",
                model=result.get("model", "unknown"),
                operation="summarize",
                input_text=text,
                output_text=result.get("text"),
                parameters={"max_length": max_length},
                input_tokens=result.get("input_tokens"),
                output_tokens=result.get("output_tokens"),
                latency_ms=latency_ms,
                status="completed",
                error_message=None,
                is_cached=False,
                cache_key=cache_key,
            )
            
            await self._update_usage(
                session=session,
                project_id=project_id,
                provider=provider or "openai",
                model=result.get("model", "unknown"),
                input_tokens=result.get("input_tokens", 0),
                output_tokens=result.get("output_tokens", 0),
                latency_ms=latency_ms,
                is_cached=False,
                is_success=True,
            )
            
            return {**result, "is_cached": False}
            
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            await self._save_request(
                session=session,
                project_id=project_id,
                provider=provider or "openai",
                model="unknown",
                operation="summarize",
                input_text=text,
                output_text=None,
                parameters={"max_length": max_length},
                input_tokens=0,
                output_tokens=0,
                latency_ms=latency_ms,
                status="failed",
                error_message=str(e),
                is_cached=False,
                cache_key=cache_key,
            )
            raise

    async def classify(
        self,
        text: str,
        categories: List[str],
        project_id: str,
        session: AsyncSession,
        provider: Optional[str] = None,
    ) -> Dict:
        """Classify text into categories."""
        start_time = time.time()
        cache_key = self._get_cache_key("classify", text, {"categories": categories})
        
        # Check cache
        cached_result = await self._get_from_cache(cache_key)
        if cached_result:
            latency_ms = int((time.time() - start_time) * 1000)
            return {**cached_result, "is_cached": True}
        
        # Generate
        ai_provider = self._get_provider(provider)
        try:
            result = await ai_provider.classify(text, categories)
            latency_ms = int((time.time() - start_time) * 1000)
            
            await self._save_to_cache(cache_key, result)
            
            return {**result, "is_cached": False}
            
        except Exception as e:
            raise
