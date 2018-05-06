#!/bin/bash

gunicorn --config gunicorn.conf.py zip_crypt.app:app
