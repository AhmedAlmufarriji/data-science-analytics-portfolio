FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY aquasentinel ./aquasentinel
COPY static ./static
RUN pip install --no-cache-dir .
ENV AQUASENTINEL_MEMORY_DB=/tmp/aquasentinel-sessions.sqlite
EXPOSE 8000
CMD ["uvicorn", "aquasentinel.api:app", "--host", "0.0.0.0", "--port", "8000"]
