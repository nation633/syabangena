# GTM – Power BI data model (Banker_locator_V1)
There are 3 Power BI native queries: DirectQuery, server <SQL_SERVER>, database <REPORT_DB>. They are pure SELECTs, because the user has read-only rights.

| File | Purpose |
|---|---|
| powerbi_queries/MPO.sql | Activity fact: one row per approved activity, with org/company/source columns, date keys, flags and the 10 product counts |
| powerbi_queries/Product.sql | <PRODUCT_LOOKUP_TABLE> + ProductColumn mapping (disconnected slicer, cross-DB to <STAGING_DB>) |
| powerbi_queries/Product_DATATABLE.dax | Import alternative for Product if cross-DB access is not allowed |
| powerbi_queries/DimDate.sql | <DATE_SCHEMA>.DIM_DATE |
| powerbi_queries/DQ_ExecutedChecks.sql | Optional SSMS data-quality check (not a Power BI table) |
| model_design.md | Rules, diagram, build steps, DAX measures |
| product_mapping.csv | Mapping reference |
| open_questions.md | Remaining questions |
