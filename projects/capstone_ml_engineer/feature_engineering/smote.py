import pandas as pd
from imblearn.over_sampling import SMOTE

from logs.logger import get_logger

logger = get_logger(__name__)


def make_balance_data(
    df: pd.DataFrame,
    target: str = "stroke",
    k_neighbors: int = 50,
    random_state: int = 8071,
    output_file_path: str = "data/df_train_smote.csv",
):
    """Make balanced data

    Args:
        df (pd.DataFrame): DataFrame to balance
        target (str): Target class
        k_neighbors (int, optional): Number of k_neighbors. Defaults to 17.
        random_state (int, optional): Random state. Defaults to 8071.
        output_file_path (str, optional): File path to save balanced DataFrame.
            Defaults to "data/df_train_smote.csv".

    Returns:
        pd.DataFrame: Balanced DataFrame
    """
    logger.info(f"Balancing data with target class {target}")
    smote = SMOTE(random_state=random_state, k_neighbors=k_neighbors)
    features = df.drop(labels=[target], axis=1)
    target = df[target].copy()
    features_smote, target_smote = smote.fit_resample(features, target)
    df_smote = pd.concat([features_smote, target_smote], axis=1)
    df_smote.to_csv(output_file_path, index=False)
    return df_smote
