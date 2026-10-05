import pandas as pd
from weather_forecasting.utils.logger import logger


class BaseFeature:

    @staticmethod
    def _validate_column(
        df: pd.DataFrame,
        column: str,
    ) -> None:
        if column not in df.columns:
            raise KeyError(
                f"Column '{column}' not found in DataFrame."
            )

    @staticmethod
    def _validate_positive_values(
        values: list[int],
        name: str,
    ) -> None:
        if any(value <= 0 for value in values):
            raise ValueError(
                f"{name} must contain only positive integers."
            )

    @staticmethod
    def add_change_features(
            df: pd.DataFrame,
            column: str,
            changes: list[int],
    ) -> pd.DataFrame:
        """
        Add difference features for a column over specified periods.

        The change is calculated as the current value minus the value
        from the specified number of periods ago.
        """
        BaseFeature._validate_column(df, column)
        BaseFeature._validate_positive_values(changes, "Changes")

        df = df.copy()
        
        for change in sorted(set(changes)):
            feature_name = f"{column}_change_{change}"

            if feature_name in df.columns:
                logger.debug(f"{feature_name} already exists. Skipping.")
                continue

            logger.debug(f"Creating feature {feature_name}")

            df[feature_name] = df[column].diff(change)

        return df

    @staticmethod
    def add_lag_features(
        df: pd.DataFrame,
        column: str,
        lags: list[int],
    ) -> pd.DataFrame:
        """
        Add lag features for a column.

        Features that already exist are skipped, making this function
        safe to call multiple times from different pipelines.
        """
        BaseFeature._validate_column(df, column)
        BaseFeature._validate_positive_values(lags, "Lags")

        df = df.copy()

        for lag in sorted(set(lags)):
            feature_name = f"{column}_lag_{lag}"

            # Skip if the feature already exists
            if feature_name in df.columns:
                logger.debug(f"{feature_name} already exists. Skipping.")
                continue
            logger.debug(f"Creating feature {feature_name}")
            df[feature_name] = df[column].shift(lag)
        return df

    @staticmethod
    def add_rolling_features(
        df : pd.DataFrame,
        column: str,
        windows: list[int],
        statistic: str,
    )-> pd.DataFrame:
        """
        Add rolling statistics for a column.
        Parameters
        ----------
        column : str
            Column to calculate rolling statistics on.
        windows: list[int]
            Rolling window sizes
        statistic: str
            One of:
                - "mean"
                - "std"
        """
        BaseFeature._validate_column(df, column)
        BaseFeature._validate_positive_values(
            windows,
            "Rolling windows",
        )

        df = df.copy()

        if statistic not in {"mean", "std"}:
            raise ValueError(
                f"Unsupported statistics '{statistic}'."
                "Expected 'mean' or 'std'."
            )

        
        for window in sorted(set(windows)):
            feature_name = f"{column}_rolling_{statistic}_{window}"

            if feature_name in df.columns:
                logger.debug(f"{feature_name} already exists. Skipping.")
                continue

            logger.debug(f"Creating {feature_name}")

            rolling = df[column].rolling(
                window=window,
                min_periods=window,
            )

            if statistic == "mean":
                df[feature_name] = rolling.mean()

            elif statistic == "std":
                df[feature_name] = rolling.std()

        return df

    @staticmethod
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
        BaseFeature._validate_column(df, column)

        if horizon <= 0:
            raise ValueError("Horizon must be a positive integer.")
        
        df = df.copy()

        if target_name is None:
            target_name = f"target_{column}_{horizon}"


        df[target_name] = df[column].shift(-horizon)
        logger.info(f"{target_name} target feature created with horizon {horizon}.")

        return df
