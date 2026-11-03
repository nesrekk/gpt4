"""Part A (Q1) dataset preparation and Part B (Q3) FAQ embedding generation."""
import logging

# Hide a harmless macOS-only torch log line printed while importing transformers
logging.getLogger("torch.distributed.elastic.multiprocessing.redirects").setLevel(logging.ERROR)
import os
import sys

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Windows terminals may not use UTF-8, so print characters like ₹ and • safely there too
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
EMBED_MODEL_NAME = "all-mpnet-base-v2"
EMBED_MODEL_PATH = os.path.join(MODEL_DIR, EMBED_MODEL_NAME)
FAQ_EMBEDDINGS_PATH = os.path.join(MODEL_DIR, "faq_embeddings.npy")


def load_datasets():
    products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    faqs = pd.read_csv(os.path.join(DATA_DIR, "faqs.csv"))
    reviews = pd.read_csv(os.path.join(DATA_DIR, "reviews.csv"))
    return products, faqs, reviews


def describe_dataset(name, df):
    """Q1: display first five records, rows, columns and attributes."""
    print("=" * 70)
    print(f"Dataset : {name}")
    print("=" * 70)
    print(df.head().to_string(index=False))
    print(f"\nRows       : {df.shape[0]}")
    print(f"Columns    : {df.shape[1]}")
    print(f"Attributes : {', '.join(df.columns)}\n")


def load_embedding_model():
    """Load the sentence-transformer from models/ (download once if missing)."""
    if os.path.isdir(EMBED_MODEL_PATH):
        return SentenceTransformer(EMBED_MODEL_PATH)
    model = SentenceTransformer(EMBED_MODEL_NAME)
    model.save(EMBED_MODEL_PATH)
    return model


def create_faq_embeddings(faqs):
    """Q3: generate and store FAQ embeddings."""
    model = load_embedding_model()
    # Question + answer together gives better matches for paraphrased questions
    texts = (faqs["Question"] + " " + faqs["Answer"]).tolist()
    embeddings = model.encode(texts, normalize_embeddings=True)
    np.save(FAQ_EMBEDDINGS_PATH, embeddings)
    return embeddings


if __name__ == "__main__":
    os.makedirs(MODEL_DIR, exist_ok=True)
    products, faqs, reviews = load_datasets()
    describe_dataset("Products", products)
    describe_dataset("FAQs", faqs)
    describe_dataset("Reviews", reviews)

    print("Generating FAQ embeddings...")
    embeddings = create_faq_embeddings(faqs)
    print(f"FAQ embeddings shape : {embeddings.shape}")
    print(f"Saved to             : models/{os.path.basename(FAQ_EMBEDDINGS_PATH)}")
