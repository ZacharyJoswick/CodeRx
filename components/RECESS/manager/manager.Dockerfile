FROM python:3.7

EXPOSE 4582

RUN apt-get update && apt-get install dumb-init && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

RUN mkdir -p /manager

WORKDIR /manager

ADD requirements.txt /manager

RUN pip install -r requirements.txt

RUN rm -rf /manager/requirements.txt

ADD manager.py /manager

CMD [ "python", "manager.py"]

