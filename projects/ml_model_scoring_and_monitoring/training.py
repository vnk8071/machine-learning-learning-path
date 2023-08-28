import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import logging
from config import get_config


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
CFG = get_config(production=False)
final_data_path = CFG["final_data_path"]
output_model_path = CFG["output_model_path"]
output_model_train_path = os.path.join(
    os.getcwd(),
    output_model_path,
    'trainedmodel.pkl'
)


def train_model(final_data_path, output_model_train_path):
    """
    Train the model and save it in the output folder

    Args:
        final_data_path (str): path to the dataset csv file
        output_model_train_path (str): path to the output model folder
    """
    logger.info('Training model')
    lr_model = LogisticRegression(
        C=1.0,
        class_weight=None,
        dual=False,
        fit_intercept=True,
        intercept_scaling=1,
        l1_ratio=None,
        max_iter=100,
        multi_class='auto',
        n_jobs=None,
        penalty='l2',
        random_state=0,
        solver='liblinear',
        tol=0.0001,
        verbose=0,
        warm_start=False)

    final_df = pd.read_csv(final_data_path)
    final_df = final_df.drop(["corporation"], axis=1)
    X = final_df.iloc[:, :-1]
    y = final_df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0)
    lr_model.fit(X_train, y_train)

    with open(output_model_train_path, 'wb') as f:
        pickle.dump(lr_model, f)
    logger.info('Model saved at {}'.format(output_model_train_path))


if __name__ == '__main__':
    train_model(final_data_path, output_model_train_path)
