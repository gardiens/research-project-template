FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04


ENV DEBIAN_FRONTEND=noninteractive
RUN : \
    && apt-get update \
    && apt-get update \
    && apt-get install -y --no-install-recommends software-properties-common \
    && apt-get install -y bash ffmpeg libsm6 libxext6 wget git tmux vim nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :

RUN apt-get install build-essential

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda init bash
RUN conda create --name myenv python=3.8 -y

# Move Config setup
COPY .setup_config/.ssh/ /root/.ssh/
## specify custom tmux config
COPY .setup_config/.tmux.conf /root/
COPY .setup_config/.tmux.conf.local /root/
# specify custon clearml conf
COPY .setup_config/clearml.conf /root/
RUN chmod 600 /root/.ssh/id_rsa

# Clone the projetct
WORKDIR /workspaces
RUN git clone https://github.com/username/repository.git #! 

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
#* From now on, every RUN will be run into myenv

#COPY and get into the env
WORKDIR /workspaces/
RUN git checkout main
RUN git pull



# set the solver to libmamba to be faster
RUN conda update -n base conda -y
RUN conda install -n base conda-libmamba-solver -y
RUN conda config --set solver libmamba

# install pytorch
RUN CUDA_VERSION=$(nvcc --version | grep "release" | sed 's/.*release //' | sed 's/,.*//') && \
    if [ "$CUDA_VERSION" = "11.4" ]; then \
        conda  install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch -y; \
    elif [ "$CUDA_VERSION" = "11.6" ]; then \
        conda install pytorch==1.13.1 torchvision==0.14.1 pytorch-cuda=11.6 -c pytorch -c nvidia -y; \
    # Add more elif branches for other CUDA versions as needed
    elif [ "$CUDA_VERSION" = "12.1" ]; then \
    conda install -n spt pytorch==2.2.0 torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y;\
    pip3 install torch torchvision torchaudio;\

    elif [ "$CUDA_VERSION" = "12.0" ]; then \
    conda install pytorch==2.2.0 torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia; \
    elif [ "$CUDA_VERSION" = "11.8" ]; then \
    conda install pytorch==2.2.0 torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia; \
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118; \
    else \
        CUDA_MAJOR=`echo ${CUDA_VERSION} | sed 's/\..*//'`
        CUDA_MINOR=`echo ${CUDA_VERSION} | sed 's/.*\.//'`
        conda install pytorch torchvision torchaudio pytorch-cuda=${CUDA_MAJOR}${CUDA_MINOR} -c pytorch -c nvidia

    fi



RUN echo 'conda deactivate' >> /root/.bashrc
RUN echo 'conda activate myenv' >> /root/.bashrc

# install required packages
RUN pip install -r requirements.txt

# Install dev dependencies
RUN pip install pre-commit

RUN pre-commit install