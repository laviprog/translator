FROM python:3.10-slim

RUN apt update && apt install ffmpeg -y

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]
