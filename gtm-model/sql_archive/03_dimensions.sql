/* Run FIRST. Views are created in <REPORT_DB>.rpt (placeholder schema; alternative is
   <LANDING_DB> - see open_questions). Source: <LANDING_DB>.<LANDING_SCHEMA>.MonthlyPlannerOther (MPO).
   Removed vs original query: Executed_Concat, ExecutedDay, ExecutedYear, ExecutedMonth
   -> derive from DimDate via ExecutedDateKey instead. */
USE <REPORT_DB>;
GO
IF SCHEMA_ID('rpt') IS NULL EXEC('CREATE SCHEMA rpt');
GO
/* Base view = user's source query, cleaned. Sargable date filter. */
CREATE OR ALTER VIEW rpt.vPlannerActivity AS
SELECT
  MPO.Id                                   AS ActivityId,
  MPO.Banker                               AS StaffNumber,
  MPO.BankerName,
  CONVERT(int, CONVERT(char(8), MPO.[Date], 112)) AS PlannedDateKey,
  CONVERT(date, MPO.[Date])                AS PlannedDate,
  ISNULL(NULLIF(LTRIM(RTRIM(CASE WHEN MPO.Store = 'Other' THEN MPO.Other ELSE MPO.Store END)),''),'Unknown') AS Company,
  MPO.SizeOfOpportunity                    AS SourceOfOpportunityId,  -- FK to SourceOfOpportunity.Id
  ISNULL(LTRIM(RTRIM(MPO.BusinessUnit)),'Unknown') AS BusinessUnit,
  ISNULL(LTRIM(RTRIM(MPO.Province)),'Unknown')     AS Region,        -- Region = Province
  ISNULL(LTRIM(RTRIM(MPO.MicroMarket)),'Unknown')  AS MicroMarket,
  ISNULL(LTRIM(RTRIM(MPO.Branch)),'Unknown')       AS Branch,
  MPO.ExecutedTimeFrom, MPO.ExecutedTimeEnd, MPO.DateCreated, MPO.ExecutedAt,
  MPO.ExecutionDateAddedManually           AS ExecutedDate_Update,
  'Planned'                                AS ActivationType,
  x.Executed_Date,
  CONVERT(int, CONVERT(char(8), x.Executed_Date, 112)) AS ExecutedDateKey, -- NULL if not executed
  CAST(CASE WHEN MPO.Executed = 1 THEN 1 ELSE 0 END AS int) AS IsExecuted,
  CAST(CASE WHEN t.TotalSaleCount > 0 THEN 1 ELSE 0 END AS int) AS HasSale,
  t.TotalSaleCount
FROM <LANDING_DB>.<LANDING_SCHEMA>.MonthlyPlannerOther MPO
CROSS APPLY (SELECT CASE
     WHEN MPO.Executed = 1 AND MPO.ExecutedAt IS NOT NULL THEN MPO.ExecutedAt
     WHEN MPO.Executed = 1 AND MPO.ExecutedAt IS NULL
          AND MPO.ExecutedTimeFrom IS NOT NULL AND MPO.ExecutedTimeEnd IS NOT NULL THEN MPO.[Date]
     END AS Executed_Date) x
CROSS APPLY (SELECT ISNULL(MPO.MiGoals,0)+ISNULL(MPO.MiGoalsPlus,0)+ISNULL(MPO.MiGoalsPremium,0)
   +ISNULL(MPO.PlIntake,0)+ISNULL(MPO.OdApp,0)+ISNULL(MPO.CcApp,0)+ISNULL(MPO.Investments,0)
   +ISNULL(MPO.FPFixed,0)+ISNULL(MPO.FPBYO,0)+ISNULL(MPO.FPMCL,0) AS TotalSaleCount) t
WHERE MPO.IsActive = 1 AND MPO.StatusId = 2 AND MPO.[Date] >= '2025-01-01';
GO
/* Fact activity: keys only + flags (one row per ActivityId). */
CREATE OR ALTER VIEW rpt.vFactActivity AS
SELECT ActivityId, PlannedDateKey, ExecutedDateKey,
  CAST(CHECKSUM(BusinessUnit, Region, MicroMarket, Branch) AS int) AS OrgKey,
  StaffNumber AS BankerKey,
  CAST(CHECKSUM(Company) AS int) AS CompanyKey,
  ISNULL(SourceOfOpportunityId, -1) AS SourceOfOpportunityKey,
  ActivationType, IsExecuted, HasSale, TotalSaleCount,
  ExecutedTimeFrom, ExecutedTimeEnd, ExecutedAt, ExecutedDate_Update, DateCreated
FROM rpt.vPlannerActivity;
GO
/* Org: one row per BU > Region(Province) > MicroMarket > Branch. BranchCode parsed from 'NAME (415)'. */
CREATE OR ALTER VIEW rpt.vDimOrg AS
SELECT CAST(CHECKSUM(BusinessUnit, Region, MicroMarket, Branch) AS int) AS OrgKey,
  BusinessUnit, Region, MicroMarket, Branch,
  CASE WHEN CHARINDEX('(',Branch)>0 AND RIGHT(Branch,1)=')'
       THEN TRY_CAST(SUBSTRING(Branch,CHARINDEX('(',Branch)+1,LEN(Branch)-CHARINDEX('(',Branch)-1) AS int) END AS BranchCode,
  LTRIM(RTRIM(CASE WHEN CHARINDEX('(',Branch)>0 THEN LEFT(Branch,CHARINDEX('(',Branch)-1) ELSE Branch END)) AS BranchName
FROM (SELECT DISTINCT BusinessUnit, Region, MicroMarket, Branch FROM rpt.vPlannerActivity) o;
GO
/* Banker: natural key StaffNumber; latest BankerName (by DateCreated, then Id). */
CREATE OR ALTER VIEW rpt.vDimBanker AS
SELECT StaffNumber AS BankerKey, StaffNumber, BankerName
FROM (SELECT StaffNumber, BankerName,
        ROW_NUMBER() OVER (PARTITION BY StaffNumber ORDER BY DateCreated DESC, ActivityId DESC) AS rn
      FROM rpt.vPlannerActivity) b
WHERE rn = 1;
GO
/* Company: free text (Store, or Other text when Store='Other') - data quality issue, no master key. */
CREATE OR ALTER VIEW rpt.vDimCompany AS
SELECT CAST(CHECKSUM(Company) AS int) AS CompanyKey, Company
FROM (SELECT DISTINCT Company FROM rpt.vPlannerActivity) c;
GO
/* Source of opportunity: small dim, key = SOO.Id; -1 = Unknown for unmatched/NULL. */
CREATE OR ALTER VIEW rpt.vDimSourceOfOpportunity AS
SELECT SOO.Id AS SourceOfOpportunityKey, SOO.Name AS SourceOfOpportunity
FROM <LANDING_DB>.<LANDING_SCHEMA>.SourceOfOpportunity SOO
UNION ALL SELECT -1, 'Unknown';
GO
/* Checks: duplicate hash keys / orphans
SELECT OrgKey,COUNT(*) FROM rpt.vDimOrg GROUP BY OrgKey HAVING COUNT(*)>1;
SELECT CompanyKey,COUNT(*) FROM rpt.vDimCompany GROUP BY CompanyKey HAVING COUNT(*)>1;
SELECT DISTINCT SourceOfOpportunityId FROM rpt.vPlannerActivity p
 WHERE NOT EXISTS (SELECT 1 FROM <LANDING_DB>.<LANDING_SCHEMA>.SourceOfOpportunity s WHERE s.Id=p.SourceOfOpportunityId); */
