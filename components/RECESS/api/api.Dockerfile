FROM python:3.7

RUN apt-get update && apt-get install dumb-init && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

RUN mkdir -p /api

WORKDIR /api

ADD requirements.txt /api

RUN pip install -r requirements.txt

RUN rm -rf /api/requirements.txt

ADD recess_api.py /api

CMD [ "python", "recess_api.py"]

