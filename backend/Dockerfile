FROM python:3.11-slim

WORKDIR /app

# System deps for OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ../models /app/models
COPY ../dataset /app/dataset

# Train model if not present
RUN python -c "import os; os.path.exists('/app/models/injection_detector.pkl') or __import__('subprocess').run(['python', '/app/../training/train_model.py'])"

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
