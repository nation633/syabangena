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
- [ ] PENDING N1/N2/N8 subtitle; N2 partial shading; N3/N4 like-for-like deltas; N5 grey-out.
## Exec Overview
- [ ] KPI arrows (4 SVGs). Gap to Plan card: arrow DOWN shows GREEN #006341 (test with a month where gap fell).
- [ ] Execution Rate card: bullet + pill.
- [ ] BU matrix 4 SVG columns.
- [ ] Plan Bridge waterfall (Step sorted by Order; total "Executed"); MoM waterfall; 7D Avg line on Daily.
## Business Unit
- [ ] Cards relabelled (PENDING N7 for YTD).
- [ ] Donut → stacked with-sale/no-sale bar.
- [ ] BU table 8 columns; title Title - Business Unit; circles single label.
## Region
- [ ] Executed + Gap to Plan (grey) stacked bar.
- [ ] Sales donut → 100% stacked (or MoM Diff waterfall).
- [ ] Product matrix: progress column + data bars.
- [ ] Region table + Top/Bottom 10 filter; Title - Region; drill to MicroMarket > Branch.
## QA
- [ ] Slicer changes move all SVGs; CY vs PY blank for 2025 (no 2024 data) footnoted.
- [ ] No bank name anywhere; nothing pushed to GitHub.
- [ ] Page cleanup only after user confirms the tab list.


- [ ] Business Unit (L12M rework, see enhancement_spec 02): add 'Month Anchor' + 'L12M Axis' from dax/l12m_measures.dax (no relationships; ignore superseded l12m_axis.tmdl); swap Year/Month slicers to Month Anchor (single select) - NOT synced with DimDate slicers on other pages; KPI cards = 6 Anchor measures; chart X Axis Label, tooltip L12M Month Label, filter L12M Visible Flag = 1, title fx L12M Title, per-series colour fx (Planned/Executed/Sales). Use only the per-series colour measures above.
- [ ] QA (untested in Power BI): 2026 + Aug -> 12 columns Sep..Aug chronological, Aug darker in all 3 series; tooltip shows year; window-edge duplicate month names stay separate; nothing selected ends at latest data month; cards match DimDate measures for Aug 2026 elsewhere; BU-page month does not affect other pages; BU slicer filters cards and chart.
