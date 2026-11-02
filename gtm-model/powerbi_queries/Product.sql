/* Power BI native query: Get Data > SQL Server > <SQL_SERVER>, database <REPORT_DB>, DirectQuery,
   Advanced options > SQL statement. Pure SELECT (read-only rights); no CTE / ORDER BY / USE.
   Cross-database 3-part names need read access to <LANDING_DB> / <STAGING_DB> on the same instance. */
/* Product - disconnected slicer table (Dual or Import; no relationships).
   One row per mapped <PRODUCT_LOOKUP_TABLE> row; ProductColumn = MPO column name it is counted in.
   Unmapped columns (CcApp, Investments, FPMCL) still appear once with lookup fields NULL.
   Several lookup rows can share a ProductColumn (e.g. FP-A FIXED) - measures use DISTINCT ProductColumn. */
SELECT m.ProductColumn, m.ProductLabel, m.ProductSort,
  COALESCE(g.PRODUCTGROUPNAME, m.MapProductGroup) AS ProductGroup,
  g.PRODUCTSORTID, g.CMS_PRODUCT_KEY, g.CMS_PRODUCT_ID, g.PRODUCTNAME, g.REPORTINGPRODUCTNAME,
  g.TARGETNAME, g.MTD_PRODUCT_GROUP,
  m.Confidence, m.NeedsConfirmation
FROM (VALUES
  ('MiGoals',       'MiGoals',                 1,'TP',        'TP',        'MiGoals',        'High',  'N'),
  ('MiGoalsPlus',   'MiGoals Plus',            2,'TP',        'TP',        'MiGoals Plus',   'High',  'N'),
  ('MiGoalsPremium','MiGoals Premium',         3,'TP',        'TP',        'MiGoals Premium','High',  'N'),
  ('PlIntake',      'Personal Loan Intake',    4,'PLI',       'PLI',       NULL,             'High',  'N'),
  ('OdApp',         'Overdraft Application',   5,'OD',        'OD',        NULL,             'Medium','Y'),
  ('CcApp',         'Credit Card Application', 6,NULL,        'UNKNOWN',   NULL,             'Low',   'Y'),
  ('Investments',   'Investments',             7,NULL,        'UNKNOWN',   NULL,             'Low',   'Y'),
  ('FPFixed',       'Funeral Plan Fixed',      8,'FP-A FIXED','FP-A FIXED',NULL,             'High',  'N'),
  ('FPBYO',         'Funeral Plan BYO',        9,'FP-A BYO',  'FP-A BYO',  NULL,             'High',  'N'),
  ('FPMCL',         'Funeral Plan MCL',       10,NULL,        'UNKNOWN',   NULL,             'Low',   'Y')
) m(ProductColumn, ProductLabel, ProductSort, MapProductName, MapProductGroup, MapMTDGroup, Confidence, NeedsConfirmation)
LEFT JOIN <STAGING_DB>.dbo.<PRODUCT_LOOKUP_TABLE> g
  ON g.PRODUCTNAME = m.MapProductName
 AND (m.MapMTDGroup IS NULL OR g.MTD_PRODUCT_GROUP = m.MapMTDGroup)
