FROM python:3.7-alpine

ADD . /code

WORKDIR /code

ENV FLASK_APP app.py

RUN pip install -r requirements.txt

RUN chmod a+x ./start.sh

CMD ["sh", "start.sh"]
# CMD ["python", "app.py"]