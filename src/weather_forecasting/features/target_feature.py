import pandas as pd
from weather_forecasting.utils.logger import logger


def create_target(
    df: pd.DataFrame,
    column: str,
    horizon: int,
    target_name: str | None = None,
) -> pd.DataFrame:
    """
    Create future prediction target.
    Example:
        horizon = 1 -> next hour
        horizon = 6 -> next 6 hours
        horizon = 24 -> next day
    """

    df = df.copy()

    if target_name is None:
        target_name = f"target_{column}_{horizon}"

    df[target_name] = df[column].shift(-horizon)
    logger.info(f"{target_name} target feature created")

    return df
