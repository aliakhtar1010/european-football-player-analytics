# European Football Player Performance Analytics

An end-to-end data analytics project exploring player performance across Europe's Top 5 football leagues using Python, SQL, and Power BI.

The project transforms raw 2024/25 player statistics into analysis-ready data, creates performance metrics for meaningful player comparisons, and explores trends across players and leagues.

## What the Project Does

- Cleans and validates raw football player data
- Focuses on outfield players using relevant performance metrics
- Engineers per-90 statistics to improve comparisons between players
- Analyzes attacking, creative, progressive, and defensive performance
- Creates player leaderboards and league-level summaries
- Uses a 900-minute threshold for per-90 rankings to reduce small-sample bias
- Uses SQL for further analysis
- Visualizes the final results in Power BI

## Python Pipeline

The data pipeline consists of four stages:

1. **Load** — Import and validate the raw dataset
2. **Clean** — Select relevant columns, remove duplicates, handle missing data, and separate goalkeepers
3. **Engineer** — Create 13 new per-90 performance metrics
4. **Analyze** — Generate player leaderboards and league-level summaries

## Project Structure

```text
├── data/
│   ├── processed/
│   └── analysis/
├── scripts/
│   ├── 01_load_data.py
│   ├── 02_clean_data.py
│   ├── 03_feature_engineering.py
│   └── 04_exploratory_analysis.py
├── sql/
├── powerbi/
├── requirements.txt
└── README.md
```

## Technologies

- Python
- Pandas
- SQL
- Power BI
- Git & GitHub

## Dataset

Player-level statistics from Europe's Top 5 leagues for the 2024/25 season:

- Premier League
- La Liga
- Serie A
- Bundesliga
- Ligue 1

The raw dataset is not tracked in the repository. Processed datasets and generated analysis outputs are included.