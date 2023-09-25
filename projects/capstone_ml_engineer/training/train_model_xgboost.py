import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    roc_auc_score,
    confusion_matrix
)
from sklearn.model_selection import KFold
from xgboost import XGBClassifier

import argparse
import pickle
import os

try:
    from logs.logger import get_logger
except ModuleNotFoundError:
    import sys
    sys.path.append(".")
    from logs.logger import get_logger

logger = get_logger(__name__)


def pipeline(args):
    features_train, target_train, features_test, target_test = load_data(
        args=args)
    model = net(args=args)
    kfold_cv(model, features_train, target_train,
             random_state=args.random_state)
    model.fit(features_train, target_train)
    target_pred = model.predict(features_test)
    evaluate_performance(
        y_ground_truth=target_test,
        y_pred=target_pred
    )
    cm = confusion_matrix(target_test, target_pred)
    logger.info(f"Confusion matrix: \n{cm}")
    df_model_coef = pd.DataFrame(
        data={
            "feature_name": features_train.columns,
            "coef": model.feature_importances_,
        }
    ).sort_values(by="coef", ascending=False)

    df_model_coef["coef_abs"] = np.abs(df_model_coef["coef"])
    logger.info(model.get_params())

    logger.info("Feature importances:")
    logger.info(df_model_coef)
    model_output_file_path = os.path.join(args.model_output_dir, "model.pkl")
    pickle.dump(model, open(model_output_file_path, "wb"))


def load_data(args, target_class: str = "stroke"):
    df_train = pd.read_csv(args.training_input, engine="python")
    df_test = pd.read_csv(args.test_input, engine="python")

    features_train = df_train.drop(labels=[target_class], axis=1)
    target_train = df_train[target_class].copy()

    features_test = df_test.drop(labels=[target_class], axis=1)
    target_test = df_test[target_class].copy()
    return features_train, target_train, features_test, target_test


def net(args):
    model = XGBClassifier(
        random_state=args.random_state,
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
    )
    return model


def evaluate_performance(
    y_ground_truth: pd.Series,
    y_pred: pd.Series,
    evaluation_type: str = "test",
    verbose: bool = True
):
    """
    Evaluate classification model performance.

    Args:
        y_ground_truth: (pd.Series) actual class
        y_true: (pd.Series) predicted class
        evaluation_type: (str) dataset used to generate y_pred, e.g., train, validation, or test

    Returns:
        tuple of three elements (accuracy, F1 score, and AUC)
    """
    accuracy = accuracy_score(y_ground_truth, y_pred)
    f_score = f1_score(y_ground_truth, y_pred)
    auc = roc_auc_score(y_ground_truth, y_pred)

    if verbose:
        logger.info(f"{evaluation_type} set - Accuracy : {accuracy:.3%}")
        logger.info(f"{evaluation_type} set - F1-score : {f_score:.3%}")
        logger.info(f"{evaluation_type} set - AUC: {auc:.3f}")
        logger.info("Classification_report \n" +
                    classification_report(y_ground_truth, y_pred))
    return accuracy, f_score, auc


def kfold_cv(clf, features_train, target_train, k: int = 5, random_state: int = 8071):
    """
    Run k-fold cross-validation by splitting the training set into train and validation set.

    Args:
        clf: (sklearn classifier) classifier object
        features_train: (pd.DataFrame) training set
        target_train: (pd.Series) training set
        k: (int) number of folds
        random_state: (int) random state
    """
    kfold = KFold(random_state=random_state, shuffle=True, n_splits=k)

    kfold_cv_accuracy = np.zeros(shape=k)
    kfold_cv_f1 = np.zeros(shape=k)
    kfold_cv_auc = np.zeros(shape=k)

    fold = 0
    logger.info("Running k-fold cross-validation")
    for train_index, val_index in kfold.split(features_train):
        features_train_kfold = features_train.iloc[train_index]
        target_train_kfold = target_train.iloc[train_index]
        features_valid_kfold = features_train.iloc[val_index]
        target_valid_kfold = target_train.iloc[val_index]

        clf.fit(features_train_kfold, target_train_kfold)
        y_pred = clf.predict(features_valid_kfold)
        accuracy, f_score, auc = evaluate_performance(
            y_ground_truth=target_valid_kfold,
            y_pred=y_pred,
            evaluation_type="validation",
            verbose=False
        )
        logger.info(
            f"Fold {fold+1}: Accuracy={accuracy:.3%} | F1-score={f_score:.3%} | AUC={auc:.3f}"
        )

        kfold_cv_accuracy[fold] = accuracy
        kfold_cv_f1[fold] = f_score
        kfold_cv_auc[fold] = auc

        fold += 1

    logger.info(
        f"CV Accuracy: Mean {np.mean(kfold_cv_accuracy):.3%} & STD {np.std(kfold_cv_accuracy):.3%}")
    logger.info(
        f"CV F1-score: Mean {np.mean(kfold_cv_f1):.3%} & STD  {np.std(kfold_cv_f1):.3%}")
    logger.info(
        f"CV AUC: Mean {np.mean(kfold_cv_auc):.3f} & STD  {np.std(kfold_cv_auc):.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n-estimators",
        type=int,
        default=100,
        metavar="N",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=5,
        metavar="N",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.1,
    )
    parser.add_argument(
        "--model-output-dir",
        type=str,
        help="Define where the best model object from hp tuning is stored",
    )
    parser.add_argument(
        "--training-input", type=str
    )
    parser.add_argument(
        "--test-input", type=str
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=8071,
        metavar="N",
        help="random state (default: 8071)",
    )
    args = parser.parse_args()
    pipeline(args=args)
