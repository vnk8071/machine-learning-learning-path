---
sidebar_position: 1
---

# Machine Learning in Production

## 1. Introduction
Build a machine learning project in production. This repo contains the following features:

| # | Feature | Stack |
|---|-----------------------|:-----------------:|
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

Inspired by Machine Learning Engineer & Machine Learning DevOps Engineer by Udacity.

Noted course: [Google drive](https://drive.google.com/drive/folders/1Y6Or5U399MrGJBZRVrKwX2YfBPScoMYK?usp=sharing)

## 2. Installation
### 2.1. Create virtual environment
```bash
make poetry-download
make install
```

### 2.2. Install pre-commit hooks
```bash
make pre-commit-install
```
