FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . .


EXPOSE 8501


CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false"]
