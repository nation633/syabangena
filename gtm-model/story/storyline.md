# GTM Dashboard - Storyline v2 (Data Storyteller)

Status: DRAFT v2, 2026-11-02. This version follows two user decisions logged in TEAM_CONTEXT.md:
1. **Story order:** Exec > BU > Region > Branch > Individual (banker) > Product > Company.
2. **Target = Planned:** bullets, pills and progress bars compare Executed with Planned (execution rate vs 100% of plan). PY is secondary context, shown as a grey tick.

The file uses only measures in `dax/measures.dax` (64 measures, including 6. SVG and 7. Titles), the field parameters in `dax/field_parameters.tmdl` (Metric, Level), and the columns in `powerbi_queries/`. Revised and new SVG drafts are in `story/svg_measures_proposal.dax` for the DAX Analyst. Visual IDs refer to `viz/layout_spec.md`, which the Viz Designer owns. The page renumbering below is a request to the Viz Designer and is not built yet.

## Ground rules
- Only counts, sums and % of counts. No rand values. Executed means MPO[Executed] = "Yes". Not Executed is always visible.
- **Target = Planned Activities.** "On plan" means Execution Rate % >= 100%. PY appears only as a secondary marker or label.
- Sales and **Product are PROVISIONAL.** `Sales Count (Product)` is a stub, so the Product slicer changes nothing yet.
- Open questions stay open: #2 (sales on non-executed rows), #3 (date axis; the planned date is used, and "(Exec Date)" visuals are a separate lens), #11 (product mapping), #14 (weekends).
- Everything responds to the synced slicers. Dynamic titles state the selection.
- Style: #006341, Arial 10, black text, 0 padding, headers white on green, no lime green. No organisation names. Mockup numbers are EXAMPLE DATA.

## Page order and drill path
| # | Page (proposed name) | Today in layout_spec | Level | Drill to next level |
|---|---|---|---|---|
| 1 | **Exec Overview** | Page 1 Overview, plus Page 2 Execution as its detail | Whole business | Click a BU bar, or drill down on the MPO hierarchy |
| 2 | **Business Unit** | Page 4 Hierarchy (BU level) | MPO[BusinessUnit] | Drill down to Region; page navigation passes the BU selection through synced slicers |
| 3 | **Region** | Page 4 Hierarchy (Region small multiples) | MPO[Region] (> MicroMarket) | Drill down to MicroMarket > Branch |
| 4 | **Branch** | Page 2 Execution V4/V4T + Page 4 ribbon | MPO[Branch] | Right-click > drill-through **Branch Detail** (optional page) or drill down to Banker |
| 5 | **Banker (Individual)** | Page 5 Banker | MPO[BankerName] | Right-click > drill-through **Banker Detail** (5a) |
| 5a | Banker Detail (drill-through, hidden) | Page 5a | One banker | Company table on the page; Back button |
| 6 | **Product (PROVISIONAL)** | Page 3 Sales Conversion | Product[ProductGroup] > ProductLabel | Inactive until #11; conversion by branch and banker is shown meanwhile |
| 7 | **Company** | Page 6 Company | MPO[Company] | Drill-through Banker Detail (which bankers visit it) |
| S1 | Daily (supporting) | Page 7 | Day | - |
| S2 | Glossary (supporting) | Page 8 | - | - |

**One drill spine:** BU > Region > MicroMarket > Branch > BankerName, using the existing MPO hierarchy and the **Level** field parameter. Each page fixes the level and keeps the slicers synced, so a selection made on an earlier page carries forward. A "Next level" button at the top right of each page navigates to the next page in the order.

---

## 1. Exec Overview
**Questions:** Are we on plan? How many planned activities were not executed? Is that better or worse than last month and last year?

| Visual | Insight | Interaction / SVG |
|---|---|---|
| K1-K5 KPI cards | Planned, Executed, Not Executed, Execution Rate %, Sales Count (provisional). Trends vs MoM and PY | `SVG KPI Arrow * MoM` (existing). K4 changes to `SVG Bullet Execution Rate vs Plan` + `SVG Status Pill` (revised: % of plan) |
| Funnel Planned > Executed > With Sales | Execution gap, then conversion gap | Interaction None |
| Executed and not executed by month vs PY | Months below plan | `Title - Executed vs PY`; drill YEAR > MONTH |
| Bar by BU (NEW, replaces the donut) | Which BU is furthest from plan | Click to cross-filter; this is the entry to page 2 |
| Execution detail (current Execution page) | Non-executed volume and the donut on MPO[Executed] | Keep it as the second tab of the Exec section, or fold its V1/V2 into this page |

