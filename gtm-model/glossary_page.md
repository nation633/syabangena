# GTM Dashboard - Glossary page (draft text)
Paste each block into a text box on a "Glossary" report page. Formatting: Arial 10, black text, section headers white on corporate green (#005B33), zero padding.

## How to use this report
- Use the slicers at the top (Year, Month, Business Unit, Region, MicroMarket, Branch, Banker, Company, Source of Opportunity, Product Group/Product). Press Apply after changing slicers.
- All numbers are counts or sums of counts. No rand values are shown.
- Only approved (StatusId 2), active activities planned on or after 1 January 2025 are included.
- Drill down on org visuals: Business Unit > Region > MicroMarket > Branch > Banker. Use the drill arrows on the visual header, or right-click > Drill down.
- The Product slicer changes only Sales Count and Activities With Sales. Planned, Executed and Not Executed ignore it.

## Measure definitions
| Measure | What it means | How it is calculated |
|---|---|---|
| Planned Activities | Approved activities bankers planned | Count of activity rows, dated by the planned date |
| Executed Activities | Planned activities that were carried out | Count of activities marked Executed = Yes, dated by the planned date |
| Executed (Exec Date) | Same activities, placed on the day they were executed | Executed Activities using the executed date instead of the planned date; activities marked Yes without an executed date are left out |
| Not Executed | Planned activities not marked as executed | Planned Activities minus Executed Activities |
| Sales Count | Number of product sales recorded on activities | Sum of the 10 product columns, or only the products selected in the Product slicer |
| Activities With Sales | Activities that produced at least one sale | Count of activities where the selected products have a sale greater than 0 |
| ... PY | Same measure for the same period last year | Same-period-last-year comparison |
| ... PM | Same measure for the previous month | Shifted back one month |
| ... MoM % | Change versus previous month | (This month - previous month) / previous month |

## Key rules
- An activity counts as executed when its Executed flag is Yes. The executed date only places it on Exec Date charts, so an activity marked Yes with no executed date counts as executed but does not appear on Exec Date charts.
- Region is the Province on the activity.
- Company is the store name, or the free-text "Other" value when the store is "Other", so spelling can vary.
- Bankers and branches are shown as recorded on each activity. A banker who moved branch appears under each branch for the dates they worked there.

## How to read the trend charts
- The line or column shows the measure per day or month on the planned date, unless the title says "Exec Date".
- Planned vs Executed: the gap between the two lines is Not Executed. A widening gap means more activities are slipping.
- Recent days can look low for Executed because activities may not be completed yet.
- Compare against the PY line to see whether activity is up or down on last year.

## How to read KPI cards
- The big number is the selected period. The smaller line shows previous year and month-on-month change. Green means up, red means down.
