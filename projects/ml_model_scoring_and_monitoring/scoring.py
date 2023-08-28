from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from config import get_config
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
CFG = get_config(production=False)
output_model_path = CFG["output_model_path"]
test_data_csv_path = CFG["test_data_csv_path"]
test_data_csv = pd.read_csv(test_data_csv_path)
output_model_train_path = os.path.join(
    os.getcwd(),
    output_model_path,
    'trainedmodel.pkl'
)


def score_model(output_model_train_path, test_data_csv):
    """
    Score the model and save the score in the output folder

    Args:
        output_model_train_path (str): path to the trained model pickle file
        test_data_csv (pd.Dataframe): test data

    Returns:
        f1_score (float): f1 score of the model
    """
    logger.info('Scoring model')

    lr_model = pickle.load(open(output_model_train_path, 'rb'))
    test_df = test_data_csv.drop(["corporation"], axis=1)
    X_test = test_df.iloc[:, :-1]
    y_test = test_df.iloc[:, -1]

    y_pred = lr_model.predict(X_test)
    f1_score = metrics.f1_score(y_test, y_pred)

    latest_score_path = os.path.join(
        os.getcwd(),
        output_model_path,
        'latestscore.txt'
    )
    with open(latest_score_path, 'w') as f:
        f.write(str(f1_score))
    logger.info('F1 score: {}'.format(f1_score))
    return f1_score


if __name__ == '__main__':
    score_model(output_model_train_path, test_data_csv)
