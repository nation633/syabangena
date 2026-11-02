# Visual 01 - Last 12 Months clustered column (Business Unit page)

_Status: DAX final, untested in Power BI. Counts only (no rand values). Last reviewed 2026-11-02._

## 1. Purpose and story question

**Question:** *Over the last 12 months up to the month I picked, how many activities did we plan, and how many did we execute?*

It replaces the old MoM chart on the BU page. Planned = target. The gap between the two bars in a month is the visible **non-executed** volume. Story position: Exec > **BU** (this visual) > Region > Branch > Individual > Product > Company.

Example: select **2026 / Aug** and the axis shows Sep, Oct, Nov, Dec, Jan ... Jul, **Aug** (Sep 2025 to Aug 2026), with Aug last and highlighted.

## 2. Model objects used

| Object | Type | Role |
|---|---|---|
| `Month Anchor` | Calculated table, disconnected | Year and Month slicers |
| `L12M Axis` | Calculated table, disconnected | Chart X axis (`Axis Label`) |
| `Dim_Date` | Date dimension | `ACTUAL_DATE`, `DATE_KEY`, `YEAR`, `MONTH` |
| `MPO` | Fact | `ActivityId`, `Executed` ("Yes"/"No"), `DateKey` (active, planned), `ExecutedDateKey` (inactive) |
| `_mymeasures` | Measures home table | All measures below, folder `10. L12M` |

Both new tables have **no relationships**. That is deliberate: a slicer on `Month Anchor` would otherwise cut the axis down to one month.

## 3. Build steps in Power BI Desktop

1. **Modeling > New table** and paste `Month Anchor` (section 4). Select `Month Short` and set **Sort by column = Month Number**. Hide `Month Number` and `Month Sort Key`.
2. **Modeling > New table** and paste `L12M Axis`. Select `Axis Label` and set **Sort by column = Month Sort Key**. Hide `Month Start` and `Month Sort Key`.
3. Model view: confirm that neither table has a relationship. Delete any auto-detected one.
4. In `_mymeasures`, create the measures in section 5 (base measures from section 6 should already exist in `measures.dax`).
5. Slicers: add a slicer on `'Month Anchor'[Year]` and one on `'Month Anchor'[Month Short]`. For both, **Format > Slicer settings > Selection > Single select = On**. Don't sync them with any Dim_Date slicer.
6. Insert a **Clustered column chart**:
   - **X-axis:** `'L12M Axis'[Axis Label]`. Use the field itself, not a date hierarchy, and turn drill off.
   - **Y-axis:** `[L12M Planned]` first, then `[L12M Executed]`.
   - **Legend:** leave empty. The two measures are the series (Planned, Executed).
   - **Tooltips:** `[L12M Month Label]` (and optionally `[L12M Position]` for QA).
   - **Filters on this visual:** `[L12M Visible Flag]` **is 1**.
   - **Sort:** More options (...) > Sort axis > `Axis Label`, **ascending**. Because of the sort-by column, this sorts chronologically.
   - **Title:** Format > Title > fx > Field value = `[L12M Title]`.
7. Rename the series in the visual (double-click in the Y well) to **Planned** and **Executed**.
8. Optional third series `[L12M Activities With Sales]` is **PROVISIONAL** (sales definition is still open). Leave it off until it is confirmed.

## 4. Calculated tables (full DAX)

### Month Anchor
```DAX
Month Anchor =
VAR _Months =
    DISTINCT (
        SELECTCOLUMNS (
            Dim_Date,
            "Month Start", DATE ( YEAR ( Dim_Date[ACTUAL_DATE] ), MONTH ( Dim_Date[ACTUAL_DATE] ), 1 )
        )
    )
VAR _TodayIdx = YEAR ( TODAY () ) * 12 + MONTH ( TODAY () )
RETURN
    ADDCOLUMNS (
        _Months,
        "Year", YEAR ( [Month Start] ),
        "Month Number", MONTH ( [Month Start] ),
        "Month Short", FORMAT ( [Month Start], "mmm" ),
        "Month Sort Key", YEAR ( [Month Start] ) * 100 + MONTH ( [Month Start] ),
        "Relative Month Index", YEAR ( [Month Start] ) * 12 + MONTH ( [Month Start] ) - _TodayIdx
    )
```