## 2. Business Unit
**Questions:** Which BU misses plan, and is it worsening?
- Matrix on MPO[BusinessUnit] with expand to Region. Columns: Planned, Executed, Not Executed, `SVG Bullet Executed vs Planned`, `SVG Status Pill`, `SVG Sparkline Executed`.
- Decomposition tree (Analyze uses the **Metric** parameter, default Not Executed), starting at BU.
- A trend line per BU: Execution Rate % vs Execution Rate PY.
- Rolling 12 months trend (replaces month-on-month): clustered column of `L12M Planned`, `L12M Executed`, `L12M Activities With Sales` (provisional) on 'L12M Axis'[Month Label], ending at the selected month (last bar #006341 via `L12M Bar Colour`). Planned and Activities With Sales on planned date, Executed on executed date. No month selected = ends at the latest month with data, last bar may be partial. See glossary "Rolling 12 months (Business Unit page)".

## 3. Region
**Questions:** Within the BU, which regions and micro-markets drive the gap?
- Small multiples by MPO[Region]: Planned vs Executed by month (existing Hierarchy V2).
- Bar chart on the **Level** parameter (Region / MicroMarket), with Execution Rate % plus a bullet column in a companion table.
- Outliers: regions with a pill below plan and a falling sparkline.

## 4. Branch
**Questions:** Which branches have the most non-executed activities, and which fall furthest below plan?
- Top 15 branches by Not Executed (existing Execution V4), with the Chart/Table toggle (V4T). Table columns: progress bar (revised, with a PY tick), pill (revised), sparkline, `SVG Bullet Executed vs Planned`.
- A ribbon chart of branch rank (existing Hierarchy V3).
- TT Branch tooltip with the sparkline. Drill-through: optional Branch Detail.

## 5. Banker (Individual)
**Questions:** Who plans but doesn't execute? Who is on plan? Who converts? (Conversion is provisional.)
- Scorecard table (existing V4): BankerName, Planned, Executed, Not Executed, `SVG Bullet Execution Rate vs Plan` (rate bullet, so bankers of different sizes compare fairly), `SVG Status Pill`, `SVG Sparkline Executed`.
- Scatter: Execution Rate % vs Conversion % (provisional).
- TT Banker tooltip. Drill-through goes to Banker Detail.

### 5a. Banker Detail
- KPI strip; `Title - Banker Detail`.
- Monthly executed and not executed with the execution rate.
- Company table: Company, Planned, Executed, Not Executed, **`SVG Status Pill` (execution vs plan for that company)**, and a **separate `Executed No Sale` number column** (provisional, with a "(provisional)" header). The pill and Executed No Sale are separate columns, and the pill does not show sales.
- **Gauge decision: no `SVG Conversion Gauge` on Banker Detail.** Conversion is provisional, and the KPI strip already shows the banker's Conversion % as a number. The gauge stays on the Product page only.

## 6. Product (PROVISIONAL)
**Questions:** Which products drive conversion? This waits on #11.
- Executed, With Sales and Conversion % by month; `Title - Conversion`; `SVG Conversion Gauge` (existing, provisional).
- Product group and product visuals show a "Pending product mapping" placeholder.
- Scatter of Executed vs Sales by branch, as an interim conversion-driver view.

## 7. Company
**Questions:** Where do visits produce nothing, and where are repeat no-sale visits?
- Top 20 companies, executed and not executed, with a pill column (vs plan).
- Visits vs sales scatter (provisional).
- `Repeat No-Sale Companies` card and an `Executed No Sale` bar (both provisional).
- Free-text Company caveat (#7). Drill-through to Banker Detail.

## Supporting: Daily, Glossary
- **Daily:** calendar heatmap, daily view with 7D Avg, weekday pattern, Exec Date vs PY. Weekends are included (#14 open).
- **Glossary:** add "Target = Planned: on plan = execution rate 100%. The black line is the plan, and the grey tick is last year." Add "Pill (3 bands): green = 100% of plan or more, amber = 90% to under 100%, red = under 90%." Add "Sparkline: months in the current filter, not a fixed 12 months."

## Interactivity (unchanged principles)
- Cross-filter by default; the funnel is set to None.
- Drill-down on the MPO hierarchy, and DimDate YEAR > MONTH > day.
- Drill-through to Banker Detail, plus the optional Branch Detail.
- Tooltip pages: TT Branch and TT Banker.
- Field parameters: Metric on the decomposition tree and trend visuals; Level on the BU/Region bars.
- Bookmarks: Reset and Chart/Table.
- Dynamic titles from folder 7. Titles. Optional smart narrative.

## SVG shortlist (Target = Planned)
| Visual | Measure | Status | Depends on (existing) |
|---|---|---|---|
| Progress bar with plan end mark and PY tick | SVG Execution Progress | REVISED | Execution Rate %, Execution Rate PY, Planned Activities |
| Status pill (% of plan, 3 bands: green >=100%, amber 90-<100%, red <90%) | SVG Status Pill | IN measures.dax (3 bands) | Execution Rate %, Planned Activities |
| Bullet, counts | SVG Bullet Executed vs Planned | NEW | Executed Activities, Planned Activities, Executed PY |
| Bullet, rate | SVG Bullet Execution Rate vs Plan | NEW | Execution Rate %, Execution Rate PY, Planned Activities |
| Sparkline | SVG Sparkline Executed | unchanged (spans the months in filter context) | Planned/Executed Activities, Not Executed |
| Gauge (provisional) | SVG Conversion Gauge | unchanged; Product page only | Conversion %, Conversion PY, Executed Activities |
| KPI arrows | SVG KPI Arrow Planned / Executed / Not Executed / Sales Count MoM | unchanged | the * MoM % measures |
