FROM python:2.7.15

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 5002

CMD ["python", "app.py"]
