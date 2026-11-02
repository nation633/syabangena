# Baseline enhancement spec (Viz Designer, 2026-11-02 15:20 SAST)
Source: story/baseline_enhancements.md. ENHANCE the user's existing report; do not rebuild pages. Keep the look: dark green #006341, lime #7AB800, grey #9AA5AB columns on white, green header bars, Arial 10, black text, white-on-green headers. Counts only. Measures: only those in dax/measures.dax. PENDING = depends on N1–N8 (DAX Analyst). Mockups: viz/baseline/mockups/*_v2.png (EXAMPLE DATA).

## Colour rule for arrows
- Executed / Planned / Sales: up = #006341, down = #B03A2E.
- Not Executed and Gap to Plan (reversed): DOWN = #006341 (smaller gap is good), up = #B03A2E. Use **SVG KPI Arrow Not Executed MoM** (already reversed in measures.dax). Gap to Plan = Not Executed, so the same arrow serves the Gap card. If built with native card conditional formatting instead, set the rule: Not Executed MoM % < 0 → #006341.

## Global (every page)
| Item | Action | Measures | Status |
|---|---|---|---|
| Partial-month subtitle | Text box/card under the header | N1 Data Through Date, N2 Is Partial Month, N8 label | PENDING |
| Interim note | Static text "Partial month: the MoM % is not like-for-like" | – | Do now; remove when N3/N4 land |
| Like-for-like MoM on cards | Swap card deltas | N3, N4 (+ arrow variant) | PENDING |
| Partial month light shade in MoM columns | Column colour fx rule | N2 | PENDING |
| ROUTE 99 | Page filter excluding it + "Show low-volume units" bookmark toggle | – (filter); grey-out needs N5 | Filter: do now once column confirmed; grey: PENDING |
| Label clutter | Data labels on Executed only; Planned in tooltip/outline; rate line labels last point + min/max; display units K, 0 dp; secondary labels 9pt grey #9AA5AB | existing | Do now |

## 01 Executive Overview
KEEP: Year/Month slicers, 7 KPI cards, Planned vs Executed MoM + Execution % line, BU matrix, product-group bar, Daily Executed Vol.
CHANGE:
- KPI deltas → SVG KPI Arrow Planned MoM / Executed MoM / Sales Count MoM / Not Executed MoM (Image URL, 120x20 card image or new card visual image). Activities with a Sale and Conversion % keep text deltas (Activities With Sales MoM %, Conversion MoM pp; no arrow SVG exists).
- Execution Rate card: add SVG Bullet Execution Rate vs Plan + SVG Status Pill.
- Not Executed card → relabel "Gap to Plan" showing Gap to Plan, subtitle Gap to Plan %, arrow SVG KPI Arrow Not Executed MoM (down = green).
- MoM chart: labels per global rule; Nov light = PENDING N2.
- BU matrix: add SVG Execution Progress, SVG Floating Bar Gap to Plan, SVG Status Pill, SVG Dumbbell CY vs PY (grid image H20/W120).
ADD: Plan Bridge waterfall ('Plan Bridge'[Step] sorted by Order, Plan Bridge Value, total renamed "Executed"); MoM change waterfall (month axis, Executed MoM Diff); Executed 7D Avg line on Daily (line-and-column).

## 02 Business Unit
CHANGE (DAX Analyst request, 15:30): MoM chart -> rolling last 12 months clustered column, same position/size. X = 'L12M Axis'[Month Label] (sorted by hidden Month Sort Key, not a date hierarchy, drill off); Y = L12M Planned, L12M Executed, L12M Activities With Sales (PROVISIONAL); visual filter L12M Visible Flag = 1; Columns colour fx Field value = L12M Bar Colour (#006341 selected month, #A6A6A6 others). Table from dax/l12m_axis.tmdl (no relationships); measures folder 10. L12M (verified present, untested in Power BI). Month slicer stays on DimDate. Aug 2026 selected = Sep 2025-Aug 2026; nothing selected = 12 months to latest month with data. Replaces the "Nov light = PENDING N2" shading on this chart (selected-month colour wins).
KEEP: Year/Month/Day/BU slicers, BU Executed vs Sale + conversion circles, Daily Executed Vol.
CHANGE:
- YTD cards: keep on slicer context; true YTD = PENDING N7 (Executed/Planned/Sales Count YTD). Relabel to drop "YTD" until then.
- Product Group % donut → stacked bar per BU: Activities With Sales + Executed No Sale (100% stacked). Product-share version waits on Sales Count (Product) (mapping #11).
- Conversion circles: one label per circle; remove column labels.
ADD: BU table (SVG Bullet Executed vs Planned, SVG Floating Bar Gap to Plan, SVG Dumbbell CY vs PY, Executed CY vs PY Diff, SVG Status Pill, SVG Sparkline Executed, SVG MoM Change Bar, Executed MoM Diff); title fx = Title - Business Unit.

## 03 Region
KEEP: MoM chart, Region Executed vs Sale + conversion circles, MTD product matrix (report's own 6 product columns, unchanged).
CHANGE:
- Not Executed by BU bar → stacked bar Executed Activities (#006341) + Gap to Plan (grey #9AA5AB per spec; mockup draws it red – build grey).
- Region sales % donut → 100% stacked bar of Sales Count by Region (preferred alt: waterfall of Executed MoM Diff by Region).
- Product matrix: add SVG Execution Progress totals column + data bars per product column.
ADD: Region table (SVG Status Pill, SVG Dumbbell CY vs PY, SVG MoM Change Bar; visual filter MoM Top Bottom Flag = 1, colour/group MoM Top Bottom Group); title fx = Title - Region; drill Region > MicroMarket > Branch.

## Not in baseline doc
Branch, Banker, Product, Company, Daily, Glossary: baseline_enhancements.md gives no notes and there are no baseline screenshots/mockups, so no changes specified here.
