"""Part C - Product recommendation with TF-IDF retrieval + Ollama reasoning (Q6, Q7)."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from create_embeddings import load_datasets
from llm_utils import ask_llm


def product_text(row):
    return f"{row['ProductName']} {row['Category']} {row['Brand']} {row['Description']}"


class RecommendationModule:
    def __init__(self):
        self.products, _, _ = load_datasets()
        # Q6: TF-IDF vectors for product descriptions
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.products.apply(product_text, axis=1))

    def retrieve(self, query, top_k=3):
        """Top-k products by TF-IDF similarity; ties are broken by higher rating."""
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix)[0]
        ranked = self.products.assign(Similarity=scores)
        ranked = ranked.sort_values(["Similarity", "Rating"], ascending=[False, False])
        return ranked.head(top_k)

    def recommend(self, query):
        """Q7: retrieve the Top-3 products and ask Ollama to pick the best one."""
        top = self.retrieve(query)
        context = "\n".join(
            f"- {r.ProductName} | Brand: {r.Brand} | Category: {r.Category} | "
            f"Price: ₹{r.Price:,} | Rating: {r.Rating} | {r.Description}"
            for r in top.itertuples()
        )
        answer = ask_llm(
            "You are a shopping assistant. Choose the single best product for the "
            "customer ONLY from the retrieved products, considering relevance, rating "
            "and value for money. Reply in exactly two lines:\n"
            "Product: <exact product name>\nReason: <2 sentences>",
            f"Customer request: {query}\n\nRetrieved products:\n{context}",
            temperature=0.1,
        )
        # Use the dataset row for brand/price so the facts shown are always correct.
        chosen = top.iloc[0]
        for row in top.itertuples():
            if row.ProductName.lower() in answer.lower():
                chosen = top.loc[row.Index]
                break
        reason = answer.split("Reason:", 1)[1].strip() if "Reason:" in answer else answer
        reply = (
            f"Among the retrieved products, I recommend\n{chosen['ProductName']}.\n"
            f"Brand : {chosen['Brand']}\n"
            f"Price : ₹{int(chosen['Price']):,}\n"
            f"Rating : {chosen['Rating']}\n"
            f"Reason:\n{reason}"
        )
        return top, reply


if __name__ == "__main__":
    module = RecommendationModule()
    query = input("Search Product :\n")
    top, reply = module.recommend(query)
    print("\nRetrieved Products")
    for name in top["ProductName"]:
        print(name)
    print("\nGPT Response")
    print(reply)
