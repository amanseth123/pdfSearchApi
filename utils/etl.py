import fitz  
import pdfplumber
import io
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_chunks(pdf_bytes):
    chunks = []
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            chunks.append({"type": "paragraph", "content": block[4]})
        images = page.get_images(full=True)
        for i, _ in enumerate(images):
            chunks.append({"type": "image_caption", "content": f"Image {i} on page {page.number}"})

    # Tables using pdfplumber
    # with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
    #     for page in pdf.pages:
    #         extracted_tables = page.extract_tables()
    #         for table in extracted_tables:
    #             formatted = "\n".join([" | ".join(row) for row in table if row])
    #             chunks.append({"type": "table", "content": formatted})

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page_num, page in enumerate(pdf.pages):
            extracted_tables = page.extract_tables()
            for t_idx, table in enumerate(extracted_tables):
                if table:
                    formatted = "\n".join(
                        [" | ".join([cell if cell else "" for cell in row]) for row in table if row]
                    )
                    table_text = f"Table {t_idx} on page {page_num}:\n{formatted}"
                    chunks.append({"type": "table", "content": table_text})


    return chunks

def build_index(chunks):
    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(texts)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    metadata = {i: chunks[i] for i in range(len(chunks))}
    return index, metadata