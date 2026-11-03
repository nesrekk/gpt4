"""Part C - Similar email retrieval from previous interactions (Q4, Q5)."""
from utils import DATA_FILE  # imported first: it also silences a noisy torch log line

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "all-mpnet-base-v2"


class EmailRetriever:
    def __init__(self):
        # Q4: load previous customer interactions from CSV
        self.history = pd.read_csv(DATA_FILE)
        self.model = SentenceTransformer(EMBED_MODEL)
        texts = (self.history["Subject"] + ". " + self.history["Customer_Email"]).tolist()
        self.embeddings = self.model.encode(texts, normalize_embeddings=True)

    def most_similar(self, email):
        """Q5: return the most similar previous email, its reply and the similarity score."""
        query = self.model.encode([f"{email['subject']}. {email['body']}"], normalize_embeddings=True)
        scores = (query @ self.embeddings.T)[0]
        best = int(np.argmax(scores))
        return self.history.iloc[best], float(scores[best])


def display_match(row, score):
    print(f"Matched Record  : {row['Email_ID']} ({row['Category']}, similarity {score:.2f})")
    print("Previous Email")
    print(row["Customer_Email"])
    print("Previous Reply")
    print(row["Previous_Reply"])


if __name__ == "__main__":
    from input_module import read_email

    retriever = EmailRetriever()
    print(f"Loaded {len(retriever.history)} previous interactions from data/emails.csv\n")
    row, score = retriever.most_similar(read_email())
    print()
    display_match(row, score)
