"""Perplexity Agent API Configuration

This module provides configuration and utilities for integrating with 
the Perplexity Agent API - a multi-provider, interoperable API for 
building LLM applications.

Documentation: https://docs.perplexity.ai/docs/agent-api/quickstart
Notion Integration: https://www.notion.so/Perplexity-Agent-API-Integration
"""

import os
from typing import Optional, List, Dict, Any

# API Configuration
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
PERPLEXITY_BASE_URL = "https://api.perplexity.ai/v2"

# Available Models
MODELS = {
    "perplexity": {
        "sonar": "perplexity/sonar",
    },
    "anthropic": {
        "claude-opus-4-6": "anthropic/claude-opus-4-6",
        "claude-opus-4-5": "anthropic/claude-opus-4-5",
        "claude-sonnet-4-5": "anthropic/claude-sonnet-4-5",
        "claude-haiku-4-5": "anthropic/claude-haiku-4-5",
    },
    "openai": {
        "gpt-5.2": "openai/gpt-5.2",
        "gpt-5.1": "openai/gpt-5.1",
        "gpt-5-mini": "openai/gpt-5-mini",
    },
    "google": {
        "gemini-3-pro": "google/gemini-3-pro-preview",
        "gemini-3-flash": "google/gemini-3-flash-preview",
        "gemini-2.5-pro": "google/gemini-2.5-pro",
        "gemini-2.5-flash": "google/gemini-2.5-flash",
    },
    "xai": {
        "grok-4-1-fast": "xai/grok-4-1-fast-non-reasoning",
    }
}

# Presets for quick configuration
PRESETS = {
    "fast-search": {
        "model": "xai/grok-4-1-fast-non-reasoning",
        "max_steps": 1,
        "max_tokens": 3000,
        "tools": ["web_search"],
    },
    "pro-search": {
        "model": "openai/gpt-5.1",
        "max_steps": 3,
        "max_tokens": 3000,
        "tools": ["web_search", "fetch_url"],
    },
    "deep-research": {
        "model": "openai/gpt-5.2",
        "max_steps": 10,
        "max_tokens": 10000,
        "tools": ["web_search", "fetch_url"],
    },
    "advanced-deep-research": {
        "model": "anthropic/claude-opus-4-6",
        "max_steps": 10,
        "max_tokens": 10000,
        "tools": ["web_search", "fetch_url"],
    },
}


def get_client():
    """Get a configured Perplexity client."""
    try:
        from perplexity import Perplexity
        return Perplexity(api_key=PERPLEXITY_API_KEY)
    except ImportError:
        raise ImportError("Please install perplexityai: pip install perplexityai")


def create_response(
    input_text: str,
    preset: Optional[str] = None,
    model: Optional[str] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    instructions: Optional[str] = None,
    stream: bool = False,
    **kwargs
) -> Any:
    """Create a response using the Perplexity Agent API.
    
    Args:
        input_text: The input query or message
        preset: Use a preset configuration (fast-search, pro-search, etc.)
        model: Specific model to use (overrides preset)
        tools: List of tools to enable
        instructions: System instructions for the model
        stream: Enable streaming responses
        **kwargs: Additional parameters
    
    Returns:
        Response object from the API
    """
    client = get_client()
    
    params = {
        "input": input_text,
        "stream": stream,
    }
    
    if preset:
        params["preset"] = preset
    elif model:
        params["model"] = model
    
    if tools:
        params["tools"] = tools
    
    if instructions:
        params["instructions"] = instructions
    
    params.update(kwargs)
    
    return client.responses.create(**params)


def search_web(query: str, preset: str = "pro-search") -> str:
    """Perform a web search using the Agent API.
    
    Args:
        query: Search query
        preset: Preset to use (default: pro-search)
    
    Returns:
        Response text from the search
    """
    response = create_response(
        input_text=query,
        preset=preset,
    )
    return response.output_text
