<div align="center">

# Research Project Template
### A starting point for students

[![python](https://img.shields.io/badge/-Python_3.10-blue?logo=python&logoColor=white)](https://www.python.org/)

<p align="center">
  <img width="60%" src="./images/logo_safe.jpg">
</p>

</div>

## 📌 What this is

A minimal template for a research codebase: environment setup, SLURM scripts, pre-commit hooks.


You are not obliged to start from this repo. But if you are one of my students, I strongly
recommend following the structure and following the below README template.

---

## 🚀 Quickstart

```bash
git clone <...>
cd research-project-template

# Read this file before running it: it pins a CUDA version and creates a conda env.
bash script/first_install.sh

conda activate venv
python train.py
```

`train.py` is a skeleton. It sets the seed, picks a device and prints a message: your
training loop goes there.

> **Note:** `conda activate` does not work inside a plain `bash script.sh` unless conda has
> been initialised in that shell. If the script stops at the activate step, run the commands
> one by one, or `source script/first_install.sh`.

---

## 🧱 What is in the box

### `script/first_install.sh` — environment setup

Creates a conda env (`venv`, Python 3.10), installs the CUDA toolkit and a matching PyTorch
build, then `requirements.txt` and `dev_requirements.txt`.

Edit `CUDA_VERSION` at the top to match your machine or cluster (check with `nvidia-smi`).
Getting the CUDA/PyTorch versions to agree is the single most common source of lost time:
do it once, carefully.


### `script/*.batch` — SLURM jobs

Written for CentraleSupelec's DGX cluster; adapt the partition, `--gres` and walltime for
yours.

- `run_file.batch` — submit a training run: `sbatch script/run_file.batch`
- `jupyter.batch` — start a Jupyter server on a compute node, then connect through an SSH
  tunnel to the printed host and port

### `.pre-commit-config.yaml` — checks before every commit

Runs `ruff` (lint + format), strips notebook outputs, blocks large files and private keys.
This keeps diffs readable and stops you from committing a 500 MB checkpoint.

```bash
pip install pre-commit
pre-commit install          # installs the git hook, once per clone
pre-commit run --all-files # runs the pre-commit on all files. But it should be triggered automatically each time you run a git commit
```
### `CLAUDE.md` / `agents.md` — coding-agent guidelines

Instructions given to Claude Code or Codex when they edit this repo: think before coding,
keep it simple, make surgical changes. Adapted from the PyTorch guidelines; works well
enough.


### `.devcontainer/` — Docker dev environment (optional)

Only useful if you have Docker access (personal laptop, some company clusters). Open the
folder in VS Code and choose *Reopen in Container*. Edit the `mounts` entry in
`devcontainer.json` to point at your own dataset directory.



---

## 📚 To go further

- [Lightning Hydra Template](https://github.com/ashleve/lightning-hydra-template) — a much
  larger template. Powerful, but not beginner-friendly.
- [Hydra documentation](https://hydra.cc/docs/intro/) — config handling.
- [old full research project template](https://github.com/gardiens/research-project-template/tree/main/script) -  This is what I did for a student project.
**Working remotely.** :
- [SSH config](https://www.ssh.com/academy/ssh/config) — give your machines short names in
  `~/.ssh/config` instead of retyping `user@long.hostname.fr`.
- [VS Code Remote-SSH](https://code.visualstudio.com/docs/remote/ssh) — editor, terminal and
  Jupyter kernels all running on the remote machine. This is the default choice; check first
  whether your cluster allows it on the login node. ( blocked on Jean-Zay)
- [sshfs](https://github.com/libfuse/sshfs) — mount a remote directory as a local
  folder, handy for opening figures and logs with local tools. 
- [Oh my tmux](https://github.com/gpakosz/.tmux) — keep remote sessions alive when your SSH
  connection drops (Linux/macOS).

---
---

# 📄 Project README template

*Everything below is the template for **your** project's README. Copy it into your own
repository, fill in the placeholders and delete everything above.*

---

<div align="center">

# Project name: what it is

[![python](https://img.shields.io/badge/-Python_3-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Paper](http://img.shields.io/badge/paper-arxiv.1001.2234-B31B1B.svg)](https://arxiv.org/abs/2511.16542)
[![Conference](http://img.shields.io/badge/AnyConference-year-4b44ce.svg)](https://isprs-annals.copernicus.org/articles/XI-2-2026/217/2026/)

<p align="center">
  <img width="60%" src="./images/logo_safe.jpg">
</p>

</div>

## 📌 Description

One paragraph: what problem this solves, and what the main result is.

## 📁 Project structure

```
├── configs                <- Hydra configs
│   └── experiments        <- One file per experiment
├── docs                   <- Notes and guidelines
├── images                 <- Figures used in the README and the paper
├── notebooks              <- Exploration and figure generation
├── script                 <- Install and cluster job scripts
├── src                    <- Source code (datasets, models, losses)
├── tests                  <- Pytest tests
└── train.py               <- Training entry point
```

## 💻 Environment requirements

Tested on `<cluster / GPU / CUDA version>`.

## 🏗 Installation

```bash
git clone https://github.com/YourGithubName/your-repo-name
cd your-repo-name

bash script/first_install.sh
conda activate venv
```

## 📦 Datasets

Where the data lives and how to get it. Default paths point to:

```text
/workspaces/external_datasets/<your-dataset>/
```

## 🚀 Usage

```bash
python train.py                  # default config
python train.py experiments=debug    # quick run
sbatch script/run_file.batch     # on the cluster
```

## 📊 Results

A table or a figure. State the checkpoint and the config used to reproduce it.

## 📝 Citing our work

```bibtex
@article{your_key,
  title   = {...},
  author  = {...},
  journal = {arXiv preprint arXiv:XXXX.XXXXX},
  year    = {20XX}
}
```
