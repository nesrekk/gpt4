"""Part F (Q13) - integrated e-commerce chatbot with continuous interaction until Exit."""
from faq_module import FAQModule
from intent_module import detect_intent
from product_module import ProductModule
from recommendation_module import RecommendationModule
from review_module import ReviewModule, print_report


def main():
    print("Loading modules... (FAQ, Recommendation, Product QA, Review, Intent)")
    faq = FAQModule()
    recommender = RecommendationModule()
    product_qa = ProductModule()
    reviews = ReviewModule()

    print("\n" + "=" * 60)
    print("   E-COMMERCE GPT CHATBOT  (Ollama + RAG)")
    print("   Type 'exit' to quit")
    print("=" * 60)

    while True:
        question = input("\nYou :\n").strip()
        if not question:
            continue
        if question.lower() in ("exit", "quit", "bye"):
            print("Assistant : Thank you for shopping with us. Goodbye!")
            break

        intent = detect_intent(question)
        print("↓\nDetected Intent")
        print(intent)
        print("↓\nAssistant")

        if intent == "FAQ":
            reply, matched, score = faq.answer(question)
            if reply is None:
                # No FAQ is close enough - fall through to product QA
                _, _, reply = product_qa.answer(question)
            print(reply)

        elif intent == "RECOMMENDATION":
            top, reply = recommender.recommend(question)
            print("Retrieved Products : " + ", ".join(top["ProductName"]))
            print(reply)

        elif intent == "PRODUCT":
            product, score, reply = product_qa.answer(question)
            if score is not None:
                print(f"(Retrieved product : {product['ProductName']}, similarity {score:.2f})")
            print(reply)

        elif intent == "REVIEW":
            product, _ = product_qa.retrieve(question)
            result = reviews.analyze(product["ProductName"])
            if result is None:
                print(f"No customer reviews are available for {product['ProductName']} yet.")
            else:
                print(f"Reviews for {product['ProductName']}")
                print_report(product["ProductName"], result)


if __name__ == "__main__":
    main()
