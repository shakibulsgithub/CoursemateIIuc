
from langchain_community.document_loaders import PyPDFLoader

# Load PDF
loader = PyPDFLoader("documents/cse.pdf")

# Extract pages
documents = loader.load()

# Display results
print("Total pages:", len(documents))

print("\nFirst page content:\n")
print(documents[0].page_content[:1000])
