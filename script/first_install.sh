#!/bin/bash

python3 -m venv venv
source venv/bin/activate  # for linux
venv\Scripts\activate.bat  # for windows
pip install -r requirements.txt
pre-commit install