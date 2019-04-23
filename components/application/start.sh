#!/bin/bash

echo "Value of FLASK_DEBUG=$FLASK_DEBUG"

if [ $FLASK_DEBUG -eq 1 ]
then
    echo "Running In Debug Configuration"
    #flask run -h 0.0.0.0 -p 5000 --with-threads
    gunicorn --worker-class eventlet --reload -w 1 -b :5000 CodeRx:app 
else
    echo "Running In Production Configuration"
    gunicorn --worker-class eventlet --no-sendfile -w 1 -b :5000 CodeRx:app 
fi