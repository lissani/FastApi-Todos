FROM python:3.9

WORKDIR /app

# 필요한 파일만 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY todo.json .

# 비루트 유저 생성 및 전환
RUN useradd -m appuser

# 파일 권한 조정 추가
RUN chown appuser:appuser /app/todo.json

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
