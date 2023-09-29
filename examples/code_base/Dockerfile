FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app/

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "api.app:app"]
