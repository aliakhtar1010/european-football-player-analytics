from pathlib import Path

import pandas as pd


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "players_data_light-2024_2025.csv"
)


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw football player dataset from a CSV file."""

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    dataframe = pd.read_csv(file_path)

    if dataframe.empty:
        raise ValueError("The dataset was loaded, but it contains no rows.")

    return dataframe


if __name__ == "__main__":
    try:
        df = load_data(DATA_FILE)

        print("Dataset loaded successfully.")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print("\nFirst five rows:")
        print(df.head())

    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}")