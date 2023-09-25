import json
import logging
import sys
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import pickle
from io import StringIO

from logs.logger import get_logger

logger = get_logger(__name__)


def fill_missing(df: pd.DataFrame, columns: list):
    """Fill missing values in columns with the mean of the column

    Args:
        df (pd.DataFrame): DataFrame to fill missing values
        columns (list): List of columns to fill missing values

    Returns:
        pd.DataFrame: DataFrame with filled missing values
    """
    df_copy = df.copy()
    logger.info(f"Filling missing values in {columns}")
    df_copy[columns] = df_copy[columns].fillna(
        round(df_copy[columns].mean(), 2))
    return df_copy


def drop_match_values(df: pd.DataFrame, column: str, value: str):
    """Drop rows with matching values in columns

    Args:
        df (pd.DataFrame): DataFrame to drop rows
        columns (list): List of columns to check for matching values
        value (str): Value to match in columns

    Returns:
        pd.DataFrame: DataFrame with dropped rows
    """
    logger.info(f"Dropping rows with {value} in {column}")
    df.drop(labels=df[df[column] == value].index, inplace=True)
    return df


def drop_columns(df: pd.DataFrame, columns: list):
    """Drop columns

    Args:
        df (pd.DataFrame): DataFrame to drop columns
        columns (list): List of columns to drop

    Returns:
        pd.DataFrame: DataFrame with dropped columns
    """
    logger.info(f"Dropping columns {columns}")
    df.drop(labels=columns, axis=1, inplace=True)
    return df


def reformat_type(df: pd.DataFrame, columns: list, type: str):
    """Reformat type of columns"""
    df_copy = df.copy()
    logger.info(f"Reformatting type of {columns} to {type}")
    df_copy[columns] = df_copy[columns].astype(type)
    return df_copy


def label_encode(df: pd.DataFrame, columns: list):
    """Label encode columns

    Args:
        df (pd.DataFrame): DataFrame to label encode
        columns (list): List of columns to label encode

    Returns:
        pd.DataFrame: DataFrame with label encoded columns
    """
    df_copy = df.copy()
    logger.info(f"Label encoding {columns}")
    for column in columns:
        df_copy[column] = LabelEncoder().fit_transform(df_copy[column])
    return df_copy


def standardize_numeric_columns(df: pd.DataFrame, columns: list):
    """Standardize numeric columns

    Args:
        df (pd.DataFrame): DataFrame to standardize
        columns (list): List of columns to standardize

    Returns:
        pd.DataFrame: DataFrame with standardized columns
    """
    std = np.load('feature_engineering/std.npy')
    mean = np.load('feature_engineering/mean.npy')
    df_copy = df.copy()
    logger.info(f"Standardizing {columns}")
    df_copy[columns] = (df_copy[columns] - mean) / std
    return df_copy


def preprocess_input(df: pd.DataFrame):
    """Preprocess input DataFrame

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: Preprocessed DataFrame
    """
    df = drop_columns(df=df, columns=["id"])
    df = reformat_type(df=df, columns=["age"], type="int64")
    df = standardize_numeric_columns(
        df=df,
        columns=df.select_dtypes(
            include=['int64', 'float64']).columns.to_list()
    )
    df = label_encode(df=df, columns=df.select_dtypes(
        include=['object']).columns.to_list())
    return df


def model_fn(model_dir):
    """Load model object from model directory"""
    model_file_path = os.path.join(model_dir, "model.pkl")
    with open(model_file_path, "rb") as f:
        model = pickle.load(f)
    return model


def input_fn(request_body):
    """Load input data from request body"""
    logger.info(f"Request body is: {request_body}")
    df_test = pd.DataFrame(
        {k: v for k, v in request_body.dict().items()}, index=[0]
    )
    logger.info(f"Loaded DataFrame: {df_test}")

    df_test = preprocess_input(df=df_test)
    df_test = df_test[
        ['gender', 'age', 'hypertension', 'work_type',
            'avg_glucose_level', 'bmi', 'smoking_status']
    ]
    logger.info(f"Preprocessed DataFrame: {df_test}")
    return df_test


def predict_fn(input_object, model):
    """Make predictions on input data"""
    prediction = model.predict(input_object)
    logger.info(f"Prediction results: {prediction}")
    return "stroke" if prediction[0] == 1 else "no stroke"
