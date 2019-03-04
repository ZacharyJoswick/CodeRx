#!/bin/bash

echo "Value of FLASK_DEBUG=$FLASK_DEBUG"

if [ $FLASK_DEBUG -eq 1 ]
then
    echo "Running In Debug Configuration"
    flask run -h 0.0.0.0 -p 5000
else
    echo "Running In Production Configuration"
    gunicorn -w 4 -b :5000 CodeRx:app
fi