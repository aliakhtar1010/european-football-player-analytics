from pathlib import Path

import pandas as pd


# Build reliable file paths based on this script's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "players_data_light-2024_2025.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clean_players.csv"
)


# Columns needed for the outfield-player dashboard
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

    if not input_file.exists():
        raise FileNotFoundError(f"Dataset not found: {input_file}")

    # Load the original Kaggle dataset
    df = pd.read_csv(input_file)

    if df.empty:
        raise ValueError("The dataset contains no rows.")

    print(f"Original dataset shape: {df.shape}")

    # Confirm that every required column exists
    missing_columns = [
        column for column in SELECTED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing from the dataset: {missing_columns}"
        )

    # Keep only the columns required for the dashboard
    clean_df = df[SELECTED_COLUMNS].copy()

    # Remove exact duplicate rows, if any
    duplicate_count = clean_df.duplicated().sum()
    clean_df = clean_df.drop_duplicates()

    # Keep outfield players only; goalkeepers require separate metrics
    goalkeeper_mask = clean_df["Pos"].str.contains("GK", na=False)
    goalkeeper_count = goalkeeper_mask.sum()
    clean_df = clean_df[~goalkeeper_mask].copy()

    # Remove records missing core player information
    rows_before_core_cleaning = len(clean_df)
    clean_df = clean_df.dropna(subset=["Player", "Nation", "Age"])
    removed_core_rows = rows_before_core_cleaning - len(clean_df)

    # Age has no missing values now, so store it as a whole number
    clean_df["Age"] = clean_df["Age"].astype(int)

    # Reset the row index after removing records
    clean_df = clean_df.reset_index(drop=True)

    print(f"Exact duplicate rows removed: {duplicate_count}")
    print(f"Goalkeeper records removed: {goalkeeper_count}")
    print(f"Rows removed for missing core information: {removed_core_rows}")
    print(f"Clean dataset shape: {clean_df.shape}")

    print("\nRemaining missing values:")
    remaining_missing = (
        clean_df.isna()
        .sum()
        .loc[lambda values: values > 0]
        .sort_values(ascending=False)
    )
    print(remaining_missing)

    return clean_df


def save_data(dataframe: pd.DataFrame, output_file: Path) -> None:
    """Save the cleaned dataset as a CSV file."""

    output_file.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_file, index=False)

    print("\nClean dataset saved successfully.")
    print(f"Location: {output_file}")


if __name__ == "__main__":
    try:
        cleaned_players = clean_data(INPUT_FILE)
        save_data(cleaned_players, OUTPUT_FILE)

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
        PermissionError,
    ) as error:
        print(f"Error: {error}")