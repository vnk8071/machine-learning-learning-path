import os
import json


def create_folder(folder_path):
    """
    Create a folder if it does not exist

    Args:
        folder_path (str): path to the folder
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_config(production=False):
    """
    Get the configuration from config.json

    Args:
        production (bool): True if the code is running in production mode

    Returns:
        config (dict): dictionary of configuration
    """
    with open('config.json', 'r') as f:
        config = json.load(f)
    if production:
        config['input_folder_path'] = "sourcedata"
        config['output_model_path'] = "models"

    create_folder(config["output_model_path"])
    create_folder(config["prod_deployment_path"])

    # Save result paths
    config["test_data_csv_path"] = os.path.join(
        os.getcwd(),
        config["test_data_path"],
        'testdata.csv'
    )
    config["final_data_path"] = os.path.join(
        os.getcwd(),
        config["output_folder_path"],
        'finaldata.csv'
    )
    config["api_returns_path"] = os.path.join(
        os.getcwd(),
        config["output_model_path"],
        'apireturns2.txt' if production else 'apireturns.txt'
    )
    config["cfm_path"] = os.path.join(
        os.getcwd(),
        config["output_model_path"],
        'confusionmatrix2.png' if production else 'confusionmatrix.png'
    )
    return config


if __name__ == '__main__':
    config = get_config()
    print(config)
