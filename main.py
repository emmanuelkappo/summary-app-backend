# from flask import Flask, render_template, request
from openai import OpenAI
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io

# app = Flask(__name__)
app = FastAPI()

api_key = "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"
client = OpenAI(api_key=api_key)

origin = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"])

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

    
    
    # audio_file = request.files['audio_file']
    # if audio_file:
    #     transcription = client.audio.transcriptions.create(
    #         model="whisper-1", 
    #         file=audio_file
    #     )
    #     return transcription.text

# if __name__ == '__main__':
#     app.run(debug=True)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         audio_file = request.files['audio_file']
#         if audio_file:
#             transcription = client.audio.transcriptions.create(
#                 model="whisper-1", 
#                 file=audio_file
#             )
#             return render_template('result.html', transcription=transcription.text)
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)





# from openai import OpenAI
# api_key="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"

# client = OpenAI(api_key=api_key)
# audio_file= open("EarningsCallll.mp3", "rb")
# transcription = client.audio.transcriptions.create(
#   model="whisper-1", 
#   file=audio_file
# )
# print(transcription.text)

