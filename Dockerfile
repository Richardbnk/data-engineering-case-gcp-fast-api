FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Copia o .env e as credenciais
COPY .env .env
COPY credentials/ credentials/

# Define a variável de ambiente usada pela SDK
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/data-project.json

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
