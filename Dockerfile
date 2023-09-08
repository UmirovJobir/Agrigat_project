FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY . . 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000" ]