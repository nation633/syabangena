/* Run LAST. Sales fact: one row per activity x product, SaleCount > 0.
   Unpivots directly from <LANDING_DB>.<LANDING_SCHEMA>.MonthlyPlannerOther with the same filters as rpt.vPlannerActivity. */
USE <REPORT_DB>;
GO
CREATE OR ALTER VIEW rpt.vFactSales AS
SELECT
  MPO.Id AS ActivityId,
  CONVERT(int, CONVERT(char(8), MPO.[Date], 112)) AS PlannedDateKey,
  CONVERT(int, CONVERT(char(8), CASE
     WHEN MPO.Executed = 1 AND MPO.ExecutedAt IS NOT NULL THEN MPO.ExecutedAt
     WHEN MPO.Executed = 1 AND MPO.ExecutedAt IS NULL
          AND MPO.ExecutedTimeFrom IS NOT NULL AND MPO.ExecutedTimeEnd IS NOT NULL THEN MPO.[Date]
     END, 112)) AS ExecutedDateKey,
  CAST(CHECKSUM(ISNULL(LTRIM(RTRIM(MPO.BusinessUnit)),'Unknown'), ISNULL(LTRIM(RTRIM(MPO.Province)),'Unknown'),
                ISNULL(LTRIM(RTRIM(MPO.MicroMarket)),'Unknown'),  ISNULL(LTRIM(RTRIM(MPO.Branch)),'Unknown')) AS int) AS OrgKey,
  MPO.Banker AS BankerKey,
  CAST(CHECKSUM(ISNULL(NULLIF(LTRIM(RTRIM(CASE WHEN MPO.Store='Other' THEN MPO.Other ELSE MPO.Store END)),''),'Unknown')) AS int) AS CompanyKey,
  ISNULL(MPO.SizeOfOpportunity, -1) AS SourceOfOpportunityKey,
  v.ProductColumn AS ProductKey,
  v.SaleCount
FROM <LANDING_DB>.<LANDING_SCHEMA>.MonthlyPlannerOther MPO
CROSS APPLY (VALUES
  ('MiGoals',        ISNULL(MPO.MiGoals,0)),
  ('MiGoalsPlus',    ISNULL(MPO.MiGoalsPlus,0)),
  ('MiGoalsPremium', ISNULL(MPO.MiGoalsPremium,0)),
  ('PlIntake',       ISNULL(MPO.PlIntake,0)),
  ('OdApp',          ISNULL(MPO.OdApp,0)),
  ('CcApp',          ISNULL(MPO.CcApp,0)),
  ('Investments',    ISNULL(MPO.Investments,0)),
  ('FPFixed',        ISNULL(MPO.FPFixed,0)),
  ('FPBYO',          ISNULL(MPO.FPBYO,0)),
  ('FPMCL',          ISNULL(MPO.FPMCL,0))
) v(ProductColumn, SaleCount)
WHERE MPO.IsActive = 1 AND MPO.StatusId = 2 AND MPO.[Date] >= '2025-01-01'
  AND v.SaleCount > 0;
GO
/* Reconciliation (expect 0 rows):
SELECT a.ActivityId FROM rpt.vFactActivity a
LEFT JOIN (SELECT ActivityId, SUM(SaleCount) s FROM rpt.vFactSales GROUP BY ActivityId) s ON s.ActivityId = a.ActivityId
WHERE a.TotalSaleCount <> ISNULL(s.s,0); */
