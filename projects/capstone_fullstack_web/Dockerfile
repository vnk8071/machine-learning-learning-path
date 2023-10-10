FROM python:3.8-slim
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", ":5000", "api:app"]
