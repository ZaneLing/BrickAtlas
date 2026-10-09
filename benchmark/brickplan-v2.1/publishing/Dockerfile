FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY brickplan-v2.1-release.zip /tmp/release.zip
RUN python -m zipfile -e /tmp/release.zip /app && rm /tmp/release.zip
WORKDIR /app/brickplan-v2.1
RUN pip install --no-cache-dir -r benchmark/brickplan-v2.1/requirements.txt
ENV PYTHONUNBUFFERED=1
EXPOSE 7860
CMD ["python", "benchmark/brickplan-v2.1/server.py", "serve", "--host", "0.0.0.0", "--port", "7860", "--store", "/tmp/brickplan-practice"]
