from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import json
import os

from diagnostics import (
    dataframe_summary,
    execution_time,
    missing_data,
    outdated_packages_list
)
from scoring import score_model
from config import get_config

app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

CFG = get_config(production=True)

input_folder_path = CFG['input_folder_path']
output_folder_pathut = CFG['output_folder_path']
prod_deployment_path = CFG['prod_deployment_path']
test_data_csv_path = CFG['test_data_csv_path']
lr_model_path = os.path.join(
    os.getcwd(),
    prod_deployment_path,
    'trainedmodel.pkl')
prediction_model = pickle.load(open(lr_model_path, 'rb'))


@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predict():
    filename = request.args.get('inputdata')
    test_file_path = os.path.join(os.getcwd(), filename)
    if os.path.isfile(test_file_path) is False:
        return f"{test_file_path} doesn't exist"

    test_df = pd.read_csv(test_file_path)
    test_df = test_df.drop(['corporation'], axis=1)
    X = test_df.iloc[:, :-1]

    pred = prediction_model.predict(X)
    return str(pred), 200


@app.route("/scoring", methods=['GET', 'OPTIONS'])
def scoring():
    test_data_csv = pd.read_csv(test_data_csv_path)
    f1score = score_model(prod_deployment_path, test_data_csv)
    return jsonify(f1score), 200


@app.route("/summarystats", methods=['GET', 'OPTIONS'])
def stats():
    statistics = dataframe_summary(test_data_csv_path)
    return jsonify(statistics), 200


@app.route("/diagnostics", methods=['GET', 'OPTIONS'])
def diagnostics():
    timing = execution_time(input_folder_path, prod_deployment_path)
    missing = missing_data(test_data_csv_path)
    dependencies = outdated_packages_list()
    res = {
        'timing': timing,
        'missing_data': missing,
        'dependency_check': dependencies,
    }
    return jsonify(res), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
