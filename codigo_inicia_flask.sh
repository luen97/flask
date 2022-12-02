#!/bin/bash

pip install -r requirements.txt
source venv/bin/activate


export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=main.py

flask run
