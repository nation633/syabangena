/* Data-quality check (run in SSMS, not a Power BI table). */
SELECT
  SUM(CASE WHEN MPO.Executed = 1 AND MPO.ExecutedAt IS NULL     THEN 1 ELSE 0 END) AS Executed1_ExecutedAtNull,   -- counted NOT executed
  SUM(CASE WHEN ISNULL(MPO.Executed,0) = 0 AND MPO.ExecutedAt IS NOT NULL THEN 1 ELSE 0 END) AS Executed0_ExecutedAtSet, -- counted executed
  SUM(CASE WHEN MPO.ExecutedAt IS NULL AND (ISNULL(MPO.MiGoals,0)+ISNULL(MPO.MiGoalsPlus,0)+ISNULL(MPO.MiGoalsPremium,0)
      +ISNULL(MPO.PlIntake,0)+ISNULL(MPO.OdApp,0)+ISNULL(MPO.CcApp,0)+ISNULL(MPO.Investments,0)
      +ISNULL(MPO.FPFixed,0)+ISNULL(MPO.FPBYO,0)+ISNULL(MPO.FPMCL,0)) > 0 THEN 1 ELSE 0 END) AS NotExecuted_WithSales,
  COUNT(*) AS ApprovedActivities  -- optional SSMS check, not a Power BI table
FROM <LANDING_DB>.<LANDING_SCHEMA>.MonthlyPlannerOther MPO
WHERE MPO.IsActive = 1 AND MPO.StatusId = 2   -- StatusId 2 = approved
  AND MPO.[Date] >= '2025-01-01'
