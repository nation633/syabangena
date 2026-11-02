# GTM Dashboard - Build checklist (Power BI Desktop)
Follow layout_spec.md for exact fields and x/y/w/h. Mockups in mockups/ use EXAMPLE DATA only.

## 0. Prerequisites
- [ ] Model built per model_design.md (MPO DirectQuery, DimDate Dual marked as date table on ACTUAL_DATE, Product disconnected).
- [ ] Measures pasted from dax/measures.dax (table MPO), display folders visible.
- [ ] Sort columns: MONTH_NAME by MONTH; DAY_SHORT_NAME and DAY_NAME by DAY_IN_WEEK.
- [ ] Hide technical columns (ActivityId, DateKey, ExecutedDateKey, IsExecuted, HasSale, 10 product columns, TotalSaleCount, Product[ProductColumn]).

## 0b. SVG image measures and field parameters
- [ ] Confirm the folder 6. SVG and 7. Titles measures are in dax/measures.dax (accepted by the DAX Analyst 13:10 SAST). All four are now in measures.dax (re-checked 13:16 SAST): [SVG Bullet Executed vs Planned], [SVG Bullet Execution Rate vs Plan], revised [SVG Execution Progress], revised [SVG Status Pill]. Build all SVG columns.
- [ ] For EACH SVG measure ([SVG Execution Progress], [SVG Status Pill], [SVG Bullet Executed vs Planned], [SVG Bullet Execution Rate vs Plan], [SVG Sparkline Executed], [SVG Conversion Gauge], [SVG KPI Arrow Planned MoM], [SVG KPI Arrow Executed MoM], [SVG KPI Arrow Not Executed MoM], [SVG KPI Arrow Sales Count MoM]): select it in the Data pane > Measure tools > Data category = **Image URL** (measures.dax already sets dataCategory: ImageUrl; check it survived the paste).
- [ ] Paste dax/field_parameters.tmdl in TMDL view (tables Metric and Level). Check sort by 'Metric Order' / 'Level Order'.

## 1. Theme and canvas
- [ ] View > Themes > Browse for themes > /workspace/corporate-theme/CorporateGreen.json.
- [ ] For each page: Format page > Canvas settings > Type 16:9 (1280 x 720); View > Page view > Fit to page.
- [ ] Format page > Canvas background > Image > viz/backgrounds/<NN_Page>.png, Image fit = Fit, Transparency 0%. Wallpaper #F4F6F7.

## 2. Pages (create in order, rename tabs)
- [ ] Story order: 01 Exec Overview, 02 Business Unit, 03 Region, 04 Branch, 05 Banker (Individual), 05a Banker Detail (hide), 06 Product (PROVISIONAL), 07 Company; supporting S1 Daily, S2 Glossary; hidden TT Branch, TT Banker; optional Branch Detail (hide).
- [ ] Add the 'Next >' button (1168,12,52,32) on each story page: Action Page navigation to the next page (Company -> Daily).

## 3. Slicers (first page, then copy/paste + sync)
- [ ] Build one dropdown slicer, Arial 10, padding 0, Apply button on; copy for Year, Month, BU, Region, Branch.
- [ ] Place at the spec positions (y 64, h 40).
- [ ] Copy to pages 2-7 > choose "Sync" when prompted. View > Sync slicers: per spec (Company on 6 only; Day on 7 only; Product Group/Product on 3 only).

