import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

import os
import logging
import sys

from logs.logger import get_logger

logger = get_logger(__name__)


def feature_select(
    input_train_file_path: str = "data/df_train.csv",
    input_test_file_path: str = "data/df_test.csv",
    random_state: int = 8071,
    output_train_file_path: str = "data/df_train_rfe.csv",
    output_test_file_path: str = "data/df_test_rfe.csv",
    target_class: str = "stroke",
):
    df_train = pd.read_csv(input_train_file_path, engine="python")
    df_test = pd.read_csv(input_test_file_path, engine="python")

    target_train = df_train[target_class].copy()
    features_train = df_train.drop(labels=[target_class], axis=1)
    selected_feature_count = int(
        np.round(0.6 * df_train.shape[1])
    )
    rfe = RFE(
        estimator=RandomForestClassifier(random_state=random_state),
        n_features_to_select=selected_feature_count,
    )

    rfe.fit(features_train, target_train)

    mask_rfe_features = rfe.get_support()
    logger.info(f"{selected_feature_count} important features")
    logger.info(features_train.columns[mask_rfe_features])

    rfe_column_list = (features_train.columns[mask_rfe_features]).tolist()
    features_train_rfe = features_train[rfe_column_list].copy()

    df_train_rfe = pd.concat([features_train_rfe, target_train], axis=1)
    df_test_rfe = df_test[rfe_column_list + [target_class]].copy()
    df_train_rfe.to_csv(output_train_file_path, index=False)
    df_test_rfe.to_csv(output_test_file_path, index=False)
    logger.info(f"Saved {output_train_file_path} and {output_test_file_path}")
    return df_train_rfe, df_test_rfe
