#!/bin/bash
CUDA_VERSION=11.8
CUDA_TAG=cu${CUDA_VERSION//./}  # pytorch wheel index uses a dotless tag, e.g. cu126



# Set conda 
conda install -n base conda-libmamba-solver -y
conda config --set solver libmamba
conda create -n venv python=3.10 -y
conda activate venv

# Install Torch 

echo " INSTALLING THE PYTHON DEPENDENCIES "
conda install cuda-toolkit=${CUDA_VERSION} cuda-nvcc=${CUDA_VERSION} -c nvidia -y #* This will download a nvcc compiler at the specific Cuda versions. usefull if you are working with custom CUDA kernels.

pip3 install torch torchvision --index-url https://download.pytorch.org/whl/${CUDA_TAG}


# install the necessary dependencies :
pip install -r requirements.txt
pre-commit install
pip install -r dev_requirements.txt # Some package usefull when coding .
