FROM python:3.9

WORKDIR /app

# 필요한 파일만 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# 비루트 유저 생성 및 전환
RUN useradd -m appuser
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
