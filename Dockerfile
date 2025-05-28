FROM python:3.11

WORKDIR /app

# Set Python path to include the app directory
ENV PYTHONPATH=/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure the entrypoint script has Unix line endings
RUN apt-get update && apt-get install -y dos2unix \
    && dos2unix /app/start.sh \
    && chmod +x /app/start.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