## 4. Visuals per page
- [ ] Add each visual from layout_spec.md, set Format > General > Properties size and position exactly.
- [ ] Titles as in spec, padding 0, borders off, data labels Arial 10 black.
- [ ] Series colours (up/positive #006341, never #00A651): Executed #006341, Not Executed #9AA5AB, Planned #C8D1D6, with sales #7AB800, PY dashed #5E6A71.
- [ ] Exec Overview funnel: add measures as separate Values (one per stage).
- [ ] KPI cards: new Card visual, add reference labels for PY and MoM per spec; conditional colour (green up / red down, reversed for Not Executed).
- [ ] Execution V4, Company V1, Ribbon: Filters pane > Top N per spec.
- [ ] Daily heatmap: Matrix, rows WEEK, columns DAY_SHORT_NAME; Cell elements > Background colour gradient white -> #006341; turn off row/column subtotals.
- [ ] Product V2/V3: add "PROVISIONAL - pending product mapping" title suffix; leave placeholder text box until Sales Count (Product) is active.
- [ ] Business Unit V4 (rolling last 12 months, replaces the MoM chart): first add table 'L12M Axis' from dax/l12m_axis.tmdl (calculated, Import; NO relationships; Month Label sort by column = Month Sort Key, Month Sort Key hidden). Clustered column chart: X = 'L12M Axis'[Month Label] (field, not a date hierarchy; drill/expand off), sort axis by Month Sort Key ascending; Y = [L12M Planned], [L12M Executed], [L12M Activities With Sales] (label '(provisional)'); visual-level filter [L12M Visible Flag] is 1; Format > Columns > Colour > fx > Field value = [L12M Bar Colour] for each series. Month slicer stays on DimDate[MONTH_NAME]. V2/V3 narrowed to 400 w.
- [ ] Business Unit decomposition tree: Analyze Metric[Metric] (default Not Executed), explain-by fields in BU > Region > MicroMarket > Branch > BankerName order.

## 4b. SVG placements
- [ ] Every table/matrix with SVG columns (Exec Overview V4T, Business Unit V1, Region V3, Branch V4T, Banker V4, Banker Detail V3, Company V1): Format > Grid > Image size H 20, W 120; column widths bullet/progress/sparkline 130, pill 86 (pill image 80x20); headers white on #006341.
- [ ] Exec Overview K1-K3, K5: card image = [SVG KPI Arrow Planned MoM] / [SVG KPI Arrow Executed MoM] / [SVG KPI Arrow Not Executed MoM] / [SVG KPI Arrow Sales Count MoM] (provisional). K4: [SVG Bullet Execution Rate vs Plan] + [SVG Status Pill] (two images, or one image + reference-label image).
- [ ] Business Unit V1 matrix: rows BusinessUnit > Region, columns Planned, Executed, Not Executed, [SVG Bullet Executed vs Planned], [SVG Status Pill], [SVG Sparkline Executed].
- [ ] Region: Level slicer (single select, default Region, show only Region / MicroMarket); V2 bar Y = Level[Level]; V3 table Level[Level] + counts + [SVG Bullet Executed vs Planned], pill, sparkline.
- [ ] Branch V4T: progress, pill, sparkline, [SVG Bullet Executed vs Planned]. Banker V4: [SVG Bullet Execution Rate vs Plan], pill, sparkline.
- [ ] Banker Detail V3: [SVG Status Pill] and [Executed No Sale] as separate columns; no gauge. Bind V1 title to [Title - Banker Detail].
- [ ] Title bindings (Format > Title > fx > Format style: Field value): Business Unit V1 = [Title - Business Unit]; Region V3 = [Title - Region]; Branch V4 and V4T = [Title - Branch]; Company V1 = [Title - Company]; Branch Detail V1 (optional page) = [Title - Branch Detail].
- [ ] 8. Comparison measures (final, untested): confirm [Gap to Plan], [Gap to Plan %], [Executed CY vs PY Diff], [Planned CY vs PY Diff], [Executed MoM Diff], [Plan Bridge Value], [SVG Floating Bar Gap to Plan], [SVG Dumbbell CY vs PY], [SVG MoM Change Bar] are in the model.
- [ ] Set Data category = Image URL on [SVG Floating Bar Gap to Plan], [SVG Dumbbell CY vs PY], [SVG MoM Change Bar] (and all other SVG measures). Column widths: floating gap 146 (image 140), MoM change bar 136 (image 130), dumbbell 126 (image 120, final).
- [ ] Plan Bridge table: add dax/plan_bridge.tmdl (disconnected, no relationships). Column tools: Step > Sort by column = Order; hide Order.
- [ ] Waterfalls Exec V1 / Banker Detail V4: Category 'Plan Bridge'[Step]; Y [Plan Bridge Value]; Format > Columns: increase #006341, decrease #9AA5AB, total #006341; Total on, Total label renamed 'Executed'.
- [ ] MoM waterfalls Exec V8 / Banker Detail V5: Category DimDate[YEAR_MONTH_KEY]; Y [Executed MoM Diff]; increase #006341, decrease #B03A2E; total off.
- [ ] Exec K6 Gap to Plan card (616,116,192,100): value [Gap to Plan], reference [Gap to Plan %], image [SVG Floating Bar Gap to Plan]. K1-K3/K5 now 192 wide, K4 248 (see spec x).
- [ ] Gap columns: BU V1 add [Gap to Plan], floating gap, dumbbell; Branch V4T add floating gap, MoM change bar, [Executed MoM Diff]; Banker V4 add dumbbell, floating gap; Banker Detail V3 add floating gap; Company V1T floating gap + pill.
- [ ] Stacked Executed + [Gap to Plan] bars (#006341 / #9AA5AB): Region V2 (Level parameter), Banker V1, Company V1. Company Chart/Table bookmarks (optional V1T).
- [ ] Branch V5 (single visual): Y MPO[Branch]; X [Executed MoM Diff]; visual-level filter [MoM Top Bottom Flag] is 1; Bars > Colour fx by field [MoM Top Bottom Group] rules: 'Top 10' #006341, 'Bottom 10' #B03A2E; sort [Executed MoM Diff] descending. Ranks work at any level; blank changes are excluded; fewer than 20 rows can put a row in both groups, shown as Top.
- [ ] Footnote on BU V1 and Banker V4: 'PY comparison blank for 2025 (no 2024 data)'.
- [ ] Pill legend: under each table/matrix with a pill add a text box (Arial 10 black, 0 padding): 'Pill: green >= 100% of plan | amber 90% to under 100% | red below 90%'. Same line on the Glossary page.
- [ ] Company V1 table: Executed / Not Executed data bars + [SVG Status Pill]. K1 card [Repeat No-Sale Companies].
- [ ] Product G1: [SVG Conversion Gauge] (provisional), V1 title [Title - Conversion]. Exec Overview V2 title [Title - Executed vs PY].
- [ ] Chart/Table bookmarks: BM Exec - Chart/Table (Exec Overview), BM Branch - Chart/Table (Branch).
- [ ] Business Unit: Metric slicer single select, default Not Executed, in decomposition tree Analyze.

## 5. Tooltip and drill-through pages
- [ ] TT Branch / TT Banker: add the [SVG Sparkline Executed] image (table with one column, image size 300x110) at 8,72,304,130.
- [ ] TT Branch / TT Banker: Page information > Allow use as tooltip; Canvas type Tooltip (320 x 240); add tooltip field MPO[Branch] / MPO[BankerName].
- [ ] Set Format > Tooltips > Type Report page on the visuals listed in the spec.
- [ ] Banker Detail: Drill through > add MPO[BankerName], Keep all filters On; add Back button (1224,64,40,40).

## 6. Interactions
- [ ] Format > Edit interactions: Exec Overview funnel -> None; BU bar V5 filters page; Region V2 filters V1/V3; rest default cross-filter.

## 7. Buttons and bookmarks
- [ ] Insert > Buttons > Information on every page (1224,12,40,32), Action Page navigation > Glossary, tooltip "How to read this page". Icon white on header.
- [ ] Reset button (1224,64,40,40) per page; create bookmark "BM Reset - <page>" with slicers cleared (Data, Current page, uncheck Display); link via Action > Bookmark.
- [ ] Glossary: Back button (1224,12,40,32).

## 8. Glossary page
- [ ] Paste text from glossary_page.md and measures_guide.md "Glossary additions" into the 3 text boxes (headers white on #006341).

## 9. QA
- [ ] Not Executed visible on every story page and Daily.
- [ ] QA: the 5 new title measures have not been tested in Power BI. Check that each title updates with slicers/drill-through and shows no blank or error text.
- [ ] QA (8. Comparison, untested in Power BI): waterfall steps read Planned > Not Executed > Executed in Order and total = [Executed Activities]; MoM waterfall sums match month changes; floating, dumbbell and MoM SVGs render at 140/120/130 px with no cropping; MoM bar scales correctly at Branch and at every Level parameter item; CY vs PY measures blank for 2025 and populated for 2026; [Gap to Plan] = [Not Executed]; all new visuals cross-filter. Rank measures (untested): Branch V5 shows 10 green + 10 red bars, sorted desc, no blanks; check with < 20 branches (overlap shows as Top) and at another level.
- [ ] QA (10. L12M, untested in Power BI): Aug 2026 selected shows exactly 12 columns Sep 2025-Aug 2026 in date order (not alphabetical); nothing selected ends at the latest month with data ([L12M Selected Month End] / Data Through Date); Aug 2026 bars #006341, others #A6A6A6; changing Year/Month on DimDate moves the window; BU/Region/Branch slicers filter the bars; L12M Executed matches [Executed Activities] for the same month on a DimDate visual (exec date via USERELATIONSHIP) and L12M Planned matches [Planned Activities]; a month with no planned shows a gap, not a missing axis month; Performance Analyzer < 5 s.
- [ ] L12M Bar Colour applies one colour per month to all three series, so series are told apart only by order/legend; if that is unreadable, ask the user whether to keep per-series colours and highlight the selected month another way.
- [ ] Pills show three colours: #006341 (>= 100%), #C98A1A (90-<100%), #B03A2E (< 90%).
- [ ] Every SVG visual renders (Image URL category set) and nothing shows a bullet column.
- [ ] Optional items (Branch Detail, Level parameter, smart narrative) only if the user wants them.
- [ ] Every number is a count, sum or % of counts (no rand values).
- [ ] No bank name in titles, text boxes, file names or page names.
- [ ] Performance Analyzer: each page < 5 s in DirectQuery; reduce Top N if slow.
- [ ] Compare each page against mockups/ (layout only - EXAMPLE DATA).
