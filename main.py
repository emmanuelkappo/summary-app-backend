
from openai import OpenAI
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
import auth


# app = Flask(__name__)
app = FastAPI()
app.include_router(auth.router)


api_key = "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"
client = OpenAI(api_key=api_key)

origin = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"])

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/summarize")
async def summarize(content: str):
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
            max_tokens=164,
            top_p=1
            )
        
        return response
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=(str(error)))

    
    

