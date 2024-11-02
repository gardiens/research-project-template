

<a name="readme-top"></a>
<!--





<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://gitlab-student.centralesupelec.fr/alix.chazottes/fmr-2024-segmentation-hierarchique">
    <img src="images/logo_safe.jpg" alt="Logo" width=600>
  </a>

<h3 align="center">  Research Project Template </h3>

  <p align="center">
     Fast train with hydra and lightning
    <br />
    <a href="https://gitlab-student.centralesupelec.fr/alix.chazottes/fmr-2024-segmentation-hierarchique"><strong>Explore the docs »</strong></a>

  </p>
</div>


# Repository structure
The repository is structured as follows. Each point is detailed below.
```
├── README.md        <- The top-level README for developers using this project
├── configs         <- Configuration files for Hydra. The subtree is detailed below
├── src             <- Source code for use in this project
├── data            <- Data folder, ignored by git
├── logs           <- Logs folder, ignored by git (tensorboard?, wandb, CSVs, ...)
├── venv           <- Virtual environment folder, ignored by git
├── requirements.txt  <- The requirements file for reproducing the analysis environment
├── LICENSE        <- License file
├── train.py         <- Main script to run the code
└── personal_files <- Personal files, ignored by git (e.g. notes, debugging test scripts, ...)
```

This architecture is based on the fact that any research project requires a configuration, possibly decomposed into several sub-configurations


# Setup

## Virtual environment

For the sake of reproducibility, and to avoid conflicts with other projects, it is recommended to use a virtual environment.

There are several ways to create a virtual environment. A good one is Virtual Env and conda.

The following commands create a virtual environment named ``./venv/`` and install the requirements.

```bash
python3 -m venv venv
source venv/bin/activate  # for linux
venv\Scripts\activate.bat  # for windows
pip install -r requirements.txt
#pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu116 #uncomment if you areon DGX

```

# Setup the script
You just have to follow the script
```sh
bash first_install.sh
#python3 -m venv venv
#source venv/bin/activate  # for linux
#venv\Scripts\activate.bat  # for windows
#pip install -r requirements.txt
#pre-commit install
```

# Configuration system
Use Hydra , see this [doc](docs/hydra.md) for more detail

# clearml
I like clearml because I used it previously and u can plug it on top of every usual loggers, in any case you can fall back to tensorboard if needs be. For a first run you have to do and copy paste what they ask you to do  :

```py
clearml-init

```




# Other tips

## DGX 
I love DGX, the password is the usual as the centraleSupelec one 
```bash
clearml-init

```


## Use Jupyter On a Slurm Cluster
If you want to run Jupyter on a computer node ( the one that has usually GPU).
You should do 
```bash
sbatch script/jupyter.batch
```
Then go to this [notebook](notebooks/NB_cluster.ipynb) and follow instruction 

## Macros

Command line macros are extremely useful to avoid typing the same commands over and over again. This is just a small tip that I like to do, but it can save a lot of time.
## User-personal usefull files

I advice to use files gitignored (there is a `personal_*` field in the `.gitignore` file) to store personal files, such as notes, debugging scripts, etc. It is a good practice to keep the repository clean and organized.


## Disclaimer

I am highly inspired from this awesome [repo](https://github.com/tboulet/research-project-template/tree/main)

# Autotyper

It's something I've been working for a long time I found several options:

- Pytype
- MonkeyType: seems fine if your script is not too slow
-

