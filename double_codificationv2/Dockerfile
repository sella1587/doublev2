FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "double_codificationv2.asgi:application", "--host", "0.0.0.0", "--port", "8000"]