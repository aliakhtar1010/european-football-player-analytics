-- 04_advanced_queries.sql
-- Advanced SQL analysis using player categories, CTEs,
-- and window functions across Europe's Top 5 leagues.
--
-- Per-90 analysis generally uses a minimum threshold of
-- 900 minutes to reduce small-sample bias.


-- ============================================================
-- 1. CATEGORIZE PLAYERS BY AGE
-- ============================================================

-- CASE allows us to create categories based on conditions.
-- Players are grouped into broad age profiles for analysis.
SELECT
    Player,
    Squad,
    Comp,
    Age,
    CASE
        WHEN Age <= 21 THEN 'Young'
        WHEN Age <= 27 THEN 'Prime'
        ELSE 'Experienced'
    END AS Age_Group
FROM players
ORDER BY Age ASC;


-- ============================================================
-- 2. ATTACKING OUTPUT CATEGORIES
-- ============================================================

-- Categorize players according to their goal contribution rate.
-- Only players with at least 900 minutes are considered.
SELECT
    Player,
    Squad,
    Comp,
    Min,
    ROUND(Goal_Contributions_per_90, 2)
        AS Goal_Contributions_per_90,
    CASE
        WHEN Goal_Contributions_per_90 >= 0.75 THEN 'Elite Output'
        WHEN Goal_Contributions_per_90 >= 0.50 THEN 'High Output'
        WHEN Goal_Contributions_per_90 >= 0.25 THEN 'Moderate Output'
        ELSE 'Low Output'
    END AS Attacking_Output
FROM players
WHERE Min >= 900
ORDER BY Goal_Contributions_per_90 DESC;


-- ============================================================
-- 3. CTE: FILTER ELIGIBLE PLAYERS
-- ============================================================

-- A Common Table Expression (CTE) creates a temporary named
-- result that can be referenced by the main query.
--
-- Here, eligible_players contains only players who have played
-- at least 900 minutes.
WITH eligible_players AS (
    SELECT *
    FROM players
    WHERE Min >= 900
)

SELECT
    Player,
    Squad,
    Comp,
    Min,
    ROUND(Goals_per_90, 2) AS Goals_per_90
FROM eligible_players
ORDER BY Goals_per_90 DESC
LIMIT 10;


-- ============================================================
-- 4. RANK PLAYERS ACROSS THE ENTIRE DATASET
-- ============================================================

-- RANK() is a window function.
-- It assigns each eligible player a ranking based on their
-- goal contributions per 90 without collapsing the player rows.
WITH eligible_players AS (
    SELECT *
    FROM players
    WHERE Min >= 900
)

SELECT
    Player,
    Squad,
    Comp,
    ROUND(Goal_Contributions_per_90, 2)
        AS Goal_Contributions_per_90,
    RANK() OVER (
        ORDER BY Goal_Contributions_per_90 DESC
    ) AS Overall_Rank
FROM eligible_players
ORDER BY Overall_Rank;


-- ============================================================
-- 5. RANK PLAYERS WITHIN EACH LEAGUE
-- ============================================================

-- PARTITION BY creates a separate ranking for each league.
-- Instead of one overall ranking, every league starts at rank 1.
WITH ranked_players AS (
    SELECT
        Player,
        Squad,
        Comp,
        Min,
        Goal_Contributions_per_90,
        RANK() OVER (
            PARTITION BY Comp
            ORDER BY Goal_Contributions_per_90 DESC
        ) AS League_Rank
    FROM players
    WHERE Min >= 900
)

SELECT
    Player,
    Squad,
    Comp,
    Min,
    ROUND(Goal_Contributions_per_90, 2)
        AS Goal_Contributions_per_90,
    League_Rank
FROM ranked_players
WHERE League_Rank <= 5
ORDER BY Comp, League_Rank;


-- ============================================================
-- 6. TOP PROGRESSIVE PLAYERS WITHIN EACH LEAGUE
-- ============================================================

-- Rank players by progressive actions per 90 separately
-- within each competition.
WITH ranked_progressors AS (
    SELECT
        Player,
        Squad,
        Comp,
        Pos,
        Min,
        Progressive_Actions_per_90,
        RANK() OVER (
            PARTITION BY Comp
            ORDER BY Progressive_Actions_per_90 DESC
        ) AS League_Rank
    FROM players
    WHERE Min >= 900
)

