from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "players_with_features.csv"
)

DATABASE_FILE = (
    PROJECT_ROOT
    / "sql"
    / "football_analytics.db"
)


def create_database(
    input_file: Path,
    database_file: Path,
) -> None:
    """Load the processed player dataset into a SQLite database."""

    if not input_file.exists():
        raise FileNotFoundError(f"Dataset not found: {input_file}")

    # Load the processed CSV into a Pandas DataFrame.
    df = pd.read_csv(input_file)

    if df.empty:
        raise ValueError("The dataset contains no rows.")

    # Open a connection to the SQLite database.
    # SQLite creates the database file automatically if it does not exist.
    with sqlite3.connect(database_file) as connection:

        # Store the DataFrame as a SQL table named "players".
        df.to_sql(
            "players",
            connection,
            if_exists="replace",
            index=False,
        )

    print("SQLite database created successfully.")
    print(f"Database: {database_file}")
    print(f"Rows imported: {len(df)}")
    print(f"Columns imported: {len(df.columns)}")


if __name__ == "__main__":
    try:
        create_database(INPUT_FILE, DATABASE_FILE)

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
        sqlite3.Error,
    ) as error:
        print(f"Error: {error}")