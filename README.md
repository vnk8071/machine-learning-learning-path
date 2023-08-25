# Machine Learning in Production

## 1. Introduction
Build machine learning project in production. This repo contains the following topics:
- Clean code principles
- Testing
- Logging
- Data versioning
- Model versioning
- CI/CD
- Monitoring

Technologies stack used:
- Language: Python
- Lint and formatter: Autopep8, Pylint
- Testing: Pytest
- Pre-commit hooks: pre-commit
- Configuration: Hydra
- Model versioning: MLflow
- Experiment tracking: Weights & Biases

Inspired by Machine Learning DevOps Engineer by Udacity.


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

## 3. Data
### 3.1. Download data
```bash
data/census.csv
```
Link: https://archive.ics.uci.edu/ml/datasets/census+income

### 3.2. EDA
EDA in notebook: [![Jupyter](https://img.shields.io/badge/jupyter-%23FA0F.svg?style=for-the-badge&logo=jupyter&logoColor=white)](EDA.ipynb)

### 3.3. Data versioning
```bash
dvc init
mkdir ../local_remote
dvc remote add -d localremote ../local_remote
dvc add data/census.csv
dvc add data/census_clean.csv
git add data/.gitignore data/census.csv.dvc data/census_clean.csv.dvc
git commit -m "Add data"
dvc push
```

## 4. Train Model
```bash
python module/train_model.py
```
Result
```
2023-08-25 20:32:56,405 - INFO - Splitting data into train and test sets...
2023-08-25 20:32:56,412 - INFO - Processing data...
2023-08-25 20:32:56,634 - INFO - Training model...
2023-08-25 20:32:57,052 - INFO - LogisticRegression(max_iter=1000, random_state=8071)
2023-08-25 20:32:57,058 - INFO - Saving model...
2023-08-25 20:32:57,059 - INFO - Model saved.
2023-08-25 20:32:57,059 - INFO - Inference model...
2023-08-25 20:32:57,060 - INFO - Calculating model metrics...
2023-08-25 20:32:57,074 - INFO - >>>Precision: 0.6551724137931034
2023-08-25 20:32:57,074 - INFO - >>>Recall: 0.24934383202099739
2023-08-25 20:32:57,075 - INFO - >>>Fbeta: 0.36121673003802285
2023-08-25 20:32:57,075 - INFO - Calculating model metrics on slices data...
2023-08-25 20:32:58,281 - INFO - >>>Metrics with slices data:             feature  ...                    category
0         workclass  ...                     Private
1         workclass  ...                           ?
2         workclass  ...                 Federal-gov
3         workclass  ...            Self-emp-not-inc
4         workclass  ...                   State-gov
..              ...  ...                         ...
96   native-country  ...                   Nicaragua
97   native-country  ...                    Scotland
98   native-country  ...  Outlying-US(Guam-USVI-etc)
99   native-country  ...                     Ireland
100  native-country  ...                     Hungary

[101 rows x 5 columns]
```

## 5. Run sanity checks
```bash
python sanity_checks.py
```
Result
```
============= Sanity Check Report ===========
2023-08-24 23:16:57,951 - INFO - Your test cases look good!
2023-08-24 23:16:57,951 - INFO - This is a heuristic based sanity testing and cannot guarantee the correctness of your code.
2023-08-24 23:16:57,951 - INFO - You should still check your work against the rubric to ensure you meet the criteria.
```

## 6. Run tests
```bash
pytest tests/
```
Result
```
tests/test_api.py ....                                                         [ 33%]
tests/test_model.py ........                                                   [100%]
=========================== 12 passed, 4 warnings in 3.65s ===========================
```

## 7. CI/CD
### 7.1. Github Actions
<img src="images/continuous_integration.png">

### 7.2. CD with Render
Settings continuous deployment on Render
<img src="images/settings_continuous_deployment.png">
Deployed app
<img src="images/continuous_deployment.png">

## 8. Request API
### 8.1. Local
```bash
uvicorn module.api:app --reload
```
Result
<img src="images/local_post.png">

### 8.2. Render
Check API get method at: https://vnk8071-api-deployment.onrender.com/docs
<img src=images/live_get.png>

Script to request API method POST
```bash
python inference.py
```
<img src="images/live_post.png">
