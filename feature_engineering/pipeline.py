import argparse
import pandas as pd

try:
    from feature_engineering.standardlize import run as standardize_run
    from feature_engineering.smote import make_balance_data
    from feature_engineering.feature_selection import feature_select
    from logs.logger import get_logger
except ModuleNotFoundError:
    import sys
    sys.path.append(".")
    from feature_engineering.standardlize import run as standardize_run
    from feature_engineering.smote import make_balance_data
    from feature_engineering.feature_selection import feature_select
    from logs.logger import get_logger


logger = get_logger(__name__)


def pipeline(args):
    df_train = pd.read_csv(args.input_train_file_path)
    df_test = pd.read_csv(args.input_test_file_path)
    df_train = standardize_run(
        df=df_train, output_file_path=args.output_train_file_path)
    df_test = standardize_run(
        df=df_test, output_file_path=args.output_test_file_path)
    df_train = make_balance_data(
        df=df_train, output_file_path=args.output_train_smote_file_path)
    df_train, df_test = feature_select(
        input_train_file_path=args.output_train_smote_file_path,
        input_test_file_path=args.output_test_file_path,
        output_train_file_path=args.output_train_selection_file_path,
        output_test_file_path=args.output_test_selection_file_path
    )
    return df_train, df_test


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline")
    parser.add_argument(
        "--input-train-file-path",
        type=str,
        default="data/df_train_preprocess.csv"
    )
    parser.add_argument(
        "--input-test-file-path",
        type=str,
        default="data/df_test_preprocess.csv"
    )
    parser.add_argument(
        "--output-train-file-path",
        type=str,
        default="data/df_train_feature_engineering.csv"
    )
    parser.add_argument(
        "--output-test-file-path",
        type=str,
        default="data/df_test_feature_engineering.csv"
    )
    parser.add_argument(
        "--output-train-smote-file-path",
        type=str,
        default="data/df_train_feature_engineering_smote.csv"
    )
    parser.add_argument(
        "--output-train-selection-file-path",
        type=str,
        default="data/df_train_feature_engineering_smote_selection.csv"
    )
    parser.add_argument(
        "--output-test-selection-file-path",
        type=str,
        default="data/df_test_feature_engineering_selection.csv"
    )
    args = parser.parse_args()
    pipeline(args=args)
    logger.info("Pipeline completed")
