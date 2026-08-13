-- 01_basic_queries.sql
-- Foundational SQL queries for exploring the player dataset.


-- 1. View a sample of player records.
SELECT *
FROM players
LIMIT 10;


-- 2. Select only useful columns instead of the entire table.
SELECT Player, Squad, Comp, Gls, Ast
FROM players
LIMIT 10;


-- 3. Find players who scored at least 20 goals.
SELECT Player, Squad, Comp, Gls
FROM players
WHERE Gls >= 20
ORDER BY Gls DESC;


-- 4. Find players with at least 15 goals, ranked highest to lowest.
SELECT Player, Squad, Comp, Gls, Ast
FROM players
WHERE Gls >= 15
ORDER BY Gls DESC;


-- 5. Show the 10 youngest players in the dataset.
SELECT Player, Squad, Age, Min
FROM players
ORDER BY Age ASC
LIMIT 10;


-- 6. Show the 10 youngest players with at least 900 minutes played.
SELECT Player, Squad, Comp, Age, Min
FROM players
WHERE Min >= 900
ORDER BY Age ASC
LIMIT 10;


-- 7. Find players with at least 10 assists.
SELECT Player, Squad, Comp, Ast
FROM players
WHERE Ast >= 10
ORDER BY Ast DESC;


-- 8. Find players with at least 10 goals and 10 assists.
SELECT Player, Squad, Comp, Gls, Ast
FROM players
WHERE Gls >= 10
  AND Ast >= 10
ORDER BY Gls DESC, Ast DESC;


-- 9. Find Premier League players with at least 900 minutes.
SELECT Player, Squad, Age, Min, Gls, Ast
FROM players
WHERE Comp = 'eng Premier League'
  AND Min >= 900
ORDER BY Gls DESC;


-- 10. Find high-volume shooters with at least 900 minutes.
SELECT Player, Squad, Comp, Min, Sh, Shots_per_90
FROM players
WHERE Min >= 900
ORDER BY Shots_per_90 DESC
LIMIT 10;


-- 11. Find the top goal contributors per 90 with a meaningful sample size.
SELECT
    Player,
    Squad,
    Comp,
    Min,
    Gls,
    Ast,
    Goal_Contributions_per_90
FROM players
WHERE Min >= 900
ORDER BY Goal_Contributions_per_90 DESC
LIMIT 10;


-- 12. Find the top progressive players per 90 with at least 900 minutes.
SELECT
    Player,
    Squad,
    Comp,
    Pos,
    Min,
    Progressive_Actions_per_90
FROM players
WHERE Min >= 900
ORDER BY Progressive_Actions_per_90 DESC
LIMIT 10;


-- 13. Find the biggest xG overperformers.
SELECT
    Player,
    Squad,
    Comp,
    Min,
    Gls,
    xG,
    "G-xG"
FROM players
WHERE Min >= 900
ORDER BY "G-xG" DESC
LIMIT 10;


-- 14. Find the biggest xG underperformers.
SELECT
    Player,
    Squad,
    Comp,
    Min,
    Gls,
    xG,
    "G-xG"
FROM players
WHERE Min >= 900
ORDER BY "G-xG" ASC
LIMIT 10;