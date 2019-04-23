FROM python:3.7

RUN mkdir -p /api

WORKDIR /api

ADD requirements.txt /api

RUN pip install -r requirements.txt

RUN rm -rf /api/requirements.txt

ADD recess_api.py /api

CMD [ "python", "recess_api.py"]

