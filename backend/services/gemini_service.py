"""
PromptShield — Gemini LLM Service
Forwards safe prompts to Gemini and returns the response.
"""

import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger("promptshield.gemini")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview"



async def call_gemini(
    prompt: str,
    api_key: str,
    file_context: Optional[str] = None,
) -> str:
    """
    Send a prompt (with optional file context) to Gemini and return the text response.
    """
    # Build the full message
    if file_context:
        full_prompt = (
            f"The user has uploaded a document. Here is its content:\n\n"
            f"---\n{file_context[:12000]}\n---\n\n"
            f"User's question: {prompt}"
        )
    else:
        full_prompt = prompt

    payload = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048,
        },
    }

    url = f"{GEMINI_API_URL}?key={api_key}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload)

    if resp.status_code != 200:
        error_body = resp.text
        logger.error(f"Gemini API error {resp.status_code}: {error_body}")
        raise ValueError(f"Gemini API returned {resp.status_code}: {error_body}")

    data = resp.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected Gemini response structure: {data}")
        raise ValueError(f"Could not parse Gemini response: {e}")
