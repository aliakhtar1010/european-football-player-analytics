from pathlib import Path

import pandas as pd


# Resolve the project root from this script's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Script 4 analyzes the feature-engineered dataset produced by Script 3.
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "players_with_features.csv"
)

# Save exploratory analysis results separately from the processed dataset.
OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "analysis"
)

# Per-90 leaderboards can be misleading for players with very few minutes.
# Requiring at least 900 minutes gives us a more meaningful sample size.
MIN_MINUTES = 900


# Columns this script depends on for its analysis.
REQUIRED_COLUMNS = [
    "Player",
    "Squad",
    "Comp",
    "Pos",
    "Age",
    "Min",
    "Gls",
    "Ast",
    "xG",
    "G-xG",
    "Goals_per_90",
    "Assists_per_90",
    "Goal_Contributions_per_90",
    "xG_per_90",
    "Progressive_Actions_per_90",
    "Tackles_per_90",
    "Interceptions_per_90",
]


def load_analysis_data(input_file: Path) -> pd.DataFrame:
    """Load and validate the feature-engineered player dataset."""

    # Fail early if Script 3 has not produced the expected dataset.
    if not input_file.exists():
        raise FileNotFoundError(f"Dataset not found: {input_file}")

    # Load the analytics-ready CSV into a Pandas DataFrame.
    df = pd.read_csv(input_file)

    # Prevent analysis from continuing if the dataset contains no records.
    if df.empty:
        raise ValueError("The dataset contains no rows.")

    # Confirm that every field required by this analysis still exists.
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing from the dataset: {missing_columns}"
        )

    return df


def create_analysis_tables(
    df: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Create exploratory football performance analysis tables."""

    # Per-90 rankings should use players with a meaningful amount of
    # playing time so tiny samples do not dominate the leaderboards.
    eligible_players = df[df["Min"] >= MIN_MINUTES].copy()

    # ---------------------------------------------------------
    # 1. TOP GOAL SCORERS
    # ---------------------------------------------------------

    # Raw goal totals are useful for showing overall scoring output.
    top_scorers = (
        df[
            [
                "Player",
                "Squad",
                "Comp",
                "Pos",
                "Min",
                "Gls",
                "Ast",
                "xG",
                "G-xG",
            ]
        ]
        .sort_values("Gls", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    # ---------------------------------------------------------
    # 2. TOP GOAL CONTRIBUTORS PER 90
    # ---------------------------------------------------------

    # Normalize goals + assists by playing time to compare attacking
    # productivity more fairly between regular players.
    top_goal_contributors = (
        eligible_players[
            [
                "Player",
                "Squad",
                "Comp",
                "Pos",
                "Min",
                "Gls",
                "Ast",
                "Goal_Contributions_per_90",
            ]
        ]
        .sort_values(
            "Goal_Contributions_per_90",
            ascending=False,
        )
        .head(10)
        .reset_index(drop=True)
    )

    # ---------------------------------------------------------
    # 3. TOP BALL PROGRESSORS PER 90
    # ---------------------------------------------------------

    # Progressive Actions per 90 combines progressive passing and
    # carrying to identify players who frequently move the ball forward.
    top_progressors = (
        eligible_players[
            [
                "Player",
                "Squad",
                "Comp",
                "Pos",
                "Min",
                "Progressive_Actions_per_90",
            ]
        ]
        .sort_values(
            "Progressive_Actions_per_90",
            ascending=False,
        )
        .head(10)
        .reset_index(drop=True)
    )

    # ---------------------------------------------------------
    # 4. LEAGUE-LEVEL SUMMARY
    # ---------------------------------------------------------

    # Group players by competition to compare overall patterns across
    # Europe's top five leagues.
    league_summary = (
        df.groupby("Comp")
        .agg(
            Players=("Player", "count"),
            Average_Age=("Age", "mean"),
            Total_Goals=("Gls", "sum"),
            Average_Goals_per_90=("Goals_per_90", "mean"),
            Average_xG_per_90=("xG_per_90", "mean"),
            Average_Progressive_Actions_per_90=(
                "Progressive_Actions_per_90",
                "mean",
            ),
        )
        .reset_index()
    )

    # Round summary averages so the output is easier to read.
    league_summary[
        [
            "Average_Age",
            "Average_Goals_per_90",
            "Average_xG_per_90",
            "Average_Progressive_Actions_per_90",
        ]
    ] = league_summary[
        [
            "Average_Age",
            "Average_Goals_per_90",
            "Average_xG_per_90",
            "Average_Progressive_Actions_per_90",
        ]
    ].round(2)

    # Store every analysis table in one dictionary so the function
    # can return all results together.
    analysis_tables = {
        "top_scorers": top_scorers,
        "top_goal_contributors_per_90": top_goal_contributors,
        "top_progressors_per_90": top_progressors,
        "league_summary": league_summary,
    }

    return analysis_tables


def save_analysis_tables(
    tables: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:
    """Save each exploratory analysis table as a separate CSV file."""

    # Create the analysis directory automatically if it does not exist.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save each DataFrame using its dictionary name as the filename.
    for table_name, dataframe in tables.items():
        output_file = output_dir / f"{table_name}.csv"

        # Pandas' internal index is not part of the football data.
        dataframe.to_csv(output_file, index=False)

        print(f"Saved: {output_file}")


if __name__ == "__main__":
    try:
        # Load the analytics-ready dataset.
        players = load_analysis_data(INPUT_FILE)

        # Create the exploratory analysis tables.
        analysis_results = create_analysis_tables(players)

        print(
            f"Players in dataset: {len(players)}"
        )

        print(
            f"Players with at least {MIN_MINUTES} minutes: "
            f"{len(players[players['Min'] >= MIN_MINUTES])}"
        )

        print("\nTop 10 Goal Scorers:")
        print(analysis_results["top_scorers"].to_string(index=False))

        print("\nTop 10 Goal Contributors per 90:")
        print(
            analysis_results[
                "top_goal_contributors_per_90"
            ].to_string(index=False)
        )

        print("\nLeague Summary:")
        print(
            analysis_results[
                "league_summary"
            ].to_string(index=False)
        )

        # Persist the analysis results so they can be inspected in
        # Excel and later compared with equivalent SQL queries.
        save_analysis_tables(
            analysis_results,
            OUTPUT_DIR,
        )

        print("\nExploratory analysis completed successfully.")

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
        PermissionError,
    ) as error:
        print(f"Error: {error}")