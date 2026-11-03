"""Part B - FAQ semantic search (Q3, Q4, Q5)."""
import os

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from create_embeddings import (
    FAQ_EMBEDDINGS_PATH,
    create_faq_embeddings,
    load_datasets,
    load_embedding_model,
)
from llm_utils import ask_llm

SIMILARITY_THRESHOLD = 0.50


class FAQModule:
    def __init__(self):
        _, self.faqs, _ = load_datasets()
        self.model = load_embedding_model()
        if os.path.exists(FAQ_EMBEDDINGS_PATH):
            self.embeddings = np.load(FAQ_EMBEDDINGS_PATH)
        else:
            self.embeddings = create_faq_embeddings(self.faqs)

    def best_match(self, question):
        """Q4: retrieve the best FAQ using cosine similarity."""
        query = self.model.encode([question], normalize_embeddings=True)
        scores = cosine_similarity(query, self.embeddings)[0]
        best = int(np.argmax(scores))
        return self.faqs.iloc[best], float(scores[best])

    def answer(self, question):
        """Q5: if the best FAQ passes the threshold, let Ollama phrase the answer.

        Returns None when no FAQ is close enough so the chatbot can move on.
        """
        faq, score = self.best_match(question)
        if score < SIMILARITY_THRESHOLD:
            return None, faq, score
        reply = ask_llm(
            "You are a helpful e-commerce customer support assistant. Answer the "
            "customer using the FAQ answer given to you. Reply in 2 short, friendly "
            "sentences: first say what to do, then say how it helps them. "
            "Do not add new facts.",
            f"FAQ answer: {faq['Answer']}\nCustomer question: {question}\nReply:",
        )
        return reply, faq, score


if __name__ == "__main__":
    print("Loading FAQ Module...")
    module = FAQModule()
    question = input("Ask Question : ")
    reply, faq, score = module.answer(question)
    print(f"Best Matching FAQ : {faq['Question']}")
    print(f"Similarity Score {score:.2f}")
    if reply is None:
        print("\nNo FAQ matched above the threshold. Passing to the next module.")
    else:
        print(f"\nChatbot:\n{reply}")
