FROM python:3.12-slim

ENV HOST=0.0.0.0 \
    PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY content-decoder.html content_decoder_server.py frameworks.json ./

EXPOSE 8080
CMD ["python", "content_decoder_server.py"]
