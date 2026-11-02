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

## Glossary additions to paste
- Execution Rate %: Share of planned activities that were carried out — Executed Activities ÷ Planned Activities, planned date.
- Conversion % (provisional): Share of executed activities that produced at least one sale.
- ... YoY %: Change versus same period last year — (selected period − last year) / last year.
- ... 7D Avg: Average per day over the last 7 days ending on the date shown.

## DirectQuery notes
Simple aggregations + filters on int columns fold to SQL. Time intelligence runs on DimDate (Dual), so date shifts resolve locally and send key lists to SQL. No FILTER(MPO) iteration or row-level SUMX over the fact. Check with Performance Analyzer.
