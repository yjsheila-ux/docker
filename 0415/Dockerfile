# image를 만들때 사용
FROM python:3.13-slim
WORKDIR /app
COPY main.py .
    # . .
RUN pip install "fastapi[standard]"

# container 실행할때 사용 -> docker run 할때 사용됨
# CMD ["fastapi","dev"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# kubernetes(K8S) -> 여러개의 도커 컨테이너를 관리하는 기술
