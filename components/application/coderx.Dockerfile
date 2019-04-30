FROM python:3.6

RUN apt-get update && apt-get install dumb-init && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

#Create code directory
RUN mkdir -p /code

#Set the working directory to /code
WORKDIR /code

#Add our directory to the python path
RUN export PYTHONPATH="${PYTHONPATH}:/code"

#Copy in requirements and start 
#This speeds up build time later as we are not modifying these files often
COPY requirements.txt start.sh /code/

#Install requirements
RUN pip install -r requirements.txt

#Make start script executable
RUN chmod a+x /code/start.sh

#Set start command
CMD ["/code/start.sh"]

#Set flask application environment variable
ENV FLASK_APP CodeRx:app

#add the rest of the files
COPY ./CodeRx /code/CodeRx




# CMD ["python", "app.py"]