#!/bin/bash

gunicorn --config gunicorn.conf.py server:app