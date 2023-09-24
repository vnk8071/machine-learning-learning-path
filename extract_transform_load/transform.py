import pandas as pd

from logs.logger import get_logger

logger = get_logger(__name__)


def run(df: pd.DataFrame):
    df = fill_missing(df=df, columns=["bmi"])
    df = drop_match_values(df=df, column="gender", value="Other")
    df = drop_columns(df=df, columns=["id"])
    df = reformat_type(df=df, columns=["age"], type="int64")
    return df


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
