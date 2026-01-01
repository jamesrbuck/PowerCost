use powercost;

-- File: Daily_Cost24HR.sql

-- This SQL groups the hourly power readings into days to get daily cost totals.
-- Only complete (i.e., 24 hourly recording) are retrieved.
-- The cost calculated is based on PSE's cost for the first
-- 600 kWh and will not be the final and actual cost which depends on the
-- total kWh used during the montly billing period.
-- Only list days with 24 hourly values (Common Table Expression = CTE)

WITH DailyUsage AS (
    SELECT
        UDate AS Date,
        ELT(DAYOFWEEK(UDate), 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') AS DoW,
        ROUND(SUM(kWh) / COUNT(kWh), 3) AS kWh_Hr_avg,
        COUNT(kWh) AS hours,
        SUM(kWh) AS kWh_day_total,
        ROUND(0.0937212 * SUM(kWh), 2) AS KwH_24hr_Cost
    FROM
        usage_e ue
    GROUP BY
        ue.UDate
)
SELECT
    Date, DoW, kWh_Hr_avg, kWh_day_total, KwH_24hr_Cost
FROM
    DailyUsage
WHERE
    hours = 24
ORDER BY
    Date;
