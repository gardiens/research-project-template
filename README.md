
<div align="center">

# Pierrick Bournez : Student Template  .
[![python](https://img.shields.io/badge/-Python_3-blue?logo=python&logoColor=white)](https://www.python.org/)



<p align="center">
  <img width="60%" src="./images/logo_safe.jpg">
</p>


# 📌  Introduction
This is a template repository for new projects. You should not start from this repo but it may help you when you will use other's people code or if you want to write a codebase. 

I provide below a template readme . If you are one of my student, I strongly recommend to follow and adapt the template.  
## 🏗 Installation
I provided a template to set up a working python/pytorch environments. 
Look at first_install.sh and run:

```bash
bash script/first_install.sh
```
## Devcontainer
Usefull only if you have acess to docker. usually available on company clusters or personal laptop.  


## Agent and Claude.md 
It tells Codex or CLaude some guideline when coding. I took the one from torch I think and it works ok-ish

## Pre-commit explanation
It enables to apply aoperation before some git operations. in this template, it applies ruff and some standard code   check on notebook before every commit. install it with pip install pre-commit. 
install the hook with pre-commit install 







## To go further : 

A [non-friendly template of code: Lightning Hydra Template](https://github.com/ashleve/lightning-hydra-template/tree/main)
A config handler: [Hydra](https://hydra.cc/docs/intro/)
Tmux custom profile ( for linux only ): [Oh my tmux](https://github.com/gpakosz/.tmux)


--------------------------------------------------------------------------------------------




<div align="center">

# Project name: what it is  .
[![python](https://img.shields.io/badge/-Python_3-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Paper](http://img.shields.io/badge/paper-arxiv.1001.2234-B31B1B.svg)](https://arxiv.org/abs/2511.16542)
[![Conference](http://img.shields.io/badge/AnyConference-year-4b44ce.svg)](https://isprs-annals.copernicus.org/articles/XI-2-2026/217/2026/)


<p align="center">
  <img width="60%" src="./images/logo_safe.jpg">
</p>

##  📌  Description


Description of the project


## Project structure: 
The directory structure of new project looks like this: 

```
├── .github                   <- Github Actions workflows
│
├── configs                   <- Hydra configs
│   ├── callbacks                <- Callbacks configs
├── src
│   ├── datasets <- Datasets handling.
│

```
## 💻  Environment requirements

This project was tested on `CLUSTERS`.


<br>

## 🏗 Installation
Run the following command 



```bash
git clone https://github.com/YourGithubName/your-repo-name
cd your-repo-name
 
conda create -n myenv python=3.9
conda activate myenv

bash install.sh
pip install -r requirements.txt --no-build-isolation
```

## 🚀  Usage

### 📦 Datasets

Default script paths point to:
```text
/workspaces/external_datasets/satnerf/
```

### 🧠 RUN
Run the script
```bash


bash run.sh
python trian.py
```





## Citing our work

Put your arxiv here;