One row per month found in Dim_Date. `Month Start` is the 1st of the month. `Year` and `Month Short` ("Aug") are the slicer fields. `Month Number` is the sort for Month Short. `Month Sort Key` is YYYYMM. `Relative Month Index` = months from the current month at refresh (0 = this month, -1 = last month) and can be used for a default-relative filter.

### L12M Axis
```DAX
L12M Axis =
VAR _Months =
    DISTINCT (
        SELECTCOLUMNS (
            Dim_Date,
            "Month Start", DATE ( YEAR ( Dim_Date[ACTUAL_DATE] ), MONTH ( Dim_Date[ACTUAL_DATE] ), 1 )
        )
    )
VAR _FirstYear = MINX ( _Months, YEAR ( [Month Start] ) )
RETURN
    ADDCOLUMNS (
        _Months,
        "Month Sort Key", YEAR ( [Month Start] ) * 100 + MONTH ( [Month Start] ),
        "Axis Label",
            FORMAT ( [Month Start], "mmm" )
                & REPT ( UNICHAR ( 8203 ), YEAR ( [Month Start] ) - _FirstYear )
    )
```

This is a separate copy of the months for the axis. `Axis Label` is the month name plus N invisible zero-width spaces (UNICHAR 8203), where N = years after the first year in Dim_Date. "Aug" 2025 and "Aug" 2026 then look the same but are different values, so each label maps to exactly one `Month Sort Key` and the sort works. The axis shows month names only, with no year.

## 5. Measures used by the chart (full DAX, table `_mymeasures`, folder `10. L12M`)

### L12M Latest Data Month
```DAX
measure 'L12M Latest Data Month' =
// 2026-11-02 visual 01 review: capped at TODAY() so future-planned activities cannot push the default window past the current month.
VAR _Through = CALCULATE ( [Data Through Date], REMOVEFILTERS ( Dim_Date ) )
VAR _Capped  = IF ( NOT ISBLANK ( _Through ), MIN ( _Through, TODAY () ) )
RETURN
    IF ( NOT ISBLANK ( _Capped ), DATE ( YEAR ( _Capped ), MONTH ( _Capped ), 1 ) )
```
The default anchor: the first day of the latest month that has planned activities, capped at the current month so future-planned work can't push the window forward. It ignores every date filter.

### L12M Selected Month
```DAX
measure 'L12M Selected Month' =
VAR _Latest = [L12M Latest Data Month]
VAR _SelUpToLatest =
    CALCULATE ( MAX ( 'Month Anchor'[Month Start] ), KEEPFILTERS ( 'Month Anchor'[Month Start] <= _Latest ) )
RETURN
    IF (
        ISFILTERED ( 'Month Anchor' ),
        COALESCE ( _SelUpToLatest, MAX ( 'Month Anchor'[Month Start] ) ),
        _Latest
    )
```
The month the chart ends on. Year + Month picked gives that month. Month only (e.g. "Dec") gives the latest Dec up to the latest data month. Year only gives the latest data month in that year. Nothing picked gives L12M Latest Data Month.

### L12M Visible Flag
```DAX
measure 'L12M Visible Flag' =
VAR _Sel   = [L12M Selected Month]
VAR _Start = EDATE ( _Sel, -11 )
VAR _Axis  = SELECTEDVALUE ( 'L12M Axis'[Month Start] )
RETURN
    IF ( NOT ISBLANK ( _Axis ) && _Axis >= _Start && _Axis <= _Sel, 1, 0 )
```
Returns 1 for the 12 axis months from Selected Month minus 11 to Selected Month, else 0. It is the visual-level filter.

### L12M Planned
```DAX
measure 'L12M Planned' =
VAR _Axis = SELECTEDVALUE ( 'L12M Axis'[Month Start] )
RETURN
    IF (
        [L12M Visible Flag] = 1,
        CALCULATE (
            [Planned Activities],
            REMOVEFILTERS ( Dim_Date ),
            DATESBETWEEN ( Dim_Date[ACTUAL_DATE], _Axis, EOMONTH ( _Axis, 0 ) )
        )
    )
```
Planned activities (distinct ActivityId) for the axis month, by planned date (active relationship). Blank outside the window.

