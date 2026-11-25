import pymupdf
import fitz
import pytesseract

from PIL import Image
from io import BytesIO

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 1. Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# 2. Open PDF
pdf_path = "documents/cse.pdf"

pdf = pymupdf.open(pdf_path)

documents = []

print("Starting OCR...\n")


# 3. Extract text from each page
for page_number, page in enumerate(pdf):

    # Convert PDF page into image
    pix = page.get_pixmap(dpi=300)

    image = Image.open(
        BytesIO(pix.tobytes("png"))
    )

    # OCR image
    extracted_text = pytesseract.image_to_string(
        image,
        lang="eng"
    )

    # Save extracted text with page number
    document = Document(
        page_content=extracted_text,
        metadata={
            "source": pdf_path,
            "page": page_number + 1
        }
    )

    documents.append(document)

    print(
        f"Page {page_number + 1}: "
        f"{len(extracted_text)} characters extracted"
    )


# 4. Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


# 5. Create chunks
chunks = text_splitter.split_documents(documents)


# 6. Display results
print("\nTotal pages:", len(documents))
print("Total chunks:", len(chunks))


# 7. Show first chunk
if chunks:

    print("\nFirst Chunk:\n")
    print(chunks[0].page_content)

    print("\nMetadata:")
    print(chunks[0].metadata)

else:
    print("\nNo text extracted. OCR needs checking.")


# 8. Save extracted text
with open(
    "documents/extracted_text.txt",
    "w",
    encoding="utf-8"
) as file:

    for doc in documents:
        file.write(
            f"\n--- Page {doc.metadata['page']} ---\n"
        )
        file.write(doc.page_content)
        file.write("\n")

print("\nExtracted text saved successfully!")
