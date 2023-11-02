FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY .secrets omg_project/.secrets
COPY . .
EXPOSE 80
CMD ["python", "omg_project/manage.py", "runserver", "0.0.0.0:8000", "--noreload"]