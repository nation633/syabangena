# Baseline enhancements: the user's existing report (2026-11-02)
Owner: Data Storyteller. The user's built report is the BASELINE. Enhance it, don't replace it. Keep the existing style: dark green #006341, lime #7AB800, grey #9AA5AB columns on white, green header bars, Arial 10 in black.
Rules: counts only, no rand values. Executed = MPO[Executed]="Yes". No bank names. Measures in **bold** already exist in dax/measures.dax. Anything marked NEW is requested from the DAX Analyst (see the end of this file).

## How the report's labels map to measures
| Report label | Measure |
|---|---|
| Planned Activities | **Planned Activities** |
| Executed Activities | **Executed Activities** |
| Not Executed | **Not Executed** (= **Gap to Plan**) |
| Activities with a Sale | **Activities With Sales** |
| Sales Made During Activities / Total Sales | **Sales Count** |
| Execution Rate % | **Execution Rate %** |
| Executed Activities Conversion % | **Conversion %** |
| Avg Executed Activities with Sales | no exact measure exists. Please confirm the user's definition. NEW request N6 |
| vs previous month deltas | **Executed MoM %**, **Planned MoM %**, **Sales Count MoM %**, **Activities With Sales MoM %**, **Execution Rate MoM pp**, **Conversion MoM pp** |

## Global fixes (every page)
- **Partial month (November):** ADD a "Data through dd Mmm (partial month)" subtitle using NEW [Data Through Date] and [Is Partial Month]. CHANGE the MoM deltas on the cards to compare MTD with the same days of the previous month (NEW [Executed PM Same Days], [Planned PM Same Days], [Sales Count PM Same Days] and [Executed MoM % Like-for-Like]). Until those exist, add a "partial month: the MoM % is not like-for-like" note. In the MoM column charts, show the partial month in a lighter shade or with a hatched outline (conditional formatting on NEW [Is Partial Month]).
- **ROUTE 99 (near-empty):** add a page-level filter that excludes it by default, plus a "Show low-volume units" toggle bookmark. If it must stay, sort it last and grey it out where **Planned Activities** is below the threshold (NEW [Low Volume Flag]). The column that holds ROUTE 99 needs confirming (BU or Region).
- **Label clutter:** keep the data labels on the Executed columns only. Move Planned to the tooltip, or keep it as an outline column. Show the Execution % and Conversion % as one line or circle with labels on the last point plus the min and max. Use display units K at 0 decimals. Use the Top N + "Other" pattern for long axes. Use a 9pt grey font for secondary labels.
- **Page cleanup:** list every page, then delete the duplicates and test pages (e.g. "Page 1", "Copy of …", "Duplicate of …", "test", "Test2"). Hide the tooltip and drill-through pages. Keep only these pages, in story order: Exec Overview > Business Unit > Region > Branch > Banker > Product > Company, plus Daily and Glossary. The Viz Designer will draw up the exact list from the .pbix page tabs (we only have screenshots).

## 1. Executive Overview
KEEP: the Year and Month slicers; the 7 KPI cards; the Planned vs Executed MoM column chart with the Execution % line; the BU matrix; the product-group horizontal bar; Daily Executed Vol.
CHANGE:
- The KPI cards: replace the text deltas with **SVG KPI Arrow Executed MoM**, **SVG KPI Arrow Planned MoM**, **SVG KPI Arrow Sales Count MoM** and **SVG KPI Arrow Not Executed MoM** (red when it goes up). On the Execution Rate card, add **SVG Bullet Execution Rate vs Plan** and **SVG Status Pill**.
- The MoM chart: clear the labels (as above) and flag November as partial.
- The BU matrix: add the columns **SVG Execution Progress**, **SVG Floating Bar Gap to Plan** (instead of a plain Not Executed number), **SVG Status Pill** and **SVG Dumbbell CY vs PY**.
ADD:
- A Plan Bridge waterfall: 'Plan Bridge'[Step] by **Plan Bridge Value** (Planned > Not Executed > Executed).
- A MoM change waterfall of **Executed MoM Diff** by month.
- A card for **Gap to Plan** and **Gap to Plan %**.
- Daily: add the **Executed 7D Avg** line on top of the columns.

