# 
FROM python:3-slim

# 
COPY  . .

ENV OPENAI_API_KEY=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
ENV SECRET_KEY=1987Jsba430943klefglrtjbgr0348nntrt05653mlfedmg086

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade -r /requirements.txt


ENTRYPOINT ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000"]