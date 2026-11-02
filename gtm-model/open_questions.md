# Open questions
**Answered:**
- StatusId 2 = approved.
- ExecutedAt NULL = not executed (no fallback to the planned date).
- Queries live in Power BI for now.
- Also resolved earlier: DateKey = planned Date; Region = Province; banker key = StaffNumber; TotalSaleCount = sum of the 10 columns.

1. Run `DQ_ExecutedChecks.sql`. Should rows with Executed=1 but no ExecutedAt (counted as not executed) be fixed at source? And what about rows with Executed=0 but ExecutedAt set (counted as executed)?
2. Can not-executed activities carry sale counts (see the NotExecuted_WithSales check)? Should those sales count?
3. Date axis per measure: should planned/not executed use the planned date, and executed/sales the executed date? Or should everything use the planned date?
4. Product.sql reads <STAGING_DB> across databases. Does the report account have read access to <LANDING_DB> and <STAGING_DB> from the <REPORT_DB> connection? If not, use the Product_DATATABLE.dax table and ask the DBA for access or synonyms.
5. User has read-only rights today. Later, can a DBA create views/tables: in <REPORT_DB> or <LANDING_DB>, and which schema? Do we have CREATE rights?
6. Is the 2025-01-01 floor fixed or rolling (e.g. current + previous year)?
7. Company quality: is there a store/company master with an ID? Can the 'Other' free text be cleaned?
8. Org and banker columns are read from each activity row in MPO, so a banker who moves branch shows under each branch as at the activity date. A banker's name can also differ between rows. Is that acceptable?
9. Does each Branch belong to exactly one BU/Province/MicroMarket? Is there a branch master?
10. Does MPO.SizeOfOpportunity really hold the SourceOfOpportunity Id (the name suggests size)?
11. Product mapping:
    - CcApp, Investments and FPMCL: which <PRODUCT_LOOKUP_TABLE> rows?
    - OdApp: OD, ODA-A, ODA-C or ODLI?
    - Which field drives the Product Group slicer: PRODUCTGROUPNAME, MTD_PRODUCT_GROUP or TARGETNAME?
12. Is DirectQuery mandated, or is Import acceptable (volume/latency)?
13. RLS: by Province, Branch or banker? Is there a UPN mapping table?
14. Daily views: should weekends and holidays be excluded (IS_WEEKDAY / IS_HOLIDAY)?
15. The product slicer is a disconnected table, so it filters only Sales Count and Activities With Sales. Is that OK? And do the SWITCH-based measures perform acceptably in DirectQuery (Performance Analyzer)?
16. Avg Executed Activities with Sales (baseline report label, request N6): what is the definition? Per banker, per day, per branch, or something else? The measure is not written until this is answered.
17. Low Volume Flag (ROUTE 99): what Planned Activities threshold marks a unit as low volume? The placeholder is _MinPlanned = 20. Which column holds ROUTE 99 (BU or Region)?