SELECT
    Player,
    Squad,
    Comp,
    Pos,
    ROUND(Progressive_Actions_per_90, 2)
        AS Progressive_Actions_per_90,
    League_Rank
FROM ranked_progressors
WHERE League_Rank <= 5
ORDER BY Comp, League_Rank;


-- ============================================================
-- 7. RANK YOUNG PLAYERS WITHIN EACH LEAGUE
-- ============================================================

-- Compare young players against other young players in their
-- own league using goal contributions per 90.
WITH young_players AS (
    SELECT
        Player,
        Squad,
        Comp,
        Age,
        Min,
        Goal_Contributions_per_90
    FROM players
    WHERE Age <= 21
      AND Min >= 900
),

ranked_young_players AS (
    SELECT
        Player,
        Squad,
        Comp,
        Age,
        Goal_Contributions_per_90,
        RANK() OVER (
            PARTITION BY Comp
            ORDER BY Goal_Contributions_per_90 DESC
        ) AS League_Rank
    FROM young_players
)

SELECT
    Player,
    Squad,
    Comp,
    Age,
    ROUND(Goal_Contributions_per_90, 2)
        AS Goal_Contributions_per_90,
    League_Rank
FROM ranked_young_players
WHERE League_Rank <= 5
ORDER BY Comp, League_Rank;


-- ============================================================
-- 8. POSITIONAL PROGRESSION RANKINGS
-- ============================================================

-- Rank players against others with the same listed position.
-- This provides more context than comparing every position
-- directly against one another.
WITH positional_rankings AS (
    SELECT
        Player,
        Squad,
        Comp,
        Pos,
        Min,
        Progressive_Actions_per_90,
        RANK() OVER (
            PARTITION BY Pos
            ORDER BY Progressive_Actions_per_90 DESC
        ) AS Position_Rank
    FROM players
    WHERE Min >= 900
)

SELECT
    Player,
    Squad,
    Comp,
    Pos,
    ROUND(Progressive_Actions_per_90, 2)
        AS Progressive_Actions_per_90,
    Position_Rank
FROM positional_rankings
WHERE Position_Rank <= 10
ORDER BY Pos, Position_Rank;


-- ============================================================
-- 9. LEAGUE ATTACKING RANKINGS
-- ============================================================

-- First calculate league-level attacking statistics using a CTE,
-- then rank the leagues by average goal contributions per 90.
WITH league_attack AS (
    SELECT
        Comp,
        COUNT(*) AS Eligible_Players,
        ROUND(AVG(Goals_per_90), 3)
            AS Average_Goals_per_90,
        ROUND(AVG(Goal_Contributions_per_90), 3)
            AS Average_Goal_Contributions_per_90
    FROM players
    WHERE Min >= 900
    GROUP BY Comp
)

SELECT
    Comp,
    Eligible_Players,
    Average_Goals_per_90,
    Average_Goal_Contributions_per_90,
    RANK() OVER (
        ORDER BY Average_Goal_Contributions_per_90 DESC
    ) AS Attacking_Rank
FROM league_attack
ORDER BY Attacking_Rank;


-- ============================================================
-- 10. MULTI-METRIC PLAYER PROFILE
-- ============================================================

-- Categorize players using both attacking output and progression.
-- This demonstrates how CASE can combine multiple conditions.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    ROUND(Goal_Contributions_per_90, 2)
        AS Goal_Contributions_per_90,
    ROUND(Progressive_Actions_per_90, 2)
        AS Progressive_Actions_per_90,
    CASE
        WHEN Goal_Contributions_per_90 >= 0.50
             AND Progressive_Actions_per_90 >= 8
            THEN 'Attacking + Progression'
        WHEN Goal_Contributions_per_90 >= 0.50
            THEN 'Attacking'
        WHEN Progressive_Actions_per_90 >= 8
            THEN 'Progressor'
        ELSE 'Other'
    END AS Player_Profile
FROM players
WHERE Min >= 900
ORDER BY Goal_Contributions_per_90 DESC;