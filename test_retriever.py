from retriever import retrieve_documents


question = "How much is the registration fee for new students?"

results = retrieve_documents(question)


for i, document in enumerate(results):

    print(f"\n--- Result {i + 1} ---")

    print("Source:")
    print(document.metadata)

    print("\nContent:")
    print(document.page_content)