import pandas as pd
from logs.logger import get_logger

logger = get_logger(__name__)


def from_csv(file_path: str):
    logger.info(f"Reading file from {file_path}")
    df = pd.read_csv(file_path)

    logger.info("Extracting metadata")
    metadata = {
        "file_path": file_path,
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "category_columns": df.select_dtypes(include="category").columns.tolist(),
        "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
    }
    logger.info("Metadata: %s", metadata)
    return df, metadata
