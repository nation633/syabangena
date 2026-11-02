# GTM Dashboard - Glossary page (draft text)
Paste each block into a text box on a "Glossary" report page. Formatting: Arial 10, black text, section headers white on corporate green (#006341), zero padding.

## How to use this report
- Use the slicers at the top (Year, Month, Business Unit, Region, MicroMarket, Branch, Banker, Company, Source of Opportunity, Product Group/Product). Press Apply after changing slicers.
- All numbers are counts or sums of counts. No rand values are shown.
- Only approved (StatusId 2), active activities planned on or after 1 January 2025 are included.
- Drill down on org visuals: Business Unit > Region > MicroMarket > Branch > Banker. Use the drill arrows on the visual header, or right-click > Drill down.
- The Product slicer does not change any numbers yet. Sales Count and Activities With Sales will follow it once product mapping is confirmed.

## Measure definitions
| Measure | What it means | How it is calculated |
|---|---|---|
| Planned Activities | Approved activities bankers planned | Count of activity rows, dated by the planned date |
| Executed Activities | Planned activities that were carried out | Count of activities marked Executed = Yes, dated by the planned date |
| Executed (Exec Date) | Same activities, placed on the day they were executed | Executed Activities using the executed date instead of the planned date; activities marked Yes without an executed date are left out |
| Not Executed | Planned activities not marked as executed | Planned Activities minus Executed Activities |
| Sales Count | Number of product sales recorded on activities | Sum of the 10 product columns (all products; the Product slicer does not filter this yet) |
| Activities With Sales | Activities that produced at least one sale | Count of executed activities with at least one sale in any product (the Product slicer does not filter this yet) |
| Executed No Sale | Executed activities that produced no sale | Count of activities marked Executed = Yes with no sale, dated by the planned date |
| Repeat No-Sale Companies | Companies visited more than once with no sale | Count of companies with more than 1 executed activity and no sale on any of them, in the selected period and filters |
| Conversion % | Share of executed activities that produced a sale | Activities With Sales divided by Executed Activities |
| Companies Visited / Branches / Bankers | How many different companies, branches and bankers have activities | Distinct count, dated by the planned date |
| ... YoY % | Change versus same period last year | (Selected period - last year) / last year |
| ... YoY pp / MoM pp | Change in a percentage | Percentage this period minus last year / previous month, in percentage points |
| ... 7D Avg | Average per day over the last 7 days | Total for the 7 days ending on the date shown, divided by 7 |
| Gap to Plan | Planned activities still missing to reach plan | Same as Not Executed: Planned Activities minus Executed Activities |
| ... CY vs PY Diff / MoM Diff | Difference in count versus last year / previous month | This period minus last year / previous month |
| ... PY | Same measure for the same period last year | Same-period-last-year comparison |
| ... PM | Same measure for the previous month | Shifted back one month |
| ... MoM % | Change versus previous month | (This month - previous month) / previous month |
| ... MoM % Like-for-Like | Fair month-on-month change while the month is still running | Month to date compared with the same days of the previous month (e.g. 1-14 Nov vs 1-14 Oct) |
| ... YTD | Year to date | From 1 January to the end of the selected period, by planned date |
| Data Through Date | Latest day with planned activities in the data | The last date that has planned activities |
| Low Volume Flag | Marks units with very few planned activities (e.g. ROUTE 99) | 1 when Planned Activities is below the threshold (provisional: 20) |

## Key rules
- An activity counts as executed when its Executed flag is Yes. The executed date only places it on Exec Date charts, so an activity marked Yes with no executed date counts as executed but does not appear on Exec Date charts.
- Region is the Province on the activity.
- Company is the store name, or the free-text "Other" value when the store is "Other", so spelling can vary.
- Bankers and branches are shown as recorded on each activity. A banker who moved branch appears under each branch for the dates they worked there.

## How to read the trend charts
- The line or column shows the measure per day or month on the planned date, unless the title says "Exec Date".
- Planned vs Executed: the gap between the two lines is Not Executed. A widening gap means more activities are slipping.
- The current month is partial until it ends: its columns are shaded lighter and the subtitle reads "Month to date, through dd Mmm".
- Recent days can look low for Executed because activities may not be completed yet.
- Compare against the PY line to see whether activity is up or down on last year.

## How to read KPI cards
- The big number is the selected period. The smaller line shows previous year and month-on-month change. Green means up, red means down.

## How to read the icons
- Target = Planned: on plan means an execution rate of 100%. In bullets and progress bars the black line is the plan and the grey tick is last year.
- Pill: green = 100% of plan or more (all planned activities executed), amber = 90% to under 100% of plan, red = below 90% of plan. The pill text shows the % of plan, rounded down. Bullet bars use the same colours.
- Arrows: green up / red down versus the previous month. For Not Executed and Gap to Plan the colours are reversed: up is red, down is green. Arrows marked LfL compare like-for-like days.
- Sparkline: the months in the current filter, not a fixed 12 months. The green line is Executed and the grey line is Not Executed.

## Rolling 12 months (Business Unit page)
- Use the Year and Month slicers on this page to pick a month. The chart then shows the 12 months ending with it. For example, Aug 2026 shows Sep 2025 to Aug 2026, with Aug as the last bar.
- If you pick nothing, the page uses the latest month with data.
- The axis shows month names only. Hover over a bar to see the year.
- Grey = Planned and slate = Activities with a sale (provisional), both by planned date. Green = Executed, by the date it was executed. The selected month's bars are a darker shade.
- Every card, table, matrix and tree on this page shows the same single month as the last bar of the chart.
- If you pick only a Year, the page shows the latest month with data in that year. If you pick nothing, it shows the latest month with data.
- "Executed" counts executed activities in the month they were planned. "Executed (exec date)" counts them in the month they were actually executed, so the two numbers can differ.
- This page has no Day slicer: a day filter would not line up with the selected month.
