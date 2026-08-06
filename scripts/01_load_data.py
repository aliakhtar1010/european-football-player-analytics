from pathlib import Path

import pandas as pd


# Build the path to the raw dataset relative to the project root.
# Using Path makes the code portable across different operating systems.
DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "players_data_light-2024_2025.csv"
)


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw football player dataset from a CSV file."""

    # Fail early if the dataset cannot be found.
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    # Read the CSV into a Pandas DataFrame stored in memory.
    dataframe = pd.read_csv(file_path)

    # Ensure the dataset contains records before continuing.
    if dataframe.empty:
        raise ValueError("The dataset was loaded, but it contains no rows.")

    # Return the validated DataFrame so other scripts can reuse it.
    return dataframe


# Run this block only when this file is executed directly.
# It allows us to test the data-loading process independently.
if __name__ == "__main__":
    try:
        # Load the raw dataset.
        df = load_data(DATA_FILE)

        # Display a quick summary to verify everything loaded correctly.
        print("Dataset loaded successfully.")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print("\nFirst five rows:")
        print(df.head())

    # Handle expected loading errors gracefully.
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}")