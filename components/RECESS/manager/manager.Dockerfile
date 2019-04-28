FROM python:3.7

RUN mkdir -p /manager

WORKDIR /manager

ADD requirements.txt /manager

RUN pip install -r requirements.txt

RUN rm -rf /manager/requirements.txt

ADD manager.py /manager

CMD [ "python", "manager.py"]

