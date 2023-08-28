import logging
import pandas as pd
import numpy as np
import os
import json
import glob
from datetime import datetime
from config import get_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
CFG = get_config(production=False)

input_folder_path = CFG['input_folder_path']
output_folder_path = CFG['output_folder_path']
final_data_path = CFG['final_data_path']
ingested_files_path = os.path.join(
    os.getcwd(),
    output_folder_path,
    'ingestedfiles.txt'
)


def merge_multiple_dataframe(
        input_folder_path,
        ingested_files_path,
        final_data_path):
    """
    Merge multiple csv files into one dataframe and remove duplicates

    Args:
        input_folder_path (str): path to the input folder
        ingested_files_path (str): path to the ingested files
        final_data_path (str): path to the final data

    Returns:
        process_df (dataframe): dataframe with no duplicates
    """
    files_list = os.listdir(os.path.join(os.getcwd(), input_folder_path))
    logger.info('Files in the input folder: {}'.format(files_list))

    files_path = glob.glob(
        os.path.join(
            os.getcwd(),
            input_folder_path,
            '*.csv'))
    df = pd.concat([pd.read_csv(f) for f in files_path], ignore_index=True)
    logger.info('Merged dataframe: {}'.format(df))

    with open(ingested_files_path, 'w') as f:
        for file in files_list:
            f.write('{}\n'.format(file))

    process_df = df.drop_duplicates()
    process_df.to_csv(final_data_path, index=False)
    return process_df


if __name__ == '__main__':
    merge_multiple_dataframe(
        input_folder_path,
        ingested_files_path,
        final_data_path)
