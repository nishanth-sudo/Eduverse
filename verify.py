'''

from retrival.retriver import retrieve_passages
from generation.generator import generate_answer

def verify_answer(question, top_k=5):
    # Retrieve relevant passages using your retriever
    passages = retrieve_passages(question, top_k=top_k)
    
    # Generate an answer based on those passages
    answer = generate_answer(question, passages)

    # Display the result
    print("📌 Question:")
    print(question)
    print("\n✅ Generated Answer:")
    print(answer)

    print("\n🔍 Retrieved Passages:")
    for i, p in enumerate(passages):
        print(f"\n--- Passage {i + 1} ---")
        print(p[:1000])  # Display first 1000 characters

if __name__ == "__main__":
    question = input("Enter your question: ")
    verify_answer(question)
'''

from retrival.retriver import retrieve_passages
from generation.generator import generate_answer

def test_rag_pipeline():
    question = input()
    passages = retrieve_passages(question)
    answer = generate_answer(question, passages)
    assert answer is not None
    print("Test passed.")

if __name__ == "__main__":
    test_rag_pipeline()