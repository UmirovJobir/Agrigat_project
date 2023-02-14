FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY . . 


RUN pip uninstall django
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

EXPOSE 8000

COPY entrypoint.sh .
ENTRYPOINT ["sh", "entrypoint.sh"]