
import pandas as pd
import numpy as np
import timeit
import os
import subprocess
import json
import pickle
import logging
from sklearn.model_selection import train_test_split

from ingestion import merge_multiple_dataframe
from training import train_model
from config import get_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
CFG = get_config(production=False)

input_folder_path = CFG['input_folder_path']
test_data_path = CFG['test_data_path']
test_data_csv_path = CFG['test_data_csv_path']
prod_deployment_path = CFG['prod_deployment_path']
output_folder_path = CFG['output_folder_path']
final_data_path = CFG['final_data_path']


def model_predictions(test_data_csv_path, prod_deployment_path):
    """
    Predict the model and save the prediction in the output folder

    Args:
        test_data_csv (str): path to the test data csv file
        prod_deployment_path (str): path to the production deployment folder

    Returns:
        y_pred (list): list of predictions
    """
    lr_model = pickle.load(
        open(
            os.path.join(
                os.getcwd(),
                prod_deployment_path,
                "trainedmodel.pkl"),
            'rb'))
    test_df = pd.read_csv(test_data_csv_path)
    test_df = test_df.drop(['corporation'], axis=1)

    X_test = test_df.iloc[:, :-1]
    y_pred = lr_model.predict(X_test)
    return y_pred


def dataframe_summary(test_data_csv_path):
    """
    Calculate summary statistics of the training data

    Args:
        test_data_csv_path (str): path to the test data csv file

    Returns:
        summary_statistics (list): list of summary statistics
    """
    final_df = pd.read_csv(test_data_csv_path)
    final_df = final_df.drop(['corporation'], axis=1)
    X = final_df.iloc[:, :-1]

    # calculate summary statistics of the training data
    summary = X.agg(['mean', 'median', 'std', 'min', 'max'])
    summary_statistics = list(summary['lastmonth_activity']) + \
        list(summary['lastyear_activity']) + \
        list(summary['number_of_employees'])
    return summary_statistics


def missing_data(test_data_csv_path):
    """
    Calculate the percentage of missing data in the training data

    Args:
        test_data_csv_path (str): path to the test data csv file

    Returns:
        missing_values_df (list): list of missing values
    """
    final_df = pd.read_csv(test_data_csv_path)
    final_df = final_df.drop(['corporation'], axis=1)

    missing_values_df = final_df.isna().sum() / final_df.shape[0]
    return missing_values_df.values.tolist()


def execution_time(
    input_folder_path,
    prod_deployment_path
):
    """
    Calculate the average time taken for ingestion and training

    Returns:
        ingestion_timing (float): average time taken for ingestion
        training_timing (float): average time taken for training
    """
    iteration = 10
    starttime = timeit.default_timer()
    ingested_files_path = os.path.join(
        os.getcwd(),
        prod_deployment_path,
        'ingestedfiles.txt'
    )
    for i in range(iteration):
        merge_multiple_dataframe(
            input_folder_path,
            ingested_files_path,
            final_data_path)
    ingestion_timing = (timeit.default_timer() - starttime) / iteration
    logger.info('Ingestion time: {}'.format(ingestion_timing))

    prod_model_train_path = os.path.join(
        os.getcwd(),
        prod_deployment_path,
        'trainedmodel.pkl'
    )
    starttime = timeit.default_timer()
    for i in range(iteration):
        train_model(final_data_path, prod_model_train_path)
    training_timing = (timeit.default_timer() - starttime) / iteration
    logger.info('Training time: {}'.format(training_timing))
    return ingestion_timing, training_timing


def outdated_packages_list():
    """
    Check for outdated packages in the requirements.txt file

    Returns:
        df.values.tolist() (list): list of outdated packages
    """
    df = pd.DataFrame(columns=['package_name', 'current', 'recent_available'])

    with open("requirements.txt", "r") as file:
        strings = file.readlines()
        package_names = []
        curent_versions = []
        recent = []

        for line in strings:
            package_name, cur_ver = line.strip().split('==')
            package_names.append(package_name)
            curent_versions.append(cur_ver)
            info = subprocess.check_output(
                ['python', '-m', 'pip', 'show', package_name])
            recent.append(str(info).split('\\n')[1].split()[1])

        df['package_name'] = package_names
        df['current'] = curent_versions
        df['recent_available'] = recent
    logger.info('Outdated packages: {}'.format(df.values.tolist()))
    return df.values.tolist()


if __name__ == '__main__':
    model_predictions(test_data_csv_path, prod_deployment_path)
    dataframe_summary(test_data_csv_path)
    missing_data(test_data_csv_path)
    execution_time(input_folder_path, prod_deployment_path)
    outdated_packages_list()
