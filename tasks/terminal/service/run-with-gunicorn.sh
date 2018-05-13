#!/bin/bash

gunicorn --config gunicorn.conf.py server:spawn_app --worker-class aiohttp.GunicornWebWorker
