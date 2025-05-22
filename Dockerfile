FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY nasa_ai_bot.py .
CMD ["python", "nasa_ai_bot.py"]
