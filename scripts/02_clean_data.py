from pathlib import Path

import pandas as pd


# Resolve the project root from this script's location so the paths
# continue to work even if the script is run from a different directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw source data. This file should remain unchanged so the cleaning
# pipeline can always be rerun from the original dataset.
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "players_data_light-2024_2025.csv"
)

# Processed output used later by SQL, Excel, and Power BI.
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clean_players.csv"
)


# Keep only the fields relevant to outfield-player performance analysis.
# Goalkeeper-specific and unnecessary columns are intentionally excluded
# to keep the dataset focused and easier to analyze.
SELECTED_COLUMNS = [
    "Player",
    "Nation",
    "Pos",
    "Squad",
    "Comp",
    "Age",
    "MP",
    "Starts",
    "Min",
    "90s",
    "Gls",
    "Ast",
    "G+A",
    "xG",
    "npxG",
    "xAG",
    "Sh",
    "SoT",
    "SoT%",
    "G/Sh",
    "G/SoT",
    "G-xG",
    "Cmp%",
    "KP",
    "PrgP",
    "PrgC",
    "Tkl",
    "TklW",
    "Int",
    "Clr",
    "Touches",
    "Carries",
    "Succ%",
    "Recov",
]


def clean_data(input_file: Path) -> pd.DataFrame:
    """Load and clean the European football player dataset."""

    # Fail early with a clear message if the source dataset is missing.
    if not input_file.exists():
        raise FileNotFoundError(f"Dataset not found: {input_file}")

    # Load the raw CSV into memory as a Pandas DataFrame.
    df = pd.read_csv(input_file)

    # Prevent the rest of the pipeline from running on an empty dataset.
    if df.empty:
        raise ValueError("The dataset contains no rows.")

    print(f"Original dataset shape: {df.shape}")

    # Validate the schema before cleaning. If the source dataset changes
    # and a required field disappears, stop here instead of failing later.
    missing_columns = [
        column for column in SELECTED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing from the dataset: {missing_columns}"
        )

    # Create an independent working DataFrame containing only the fields
    # needed for the dashboard, while preserving the original DataFrame.
    clean_df = df[SELECTED_COLUMNS].copy()

    # Remove exact duplicate records so the same player record is not
    # counted more than once in later analysis.
    duplicate_count = clean_df.duplicated().sum()
    clean_df = clean_df.drop_duplicates()

    # Goalkeepers require different performance metrics, so this version
    # of the dashboard focuses only on outfield players.
    goalkeeper_mask = clean_df["Pos"].str.contains("GK", na=False)
    goalkeeper_count = goalkeeper_mask.sum()
    clean_df = clean_df[~goalkeeper_mask].copy()

    # Player, Nation, and Age are treated as core descriptive fields.
    # Rows missing these values are removed, while valid missing values
    # in calculated statistics such as G/Sh are preserved.
    rows_before_core_cleaning = len(clean_df)
    clean_df = clean_df.dropna(subset=["Player", "Nation", "Age"])
    removed_core_rows = rows_before_core_cleaning - len(clean_df)

    # Age represents whole years, so convert it from decimal storage
    # to an integer now that missing Age values have been removed.
    clean_df["Age"] = clean_df["Age"].astype(int)

    # Filtering removes rows but keeps their old index values.
    # Resetting the index creates a clean sequential index for the output.
    clean_df = clean_df.reset_index(drop=True)

    # Report the effect of the cleaning process for validation and debugging.
    print(f"Exact duplicate rows removed: {duplicate_count}")
    print(f"Goalkeeper records removed: {goalkeeper_count}")
    print(f"Rows removed for missing core information: {removed_core_rows}")
    print(f"Clean dataset shape: {clean_df.shape}")

    # Show only columns that still contain missing values.
    # Remaining NaNs are reviewed rather than automatically deleted,
    # because some are valid when a statistic cannot be calculated.
    print("\nRemaining missing values:")
    remaining_missing = (
        clean_df.isna()
        .sum()
        .loc[lambda values: values > 0]
        .sort_values(ascending=False)
    )
    print(remaining_missing)

    # Return the cleaned DataFrame so it can be saved or reused elsewhere.
    return clean_df


def save_data(dataframe: pd.DataFrame, output_file: Path) -> None:
    """Save the cleaned dataset as a CSV file."""

    # Create the processed-data folder automatically if it does not exist.
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save only the actual dataset columns; the Pandas index is not
    # meaningful football data and should not become an extra CSV column.
    dataframe.to_csv(output_file, index=False)

    print("\nClean dataset saved successfully.")
    print(f"Location: {output_file}")


# Allow this file to run as a standalone cleaning pipeline while still
# keeping its functions reusable by other Python modules.
if __name__ == "__main__":
    try:
        # Clean the raw dataset, then persist the processed result.
        cleaned_players = clean_data(INPUT_FILE)
        save_data(cleaned_players, OUTPUT_FILE)

    # Handle expected file, data, parsing, and write-permission problems
    # with readable messages instead of unhandled tracebacks.
    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
        PermissionError,
    ) as error:
        print(f"Error: {error}")