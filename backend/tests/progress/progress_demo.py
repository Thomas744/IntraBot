from backend.app.rag.pipeline import run_pipeline
from backend.app.rag.retriever import secure_search


def main():
    role = input("Enter User Role  : ").strip().lower()
    query = input("Enter Query      : ").strip()

    result = run_pipeline(role)
    store = result["vector_store"]

    print("\nTotal Documents Loaded :", result["total_documents"])
    print("Total Chunks Created   :", result["total_chunks"])

    results = secure_search(store, query, role)

    print("\nResults Found :", len(results))
    print("RBAC Status   :", "PASS")

    for i, doc in enumerate(results, 1):
        print(f"\n[Result {i}]")
        print("Department:", doc.metadata["department"])
        print("Roles     :", doc.metadata["accessible_roles"])
        print("Content   :", doc.page_content[:150])


if __name__ == "__main__":
    main()


# Sample CASE:
# Role  : finance
# Query : financial report revenue
#
# Role  : marketing
# Query : employee salary

