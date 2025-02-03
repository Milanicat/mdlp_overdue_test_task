FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ~/mdlp_overdue_test_task

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY app ./app

CMD ["python", "-m", "app"]