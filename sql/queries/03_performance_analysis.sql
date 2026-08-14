-- 03_performance_analysis.sql
-- Player-level performance analysis across Europe's Top 5 leagues.
--
-- Per-90 rankings use a minimum threshold of 900 minutes
-- to reduce misleading results caused by small sample sizes.


-- ============================================================
-- 1. TOP GOAL SCORERS
-- ============================================================

-- Find the 10 players with the most total goals.
-- Total goals are used here instead of goals per 90 because
-- this query measures overall scoring production.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    Gls
FROM players
ORDER BY Gls DESC
LIMIT 10;


-- ============================================================
-- 2. TOP GOAL CONTRIBUTORS PER 90
-- ============================================================

-- Rank players by combined goals and assists per 90 minutes.
-- Only players with at least 900 minutes are included.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    Gls,
    Ast,
    ROUND(Goal_Contributions_per_90, 2)
        AS Goal_Contributions_per_90
FROM players
WHERE Min >= 900
ORDER BY Goal_Contributions_per_90 DESC
LIMIT 10;


-- ============================================================
-- 3. TOP SCORERS PER 90
-- ============================================================

-- Find the players with the highest scoring rate while
-- requiring a meaningful amount of playing time.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    Gls,
    ROUND(Goals_per_90, 2) AS Goals_per_90
FROM players
WHERE Min >= 900
ORDER BY Goals_per_90 DESC
LIMIT 10;


-- ============================================================
-- 4. xG OVERPERFORMERS
-- ============================================================

-- Find players who scored the most goals above their expected
-- goals (xG). Positive G-xG means the player scored more goals
-- than expected based on the chances they received.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    Gls,
    ROUND(xG, 2) AS xG,
    ROUND("G-xG", 2) AS Goals_Above_xG
FROM players
WHERE Min >= 900
ORDER BY "G-xG" DESC
LIMIT 10;


-- ============================================================
-- 5. xG UNDERPERFORMERS
-- ============================================================

-- Find players who scored the furthest below their expected
-- goals. A negative G-xG indicates fewer goals than expected.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    Gls,
    ROUND(xG, 2) AS xG,
    ROUND("G-xG", 2) AS Goals_Below_xG
FROM players
WHERE Min >= 900
ORDER BY "G-xG" ASC
LIMIT 10;


-- ============================================================
-- 6. MOST CREATIVE PLAYERS
-- ============================================================

-- Use key passes and expected assisted goals per 90 to identify
-- players consistently creating opportunities for teammates.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    ROUND(Key_Passes_per_90, 2) AS Key_Passes_per_90,
    ROUND(xAG_per_90, 2) AS xAG_per_90,
    Ast
FROM players
WHERE Min >= 900
ORDER BY Key_Passes_per_90 DESC
LIMIT 10;


-- ============================================================
-- 7. TOP PROGRESSIVE PLAYERS
-- ============================================================

-- Progressive_Actions_per_90 combines progressive passes and
-- progressive carries to measure how frequently a player moves
-- the ball forward through passing or carrying.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    PrgP,
    PrgC,
    ROUND(Progressive_Actions_per_90, 2)
        AS Progressive_Actions_per_90
FROM players
WHERE Min >= 900
ORDER BY Progressive_Actions_per_90 DESC
LIMIT 10;


-- ============================================================
-- 8. DEFENSIVE ACTIVITY LEADERS
-- ============================================================

-- Compare players using tackles, interceptions, and recoveries
-- per 90 rather than relying on one defensive statistic.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    ROUND(Tackles_per_90, 2) AS Tackles_per_90,
    ROUND(Interceptions_per_90, 2) AS Interceptions_per_90,
    ROUND(Recoveries_per_90, 2) AS Recoveries_per_90
FROM players
WHERE Min >= 900
ORDER BY Tackles_per_90 DESC
LIMIT 10;


-- ============================================================
-- 9. YOUNG ATTACKING PLAYERS
-- ============================================================

-- Find productive young players aged 21 or younger who have
-- also played enough minutes to provide a meaningful sample.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Age,
    Min,
    Gls,
    Ast,
    ROUND(Goal_Contributions_per_90, 2)
        AS Goal_Contributions_per_90
FROM players
WHERE Age <= 21
  AND Min >= 900
ORDER BY Goal_Contributions_per_90 DESC
LIMIT 10;


-- ============================================================
-- 10. YOUNG PROGRESSIVE PLAYERS
-- ============================================================

-- Identify young players who frequently progress the ball
-- through progressive passes and carries.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Age,
    Min,
    ROUND(Progressive_Actions_per_90, 2)
        AS Progressive_Actions_per_90
FROM players
WHERE Age <= 21
  AND Min >= 900
ORDER BY Progressive_Actions_per_90 DESC
LIMIT 10;


-- ============================================================
-- 11. HIGH-VOLUME SHOOTERS
-- ============================================================

-- Find players taking the most shots per 90 and include their
-- goals and xG rates to provide context for that shot volume.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    ROUND(Shots_per_90, 2) AS Shots_per_90,
    ROUND(Shots_on_Target_per_90, 2)
        AS Shots_on_Target_per_90,
    ROUND(Goals_per_90, 2) AS Goals_per_90,
    ROUND(xG_per_90, 2) AS xG_per_90
FROM players
WHERE Min >= 900
ORDER BY Shots_per_90 DESC
LIMIT 10;


-- ============================================================
-- 12. ATTACKING + PROGRESSION PROFILE
-- ============================================================

-- Identify players who combine goal involvement with frequent
-- ball progression. This provides a broader view than ranking
-- players using only goals or assists.
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
    ROUND(Key_Passes_per_90, 2)
        AS Key_Passes_per_90
FROM players
WHERE Min >= 900
  AND Goal_Contributions_per_90 >= 0.50
ORDER BY Progressive_Actions_per_90 DESC
LIMIT 10;