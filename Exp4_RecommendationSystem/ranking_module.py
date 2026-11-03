"""Part E - Recommendation ranking (Q6)."""


def rank_recommendations(items):
    """Q6: rank recommendations by suitability score (highest first)."""
    return sorted(items, key=lambda item: item["score"], reverse=True)


def display_ranking(items):
    width = max([len(i["name"]) for i in items] + [len("Recommendation")])
    print(f"\n{'Rank':<5}| {'Recommendation':<{width}} | Score")
    print("-" * (width + 17))
    for rank, item in enumerate(items, 1):
        print(f"{rank:<5}| {item['name']:<{width}} | {item['score']}%")
