from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
EMBEDDING_DIMENSIONS = 384


def embed_text(text: str) -> list[float]:
    embedding = _model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


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