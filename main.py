from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from utils.etl import extract_chunks, build_index
import numpy as np
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from sentence_transformers import SentenceTransformer



def load_env(path=".env"):
    with open(path) as f:
        for line in f: 
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key]=value
load_env()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

app = FastAPI()
security = HTTPBearer()

index = None
metadata = {}

model = SentenceTransformer("all-MiniLM-L6-v2")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        print("Secret key " + SECRET_KEY + "\n" + "ALgorithms " + ALGORITHM)
        # print("Validating token ", 
        #       jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYW1hbiIsInJvbGUiOiJhZG1pbiJ9.seuzxENPdOqQUs3h0pfTwub5tsmf4sX5ZfHPB9QOUrE', SECRET_KEY, algorithms=[ALGORITHM]))
    
        
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), token: dict = Depends(verify_token)):
    global index, metadata
    pdf_bytes = await file.read()
    chunks = extract_chunks(pdf_bytes)
    index, metadata = build_index(chunks)
    return {"message": "PDF processed", "chunks": len(chunks)}

# @app.post("/search")
# async def search_pdf(query: str = Form(...), token: dict = Depends(verify_token)):
#     if index is None:
#         raise HTTPException(status_code=400, detail="No PDF indexed yet.")
#     from utils.etl import model
#     query_embedding = model.encode([query])
#     distances, indices = index.search(np.array(query_embedding), 3)
#     results = [metadata[idx] for idx in indices[0]]
#     return {"results": results}

@app.post("/search")
async def search_pdf(
    query: str = Form(...),
    k: int = Query(None, description="Number of top results to return. Defaults to all."),
    token: dict = Depends(verify_token)
):
    global index, metadata

    if index is None:
        raise HTTPException(status_code=400, detail="No PDF indexed yet.")

    # Encode query
    query_embedding = model.encode([query])

    # If no k is provided → search across all vectors
    if k is None:
        k = index.ntotal

    # Perform FAISS search
    distances, indices = index.search(np.array(query_embedding), k)

    # Collect results (ignore -1s)
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx != -1:
            results.append({"chunk": metadata[idx], "distance": float(dist)})

    return {"query": query, "results": results, "returned": len(results)}