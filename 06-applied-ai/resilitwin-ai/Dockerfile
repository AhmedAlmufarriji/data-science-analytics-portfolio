FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY resilitwin/ ./resilitwin/
COPY knowledge/ ./knowledge/
COPY web/ ./web/
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "resilitwin.api:app", "--host", "0.0.0.0", "--port", "8000"]
