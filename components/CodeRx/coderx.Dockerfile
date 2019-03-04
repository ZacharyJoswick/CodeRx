FROM python:3.7

#Create code/CodeRx directory
RUN mkdir -p /code/CodeRx

#Set the working directory to /code
WORKDIR /code

#Add our directory to the python path
RUN export PYTHONPATH="${PYTHONPATH}:/code"

#Copy in requirements and start 
#This speeds up build time later as we are not modifying these files often
COPY requirements.txt /code/

#Install requirements
RUN pip install -r requirements.txt

COPY start.sh /code/start.sh

#Make start script executable
RUN chmod a+x /code/start.sh

#Set start command
CMD ["/code/start.sh"]

#Set flask application environment variable
ENV FLASK_APP CodeRx:app

#add the rest of the files
ADD . /code/CodeRx



# CMD ["python", "app.py"]