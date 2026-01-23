# 1. 파이썬 3.12 버전을 기반으로 이미지를 생성
FROM python:3.12

# 2. 파이썬 로그가 버퍼링 없이 바로 출력되도록 설정
ENV PYTHONUNBUFFERED=1

# 3. 도커 안에서 작업할 폴더 생성 및 설정
WORKDIR /app

# 4. 로컬의 requirements.txt를 도커 안으로 복사
COPY requirements.txt /app/

# 5. pip 업그레이드 및 라이브러리 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. 현재 프로젝트의 모든 코드를 도커 안으로 복사
COPY . /app/

# 7. 장고 서버 실행 (외부 접속 허용 0.0.0.0:8000)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]