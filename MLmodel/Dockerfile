FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run ignora EXPOSE, pero lo dejamos por documentación
EXPOSE 8080

CMD ["python", "start.py"]