### L12M Executed
```DAX
measure 'L12M Executed' =
// 2026-11-02 visual 01 review: reuses [Executed (Exec Date)] so the USERELATIONSHIP lives in one place.
VAR _Axis = SELECTEDVALUE ( 'L12M Axis'[Month Start] )
RETURN
    IF (
        [L12M Visible Flag] = 1,
        CALCULATE (
            [Executed (Exec Date)],
            REMOVEFILTERS ( Dim_Date ),
            DATESBETWEEN ( Dim_Date[ACTUAL_DATE], _Axis, EOMONTH ( _Axis, 0 ) )
        )
    )
```
Executed activities (Executed = "Yes") for the axis month, by executed date (inactive ExecutedDateKey relationship via USERELATIONSHIP). Blank outside the window.

### L12M Is Selected Month
```DAX
measure 'L12M Is Selected Month' =
VAR _Axis = SELECTEDVALUE ( 'L12M Axis'[Month Start] )
VAR _Sel  = [L12M Selected Month]
RETURN
    IF ( NOT ISBLANK ( _Axis ) && NOT ISBLANK ( _Sel ) && _Axis = _Sel, 1, 0 )   -- guard: blank = blank must not count as selected
```
Returns 1 only on the last bar (the selected month). It drives the highlight colours.

### L12M Bar Colour Planned
```DAX
measure 'L12M Bar Colour Planned' =
IF ( [L12M Is Selected Month] = 1, "#99C2B3", "#D6E8E0" )
```
Planned series colour: pale green #D6E8E0, or #99C2B3 on the selected month.

### L12M Bar Colour Executed
```DAX
measure 'L12M Bar Colour Executed' =
IF ( [L12M Is Selected Month] = 1, "#006341", "#7FB19F" )
```
Executed series colour: #7FB19F, or full corporate green #006341 on the selected month.

### L12M Month Label
```DAX
measure 'L12M Month Label' =
VAR _Axis = SELECTEDVALUE ( 'L12M Axis'[Month Start] )
RETURN
    IF ( [L12M Visible Flag] = 1, FORMAT ( _Axis, "mmm yyyy" ) )
```
Tooltip text with the year, e.g. "Aug 2026" (the axis itself shows only "Aug").

### L12M Title
```DAX
measure 'L12M Title' =
VAR _Sel = [L12M Selected Month]
RETURN
    "Last 12 months: " & FORMAT ( EDATE ( _Sel, -11 ), "mmm yyyy" ) & " - " & FORMAT ( _Sel, "mmm yyyy" )
```
Dynamic title, e.g. "Last 12 months: Sep 2025 - Aug 2026".

### L12M Position
```DAX
measure 'L12M Position' =
VAR _Sel  = [L12M Selected Month]
VAR _Axis = SELECTEDVALUE ( 'L12M Axis'[Month Start] )
VAR _Pos  = 12 - ( ( YEAR ( _Sel ) * 12 + MONTH ( _Sel ) ) - ( YEAR ( _Axis ) * 12 + MONTH ( _Axis ) ) )
RETURN
    IF ( [L12M Visible Flag] = 1, _Pos )
```
QA/tooltip helper: 1 to 12, where 12 is the selected month.

## 6. Base measures it depends on (from dax/measures.dax)

### Planned Activities
```DAX
Planned Activities =
DISTINCTCOUNT ( MPO[ActivityId] )
```
Distinct activities. Follows the **active planned-date** relationship.

### Executed Activities
```DAX
Executed Activities =
CALCULATE (
    DISTINCTCOUNT ( MPO[ActivityId] ),
    KEEPFILTERS ( MPO[Executed] = "Yes" )
)
```
Distinct activities where `MPO[Executed] = "Yes"`. On its own it follows the planned date.

### Executed (Exec Date)
```DAX
Executed (Exec Date) =
CALCULATE (
    [Executed Activities],
    USERELATIONSHIP ( Dim_Date[DATE_KEY], MPO[ExecutedDateKey] )
)
```
Same count, placed on the **executed date** through the inactive `ExecutedDateKey` relationship.

### Data Through Date
```DAX
Data Through Date =
LASTNONBLANK ( Dim_Date[ACTUAL_DATE], [Planned Activities] )
```
Latest date with planned activities. It uses planned dates, so it can be in the future; L12M Latest Data Month caps it at today.

