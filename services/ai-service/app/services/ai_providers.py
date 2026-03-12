"""
AI Providers - OpenAI, Anthropic, Ollama.
"""

import hashlib
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import httpx


class AIProviderBase(ABC):
    """Base class for AI providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Dict:
        """Generate text from prompt."""
        pass

    @abstractmethod
    async def rewrite(
        self,
        text: str,
        style: str = "neutral",
        tone: str = "formal",
    ) -> Dict:
        """Rewrite text in different style."""
        pass

    @abstractmethod
    async def summarize(
        self,
        text: str,
        max_length: int = 100,
    ) -> Dict:
        """Summarize text."""
        pass

    @abstractmethod
    async def classify(
        self,
        text: str,
        categories: List[str],
    ) -> Dict:
        """Classify text into categories."""
        pass


class OpenAIProvider(AIProviderBase):
    """OpenAI API provider."""

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = 60.0

    async def _make_request(
        self,
        model: str,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Dict:
        """Make request to OpenAI API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "text": data["choices"][0]["message"]["content"],
                "input_tokens": data["usage"]["prompt_tokens"],
                "output_tokens": data["usage"]["completion_tokens"],
                "model": model,
            }

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Dict:
        """Generate text from prompt."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        return await self._make_request(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def rewrite(
        self,
        text: str,
        style: str = "neutral",
        tone: str = "formal",
    ) -> Dict:
        """Rewrite text in different style."""
        system_prompt = f"You are a professional editor. Rewrite text in {style} style with {tone} tone."
        prompt = f"Rewrite this text:\n\n{text}"
        
        return await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=2048,
        )

    async def summarize(
        self,
        text: str,
        max_length: int = 100,
    ) -> Dict:
        """Summarize text."""
        system_prompt = f"Summarize the text in {max_length} words or less. Keep only the most important information."
        prompt = f"Summarize this text:\n\n{text}"
        
        return await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=max_length * 2,
        )

    async def classify(
        self,
        text: str,
        categories: List[str],
    ) -> Dict:
        """Classify text into categories."""
        categories_str = ", ".join(categories)
        system_prompt = f"Classify the text into one of these categories: {categories_str}. Return only the category name."
        prompt = f"Classify this text:\n\n{text}"
        
        result = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.1,
            max_tokens=50,
        )
        
        # Extract category from result
        predicted_category = result["text"].strip()
        
        return {
            "category": predicted_category,
            "confidence": 0.9,  # OpenAI doesn't provide confidence, use placeholder
            "all_categories": categories,
        }


class AnthropicProvider(AIProviderBase):
    """Anthropic API provider."""

    def __init__(self, api_key: str, base_url: str = "https://api.anthropic.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = 60.0

    async def _make_request(
        self,
        model: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
    ) -> Dict:
        """Make request to Anthropic API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": model,
                    "max_tokens": max_tokens,
                    "system": system_prompt or "You are a helpful assistant.",
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "text": data["content"][0]["text"],
                "input_tokens": data.get("usage", {}).get("input_tokens", 0),
                "output_tokens": data.get("usage", {}).get("output_tokens", 0),
                "model": model,
            }

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Dict:
        """Generate text from prompt."""
        return await self._make_request(
            model="claude-3-haiku-20240307",
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
        )

    async def rewrite(
        self,
        text: str,
        style: str = "neutral",
        tone: str = "formal",
    ) -> Dict:
        """Rewrite text in different style."""
        system_prompt = f"You are a professional editor. Rewrite text in {style} style with {tone} tone."
        prompt = f"Rewrite this text:\n\n{text}"
        
        return await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2048,
        )

    async def summarize(
        self,
        text: str,
        max_length: int = 100,
    ) -> Dict:
        """Summarize text."""
        system_prompt = f"Summarize the text in {max_length} words or less."
        prompt = f"Summarize this text:\n\n{text}"
        
        return await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_length * 2,
        )

    async def classify(
        self,
        text: str,
        categories: List[str],
    ) -> Dict:
        """Classify text into categories."""
        categories_str = ", ".join(categories)
        system_prompt = f"Classify the text into one of these categories: {categories_str}. Return only the category name."
        prompt = f"Classify this text:\n\n{text}"
        
        result = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=50,
        )
        
        predicted_category = result["text"].strip()
        
        return {
            "category": predicted_category,
            "confidence": 0.9,
            "all_categories": categories,
        }


class OllamaProvider(AIProviderBase):
    """Ollama API provider (local models)."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.timeout = 120.0  # Local models can be slow

    async def _make_request(
        self,
        model: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
    ) -> Dict:
        """Make request to Ollama API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "system": system_prompt or "",
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                    },
                },
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "text": data.get("response", ""),
                "input_tokens": 0,  # Ollama doesn't provide token counts
                "output_tokens": 0,
                "model": model,
            }

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Dict:
        """Generate text from prompt."""
        return await self._make_request(
            model="llama3",
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
        )

    async def rewrite(
        self,
        text: str,
        style: str = "neutral",
        tone: str = "formal",
    ) -> Dict:
        """Rewrite text in different style."""
        system_prompt = f"Rewrite text in {style} style with {tone} tone."
        prompt = f"Rewrite this text:\n\n{text}"
        
        return await self._make_request(
            model="llama3",
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2048,
        )

    async def summarize(
        self,
        text: str,
        max_length: int = 100,
    ) -> Dict:
        """Summarize text."""
        system_prompt = f"Summarize in {max_length} words or less."
        prompt = f"Summarize:\n\n{text}"
        
        return await self._make_request(
            model="llama3",
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_length * 2,
        )

    async def classify(
        self,
        text: str,
        categories: List[str],
    ) -> Dict:
        """Classify text into categories."""
        categories_str = ", ".join(categories)
        system_prompt = f"Classify into one of: {categories_str}. Return only category."
        prompt = f"Classify:\n\n{text}"
        
        result = await self._make_request(
            model="llama3",
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=50,
        )
        
        predicted_category = result["text"].strip()
        
        return {
            "category": predicted_category,
            "confidence": 0.9,
            "all_categories": categories,
        }
