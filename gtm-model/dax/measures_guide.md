# GTM DAX measures guide

Source: `measures.dax` (table MPO). Dates: **planned** = active relationship DimDate[DATE_KEY]→MPO[DateKey]; **executed** = inactive DimDate[DATE_KEY]→MPO[ExecutedDateKey] via USERELATIONSHIP. Product slicer does not affect any measure except the (stubbed) product-level sales.

## Core measures

| Measure | Glossary wording | Logic | Date |
|---|---|---|---|
| Planned Activities | Approved activities bankers planned | DISTINCTCOUNT(ActivityId) | Planned |
| Executed Activities | Planned activities that were carried out | DISTINCTCOUNT(ActivityId) where MPO[Executed] = "Yes" (KEEPFILTERS) | Planned |
| Executed (Exec Date) | Same activities, placed on the day they were executed | Executed Activities + USERELATIONSHIP to ExecutedDateKey | Executed |
| Not Executed | Planned activities not marked as executed | Planned − Executed (blank when nothing planned) | Planned |
| Execution Rate % | Share of planned activities that were carried out | DIVIDE(Executed, Planned) | Planned |

## Executed flag vs executed date

**Dependency:** these measures assume the model exposes `MPO[Executed]` as text with exactly "Yes"/"No". The current MPO query does not (it drops the text flag and derives IsExecuted from ExecutedAt); this depends on the MPO query change being made by its owner. HasSale must also follow the Executed = Yes rule there.

Executed is decided only by the source Executed flag (`MPO[Executed] = "Yes"`); every Executed-based measure (Executed, Not Executed, Execution Rate %, Activities With Sales, Conversion % and all PY/PM/YoY/MoM/7D variants) uses it. ExecutedDateKey (from ExecutedAt) is used only by the USERELATIONSHIP on the executed-date axis. **Rows with Executed = 'Yes' but no ExecutedAt/ExecutedDateKey have no date on that axis, so Executed (Exec Date) can be lower than Executed Activities** for the same period (see Executed1_ExecutedAtNull in DQ_ExecutedChecks.sql).

## Comparisons (folder 2. Comparisons)

For Planned, Executed, Executed (Exec Date), Not Executed: **PY** = same period last year (SAMEPERIODLASTYEAR); **PM** = shifted back one month (DATEADD −1 MONTH); **YoY %** = (selected period − last year) / last year; **MoM %** = (this month − previous month) / previous month. Each uses the same date as its base measure (Exec Date variants shift the executed date).

Execution Rate has PY/PM plus **YoY pp / MoM pp** (difference in percentage points) instead of a % change of a %.

## Rolling (folder 3. Rolling)

