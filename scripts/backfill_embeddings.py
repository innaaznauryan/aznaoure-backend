"""One-off backfill: embeds all existing products and stores the vector.
Run once per environment after the embedding column migration is applied.

Usage:
    python -m scripts.backfill_embeddings
"""
from app.database import SessionLocal
from app.models.product import Product
from app.services.embeddings import embed_text


def build_embedding_input(product: Product) -> str:
    """Concatenate the fields worth searching on into one string."""
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


def main():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        print(f"found {len(products)} products")

        for product in products:
            text = build_embedding_input(product)
            if not text.strip():
                print(f"skipping {product.id}: no text to embed")
                continue

            try:
                embedding = embed_text(text)
                product.embedding = embedding
                db.commit()
                print(f"embedded {product.id}")
            except Exception as e:
                db.rollback()
                print(f"failed to embed {product.id}: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()