import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions
from config import get_config
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CFG = get_config(production=False)
dataset_csv_path = CFG['output_folder_path']
test_data_csv_path = CFG['test_data_csv_path']
output_model_path = CFG['output_model_path']
prod_deployment_path = CFG['prod_deployment_path']
cfm_path = CFG['cfm_path']


def report_score_model(test_data_csv_path, cfm_path, prod_deployment_path):
    """
    Score the model and save the score in the output folder

    Args:
        test_data_csv_path (str): path to the test data csv file
        cfm_path (str): path to the confusion matrix file
        prod_deployment_path (str): path to the production deployment folder
    """
    test_data_csv = pd.read_csv(test_data_csv_path)
    y_true = test_data_csv['exited'].values
    y_pred = model_predictions(test_data_csv_path, prod_deployment_path)

    cfm = metrics.confusion_matrix(y_true, y_pred)
    logger.info('Confusion matrix: {}'.format(cfm))

    classes = ["0", "1"]
    df_cfm = pd.DataFrame(cfm, index=classes, columns=classes)
    cfm_plot = sns.heatmap(df_cfm, annot=True)
    cfm_plot.figure.savefig(cfm_path)
    logger.info('Confusion matrix saved at {}'.format(cfm_path))


if __name__ == '__main__':
    report_score_model(test_data_csv_path, cfm_path, prod_deployment_path)
