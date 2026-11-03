"""Part D - Product question answering with RAG (Q8, Q9)."""
import re

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from create_embeddings import load_datasets, load_embedding_model
from llm_utils import ask_llm

# Questions such as "What is its price?" refer back to the last product discussed.
FOLLOW_UP_WORDS = {"it", "its", "it's", "this", "that", "the product", "same"}
# General requests like "Tell me about Samsung Galaxy" are rewritten with the
# catalogue name so the model describes the retrieved product instead of refusing.
GENERAL_REQUEST = re.compile(r"^\s*(tell me about|describe|details (of|about)|info(rmation)? (on|about)|show me)\b", re.I)


class ProductModule:
    def __init__(self):
        self.products, _, _ = load_datasets()
        self.model = load_embedding_model()
        texts = (self.products["ProductName"] + " " + self.products["Brand"] + " "
                 + self.products["Category"]).tolist()
        self.embeddings = self.model.encode(texts, normalize_embeddings=True)
        self.current = None  # last retrieved product (conversation memory)

    def _names_a_product(self, question):
        q = question.lower()
        return any(b.lower() in q for b in self.products["Brand"].unique()) or any(
            c.lower() in q for c in self.products["Category"].unique()
        )

    def _is_follow_up(self, question):
        words = set(re.findall(r"[a-z']+", question.lower()))
        return self.current is not None and bool(words & FOLLOW_UP_WORDS) and not self._names_a_product(question)

    def retrieve(self, question):
        """Q8: find the most relevant product (or reuse the current one for follow-ups)."""
        if self._is_follow_up(question):
            return self.current, None
        query = self.model.encode([question], normalize_embeddings=True)
        scores = cosine_similarity(query, self.embeddings)[0]
        best = int(np.argmax(scores))
        self.current = self.products.iloc[best]
        return self.current, float(scores[best])

    @staticmethod
    def build_context(product):
        """Q8: structured context passed to the LLM."""
        return (
            f"Product Name: {product['ProductName']}\n"
            f"Brand: {product['Brand']}\n"
            f"Category: {product['Category']}\n"
            f"Price: ₹{int(product['Price']):,}\n"
            f"Rating: {product['Rating']} / 5\n"
            f"Description: {product['Description']}"
        )

    def answer(self, question):
        """Q9: constrained prompt - answer only from the retrieved context."""
        product, score = self.retrieve(question)
        if GENERAL_REQUEST.search(question):
            question = f"Tell me about the {product['ProductName']}."
        reply = ask_llm(
            "You are a product assistant for an e-commerce store. Answer the customer's "
            "question using ONLY the product context below, in 1-3 short sentences. "
            "If the customer asks generally about the product, describe it using the "
            "name, brand, category, price and description from the context. "
            "If a specific detail is not in the context, reply exactly: "
            "\"Sorry, that information is not available for this product.\"",
            f"Context (closest matching product in our catalogue - treat it as the "
            f"product the customer means, even if they used a different name):\n"
            f"{self.build_context(product)}\n\nQuestion: {question}",
            temperature=0.1,
        )
        return product, score, reply


if __name__ == "__main__":
    module = ProductModule()
    print("Product Assistant (type 'exit' to stop)")
    while True:
        question = input("\nAsk :\n")
        if question.strip().lower() == "exit":
            break
        product, score, reply = module.answer(question)
        print("\nOutput")
        if score is not None:
            print("Retrieved Product")
            print(product["ProductName"])
            print(f"Similarity : {score:.2f}")
        print("\nAssistant")
        print(reply)
        print("\nNext Question")
