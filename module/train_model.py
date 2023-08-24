"""
Project: Deploy a ML Model to Cloud Application Platform with FastAPI
Author: vnk8071
Date: 2023-08-24
"""

import os
import sys
import pickle
import logging
import pandas as pd
from sklearn.model_selection import train_test_split

try:
    from module.data import process_data
    from module.model import (
        inference,
        compute_model_metrics,
        train_model,
        compute_metrics_with_slices_data
    )
except ModuleNotFoundError:
    sys.path.append('./')
    from module.data import process_data
    from module.model import (
        inference,
        compute_model_metrics,
        train_model,
        compute_metrics_with_slices_data
    )


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
data = pd.read_csv("data/census_clean.csv")
logger.info(data.describe())

# Optional enhancement, use K-fold cross validation instead of a train-test split.
logger.info("Splitting data into train and test sets...")
train, test = train_test_split(data, test_size=0.20)

cat_features = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]

# Process the training data.
logger.info("Processing data...")
X_train, y_train, encoder, lb = process_data(
    train, categorical_features=cat_features, label="salary", training=True
)

X_test, y_test, encoder, lb = process_data(
    X=test,
    categorical_features=cat_features,
    label="salary",
    training=False,
    encoder=encoder,
    lb=lb
)

# Train and save a model.
logger.info("Training model...")
model = train_model(X_train, y_train)
logger.info(model)

logger.info("Saving model...")
if not os.path.exists("model/"):
    os.mkdir("model/")
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)
logger.info("Model saved.")

# Inference on the test data.
logger.info("Inference model...")
preds = inference(model, X_test)

# Calculate accuracy, precision, recall, and F1 scores.
logger.info("Calculating model metrics...")
precision, recall, fbeta = compute_model_metrics(y_test, preds)
logger.info(f">>>Precision: {precision}")
logger.info(f">>>Recall: {recall}")
logger.info(f">>>Fbeta: {fbeta}")


# Calculate accuracy, precision, recall, and F1 scores on slices data.
logger.info("Calculating model metrics on slices data...")
precision_slices, recall_slices, fbeta_slices = compute_metrics_with_slices_data(
    df=test,
    cat_columns=cat_features,
    label="salary",
    encoder=encoder,
    lb=lb,
    model=model
)
logger.info(f">>>Precision with slices data: {precision_slices}")
logger.info(f">>>Recall with slices data: {recall_slices}")
logger.info(f">>>Fbeta with slices data: {fbeta_slices}")
