/* Power BI native query: Get Data > SQL Server > server <SQL_SERVER>, database <REPORT_DB>,
   Advanced options > SQL statement. No CTEs/ORDER BY/USE: Power BI wraps DirectQuery native SQL in a subquery.
   Cross-database 3-part names require read access to <LANDING_DB> / <STAGING_DB> on the same instance. */
/* DimDate - Dual. Mark as date table on ACTUAL_DATE. Range trimmed to the fact window (2025+); widen upper bound as needed. */
SELECT DATE_KEY, CAST(ACTUAL_DATE AS date) AS ACTUAL_DATE, [YEAR], [QUARTER], QUARTER_NAME, YEAR_MONTH_KEY,
  [MONTH], MONTH_NAME, MONTH_SHORT_NAME, [WEEK], DAY_IN_YEAR, DAY_IN_MONTH, DAY_IN_WEEK,
  DAY_NAME, DAY_SHORT_NAME, IS_WEEKDAY, IS_HOLIDAY, MONTH_SORT_LABEL
FROM <REPORT_DB>.<DATE_SCHEMA>.DIM_DATE
WHERE DATE_KEY BETWEEN 20240101 AND 20271231   -- 2024 kept so PY comparisons for 2025 resolve (no 2024 facts though)
