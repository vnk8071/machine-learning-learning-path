import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from logs.logger import get_logger

logger = get_logger(__name__)


def run(df: pd.DataFrame, output_file_path: str):
    df = standardize_numeric_columns(
        df=df,
        columns=df.drop(
            labels=["stroke"],
            axis=1
        ).select_dtypes(include=['int64', 'float64']).columns.to_list()
    )
    df = label_encode(df=df, columns=df.select_dtypes(
        include=['object']).columns.to_list())
    df.to_csv(output_file_path, index=False)
    return df


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
    sc = StandardScaler()
    df_copy = df.copy()
    logger.info(f"Standardizing {columns}")
    df_copy[columns] = sc.fit_transform(df_copy[columns])

    std = np.sqrt(sc.var_)
    np.save('feature_engineering/std.npy', std)
    np.save('feature_engineering/mean.npy', sc.mean_)
    return df_copy
