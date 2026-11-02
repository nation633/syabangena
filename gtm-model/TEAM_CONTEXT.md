# GTM Dashboard - Team Context (shared by Data Modeler, DAX Analyst, Viz Designer)

Read this before any change. Update it when a decision is made.

## Ownership
- Data Modeler: SQL / Power Query (powerbi_queries/), relationships, model_design.md.
- DAX Analyst: dax/measures.dax, dax/measures_guide.md, measure definitions in glossary_page.md.
- Viz Designer: theme (/workspace/corporate-theme/CorporateGreen.json), backgrounds, page layouts, visuals.
- Main bot coordinates and talks to the user. GitHub pushes only when the user asks.

## Decisions (user-confirmed)
- Executed activities = source column Executed = "Yes" (not ExecutedAt non-null).
- Counts and sums only, no rand values.
- Non-executed activities must be visible.
- Chart-first, trends over matrices; glossary/how-to-read page required.
- No bank name anywhere in any file or commit. Style: corporate green, Arial 10, black text, 0 padding, white-on-green column headers.
- Server/database names are masked in anything pushed to GitHub (gtm-push/).

## Open (waiting on user)
- Product mapping for OdApp, CcApp, Investments, FPMCL.
- Date axis: executed/sales on executed date vs planned date.
- Whether sales on non-executed activities count (DQ_ExecutedChecks.sql results).

## Rules
- Before changing a shared file, check the other owners' files still match (column names, measure names).
- When you change a column, measure or name, note it in the Change log below.

## Change log
- 2026-11-02: Executed definition switched to Executed = "Yes" (query: Data Modeler, measures: DAX Analyst).

- 2026-11-02 12:25 SAST, DAX Analyst: Executed is now MPO[Executed] = "Yes" (KEEPFILTERS) in measures.dax, measures_guide.md and glossary_page.md; all derived measures follow. No IsExecuted references are left in the DAX. DEPENDS ON Data Modeler: the MPO query must expose Executed as text "Yes"/"No" (the source looks like 1/0) and derive HasSale with the same rule; model_design.md still says "ExecutedAt not null". The query files were not touched.
- 2026-11-02 12:30 SAST, Data Modeler: done. MPO.sql now outputs MPO[Executed] as text "Yes"/"No" (from source Executed = 1). IsExecuted = 1 when Executed = 'Yes'. HasSale = 1 only when Executed = 'Yes' AND TotalSaleCount > 0. ExecutedDateKey comes from ExecutedAt, executed rows only; it is used only for the executed-date axis. model_design.md is updated (no more "ExecutedAt not null"). The masked copies in gtm-push/ are updated too. Not pushed.
