"""
Project: Predict Customer Churn
Author: vnk8071
Date: 2023-08-10
"""

from sklearn.metrics import classification_report, roc_curve, RocCurveDisplay
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
import os
import logging
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


os.environ['QT_QPA_PLATFORM'] = 'offscreen'
logging.basicConfig(
    filename='./logs/churn_library.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
EDA_PATH = "./images/eda"
RESULTS_PATH = "./images/results"
MODEL_PATH = "./models"
CAT_COLUMNS = [
    'Gender',
    'Education_Level',
    'Marital_Status',
    'Income_Category',
    'Card_Category'
]

QUANT_COLUMNS = [
    'Customer_Age',
    'Dependent_count',
    'Months_on_book',
    'Total_Relationship_Count',
    'Months_Inactive_12_mon',
    'Contacts_Count_12_mon',
    'Credit_Limit',
    'Total_Revolving_Bal',
    'Avg_Open_To_Buy',
    'Total_Amt_Chng_Q4_Q1',
    'Total_Trans_Amt',
    'Total_Trans_Ct',
    'Total_Ct_Chng_Q4_Q1',
    'Avg_Utilization_Ratio'
]


def import_data(data_path):
    """
    returns dataframe for the csv found at pth

    input:
        pth: a path to the csv

    output:
        df: pandas dataframe

    raises:
        FileNotFoundError: if the file is not found
    """
    try:
        df = pd.read_csv(data_path)
        logging.info("SUCCESS: Import_data")
        return df
    except FileNotFoundError as err:
        logging.error("File not found")
        raise err


def perform_eda(df):
    """
    perform eda on df and save figures to images folder
    input:
        df: pandas dataframe

    output:
        None
    """
    logging.info(df.shape)
    logging.info(df.isnull().sum())
    logging.info(df.describe())

    df['Churn'] = df['Attrition_Flag'].apply(
        lambda val: 0 if val == "Existing Customer" else 1)
    plt.figure(figsize=(20, 10))
    df['Churn'].hist()
    plt.savefig(os.path.join(EDA_PATH, "churn_histogram.png"))

    plt.figure(figsize=(20, 10))
    df['Customer_Age'].hist()
    plt.savefig(os.path.join(EDA_PATH, "customer_age_histogram.png"))

    plt.figure(figsize=(20, 10))
    df.Marital_Status.value_counts('normalize').plot(kind='bar')
    plt.savefig(os.path.join(EDA_PATH, "marital_status_counts.png"))

    plt.figure(figsize=(20, 10))
    sns.histplot(df['Total_Trans_Ct'], stat='density', kde=True)
    plt.savefig(os.path.join(EDA_PATH, "total_transaction_histogram.png"))

    plt.figure(figsize=(20, 10))
    sns.heatmap(
        df.corr(
            numeric_only=True),
        annot=False,
        cmap='Dark2_r',
        linewidths=2)
    plt.savefig(os.path.join(EDA_PATH, "heatmap.png"))


def encoder_helper(df, category_lst, response):
    """
    helper function to turn each categorical column into a new column with
    propotion of churn for each category - associated with cell 15 from the notebook

    input:
        df: pandas dataframe
        category_lst: list of columns that contain categorical features
        response: string of response name [optional argument that could be used for naming \
            variables or index y column]

    output:
        df: pandas dataframe with new columns for
    """
    for category in category_lst:
        cat_lst = []
        cat_groups = df.groupby(category).mean(numeric_only=True)[response]
        for val in df[category]:
            cat_lst.append(cat_groups.loc[val])
        df[category + "_" + response] = cat_lst
        logging.info("SUCCESS: encoder %s", category)
    return df


def perform_feature_engineering(df):
    """
    input:
        df: pandas dataframe

    output:
        X_train: X training data
        X_test: X testing data
        y_train: y training data
        y_test: y testing data
    """
    y = df['Churn']
    X = pd.DataFrame()
    keep_cols = [
        'Customer_Age', 'Dependent_count', 'Months_on_book',
        'Total_Relationship_Count', 'Months_Inactive_12_mon',
        'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
        'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt',
        'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio',
        'Gender_Churn', 'Education_Level_Churn', 'Marital_Status_Churn',
        'Income_Category_Churn', 'Card_Category_Churn'
    ]
    X[keep_cols] = df[keep_cols]

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    return (X_train, X_test, y_train, y_test)


def classification_report_image(
    y_train,
    y_test,
    y_train_preds_lr,
    y_train_preds_rf,
    y_test_preds_lr,
    y_test_preds_rf
):
    """
    produces classification report for training and testing results and stores report as image
    in images folder
    input:
        y_train: training response values
        y_test:  test response values
        y_train_preds_lr: training predictions from logistic regression
        y_train_preds_rf: training predictions from random forest
        y_test_preds_lr: test predictions from logistic regression
        y_test_preds_rf: test predictions from random forest

    output:
        None
    """
    plt.close()
    plt.clf()
    plt.rc('figure', figsize=(5, 5))
    plt.text(0.01, 1.25, str('Random Forest Train'), {
        'fontsize': 10}, fontproperties='monospace')
    plt.text(0.01, 0.05, str(classification_report(y_test, y_test_preds_rf)), {
        'fontsize': 10}, fontproperties='monospace')
    plt.text(0.01, 0.6, str('Random Forest Test'), {
        'fontsize': 10}, fontproperties='monospace')
    plt.text(
        0.01, 0.7, str(
            classification_report(
                y_train, y_train_preds_rf)), {
            'fontsize': 10}, fontproperties='monospace')
    plt.axis('off')
    plt.savefig(os.path.join(RESULTS_PATH, "rf_classification_report.png"))
    logging.info("SUCCESS: classification_report_image: random forest")

    # Save the logistic regression classification report image.
    plt.close()
    plt.clf()
    plt.rc('figure', figsize=(5, 5))
    plt.text(0.01, 1.25, str('Logistic Regression Train'), {
        'fontsize': 10}, fontproperties='monospace')
    plt.text(
        0.01, 0.05, str(
            classification_report(
                y_train, y_train_preds_lr)), {
            'fontsize': 10}, fontproperties='monospace')
    plt.text(0.01, 0.6, str('Logistic Regression Test'), {
        'fontsize': 10}, fontproperties='monospace')
    plt.text(0.01, 0.7, str(classification_report(y_test, y_test_preds_lr)), {
        'fontsize': 10}, fontproperties='monospace')
    plt.axis('off')
    plt.savefig(os.path.join(RESULTS_PATH, "lr_classification_report.png"))
    logging.info(
        msg="SUCCESS: classification_report_image: logistic regression")


def feature_importance_plot(model, X_data, output_pth):
    """
    creates and stores the feature importances in pth
    input:
        model: model object containing feature_importances_
        X_data: pandas dataframe of X values
        output_pth: path to store the figure

    output:
        None
    """
    # Calculate feature importances
    importances = model.best_estimator_.feature_importances_
    # Sort feature importances in descending order
    indices = np.argsort(importances)[::-1]

    # Rearrange feature names so they match the sorted feature importances
    names = [X_data.columns[i] for i in indices]

    # Create plot
    plt.figure(figsize=(20, 5))

    # Create plot title
    plt.title("Feature Importance")
    plt.ylabel('Importance')

    # Add bars
    plt.bar(range(X_data.shape[1]), importances[indices])

    # Add feature names as x-axis labels
    plt.xticks(range(X_data.shape[1]), names, rotation=90)
    plt.savefig(output_pth)
    logging.info(
        "%s : %s",
        "SUCCESS: feature_importance_plot and saved feature report to ",
        output_pth)


def train_models(X_train, X_test, y_train, y_test):
    """
    train, store model results: images + scores, and store models
    input:
        X_train: X training data
        X_test: X testing data
        y_train: y training data
        y_test: y testing data
    output:
        None
    """
    rfc = RandomForestClassifier(random_state=42)
    # Use a different solver if the default 'lbfgs' fails to converge
    # Reference:
    # https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
    lrc = LogisticRegression(solver='lbfgs', max_iter=3000)

    param_grid = {
        'n_estimators': [200, 500],
        'max_features': ['sqrt'],
        'max_depth': [4, 5, 100],
        'criterion': ['gini', 'entropy']
    }

    cv_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
    cv_rfc.fit(X_train, y_train)

    lrc.fit(X_train, y_train)

    y_train_preds_rf = cv_rfc.best_estimator_.predict(X_train)
    y_test_preds_rf = cv_rfc.best_estimator_.predict(X_test)

    y_train_preds_lr = lrc.predict(X_train)
    y_test_preds_lr = lrc.predict(X_test)

    # scores
    print('random forest results')
    print('test results')
    print(classification_report(y_test, y_test_preds_rf))
    print('train results')
    print(classification_report(y_train, y_train_preds_rf))

    print('logistic regression results')
    print('test results')
    print(classification_report(y_test, y_test_preds_lr))
    print('train results')
    print(classification_report(y_train, y_train_preds_lr))

    # Save the models
    joblib.dump(
        cv_rfc.best_estimator_,
        os.path.join(
            MODEL_PATH,
            "rfc_model.pkl"))
    joblib.dump(lrc, os.path.join(MODEL_PATH, "logistic_model.pkl"))

    # Save the classification report images
    classification_report_image(
        y_train=y_train,
        y_test=y_test,
        y_train_preds_lr=y_train_preds_rf,
        y_train_preds_rf=y_train_preds_lr,
        y_test_preds_lr=y_test_preds_lr,
        y_test_preds_rf=y_test_preds_rf
    )

    # Save the feature importance plot
    feature_importance_plot(
        model=cv_rfc,
        X_data=X_train,
        output_pth=os.path.join(RESULTS_PATH, "cv_feature_importance.png")
    )

    lrc_plot = RocCurveDisplay.from_estimator(
        lrc, X_test, y_test)
    plt.savefig(os.path.join(RESULTS_PATH, "lr_roc_curve.png"))
    logging.info("SUCCESS: model_train: save lr roc curve")

    # Combine both lrc ans rfc roc plots
    plt.figure(figsize=(15, 8))
    ax = plt.gca()
    _ = RocCurveDisplay.from_estimator(
        cv_rfc.best_estimator_, X_test, y_test, ax=ax, alpha=0.8)
    lrc_plot.plot(ax=ax, alpha=0.8)
    plt.savefig(os.path.join(RESULTS_PATH, "lr_rf_roc_curves.png"))
    logging.info("SUCCESS: model_train: save lr and rf roc curves")


if __name__ == '__main__':
    df = import_data("./data/bank_data.csv")
    logging.info(df)
    perform_eda(df)
    logging.info("SUCCESS: perform_eda")
    logging.info("START: encoder_helper")
    df = encoder_helper(df, CAT_COLUMNS, "Churn")
    logging.info("SUCCESS: encoder_helper")
    logging.info("START: perform_feature_engineering")
    X_train, X_test, y_train, y_test = perform_feature_engineering(df)
    logging.info("SUCCESS: perform_feature_engineering")
    logging.info("START: train_models")
    train_models(X_train, X_test, y_train, y_test)
    logging.info("SUCCESS: train_models")
