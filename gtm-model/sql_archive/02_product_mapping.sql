/* Run SECOND (after 03_dimensions.sql). Database: <REPORT_DB>, schema rpt. */
USE <REPORT_DB>;
GO
/* Mapping fact product column -> <PRODUCT_LOOKUP_TABLE>. Table so business can maintain it. */
IF OBJECT_ID('rpt.ProductColumnMap') IS NULL
CREATE TABLE rpt.ProductColumnMap(
  ProductColumn varchar(50) NOT NULL PRIMARY KEY,
  ProductSort int NOT NULL,
  ReportingProduct varchar(100) NOT NULL,
  MapToProductName_Like varchar(100) NULL,   -- PRODUCTNAME code in lookup
  MapToProductGroupName varchar(100) NULL,
  MapToMTDProductGroup varchar(100) NULL,
  Confidence varchar(10) NOT NULL,
  NeedsConfirmation char(1) NOT NULL);
GO
TRUNCATE TABLE rpt.ProductColumnMap;
INSERT rpt.ProductColumnMap VALUES
('MiGoals',1,'MiGoals','TP','TP','MiGoals','High','N'),
('MiGoalsPlus',2,'MiGoals Plus','TP','TP','MiGoals Plus','High','N'),
('MiGoalsPremium',3,'MiGoals Premium','TP','TP','MiGoals Premium','High','N'),
('PlIntake',4,'Personal Loan Intake','PLI','PLI',NULL,'High','N'),
('OdApp',5,'Overdraft Application','OD','OD',NULL,'Medium','Y'),
('CcApp',6,'Credit Card Application',NULL,'UNKNOWN',NULL,'Low','Y'),
('Investments',7,'Investments',NULL,'UNKNOWN',NULL,'Low','Y'),
('FPFixed',8,'Funeral Plan Fixed','FP-A FIXED','FP-A FIXED',NULL,'High','N'),
('FPBYO',9,'Funeral Plan BYO','FP-A BYO','FP-A BYO',NULL,'High','N'),
('FPMCL',10,'Funeral Plan MCL',NULL,'UNKNOWN',NULL,'Low','Y');
GO
/* Dim Product at fact-column grain (10 rows) so every sale maps to exactly one product.
   Lookup attributes taken from first matching lookup row (lookup has many rows per group). */
CREATE OR ALTER VIEW rpt.vDimProduct AS
SELECT m.ProductColumn AS ProductKey, m.ReportingProduct AS Product, m.ProductSort,
  COALESCE(l.PRODUCTGROUPNAME, m.MapToProductGroupName) AS ProductGroup,
  l.REPORTINGPRODUCTNAME, l.TARGETNAME, l.MTD_PRODUCT_GROUP, l.CMS_PRODUCT_KEY,
  m.Confidence, m.NeedsConfirmation
FROM rpt.ProductColumnMap m
OUTER APPLY (SELECT TOP 1 g.* FROM [<STAGING_DB>].[dbo].[<PRODUCT_LOOKUP_TABLE>] g
   WHERE g.PRODUCTNAME = m.MapToProductName_Like
     AND (m.MapToMTDProductGroup IS NULL OR g.MTD_PRODUCT_GROUP = m.MapToMTDProductGroup)
   ORDER BY g.PRODUCTSORTID) l;
GO
/* Cross-database reference to <STAGING_DB>: in DirectQuery, prefer copying the lookup into
   <REPORT_DB> (or a synonym) so Power BI queries a single database. */
