-- 02_aggregate_queries.sql
-- Aggregate analysis across leagues and squads.


-- 1. Count the number of players in each league.
SELECT
    Comp,
    COUNT(*) AS Player_Count
FROM players
GROUP BY Comp
ORDER BY Player_Count DESC;


-- 2. Calculate total goals scored by players in each league.
SELECT
    Comp,
    SUM(Gls) AS Total_Goals
FROM players
GROUP BY Comp
ORDER BY Total_Goals DESC;


-- 3. Calculate the average player age in each league.
SELECT
    Comp,
    ROUND(AVG(Age), 2) AS Average_Age
FROM players
GROUP BY Comp
ORDER BY Average_Age ASC;


-- 4. Find the highest-scoring squads.
SELECT
    Squad,
    Comp,
    SUM(Gls) AS Total_Goals
FROM players
GROUP BY Squad, Comp
ORDER BY Total_Goals DESC
LIMIT 10;


-- 5. Create a statistical summary of each league.
SELECT
    Comp,
    COUNT(*) AS Player_Count,
    ROUND(AVG(Age), 2) AS Average_Age,
    SUM(Gls) AS Total_Goals,
    SUM(Ast) AS Total_Assists,
    MAX(Gls) AS Highest_Player_Goal_Total,
    MIN(Age) AS Youngest_Player_Age
FROM players
GROUP BY Comp
ORDER BY Total_Goals DESC;


-- 6. Find squads whose players combined for at least 60 goals.
SELECT
    Squad,
    Comp,
    SUM(Gls) AS Total_Goals
FROM players
GROUP BY Squad, Comp
HAVING SUM(Gls) >= 60
ORDER BY Total_Goals DESC;


-- 7. Calculate average goals among players with at least 900 minutes.
SELECT
    Comp,
    ROUND(AVG(Gls), 2) AS Average_Goals
FROM players
WHERE Min >= 900
GROUP BY Comp
ORDER BY Average_Goals DESC;


-- 8. Find squads with at least 20 player records.
SELECT
    Squad,
    COUNT(*) AS Player_Count
FROM players
GROUP BY Squad
HAVING COUNT(*) >= 20
ORDER BY Player_Count DESC;


-- 9. Compare average goals per 90 across leagues
-- using only players with at least 900 minutes.
SELECT
    Comp,
    ROUND(AVG(Goals_per_90), 2) AS Average_Goals_per_90
FROM players
WHERE Min >= 900
GROUP BY Comp
ORDER BY Average_Goals_per_90 DESC;


-- 10. Compare average xG per 90 across leagues
-- using only players with at least 900 minutes.
SELECT
    Comp,
    ROUND(AVG(xG_per_90), 2) AS Average_xG_per_90
FROM players
WHERE Min >= 900
GROUP BY Comp
ORDER BY Average_xG_per_90 DESC;


-- 11. Compare average progressive actions per 90 across leagues.
SELECT
    Comp,
    ROUND(
        AVG(Progressive_Actions_per_90),
        2
    ) AS Average_Progressive_Actions_per_90
FROM players
WHERE Min >= 900
GROUP BY Comp
ORDER BY Average_Progressive_Actions_per_90 DESC;


-- 12. Find squads with strong attacking output among players
-- who have meaningful playing time.
SELECT
    Squad,
    Comp,
    COUNT(*) AS Eligible_Player_Count,
    SUM(Gls) AS Total_Goals,
    ROUND(AVG(Goal_Contributions_per_90), 2)
        AS Average_Goal_Contributions_per_90
FROM players
WHERE Min >= 900
GROUP BY Squad, Comp
HAVING COUNT(*) >= 5
ORDER BY Average_Goal_Contributions_per_90 DESC
LIMIT 10;