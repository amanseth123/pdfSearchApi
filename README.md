PDF Search API with RAG & JWT Authentication

A FastAPI-based backend for secure PDF upload and semantic search.
This project uses FAISS + Sentence Transformers to enable Retrieval-Augmented Generation (RAG)-style document search across PDFs.

It supports:

🔐 JWT Authentication for protected endpoints

📑 PDF ingestion with paragraph, table, and image extraction

🔎 Semantic search using embeddings (all-MiniLM-L6-v2)

⚡ FAISS vector index for efficient similarity search

🚀 Features

Upload a PDF and automatically:

Extract paragraphs, tables, and images

Generate embeddings and build a FAISS index

Search across the PDF using:

Semantic search (default, embedding-based)

Optional exact keyword search (can be extended)

Secure all API endpoints with JWT tokens

Project Structure
.
├── main.py               # FastAPI app with endpoints (/upload, /search)
├── utils/
│   └── etl.py            # PDF extraction (paragraphs, tables, images) & FAISS index
│   └── generate_token.py # JWT token generator
├── .env                  # Secret key and algorithm for JWT
├── requirements.txt      # Dependencies
└── README.md             # Documentation


Setup & Installation
1. Clone the repository
git clone https://github.com/yourusername/pdf-search-api.git
cd pdf-search-api

2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the root:

SECRET_KEY=denfubnriufbeuifbwdbweudfbeirbfewwefderf
ALGORITHM=HS256

🔑 Generating a JWT Token

Run:

python utils/generate_token.py


This prints a JWT token:

JWT TOKEN: <your_generated_token>
Use this token in API requests (Authorization: Bearer <token>).

▶️ Running the API
Start the server:

bash
Copy
Edit
uvicorn main:app --reload
API docs available at:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

API Endpoints
🔹 Upload a PDF

POST /upload
Upload and index a PDF.

Headers: Authorization: Bearer <JWT>

Body: multipart/form-data with file

Example (curl):

curl -X POST "http://127.0.0.1:8000/upload" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -F "file=@document.pdf"


Response:

{
  "message": "PDF processed",
  "chunks": 42
}

🔹 Search PDF

POST /search
Search indexed PDF chunks.

Headers: Authorization: Bearer <JWT>

Body: form-data

query: Search string

k (optional): Number of top results (default = all)

Example (curl):

curl -X POST "http://127.0.0.1:8000/search" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -F "query=salary"


Response:

{
  "query": "salary",
  "results": [
    {
      "chunk": {"type": "table", "content": "Basic Pay 77917.00 687087.00 ..."},
      "distance": 1.07
    },
    {
      "chunk": {"type": "paragraph", "content": "Net PAY : 127,218.00"},
      "distance": 1.06
    },
    {
      "chunk": {"type": "image_caption", "content": "Image 0 on page 0"},
      "distance": 1.644338846206665
        }
  ],
  "returned": 3
}

🔮 Roadmap

 Add hybrid search (semantic + keyword)

 Support multiple PDF uploads

 Add RAG integration with an LLM

 Store embeddings & metadata in persistent DB (e.g., Pinecone, Weaviate, Postgres + pgvector)

Demo Video: https://drive.google.com/file/d/1XcIEdSmo62WHia76k5w5eM04tn-pdITZ/view?usp=sharing
