# GTM Dashboard - Comparison, progress and floating-bar visuals (Data Storyteller)

DRAFT, 2026-11-02. **Target = Planned.** PY and previous month are secondary context. Measures marked **existing** are in `dax/measures.dax`. Measures marked **NEW** are drafted in `story/svg_measures_proposal.dax` section v3 for the DAX Analyst. Placement is a request to the Viz Designer (`viz/layout_spec.md` page IDs).

Style: #006341 green, amber #C98A1A, red #B03A2E, grey #9AA5AB, PY #5E6A71, Arial 10, black text, 0 padding, headers white on green. Counts and sums only, no rand values. SVG measures use Data category Image URL, with %23/%25 encoding. Pill and bullet bands follow measures.dax: green >= 100% of plan, amber 90 to < 100%, red < 90%. Deneb is used only where noted. Every item responds to the synced slicers. Mockup numbers are EXAMPLE DATA.

## 01 Exec Overview
| Visual | Where | Fields / measures | Interaction |
|---|---|---|---|
| Native **Waterfall: Planned -> Not Executed -> Executed (total)** | Replaces or sits next to the funnel | Category 'Plan Bridge'[Step] (NEW table); Y [Plan Bridge Value] (NEW); Total renamed "Executed" | Cross-filtered by slicers and the BU bar; tooltip [Execution Rate %] (existing), [Gap to Plan %] (NEW) |
| Native **Waterfall: monthly change in Executed** | Under the monthly trend | Category DimDate[YEAR_MONTH_KEY]; Y [Executed MoM Diff] (NEW) | Click a month to filter the page; drill YEAR > MONTH |
| KPI K4 rate bullet and pill | Existing | [SVG Bullet Execution Rate vs Plan], [SVG Status Pill] (existing) | - |
| Card **Gap to Plan** with a floating bar | Next to K3, or replacing the K3 image | [Gap to Plan] (NEW), [SVG Floating Bar Gap to Plan] (NEW) | Title fx [Title - Executed vs PY] (existing) |

## 02 Business Unit
| Visual | Where | Fields / measures | Interaction |
|---|---|---|---|
| Matrix with **floating-bar gap column** | Add a column to the BU > Region matrix | MPO[BusinessUnit] > MPO[Region]; [Planned Activities], [Executed Activities], [Gap to Plan] (NEW), [SVG Floating Bar Gap to Plan] (NEW), [SVG Status Pill] (existing) | Drill-down +/-; cross-filter |
| **CY vs PY dumbbell column** | Same matrix | [SVG Dumbbell CY vs PY] (NEW; uses existing Execution Rate % / PY) | Tooltip [Execution Rate YoY pp] (existing) |
| Native **clustered bar CY vs PY** (alternative to the dumbbell) | Replaces "rate vs PY per BU" if preferred | Y MPO[BusinessUnit]; X [Executed Activities], [Executed PY] (existing); data label [Executed CY vs PY Diff] (NEW) | Metric field parameter (existing) can swap the X measure |

## 03 Region
| Visual | Where | Fields / measures | Interaction |
|---|---|---|---|
| **Gap-to-plan floating bars by level** (table) | Companion table to the Level bar | Level field parameter (existing) rows; [Planned Activities], [Executed Activities], [SVG Floating Bar Gap to Plan] (NEW), [Gap to Plan %] (NEW) | Level parameter switches Region / MicroMarket; sorted by [Gap to Plan] desc |
| Native **Line and stacked column**: Executed + Gap to Plan stacked = Planned | Replaces the Level bar if a native chart is wanted | X Level parameter; columns [Executed Activities] (green), [Gap to Plan] (NEW, grey); line [Execution Rate %] | Cross-filter; TT Branch |
| Optional **Deneb range bar** Executed -> Planned with a PY tick | Only if the native stacked bar is not clear enough | [Executed Activities], [Planned Activities], [Executed PY] | Deneb cross-filter on; needs tenant approval |

## 04 Branch
| Visual | Where | Fields / measures | Interaction |
|---|---|---|---|
| Table V4T: add **floating bar** and **MoM change bar** | Next to the existing progress, pill, sparkline and counts bullet | [SVG Floating Bar Gap to Plan] (NEW), [SVG MoM Change Bar] (NEW, scaled over ALLSELECTED Branch), [Executed MoM Diff] (NEW) | Chart/Table bookmark (existing); TT Branch; drill-through Branch Detail |
| Native **bar: Executed MoM Diff by branch** (Top/Bottom 10) | Chart view, below the ribbon | Y MPO[Branch]; X [Executed MoM Diff] (NEW); colour by sign via a rule (green/red) | Cross-filter |

## 05 Banker
| Visual | Where | Fields / measures | Interaction |
|---|---|---|---|
| Scorecard: add **dumbbell CY vs PY** and **floating gap** | Scorecard table V4 | [SVG Dumbbell CY vs PY] (NEW), [SVG Floating Bar Gap to Plan] (NEW), existing rate bullet and pill | Drill-through Banker Detail; TT Banker |
| Native **stacked bar Executed + Gap to Plan** (= Planned) | Replaces V1 executed/not executed (same visual, target wording) | Y MPO[BankerName]; X [Executed Activities], [Gap to Plan] (NEW) | Cross-filter |

## 05a Banker Detail
| Visual | Where | Fields / measures | Interaction |
|---|---|---|---|
| Native **Waterfall Planned -> Not Executed -> Executed** for the banker | Next to the KPI strip, or replacing one KPI | 'Plan Bridge'[Step], [Plan Bridge Value] (NEW) | Drill-through context (BankerName) |
| Native **Waterfall: monthly change in Executed** | Under the monthly chart, or as a bookmark toggle | DimDate[YEAR_MONTH_KEY]; [Executed MoM Diff] (NEW) | - |
| Company table: add a **floating bar** column | Next to the pill and Executed No Sale (separate columns) | [SVG Floating Bar Gap to Plan] (NEW) | - |

## 06 Product (PROVISIONAL)
- Product comparisons wait on `Sales Count (Product)` (stub) and open question #11. **No product floating bars yet.**
- Interim: native clustered column **Conversion % vs Conversion PY by month** (existing, provisional) and the existing gauge. Execution-vs-plan visuals don't apply to products, because Planned has no product grain.

## 07 Company
| Visual | Where | Fields / measures | Interaction |
|---|---|---|---|
| Top 20: native **stacked bar Executed + Gap to Plan** | V1 | MPO[Company]; [Executed Activities], [Gap to Plan] (NEW) | Drill-through Banker Detail; title [Title - Company] (existing) |
| Table: **floating bar** and **pill** | Optional table view of V1 | [SVG Floating Bar Gap to Plan] (NEW), [SVG Status Pill] (existing) | Bookmark Chart/Table |

## Notes
- [Gap to Plan] equals [Not Executed] by definition. It is a named alias so the target wording reads naturally. The DAX Analyst may prefer to keep only [Not Executed].
- The MoM waterfall and the CY vs PY measures use the planned date (open question #3 is not decided).
- [SVG MoM Change Bar] scales over ALLSELECTED(MPO[Branch]), so on other levels it should be re-pointed or duplicated (a request to the DAX Analyst).
