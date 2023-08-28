import os
import sys
import json
import logging
import pandas as pd

from training import train_model
from scoring import score_model
from deployment import store_model_into_pickle
from diagnostics import (
    model_predictions,
    dataframe_summary,
    missing_data,
    execution_time,
    outdated_packages_list,
)
from reporting import report_score_model
from ingestion import merge_multiple_dataframe
from apicalls import request_api
from config import get_config


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CFG = get_config(production=True)
input_folder_path = CFG['input_folder_path']
output_folder_path = CFG['output_folder_path']
output_model_path = CFG['output_model_path']
test_data_csv_path = CFG['test_data_csv_path']
final_data_path = CFG['final_data_path']
prod_deployment_path = CFG['prod_deployment_path']
cfm_path = CFG['cfm_path']
api_returns_path = CFG['api_returns_path']


def ingest_files(output_folder_path):
    """
    Ingest data from the input folder and save it in the output folder

    Args:
        output_folder_path (str): path to the output folder

    Returns:
        ingested (list): list of ingested files
    """
    ingested_file_path = os.path.join(
        os.getcwd(),
        output_folder_path,
        'ingestedfiles.txt')
    with open(ingested_file_path, 'r') as ingested_file:
        ingested = ingested_file.readlines()
        ingested = [x.strip() for x in ingested]
    return ingested


def check_new_files(ingested, input_folder_path):
    """
    Check if there is new files in the input folder

    Args:
        ingested (list): list of ingested files
        input_folder_path (str): path to the input folder

    Returns:
        new_df (dataframe): dataframe with no duplicates
    """
    input_dir = os.path.join(os.getcwd(), input_folder_path)
    input_files = os.listdir(input_dir)

    all_ingest_files = list(set(ingested + input_files))
    has_new_files = False
    if len(all_ingest_files) > len(ingested):
        has_new_files = True
        logger.info('There is new files. Ingesting new files...')
    if not has_new_files:
        logger.info('There is no new file')
        sys.exit()
    ingested_file_path = os.path.join(
        os.getcwd(),
        output_folder_path,
        'ingestedfiles.txt'
    )
    new_df = merge_multiple_dataframe(
        input_folder_path,
        ingested_file_path,
        final_data_path)

    record_file_path = os.path.join(
        os.getcwd(),
        output_folder_path,
        'ingestedfiles.txt')
    with open(record_file_path, 'w') as record_file:
        for each_filename in all_ingest_files:
            record_file.write(each_filename + '\n')
    return new_df


def check_drift(new_df, prod_deployment_path):
    latest_score_file = os.path.join(
        os.getcwd(),
        prod_deployment_path,
        'latestscore.txt')
    with open(latest_score_file, 'r') as score_file:
        prev_f1_score = float(score_file.readline())

    prod_model_train_path = os.path.join(
        os.getcwd(),
        prod_deployment_path,
        'trainedmodel.pkl'
    )

    new_f1_score = score_model(prod_model_train_path, new_df)
    model_drift = False
    if new_f1_score != prev_f1_score:
        model_drift = True

    if not model_drift:
        logger.info(
            f"No drift >> Previous F1_score {prev_f1_score} = New F1_score {new_f1_score}")
        sys.exit()
    else:
        logger.info(
            f"Model drift >> Previous F1_score {prev_f1_score} != New F1_score {new_f1_score}")
        logger.info("Re-training...")
        output_model_train_path = os.path.join(
            os.getcwd(),
            output_model_path,
            'trainedmodel.pkl'
        )
        train_model(final_data_path, output_model_train_path)

        logger.info('Re-deploying')
        store_model_into_pickle(
            output_model_path,
            output_folder_path,
            prod_deployment_path)
        model_predictions(test_data_csv_path, prod_deployment_path)
        dataframe_summary(test_data_csv_path)
        missing_data(test_data_csv_path)
        execution_time(input_folder_path, prod_deployment_path)
        outdated_packages_list()
        report_score_model(test_data_csv_path, cfm_path, prod_deployment_path)
        request_api(
            URL="http://127.0.0.1:5000",
            api_returns_path=api_returns_path)
        logger.info('Done')


if __name__ == '__main__':
    ingested = ingest_files(output_folder_path)
    new_df = check_new_files(ingested, input_folder_path)
    check_drift(new_df, prod_deployment_path)
