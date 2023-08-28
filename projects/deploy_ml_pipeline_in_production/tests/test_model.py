"""
Project: Deploy a ML Model to Cloud Application Platform with FastAPI
Author: vnk8071
Date: 2023-08-24
"""

import pickle
import pandas as pd
import pandas.api.types as pdtypes
import pytest
from sklearn.model_selection import train_test_split

from module.data import process_data
from module.model import inference, compute_model_metrics

fake_categorical_features = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",

]


@pytest.fixture(scope="module")
def data():
    return pd.read_csv("data/census_clean.csv", skipinitialspace=True)


def test_column_presence_and_type(data):
    """Tests that cleaned csv file has expected columns and types.

    Args:
        data (pd.DataFrame): Dataset for testing
    """

    required_columns = {
        "age": pdtypes.is_int64_dtype,
        "workclass": pdtypes.is_object_dtype,
        "fnlgt": pdtypes.is_int64_dtype,
        "education": pdtypes.is_object_dtype,
        "education-num": pdtypes.is_int64_dtype,
        "marital-status": pdtypes.is_object_dtype,
        "occupation": pdtypes.is_object_dtype,
        "relationship": pdtypes.is_object_dtype,
        "race": pdtypes.is_object_dtype,
        "sex": pdtypes.is_object_dtype,
        "capital-gain": pdtypes.is_int64_dtype,
        "capital-loss": pdtypes.is_int64_dtype,
        "hours-per-week": pdtypes.is_int64_dtype,
        "native-country": pdtypes.is_object_dtype,
        "salary": pdtypes.is_object_dtype,
    }

    assert set(data.columns.values).issuperset(set(required_columns.keys()))

    # Check that the columns are of the right dtype
    for col_name, format_verification_funct in required_columns.items():

        assert format_verification_funct(
            data[col_name]
        ), f"Column {col_name} failed test {format_verification_funct}"


def workclass_values(data):
    """Tests that the workclass column has the expected values.

    Args:
        data (pd.DataFrame): Dataset for testing
    """
    expected_values = {
        "Private",
        "Self-emp-not-inc",
        "Self-emp-inc",
        "Federal-gov",
        "Local-gov",
        "State-gov",
        "Without-pay",
        "Never-worked",
    }

    assert set(data["workclass"].unique()) == expected_values


def education_values(data):
    """Tests that the education column has the expected values.

    Args:
        data (pd.DataFrame): Dataset for testing
    """
    expected_values = {
        "Bachelors",
        "Some-college",
        "11th",
        "HS-grad",
        "Prof-school",
        "Assoc-acdm",
        "Assoc-voc",
        "9th",
        "7th-8th",
        "12th",
        "Masters",
        "1st-4th",
        "10th",
        "Doctorate",
        "5th-6th",
        "Preschool",
    }

    assert set(data["education"].unique()) == expected_values


def marital_status_values(data):
    """Tests that the marital-status column has the expected values.

    Args:
        data (pd.DataFrame): Dataset for testing
    """
    expected_values = {
        "Married-civ-spouse",
        "Divorced",
        "Never-married",
        "Separated",
        "Widowed",
        "Married-spouse-absent",
        "Married-AF-spouse",
    }

    assert set(data["marital-status"].unique()) == expected_values


def occupation_values(data):
    """Tests that the occupation column has the expected values.

    Args:
        data (pd.DataFrame): Dataset for testing
    """
    expected_values = {
        "Tech-support",
        "Craft-repair",
        "Other-service",
        "Sales",
        "Exec-managerial",
        "Prof-specialty",
        "Handlers-cleaners",
        "Machine-op-inspct",
        "Adm-clerical",
        "Farming-fishing",
        "Transport-moving",
        "Priv-house-serv",
        "Protective-serv",
        "Armed-Forces",
    }

    assert set(data["occupation"].unique()) == expected_values


def relationship_values(data):
    """Tests that the relationship column has the expected values.

    Args:
        data (pd.DataFrame): Dataset for testing
    """
    expected_values = {
        "Wife",
        "Own-child",
        "Husband",
        "Not-in-family",
        "Other-relative",
        "Unmarried",
    }

    assert set(data["relationship"].unique()) == expected_values


def test_sex_values(data):
    """Tests that the sex column has the expected values.

    Args:
        data (pd.DataFrame): Dataset for testing
    """
    expected_values = {
        "Male",
        "Female"
    }

    assert set(data["sex"]) == expected_values


def test_salary_values(data):
    """Tests that the salary column has the expected values.

    Args:
        data (pd.DataFrame): Dataset for testing
    """
    expected_values = {
        "<=50K",
        ">50K"
    }

    assert set(data["salary"]) == expected_values


def test_column_ranges(data):

    ranges = {
        "age": (17, 90),
        "education-num": (1, 16),
        "hours-per-week": (1, 99),
        "capital-gain": (0, 99999),
        "capital-loss": (0, 4356),
    }

    for col_name, (minimum, maximum) in ranges.items():
        assert data[col_name].min() >= minimum
        assert data[col_name].max() <= maximum


def test_column_values(data):
    # Check that the columns are of the right dtype
    for col_name in data.columns.values:
        assert not data[col_name].isnull().any(
        ), f"Column {col_name} has null values"


def test_model_input(data):
    for col_name in data.columns.values:
        assert not data[col_name].isnull().any(
        ), f"Features {col_name} has null values"


def test_inference(data):
    """
    Assert that inference function returns correct
    amount of predictions with respect to the input
    """

    _, test_df = train_test_split(data, test_size=0.20)
    [encoder, lb, lr_model] = pickle.load(open("model/lr_model.pkl", "rb"))

    X_test, y_test, _, _ = process_data(
        X=test_df,
        categorical_features=fake_categorical_features,
        label="salary",
        training=False,
        encoder=encoder,
        lb=lb
    )
    preds = inference(lr_model, X_test)

    assert len(preds) == len(X_test)


def test_output_metrics(data):
    """
    Assert that output metrics are in the correct range
    """

    _, test_df = train_test_split(data, test_size=0.20)
    [encoder, lb, lr_model] = pickle.load(open("model/lr_model.pkl", "rb"))

    X_test, y_test, _, _ = process_data(
        X=test_df,
        categorical_features=fake_categorical_features,
        label="salary",
        training=False,
        encoder=encoder,
        lb=lb
    )

    preds = inference(lr_model, X_test)
    precision, recall, fbeta = compute_model_metrics(y_test, preds)

    assert precision >= 0.0
    assert precision <= 1.0

    assert recall >= 0.0
    assert recall <= 1.0

    assert fbeta >= 0.0
    assert fbeta <= 1.0
