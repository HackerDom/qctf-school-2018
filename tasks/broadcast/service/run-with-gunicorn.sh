#!/bin/bash

gunicorn --config gunicorn.conf.py --worker-class sanic.worker.GunicornWorker main:app
