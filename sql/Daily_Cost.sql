-- File: Daily_Cost.sql

-- This SQL groups the hourly power readings into days to get daily cost totals.
-- The number of hourly recordings in a particular day may be less than 24 due
-- to various issues.  The user can see if a full day's readings have been
-- stored or not.  The cost calculated is based on PSE's cost for the first
-- 600 kWh and will not be the final and actual cost which depends on the
-- total kWh used during the montly billing period.

use pse;

select
   UDate as Date
   ,ELT(dayofweek(UDate),'Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') as DoW
   ,round(sum(kWh)/count(kWh),3) as kWh_Hr_avg
   ,count(kWh) as hours
   ,sum(kWh) as kWh_total
   ,round(((sum(kWh)/count(kWh))*(count(kWh))*0.115433),2) as kWh_cost
from
   pse.usage_e
group by
   UDate
order by
   UDate
;