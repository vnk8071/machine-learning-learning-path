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
In order to run these components you need to have conda (Miniconda or Anaconda) and MLflow installed.
```bash
conda env create -f environment.yml
conda activate nyc_airbnb_dev
```

## 3. Cookie cutter
Using this template you can quickly generate new steps to be used with MLFlow.
```bash
cookiecutter cookiecutter-mlflow-template -o src

step_name [step_name]: basic_cleaning
script_name [run.py]: run.py
job_type [my_step]: basic_cleaning
short_description [My step]: This steps cleans the data
long_description [An example of a step using MLflow and Weights & Biases]: Performs basic cleaning on the data and save the results in Weights & Biases
parameters [parameter1,parameter2]: parameter1,parameter2,parameter3
```

## 4. Step-by-step
### 4.1. Download data
```bash
mlflow run . -P steps=download
```

### 4.2. EDA
```bash
mlflow run src/eda
```
More details in [![Jupyter](https://img.shields.io/badge/jupyter-%23FA0F.svg?style=for-the-badge&logo=jupyter&logoColor=white)](src/eda/EDA.ipynb)

<img src="images/EDA.png">

### 4.3. Basic cleaning
```bash
mlflow run . -P steps=basic_cleaning
...
2023-08-20 22:17:49,537 Dropping duplicates
2023-08-20 22:17:49,566 Dropping outliers
2023-08-20 22:17:49,566 Number of rows before dropping outliers: 20000
2023-08-20 22:17:49,570 Number of rows after dropping outliers: 19001
2023-08-20 22:17:49,570 Converting last_review to datetime
2023-08-20 22:17:49,577 Saving cleaned dataframe to csv
2023-08-20 22:17:49,743 Logging artifact
```

### 4.4. Check data
```bash
mlflow run . -P steps=check_data
...
test_data.py::test_column_names PASSED                                        [ 16%]
test_data.py::test_neighborhood_names PASSED                                  [ 33%]
test_data.py::test_proper_boundaries PASSED                                   [ 50%]
test_data.py::test_similar_neigh_distrib PASSED                               [ 66%]
test_data.py::test_price_range PASSED                                         [ 83%]
test_data.py::test_row_count PASSED                                           [100%]
```

### 4.5. Split data
```bash
mlflow run . -P steps=data_split
...
2023-08-21 19:13:21,935 Fetching artifact clean_sample.csv:latest
2023-08-21 19:13:25,410 Splitting trainval and test
2023-08-21 19:13:25,461 Uploading trainval_data.csv dataset
2023-08-21 19:13:31,353 Uploading test_data.csv dataset
```

### 4.6. Train and evaluate model
```bash
mlflow run . -P steps=train_random_forest
...
2023-08-21 19:55:39,523 Minimum price: 10, Maximum price: 350
2023-08-21 19:55:39,549 Preparing sklearn pipeline
2023-08-21 19:55:39,550 Fitting
2023-08-21 19:55:41,063 Computing and scoring r2 and MAE
2023-08-21 19:55:41,240 Score: 0.5519470714568394
2023-08-21 19:55:41,241 MAE: 34.12780800870754
2023-08-21 19:55:41,241 Exporting model
2023-08-21 19:55:41,242 Uploading model
```

Optimize hyper-parameters
```bash
mlflow run . \
    -P steps=train_random_forest \
    -P hydra_options="modeling.random_forest.max_depth=10,50,100 modeling.random_forest.n_estimators=100,200,500 -m"
```
<img src="images/optimize_hyper_parameters.png">

### 4.7. Test model
```bash
mlflow run . -P steps=test_regression_model
...
2023-08-21 20:52:23,425 Downloading artifacts
2023-08-21 20:52:29,760 Loading model and performing inference on test set
2023-08-21 20:52:32,254 Scoring
2023-08-21 20:52:32,341 Score: 0.5640242000942114
2023-08-21 20:52:32,341 MAE: 33.850181065122136
```

### 4.8. Test model with new dataset
```
mlflow run https://github.com/vnk8071/ml-production.git -v 1.0.1 -P hydra_options="etl.sample='sample2.csv'"
...
2023-08-21 22:06:44,481 Dropping duplicates
2023-08-21 22:06:44,607 Dropping outliers
2023-08-21 22:06:44,607 Number of rows before dropping outliers: 48895
2023-08-21 22:06:44,630 Number of rows after dropping outliers: 46427
2023-08-21 22:06:44,631 Converting last_review to datetime
2023-08-21 22:06:44,654 Saving cleaned dataframe to csv
2023-08-21 22:06:45,052 Logging artifact
...
test_data.py::test_column_names PASSED                            [ 16%]
test_data.py::test_neighborhood_names PASSED                      [ 33%]
test_data.py::test_proper_boundaries PASSED                       [ 50%]
test_data.py::test_similar_neigh_distrib PASSED                   [ 66%]
test_data.py::test_price_range PASSED                             [ 83%]
test_data.py::test_row_count PASSED                               [100%]
...
2023-08-21 22:09:01,322 Downloading artifacts
2023-08-21 22:09:04,782 Loading model and performing inference on test set
2023-08-21 22:09:05,168 Scoring
2023-08-21 22:09:05,298 Score: 0.6195968265496492
2023-08-21 22:09:05,298 MAE: 31.64257699859779
```
## 5. Public W&B project
```bash
Link: https://wandb.ai/nguyenkhoi8071/nyc_airbnb/overview?workspace=user-nguyenkhoi8071
```
