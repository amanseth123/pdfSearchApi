from jose import jwt
import datetime
import os


# Load .env file
def load_env(path=".env"):
    with open(path) as f:
        for line in f: 
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key]=value
load_env()

SECRET_KEY = os.getenv("SECRET_KEY")  
ALGORITHM = os.getenv("ALGORITHM")

payload = {
    "user": "aman",
    "role": "admin",
    "iat": datetime.datetime.now(datetime.UTC),  # issued at (timezone-aware)
    "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)  # expires in 1 hour
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print("JWT TOKEN:", token)
