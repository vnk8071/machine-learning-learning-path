# Machine Learning in Production

[**Introduction**](#1-introduction) | [**Workflow**](#2-workflow) | [**Installation**](#3-installation) | [**Contact**](#contact)

Released Github Pages: https://khoivn.space/machine-learning-in-production/

## 1. Introduction
Build a machine learning project in production. This repo contains the following features:

| # | Feature               | Stack             |
|:-:|-----------------------|:-----------------:|
| 0 | Language              | Python            |
| 1 | Clean code principles | Autopep8, Pylint  |
| 2 | Testing               | Pytest            |
| 3 | Logging               | Logging           |
| 4 | Data versioning       | DVC               |
| 5 | Model versioning      | DVC               |
| 6 | Configuration         | Hydra             |
| 7 | Pipeline & Monitoring | Mlflow            |
| 8 | Experiment tracking   | Weights & Biases  |
| 9 | CI/CD                 | Github Actions    |
| 10| Github Pages          | Docusaurus        |

Inspired by Machine Learning DevOps Engineer by Udacity.

Noted course: [Google drive](https://docs.google.com/document/d/1AnAgK40kud97YgnJrbMrQCO08XKDO0Zz8J6u3xR17_Q/edit?usp=sharing)

## 2. Workflow

## 3. Installation
### 3.1. Create virtual environment
```bash
pip install -r requirements.txt
```

### 3.2. Install pre-commit hooks
```bash
make pre-commit-install
```