## 2. Business Unit
KEEP: the Year, Month, Day and BU slicers; the BU Executed vs Sale chart with conversion circles; Daily Executed Vol.
CHANGE:
- The YTD cards: there are no YTD measures, so the cards use the slicer context now. NEW [Executed YTD], [Planned YTD] and [Sales Count YTD] would give true YTD cards.
- The Product Group % donut becomes a stacked 100% bar (product share of the sales). It needs product-level sales, and **Sales Count (Product)** is still commented out (provisional, mapping #11). Until then, use a stacked bar per BU of **Executed Activities** split into **Activities With Sales** and **Executed No Sale**.
- The conversion circles: one label on each circle, no column labels.
ADD:
- A BU table with **SVG Bullet Executed vs Planned**, **SVG Floating Bar Gap to Plan**, **SVG Dumbbell CY vs PY**, **SVG Status Pill**, **SVG Sparkline Executed** and **Executed CY vs PY Diff**.
- **SVG MoM Change Bar** per BU, plus **Executed MoM Diff**.
- A dynamic title bound to **Title - Business Unit**.

**CHANGE (2026-11-02, DAX Analyst): trend chart = rolling 12 months (L12M), replacing month-on-month.**
- Clustered column on 'L12M Axis'[Month Label] (date drill off) with **L12M Planned**, **L12M Executed**, **L12M Activities With Sales** (provisional); colour via **L12M Bar Colour**.
- The 12 months end at the selected month; the selected month is the last bar, highlighted #006341 (others grey).
- Planned and Activities With Sales (provisional) count on the planned date; Executed counts on the executed date.
- With no month selected, the chart ends at the latest month with data (**L12M Selected Month End** / Data Through Date); that last bar may be partial.
- Definitions: see the glossary's existing "Rolling 12 months (Business Unit page)" section (glossary_page.md).

## 3. Region
KEEP: the MoM chart; the Region Executed vs Sale chart with conversion circles; the MTD product matrix by region (the 6 product columns).
CHANGE:
- The Not Executed by BU bar becomes a floating bar chart (stacked bar: **Executed Activities** + **Gap to Plan**, with the gap in grey) or the **SVG Floating Bar Gap to Plan** table column.
- The Region sales % donut becomes a stacked 100% bar of **Sales Count** share by Region. Or, better, a waterfall of **Executed MoM Diff** by Region (MoM change contribution).
- The MTD product matrix: add the Region totals column **SVG Execution Progress** and turn on conditional-formatting data bars per product column. Product-level counts depend on **Sales Count (Product)** (provisional). The matrix currently uses the report's own product columns; keep them as they are.
ADD:
- A Region matrix with **SVG Status Pill**, **SVG Dumbbell CY vs PY**, **SVG MoM Change Bar**, and the **MoM Top Bottom Flag** / **MoM Top Bottom Group** for a Top/Bottom 10 view.
- A dynamic title bound to **Title - Region**. A drill path from Region to MicroMarket to Branch.

## NEW measures requested (DAX Analyst)
- N1 [Data Through Date]: the max DimDate[ACTUAL_DATE] with planned activities in context.
- N2 [Is Partial Month]: 1 when [Data Through Date] is before the end of the month.
- N3 [Executed PM Same Days], [Planned PM Same Days], [Sales Count PM Same Days]: the previous month, days 1..DAY([Data Through Date]).
- N4 [Executed MoM % Like-for-Like] (plus Planned and Sales): MTD vs PM Same Days. Also an SVG KPI Arrow variant.
- N5 [Low Volume Flag]: 1 when [Planned Activities] is below a VAR threshold (placeholder; ask the user). Used for ROUTE 99.
- N6 [Avg Executed Activities with Sales]: the user's definition is needed (per banker? per day?).
- N7 [Executed YTD], [Planned YTD], [Sales Count YTD] (DATESYTD on DimDate).
- N8 (optional) [Partial Month Label] for the subtitles.


## Status (2026-11-02)
- N1–N8 are in dax/measures.dax: folder 9. Partial Month & YTD, with the arrows in 6. SVG. Untested in Power BI.
- N6 (Avg Executed Activities with Sales) waits on the user's definition (open_questions #16).
- Low Volume Flag uses a PLACEHOLDER threshold of 20 planned (open_questions #17).
- SVG KPI Arrow Gap to Plan added, with reversed colours (a drop = green).
- Region gap: grey is correct, not red (the earlier red in the Storyteller Region mockup was a mistake).
- BU trend chart: now rolling 12 months (see section 2).
