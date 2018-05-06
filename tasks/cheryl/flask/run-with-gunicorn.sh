#!/bin/bash

python3 init_db.py
gunicorn --config gunicorn.conf.py server:app
