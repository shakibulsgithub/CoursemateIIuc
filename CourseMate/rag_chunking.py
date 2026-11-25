
from langchain_community.document_loaders import PyPDFLoader

# Load PDF
loader = PyPDFLoader("documents/cse.pdf")
documents = loader.load()

print("Total pages:", len(documents))

# Check extracted text page by page
for i, doc in enumerate(documents):

    text = doc.page_content

    print(f"\nPage {i+1}")
    print("Extracted characters:", len(text))

    if text.strip():
        print("Text found:")
        print(text[:300])
    else:
        print("No text extracted!")
