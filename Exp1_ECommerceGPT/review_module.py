"""Part E - Customer review intelligence (Q10, Q11)."""
import logging

# Hide a harmless macOS-only torch log line printed while importing transformers
logging.getLogger("torch.distributed.elastic.multiprocessing.redirects").setLevel(logging.ERROR)
import os

from transformers import pipeline

from create_embeddings import MODEL_DIR, load_datasets
from llm_utils import ask_llm

SENTIMENT_MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
SENTIMENT_MODEL_PATH = os.path.join(MODEL_DIR, "twitter-roberta-base-sentiment-latest")


def load_sentiment_model():
    """Q10: load a pre-trained 3-class (positive / neutral / negative) sentiment model."""
    if os.path.isdir(SENTIMENT_MODEL_PATH):
        return pipeline("sentiment-analysis", model=SENTIMENT_MODEL_PATH)
    classifier = pipeline("sentiment-analysis", model=SENTIMENT_MODEL_NAME)
    classifier.save_pretrained(SENTIMENT_MODEL_PATH)
    return classifier


class ReviewModule:
    def __init__(self):
        _, _, self.reviews = load_datasets()
        self.classifier = load_sentiment_model()

    def reviews_for(self, product_name):
        """Exact product name if it exists, otherwise every product that contains the text."""
        names = self.reviews["ProductName"].str.lower()
        key = product_name.strip().lower()
        exact = self.reviews[names == key]
        return exact if not exact.empty else self.reviews[names.str.contains(key, regex=False)]

    def analyze(self, product_name):
        """Q11: sentiment for each review + Ollama summary and buying suggestion."""
        subset = self.reviews_for(product_name)
        if subset.empty:
            return None
        texts = subset["Review"].tolist()
        results = self.classifier(texts)
        details = [(t, r["label"].capitalize(), r["score"]) for t, r in zip(texts, results)]
        counts = {s: sum(1 for _, label, _ in details if label == s)
                  for s in ("Positive", "Neutral", "Negative")}

        # Group identical reviews so the LLM sees themes instead of repeated lines
        grouped = {}
        for text, label, _ in details:
            grouped.setdefault((text, label), 0)
            grouped[(text, label)] += 1
        review_lines = "\n".join(f"- \"{t}\" x{n} ({label})" for (t, label), n in grouped.items())
        summary = ask_llm(
            "You summarise customer reviews for shoppers using ONLY the given reviews. "
            "Write in your own words and never repeat the same point. Use exactly this layout:\n"
            "Overall Opinion\n<one sentence>\n\nStrengths\n• <point>\n• <point>\n\n"
            "Weaknesses\n• <point>\n\nBuying Suggestion\n<one or two sentences>",
            f"Product: {product_name}\n"
            f"Sentiment counts: Positive {counts['Positive']}, Neutral {counts['Neutral']}, "
            f"Negative {counts['Negative']}\nReviews (text x times, sentiment):\n{review_lines}",
        )
        return counts, details, summary


def print_report(product_name, result):
    counts, details, summary = result
    print("\nOutput")
    for label in ("Positive", "Neutral", "Negative"):
        print(f"{label} : {counts[label]}")
    print("\nDetailed Review")
    for text, label, score in details:
        print(text)
        print(label)
        print(f"{score:.3f}")
        print("-" * 18)
    print("\nGPT Summary")
    print(summary)


if __name__ == "__main__":
    module = ReviewModule()
    name = input("Enter Product\n")
    result = module.analyze(name)
    if result is None:
        print("No reviews found for this product.")
    else:
        print_report(name, result)
