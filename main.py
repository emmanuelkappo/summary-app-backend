from jose.exceptions import JWTClaimsError
from openai import OpenAI
from fastapi import FastAPI, HTTPException, Depends, Security, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError, ExpiredSignatureError
import auth
import os


security = HTTPBearer()

app = FastAPI()
app.include_router(auth.router)

SECRET_KEY = os.environ['SECRET_KEY']

ALGORITHM = 'HS256'

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

origin = ["http://localhost", "http://localhost:3000","https://dapper-nougat-a1c723.netlify.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"])

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/summarize")
async def summarize(db: db_dependency, content: str, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except ExpiredSignatureError as error:
        raise HTTPException(status_code=401, detail=(str(error)))
    except JWTClaimsError as error:
        raise HTTPException(status_code=401, detail=(str(error)))
    except JWTError as error:
        raise HTTPException(status_code=401, detail=(str(error)))
    email = payload.get("sub")
    # Find the user and check the credit
    logged_user = db.query(models.Users).filter(models.Users.email == email).first()
    quota = db.query(models.Quota).filter(models.Quota.user_id == logged_user.id).first()
    if quota.used == quota.quota:
        raise HTTPException(status_code=403, detail="You have exceeded your quota")
    print(payload)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with meeting notes, and your task is to summarize the meeting as follows:\n    \n    -Overall summary of discussion\n    -Action items (what needs to be done and who is doing it)\n    -If applicable, a list of topics that need to be discussed more fully in the next meeting."
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            temperature=0.7,
            max_tokens=464,
            top_p=1
        )
        # Update the quota
        quota.used += 1
        db.commit()

        return response
    except ExpiredSignatureError as error:
        raise HTTPException(status_code=401, detail=(str(error)))
    except Exception as error:
        raise HTTPException(status_code=403, detail=(str(error)))
