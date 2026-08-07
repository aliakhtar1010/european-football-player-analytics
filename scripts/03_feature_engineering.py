from pathlib import Path

import pandas as pd


# Resolve the project root from this script's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Script 3 starts from the cleaned dataset produced by Script 2.
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clean_players.csv"
)

# Save the feature-engineered dataset separately so the cleaned
# dataset from Script 2 remains unchanged.
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "players_with_features.csv"
)


# Columns required to calculate the new performance metrics.
REQUIRED_COLUMNS = [
    "Min",
    "Gls",
    "Ast",
    "G+A",
    "xG",
    "xAG",
    "Sh",
    "SoT",
    "KP",
    "PrgP",
    "PrgC",
    "Tkl",
    "Int",
    "Clr",
    "Recov",
]


def engineer_features(input_file: Path) -> pd.DataFrame:
    """Create new per-90 player performance metrics for analysis."""

    # Stop early if the cleaned dataset cannot be found.
    if not input_file.exists():
        raise FileNotFoundError(f"Dataset not found: {input_file}")

    # Load the cleaned dataset created by Script 2.
    df = pd.read_csv(input_file)

    # Prevent feature engineering from running on an empty dataset.
    if df.empty:
        raise ValueError("The dataset contains no rows.")

    # Make sure every column needed for feature engineering exists.
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing from the dataset: {missing_columns}"
        )

    # Per-90 statistics require playing time.
    # Replace zero minutes with a missing value to prevent division by zero.
    minutes = df["Min"].replace(0, pd.NA)

    # -----------------------------
    # ATTACKING FEATURES
    # -----------------------------

    # Scoring rate per full 90 minutes.
    df["Goals_per_90"] = (df["Gls"] / minutes) * 90

    # Assist rate per full 90 minutes.
    df["Assists_per_90"] = (df["Ast"] / minutes) * 90

    # Combined scoring and assisting output per 90.
    df["Goal_Contributions_per_90"] = (
        df["G+A"] / minutes
    ) * 90

    # Expected scoring output normalized for playing time.
    df["xG_per_90"] = (df["xG"] / minutes) * 90

    # Expected assisted-goal creation normalized for playing time.
    df["xAG_per_90"] = (df["xAG"] / minutes) * 90   

    # Shooting volume per 90 minutes.
    df["Shots_per_90"] = (df["Sh"] / minutes) * 90

    # Shots on target per 90 minutes.
    df["Shots_on_Target_per_90"] = (
        df["SoT"] / minutes
    ) * 90

    # -----------------------------
    # CREATIVITY & PROGRESSION
    # -----------------------------

    # Key passes per 90 minutes.
    df["Key_Passes_per_90"] = (
        df["KP"] / minutes
    ) * 90

    # Combine progressive passes and progressive carries to measure
    # overall ball progression per full match.
    df["Progressive_Actions_per_90"] = (
        (df["PrgP"] + df["PrgC"]) / minutes
    ) * 90

    # -----------------------------
    # DEFENSIVE FEATURES
    # -----------------------------

    # Tackles per 90 minutes.
    df["Tackles_per_90"] = (
        df["Tkl"] / minutes
    ) * 90

    # Interceptions per 90 minutes.
    df["Interceptions_per_90"] = (
        df["Int"] / minutes
    ) * 90

    # Ball recoveries per 90 minutes.
    df["Recoveries_per_90"] = (
        df["Recov"] / minutes
    ) * 90

    # Clearances per 90 minutes.
    df["Clearances_per_90"] = (
        df["Clr"] / minutes
    ) * 90

    print(f"Dataset shape after feature engineering: {df.shape}")
    print("\nNew features created:")

    engineered_columns = [
        "Goals_per_90",
        "Assists_per_90",
        "Goal_Contributions_per_90",
        "xG_per_90",
        "xAG_per_90",
        "Shots_per_90",
        "Shots_on_Target_per_90",
        "Key_Passes_per_90",
        "Progressive_Actions_per_90",
        "Tackles_per_90",
        "Interceptions_per_90",
        "Recoveries_per_90",
        "Clearances_per_90",
    ]

    for column in engineered_columns:
        print(f"- {column}")

    return df


def save_data(dataframe: pd.DataFrame, output_file: Path) -> None:
    """Save the feature-engineered dataset as a CSV file."""

    # Create the output directory if necessary.
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Do not export Pandas' internal row index as a dataset column.
    dataframe.to_csv(output_file, index=False)

    print("\nFeature-engineered dataset saved successfully.")
    print(f"Location: {output_file}")


if __name__ == "__main__":
    try:
        players_with_features = engineer_features(INPUT_FILE)
        save_data(players_with_features, OUTPUT_FILE)

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
        PermissionError,
    ) as error:
        print(f"Error: {error}")