import argparse

try:
    from extract_transform_load.extract import from_csv
    from extract_transform_load.load import run as load_run
    from extract_transform_load.transform import run as transform_run
    from logs.logger import get_logger
except ModuleNotFoundError:
    import sys
    sys.path.append(".")
    from extract_transform_load.extract import from_csv
    from extract_transform_load.load import run as load_run
    from extract_transform_load.transform import run as transform_run
    from logs.logger import get_logger

logger = get_logger(__name__)


def pipeline(args):
    df, metadata = from_csv(file_path=args.file_path)
    df = transform_run(df=df)
    df_train, df_test = load_run(
        df=df,
        output_train_file_path=args.output_train_file_path,
        output_test_file_path=args.output_test_file_path
    )
    return df, metadata, df_train, df_test


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline")
    parser.add_argument(
        "--file-path",
        type=str,
        help="File path to CSV",
        default="data/healthcare-dataset-stroke-data.csv"
    )
    parser.add_argument(
        "--output-train-file-path",
        type=str,
        help="File path to save CSV",
        default="data/df_train_preprocess.csv"
    )
    parser.add_argument(
        "--output-test-file-path",
        type=str,
        help="File path to save CSV",
        default="data/df_test_preprocess.csv"
    )
    args = parser.parse_args()
    pipeline(args=args)
    logger.info("Pipeline completed")
