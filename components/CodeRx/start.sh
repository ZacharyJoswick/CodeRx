#!/bin/sh

gunicorn -w 4 -b :5000 app:app