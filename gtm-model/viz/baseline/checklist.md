# Baseline enhancement build checklist (2026-11-02)
Work on a COPY of the .pbix. Do not rebuild pages.
## Before
- [ ] Theme/look unchanged (#006341 / #7AB800 / #9AA5AB, Arial 10, white-on-green headers).
- [ ] All SVG measures: Data category = Image URL.
- [ ] Confirm ROUTE 99 column (BU or Region).
## Global
- [ ] Interim "partial month: MoM % is not like-for-like" note on Exec, BU, Region.
- [ ] Labels: Executed only; display units K, 0 dp; secondary 9pt grey.
- [ ] ROUTE 99 page filter + "Show low-volume units" bookmark.
- [ ] Partial-month subtitle = [Partial Month Label] (fx amber when [Is Partial Month] = 1); Nov light shade = column fx on [Is Partial Month] (Exec Overview, Region). BU page uses [Anchor Partial Month Label] / [Anchor Data Through Date] / [Anchor Is Partial Month]. Still PENDING here: N3/N4 like-for-like deltas, N5 grey-out (not in scope of this update).
## Exec Overview
- [ ] KPI arrows (4 SVGs). Gap to Plan card: arrow DOWN shows GREEN #006341 (test with a month where gap fell).
- [ ] Execution Rate card: bullet + pill.
- [ ] BU matrix 4 SVG columns.
- [ ] Plan Bridge waterfall (Step sorted by Order; total "Executed"); MoM waterfall; 7D Avg line on Daily.
## Business Unit
- [ ] Cards relabelled (PENDING N7 for YTD).
- [ ] Donut → stacked with-sale/no-sale bar.
- [ ] BU table 8 columns, Anchor versions (see enhancement_spec 02); title fx Anchor Title - Business Unit; split bars Anchor Activities With Sales + Anchor Executed No Sale (prov.); circles Anchor Executed / Anchor Activities With Sales / Anchor Conversion % (prov.), single label; remove the Dim_Date Day slicer; PY footnote.
## Region
- [ ] Executed + Gap to Plan (grey) stacked bar.
- [ ] Sales donut → 100% stacked (or MoM Diff waterfall).
- [ ] Product matrix: progress column + data bars.
- [ ] Region table + Top/Bottom 10 filter; Title - Region; drill to MicroMarket > Branch.
## QA
- [ ] Slicer changes move all SVGs; CY vs PY blank for 2025 (no 2024 data) footnoted.
- [ ] No bank name anywhere; nothing pushed to GitHub.
- [ ] Page cleanup only after user confirms the tab list.


- [ ] Business Unit (L12M rework, see enhancement_spec 02): add 'Month Anchor' + 'L12M Axis' from dax/l12m_measures.dax (no relationships; ignore superseded l12m_axis.tmdl); swap Year/Month slicers to Month Anchor (single select) - NOT synced with Dim_Date slicers on other pages; KPI cards = 6 Anchor measures; chart X Axis Label, tooltip L12M Month Label, filter L12M Visible Flag = 1, title fx L12M Title, per-series colour fx (Planned/Executed/Sales). Use only the per-series colour measures above.
- [ ] QA (untested in Power BI): 2026 + Aug -> 12 columns Sep..Aug chronological, Aug darker in all 3 series; tooltip shows year; window-edge duplicate month names stay separate; nothing selected ends at latest data month; cards match Dim_Date measures for Aug 2026 elsewhere; BU-page month does not affect other pages; BU slicer filters cards and chart.
- [ ] QA (Anchor visuals, untested in Power BI): (1) Year only selected (no month) -> cards, V1, tables and chart end at the latest month with data in that year; (2) nothing selected -> latest month with data; (3) (main page) V3 small multiples show exactly 12 months (Anchor L12M Window Flag) matching the chart window; (4) every Anchor card/matrix/table total equals the chart's last (selected) bar for Planned, Executed and Activities With Sales; (5) PY values (Anchor Execution Rate YoY pp, Anchor SVG Dumbbell CY vs PY, Anchor Executed CY vs PY Diff) are blank for 2025 - footnote 'PY comparison blank for 2025 (no 2024 data)' present; (7) no Dim_Date Day slicer on the BU page.
- [ ] No Dim_Date slicer on the BU page (Year/Month = 'Month Anchor', no Day).
- [ ] QA partial month (untested in Power BI): with Nov 2026 partial, subtitle reads data-through date and is amber; Nov columns light on Exec Overview/Region, earlier months full colour; complete month -> no amber/shade. BU banner follows the anchor month (Aug 2026 complete -> no partial flag; anchor = latest partial month -> partial text).
- [ ] QA Anchor L12M Window Flag (rewritten): V3 / any Dim_Date-month visual shows 12 single months ending at the anchor month; TOTAL rows return 0, so a visual filter "is 1" hides totals/subtotals - turn totals off or expect them blank; a visual without a Dim_Date month on rows shows nothing.
