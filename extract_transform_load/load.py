import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from logs.logger import get_logger

logger = get_logger(__name__)


def run(
    df: pd.DataFrame,
    output_train_file_path: str,
    output_test_file_path: str
):
    df_train, df_test = split_data(
        df=df,
        test_size=0.2,
        random_state=8071
    )
    save_csv(df=df_train, output_file_path=output_train_file_path)
    save_csv(df=df_test, output_file_path=output_test_file_path)
    return df_train, df_test


def save_csv(df: pd.DataFrame, output_file_path: str):
    """Save DataFrame to CSV

    Args:
        df (pd.DataFrame): DataFrame to save
        output_file_path (str): File path to save DataFrame
    """
    logger.info(f"Saving file to {output_file_path}")
    df.to_csv(output_file_path, index=False)


def split_data(df: pd.DataFrame, test_size: float, random_state: int):
    """Split DataFrame into train and test sets

    Args:
        df (pd.DataFrame): DataFrame to split
        test_size (float): Test size
        random_state (int): Random state

    Returns:
        df_train (pd.DataFrame): DataFrame of train set
        df_test (pd.DataFrame): DataFrame of test set
    """
    df_stroke = df[df["stroke"] == 1]
    features_stroke = df_stroke.drop(labels=["stroke"], axis=1)
    target_stroke = df_stroke["stroke"]

    df_no_stroke = df[df["stroke"] == 0]
    features_no_stroke = df_no_stroke.drop(labels=["stroke"], axis=1)
    target_no_stroke = df_no_stroke["stroke"]

    logger.info(
        "Splitting data into train and test sets with no stroke record test size of 0.05")
    features_no_stroke_train, features_no_stroke_test, target_no_stroke_train, target_no_stroke_test = train_test_split(
        features_no_stroke,
        target_no_stroke,
        test_size=0.05,
        random_state=random_state
    )
    logger.info(
        f"Splitting data into train and test sets with stroke record test size of {test_size}")
    features_stroke_train, features_stroke_test, target_stroke_train, target_stroke_test = train_test_split(
        features_stroke,
        target_stroke,
        test_size=test_size,
        random_state=random_state
    )
    features_train = pd.concat(
        [features_no_stroke_train, features_stroke_train], axis=0)
    target_train = pd.concat(
        [target_no_stroke_train, target_stroke_train], axis=0)
    features_test = pd.concat(
        [features_no_stroke_test, features_stroke_test], axis=0)
    target_test = pd.concat(
        [target_no_stroke_test, target_stroke_test], axis=0)
    df_train = pd.concat([features_train, target_train], axis=1)
    df_test = pd.concat([features_test, target_test], axis=1)
    return df_train, df_test
