#!/bin/bash

gunicorn --config gunicorn.conf.py main:app