## 7. Formatting
- Font: **Arial 10** everywhere (title, axis, legend, data labels). Text is black (#000000).
- Padding: visual **inner and outer padding = 0**. Background white, no border/shadow, nothing neon.
- Data labels: On, black, Arial 10, display units None, `#,0` (counts only).
- Gridlines: light (#E6E6E6) or off. Legend at the top left: Planned, Executed.
- **Colours** (Columns > Colors > choose each series > fx > Format style **Field value**):
  - Planned -> `[L12M Bar Colour Planned]`: #D6E8E0, selected month #99C2B3.
  - Executed -> `[L12M Bar Colour Executed]`: #7FB19F, selected month **#006341**.
  - So the last bar pair (selected month) is visibly darker.
- **Caveat:** fx (Field value) colour isn't available, or is ignored, on some multi-series column charts and in older Desktop versions. In that case the fx button doesn't appear for each series, or all bars show one colour.
  - **Fallback A:** use static colours, Planned #99C2B3 and Executed #006341, and show the selection through the title (`L12M Title`) and the tooltip.
  - **Fallback B:** add a hidden line `[L12M Is Selected Month]` on a secondary axis with markers only, or use an analytics constant line, to mark the last bar.

## 8. Interactions
- The Month Anchor Year/Month slicers drive the window. They don't filter the axis directly; the measures read them.
- BU, Region and other dimension slicers and cross-filtering from the BU matrix/visuals filter the chart normally (the counts are on MPO).
- **Any Dim_Date slicer on the page is ignored** (the measures use REMOVEFILTERS(Dim_Date)). Remove day/date slicers from the BU page to avoid confusion.
- Clicking a bar: the month is a disconnected axis, so it **won't** cross-filter other visuals by date. Set Edit interactions to *None* from this chart to the KPI cards. The Anchor KPI cards follow the slicers and equal this chart's last bar (Planned card = last Planned bar; the Executed (Exec Date) card = last Executed bar).

## 9. How to read it
- Each month has two bars: light = Planned (target), dark = Executed.
- **The gap between Planned and Executed is non-executed activity** for that month. The bigger the gap, the more planned work didn't happen.
- The last, darker pair is the selected month. Check the tooltip for the year.
- The current (running) month is partial, so expect lower bars.

## 10. Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| "Sort by column" error: *can't sort Axis Label by Month Sort Key because there's more than one value...* | The label was plain "mmm", so one name mapped to two keys (Aug 2025, Aug 2026). | Use the `L12M Axis` DAX above (zero-width-space suffix). Refresh the table, then set the sort again. |
| Axis is in alphabetical order (Apr, Aug, Dec...) | The sort isn't on the axis field. | (...) > Sort axis > Axis Label ascending; check that Sort by column = Month Sort Key. |
| *"A table of multiple values was supplied where a single value was expected"* / *"multiple columns cannot be converted to a scalar value"* | An IF/SWITCH returned a table into a VAR, or a column was referenced without an aggregate. | Keep IF **outside** CALCULATE (pattern used in all L12M/Anchor measures). Use SELECTEDVALUE/MAX for single values. Paste the DAX exactly as above. |
| Only one month shows | A relationship was auto-created on `Month Anchor` or `L12M Axis`, or the slicer is on the wrong table. | Delete the relationships. Slicers must be on `Month Anchor`, and the axis on `L12M Axis`. |
| More than 12 months or none | The visual filter is missing, or the slicer picks a month with no data. | Filter `[L12M Visible Flag]` is 1. A month later than the latest data month falls back to the latest data month. |
| **Executed is higher than Planned in a month** | Expected. Planned counts by **planned date**, and Executed by **executed date**. Work planned in Jul but done in Aug counts as Planned in Jul and Executed in Aug. | Explain in a subtitle/glossary. For a like-for-like rate, use `Executed Activities` (planned date) in cards. **Confirm with the user** which date the chart should use (see below). |
| Fx colour missing / one colour | Multi-series fx limitation. | See the fallbacks in section 7. |
| Default window ends in a future month | Planned dates in the future (old behaviour). | Fixed: `L12M Latest Data Month` is capped at TODAY(). |

## 11. Open points for the user
1. Should Executed on this chart use the **executed date** (current, can exceed Planned) or the **planned date** (Executed never exceeds Planned, and the gap equals Not Executed exactly)?
2. Are the Planned greens #D6E8E0/#99C2B3 and the Executed greens #7FB19F/#006341 acceptable?
3. Should Activities With Sales be added as a third series once the sales definition is confirmed?
