FROM python3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

celery frontend_project.celery worker --pool=solo -l info \
celery -A frontend_project beat -l info