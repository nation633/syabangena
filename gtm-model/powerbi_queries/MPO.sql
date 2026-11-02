/* Power BI native query: Get Data > SQL Server > <SQL_SERVER>, database <REPORT_DB>, DirectQuery,
   Advanced options > SQL statement. Pure SELECT (read-only rights); no CTE / ORDER BY / USE.
   Cross-database 3-part names need read access to <LANDING_DB> / <STAGING_DB> on the same instance. */
/* MPO - activity fact, DirectQuery. One row per approved activity (MPO.Id).
   Executed = ExecutedAt IS NOT NULL (MPO.Executed flag not used; see DQ_ExecutedChecks.sql). */
SELECT
  MPO.Id                                                AS ActivityId,
  CONVERT(int, CONVERT(char(8), MPO.[Date], 112))       AS DateKey,           -- planned date
  CONVERT(int, CONVERT(char(8), MPO.ExecutedAt, 112))   AS ExecutedDateKey,   -- NULL = not executed
  ISNULL(LTRIM(RTRIM(MPO.BusinessUnit)),'Unknown')      AS BusinessUnit,
  ISNULL(LTRIM(RTRIM(MPO.Province)),'Unknown')          AS Region,
  ISNULL(LTRIM(RTRIM(MPO.MicroMarket)),'Unknown')       AS MicroMarket,
  ISNULL(LTRIM(RTRIM(MPO.Branch)),'Unknown')            AS Branch,
  MPO.Banker                                            AS StaffNumber,
  ISNULL(LTRIM(RTRIM(MPO.BankerName)),'Unknown')        AS BankerName,
  ISNULL(NULLIF(LTRIM(RTRIM(CASE WHEN MPO.Store = 'Other' THEN MPO.Other ELSE MPO.Store END)),''),'Unknown') AS Company,
  ISNULL(SOO.Name,'Unknown')                            AS SourceOfOpportunity,
  CAST(CASE WHEN MPO.ExecutedAt IS NOT NULL THEN 1 ELSE 0 END AS int) AS IsExecuted,
  CAST(CASE WHEN t.TotalSaleCount > 0 THEN 1 ELSE 0 END AS int)       AS HasSale,
  ISNULL(MPO.MiGoals,0)        AS MiGoals,
  ISNULL(MPO.MiGoalsPlus,0)    AS MiGoalsPlus,
  ISNULL(MPO.MiGoalsPremium,0) AS MiGoalsPremium,
  ISNULL(MPO.PlIntake,0)       AS PlIntake,
  ISNULL(MPO.OdApp,0)          AS OdApp,
  ISNULL(MPO.CcApp,0)          AS CcApp,
  ISNULL(MPO.Investments,0)    AS Investments,
  ISNULL(MPO.FPFixed,0)        AS FPFixed,
  ISNULL(MPO.FPBYO,0)          AS FPBYO,
  ISNULL(MPO.FPMCL,0)          AS FPMCL,
  t.TotalSaleCount
FROM <LANDING_DB>.<LANDING_SCHEMA>.MonthlyPlannerOther MPO
LEFT JOIN <LANDING_DB>.<LANDING_SCHEMA>.SourceOfOpportunity SOO ON SOO.Id = MPO.SizeOfOpportunity
CROSS APPLY (SELECT ISNULL(MPO.MiGoals,0)+ISNULL(MPO.MiGoalsPlus,0)+ISNULL(MPO.MiGoalsPremium,0)
   +ISNULL(MPO.PlIntake,0)+ISNULL(MPO.OdApp,0)+ISNULL(MPO.CcApp,0)+ISNULL(MPO.Investments,0)
   +ISNULL(MPO.FPFixed,0)+ISNULL(MPO.FPBYO,0)+ISNULL(MPO.FPMCL,0) AS TotalSaleCount) t
WHERE MPO.IsActive = 1 AND MPO.StatusId = 2   -- StatusId 2 = approved
  AND MPO.[Date] >= '2025-01-01'
