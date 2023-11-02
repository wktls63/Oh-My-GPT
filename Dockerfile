FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY .secrets omg_project/.secrets
COPY . .

# collectstatic 명령어 추가
RUN python omg_project/manage.py collectstatic --noinput

EXPOSE 80

# gunicorn을 사용하여 애플리케이션 실행
CMD ["gunicorn", "omg_project.wsgi:application", "--bind", "0.0.0.0:80", "--workers", "3"]