`<measure> 7D Avg` for Planned, Executed, Executed (Exec Date), Not Executed: total over the 7 calendar days ending on the day in context ÷ 7 (days in DimDate window). Use on daily axes. Weekends/holidays are included (open question #14; filter IS_WEEKDAY if excluded).

## Sales – PROVISIONAL (folder 4)

| Measure | Glossary wording | Logic | Date |
|---|---|---|---|
| Sales Count | Number of product sales recorded on activities | SUM(TotalSaleCount), all 10 products; ignores Product slicer; includes not-executed rows | Planned |
| Activities With Sales | Activities that produced at least one sale | DISTINCTCOUNT(ActivityId) where MPO[Executed] = "Yes" and HasSale = 1 | Planned |
| Conversion % | Share of executed activities that produced a sale | DIVIDE(Activities With Sales, Executed Activities) | Planned |
| Sales Count PY / PM | as above | SAMEPERIODLASTYEAR / DATEADD | Planned |

Open: product mapping for OdApp, CcApp, Investments, FPMCL (#11); date axis for sales (#3); whether sales on not-executed activities count (#2). The SWITCH-based `Sales Count (Product)` is commented out at the end of measures.dax until answered. Note Sales Count includes unexecuted rows while Activities With Sales excludes them — align once #2 is answered.

## Added 2026-11-02 (all planned date; sales-based ones PROVISIONAL)

| Measure | Folder | Glossary wording | Logic |
|---|---|---|---|
| Sales Count YoY % / MoM % | 4. Sales | Change in Sales Count vs last year / previous month | DIVIDE(cur − PY/PM, PY/PM) |
| Activities With Sales PY / PM / YoY % / MoM % | 4. Sales | Same, for activities with sales | SAMEPERIODLASTYEAR / DATEADD −1 MONTH; DIVIDE |
| Conversion PY / PM | 4. Sales | Conversion % last year / previous month | CALCULATE([Conversion %], shift) |
| Conversion YoY pp / MoM pp | 4. Sales | Change in conversion, in percentage points | Conversion % − PY/PM (blank if either is blank) |
| Executed No Sale | 4. Sales | Executed activities that produced no sale | DISTINCTCOUNT(ActivityId), Executed = "Yes" and HasSale = 0 |
| Repeat No-Sale Companies | 4. Sales | Companies visited more than once with no sale on any visit | ADDCOLUMNS(VALUES(MPO[Company]), Executed, With Sales) → COUNTROWS(FILTER(Executed > 1 and With Sales = 0)). Iterates only the small company list; each row is one aggregated SQL query batch |
| Sales Count 7D Avg | 3. Rolling | Average sales per day over the last 7 days | Same window as other 7D Avg measures |
| Companies Visited / Branches / Bankers | 5. Coverage | Number of distinct companies / branches / bankers with activities | DISTINCTCOUNT on Company / Branch / StaffNumber |

Notes: Executed No Sale + Activities With Sales = Executed Activities (HasSale is 1 only when Executed = Yes). Repeat No-Sale Companies counts 'Unknown' as one company if it qualifies, and its result depends on the slicers (period, org); it is not additive across rows. Bankers uses StaffNumber (the banker key) not BankerName, since names vary between rows.

## 6. SVG (Data category = Image URL)

Set Data category to **Image URL** on each measure. measures.dax already does this with `dataCategory: ImageUrl`. Tables and matrices: Format > Image size. New card: Image > fx > field value. Every `#` colour is written as `%23`, and every `%` in a text label is written as `%25` inside the `data:image/svg+xml;utf8,` URI. Palette: #006341 green (good), #B03A2E muted red (bad), #9AA5AB / #5E6A71 / #E6E9EB greys, white and black text. These are all DirectQuery-safe: they are scalar measures over existing measures, and the sparkline sends one query grouped by month.

| Measure | Shows | Driven by | Date | Size |
|---|---|---|---|---|
| SVG Execution Progress | Bar = Execution Rate % (80 px = 100% of plan), black end mark = plan, grey tick = Execution Rate PY, plus a % label | Execution Rate %, Execution Rate PY | Planned | 120x20 |
| SVG Status Pill | **Target = Planned.** Three bands (user decision 2026-11-02): green >= 100% of plan, amber (%23C98A1A, i.e. #C98A1A) >= 90% and < 100%, red < 90%. Cut-offs are `_GreenFrom = 1` and `_AmberFrom = 0.9`. Reads "NN% of plan", rounded down so 99.6% reads 99%. 0% when planned but nothing executed | Execution Rate %, Planned Activities | Planned | 80x20 |
| SVG Bullet Executed vs Planned | Bar = Executed (same three bands as the pill, on Executed / Planned), black line = Planned, grey tick = Executed PY. Scale = largest of the three x 1.1 | Executed Activities, Planned Activities, Executed PY | Planned | 120x20 |
| SVG Bullet Execution Rate vs Plan | Fixed 0-100% scale. Bar = Execution Rate % (same three bands), black line = 100% (plan), grey tick = Execution Rate PY. Compares units of different size fairly | Execution Rate %, Execution Rate PY | Planned | 120x20 |
| SVG Sparkline Executed | Monthly Executed (green) and Not Executed (grey) lines for the months in context that have planned activities | Executed Activities, Not Executed, Planned Activities | Planned | 120x20 |
| SVG Conversion Gauge | PROVISIONAL. Semicircle 0-100%, grey tick = PY | Conversion %, Conversion PY | Planned | 120x70 |
| SVG KPI Arrow Planned MoM | Up arrow green, down red, flat grey dash, plus MoM % | Planned MoM % | Planned | 80x18 |
| SVG KPI Arrow Executed MoM | Same pattern | Executed MoM % | Planned | 80x18 |
| SVG KPI Arrow Sales Count MoM | PROVISIONAL. Same pattern | Sales Count MoM % | Planned | 80x18 |
| SVG KPI Arrow Not Executed MoM | **Reversed:** a rise is red, a fall is green | Not Executed MoM % | Planned | 80x18 |

**Target = Planned** (user decision 2026-11-02, reported via the Data Storyteller): the bullets, pill and progress bar compare against Planned Activities, with PY as a grey tick. There is no separate target table. Not built: SVG Bullet Sales vs PY, because sales have no target.

Note: Executed can never exceed Planned, so green means every planned activity was executed. Amber (90% to under 100%) is the 'on track' band.

## 7. Titles (bind via Format > Title > fx)

| Measure | Text |
|---|---|
| Sel Region | Name of the one selected region, "N regions", or "All regions" |
| Sel Period | "d MMM yyyy - d MMM yyyy" from DimDate when it is filtered, otherwise "All dates" |
| Title - Executed vs PY | Overview V2: "Executed vs not executed by month \| [BU] \| region \| [Branch] \| period" |
| Title - Banker Detail | "Banker: name \| period \| Executed NN.N% of plan (x of y) (+n.n pp vs PY)", where the pp suffix appears only when PY exists; or "no planned activities" |
| Title - Business Unit / Title - Region / Title - Branch / Title - Company | "<Level>: All <level>s / single value / N <level>s \| period \| Executed NN.N% of plan (x of y) (+n.n pp vs PY)". The pp suffix only appears when PY exists; "no planned activities" when Planned is blank. % rounded down |
| Title - Branch Detail | "Branch: name (Region / MicroMarket) \| period \| …" same tail. Region/MicroMarket via SELECTEDVALUE ("multiple …" if a branch spans several) |
| Title - Conversion | PROVISIONAL. Conversion % (pp MoM) - provisional \| region \| period |

## 8. Comparison (Target = Planned; planned date; Executed = "Yes" via the base measures)

| Measure | Purpose / logic |
|---|---|
| Gap to Plan | Activities still missing to reach plan. **Alias `= [Not Executed]`**, so there is one definition and the two can never drift apart. It exists for target wording in visuals |
| Gap to Plan % | DIVIDE(Gap to Plan, Planned) = 1 − Execution Rate % |
| Executed CY vs PY Diff / Planned CY vs PY Diff | Current minus PY (count). Blank when either side is blank (e.g. all of 2025, which has no 2024 data) |
| Executed MoM Diff | Executed minus PM (count). For month axes / the native waterfall |
| Plan Bridge Value | Waterfall helper over disconnected 'Plan Bridge'[Step] (dax/plan_bridge.tmdl): Planned (+), Not Executed (−); Total = Executed |
| SVG Floating Bar Gap to Plan | Green bar to Executed, gap segment Executed→Planned in the three-band colour (as the pill), black plan line, gap count label. 140x20 |
| SVG Dumbbell CY vs PY | Execution Rate PY (grey) → Execution Rate % (banded) on 0–100%, black line = 100% of plan. 120x20 (final; no labels) |
| SVG MoM Change Bar | Diverging bar of Executed MoM Diff. **Level-agnostic scale**: MAXX(ALLSELECTED(level), ABS(diff)) for the level in scope, checked deepest-first via ISINSCOPE: Company, BankerName, Branch, MicroMarket, Region, BusinessUnit. Works with the Level field parameter. With no level in scope (card), the bar is full length. 130x20 |
| Executed MoM Diff Rank (Up) / (Down) | RANKX (DENSE) of Executed MoM Diff, DESC / ASC, over FILTER(ALLSELECTED(level), diff not blank), with the level in scope found deepest-first via ISINSCOPE (same order as SVG MoM Change Bar). Blank when the diff is blank or no level is in scope |
| MoM Top Bottom Flag | 1 if Rank Up <= _N or Rank Down <= _N (`_N = 10`), else 0. Visual-level filter "is 1" |
| MoM Top Bottom Group | "Top 10" / "Bottom 10" for legend or colour rules. Top wins if a row is in both (fewer than 20 rows) |

SVG Dumbbell CY vs PY stays **120 px** wide: it has no text labels (dots and lines only), so nothing can clip.

DirectQuery: the MoM bar runs one grouped query over the visible members of the level in scope; the others are scalar. Bands: `_GreenFrom = 1`, `_AmberFrom = 0.9`, amber %23C98A1A.

## 9. Partial Month & YTD (story/baseline_enhancements.md N1-N8; planned date; sales PROVISIONAL)
- Data Through Date (N1): latest DimDate[ACTUAL_DATE] with planned activities in context (LASTNONBLANK). Note: if future-dated plans exist, this is a future date; QA in Power BI.
- Is Partial Month (N2): TRUE when the month in context runs past the overall Data Through Date (date filters removed). Use for lighter shading of the partial month.
- Executed / Planned / Sales Count PM Same Days (N3): previous month, days 1..DAY(cut-off). Cut-off = Data Through Date in a partial month, else month end; capped at the previous month's end (e.g. 31 Mar compares to 1-28/29 Feb). Needs one month in context (HASONEVALUE YEAR_MONTH_KEY), else blank.
- Executed / Planned / Sales Count MoM % Like-for-Like (N4): DIVIDE ( current - PM Same Days, PM Same Days ). Arrows: SVG KPI Arrow Executed MoM LfL, SVG KPI Arrow Planned MoM LfL, SVG KPI Arrow Sales Count MoM LfL (folder 6. SVG, 80x18, same style as the MoM arrows).
- Low Volume Flag (N5): 1 when Planned Activities < _MinPlanned (PLACEHOLDER 20), else 0. For ROUTE 99: visual/page filter, grey-out or sort-last.
- Executed / Planned / Sales Count YTD (N7): DATESYTD on DimDate[ACTUAL_DATE].
- Partial Month Label (N8): "Month to date, through 14 Oct" when partial, blank otherwise.
- NOT WRITTEN: Avg Executed Activities with Sales (N6), definition pending (open question #16).
- SVG KPI Arrow Gap to Plan (folder 6. SVG): uses Not Executed MoM % (Gap to Plan = Not Executed), REVERSED colours: rise red, drop green.
- Executed measures here use the planned date like Executed PM / Executed MoM %. Exec-date variants (USERELATIONSHIP) can be added if the date-axis answer (#3) asks for it.

## Field parameters (dax/field_parameters.tmdl)

- **Metric:** Planned Activities, Executed Activities, Not Executed, Execution Rate %, Conversion % (provisional), Executed No Sale (provisional).
- **Level:** Business Unit (BusinessUnit), Region, MicroMarket, Branch, Banker (BankerName), Company.
- Each one is an Import calculated table with columns: label, hidden `… Fields` (NAMEOF, with `ParameterMetadata` extendedProperty kind 2), and hidden `… Order` (ordinal, used to sort).
- Use: put `Metric` on a slicer and on a visual's Y axis, and `Level` on the axis or rows.
- Mixed formats: count measures and % measures share one axis when Metric is used. Prefer single-select on the Metric slicer.
- UI fallback: Modeling > New parameter > Fields (see the file header).

## Glossary additions to paste
- Execution Rate %: Share of planned activities that were carried out — Executed Activities ÷ Planned Activities, planned date.
- Conversion % (provisional): Share of executed activities that produced at least one sale.
- ... YoY %: Change versus same period last year — (selected period − last year) / last year.
- Executed No Sale: Executed activities that produced no sale.
- Repeat No-Sale Companies: Companies visited more than once in the selected period with no sale on any visit.
- ... YoY pp / MoM pp: Change in a percentage, in percentage points.
- ... 7D Avg: Average per day over the last 7 days ending on the date shown.

- Data Through Date: the latest date with planned activities; the partial-month label reads "Month to date, through dd Mmm".
- ... Like-for-Like: month to date compared with the same days of the previous month.
- ... YTD: from 1 January to the end of the selected period.

## DirectQuery notes
Simple aggregations + filters on int columns fold to SQL. Time intelligence runs on DimDate (Dual), so date shifts resolve locally and send key lists to SQL. No FILTER(MPO) iteration or row-level SUMX over the fact. Check with Performance Analyzer.

## 10. L12M (rolling last 12 months, BU page)
- Table `'L12M Axis'` (dax/l12m_axis.tmdl): a disconnected, Import calculated table built from DimDate months. Columns: Month Start, Month Label ("Aug 2026", sorted by Month Sort Key), Month Sort Key (yyyymm, hidden). It has no relationships. Fallback: the same 3 columns as an Import Power Query table.
- `L12M Selected Month End`: the end of the latest selected DimDate month. With no date filter it uses the end of the month of [Data Through Date].
- `L12M Visible Flag`: 1 when the axis month falls in the 12 months ending at the selected month.
- `L12M Planned`, `L12M Executed` (executed date, USERELATIONSHIP on ExecutedDateKey), `L12M Activities With Sales` (PROVISIONAL, planned date): REMOVEFILTERS(DimDate), then the axis month as a DATESBETWEEN range. Blank outside the window.
- `L12M Bar Colour`: #006341 for the selected month, #A6A6A6 for the others (fx > Field value).
- Example: with Aug 2026 selected, the bars run Sep 2025 to Aug 2026.
