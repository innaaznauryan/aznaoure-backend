from google import genai
from google.genai import types
from app.core.config import settings

_client = genai.Client(api_key=settings.GEMINI_API_KEY)
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 768


def embed_text(text: str) -> list[float]:
    result = _client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIMENSIONS),
    )
    return result.embeddings[0].values


def product_embedding_input(product) -> str:
    """Text blob that gets embedded for a product."""
    name = product.name or {}
    description = product.description or {}
    category = getattr(product.category, "value", product.category)

    parts = [
        name.get("en"),
        description.get("en"),
        category,
        name.get("hy"),
        description.get("hy"),
    ]
    return " | ".join(p for p in parts if p)