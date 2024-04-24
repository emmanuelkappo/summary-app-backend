# 
FROM python:3-slim

# 
COPY  . .

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

 
ENTRYPOINT ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000"]