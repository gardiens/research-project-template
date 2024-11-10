#!/bin/bash

python3 -m venv venv
source venv/bin/activate  # for linux
venv\Scripts\activate.bat  # for windows
pip install -r requirements.txt
pre-commit install
#pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu116 #uncomment if you areon DGX
