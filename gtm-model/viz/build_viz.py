# Generates layout_spec.md, backgrounds/ and mockups/ from one spec so positions always match.
import random, math
from PIL import Image, ImageDraw, ImageFont
random.seed(7)
G="#006341"; LIME="#7AB800"; G2="#00A651"; G3="#4D8B70"; G4="#A3C9B8"; GR="#5E6A71"; GR2="#9AA5AB"; GR3="#C8D1D6"; DK="#003D29"; LG="#B5D98C"
BG="#F4F6F7"; W="#FFFFFF"; RED="#B03A2E"
F="/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"; FB="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
def fnt(s,b=False): return ImageFont.truetype(FB if b else F,s)
D="DimDate"; M="MPO"; P="Product"
SL={"Year":"DimDate[YEAR]","Month":"DimDate[MONTH_NAME] (sorted by MONTH)","Day":"DimDate[ACTUAL_DATE] (between)","BU":"MPO[BusinessUnit]","Region":"MPO[Region]","Branch":"MPO[Branch]","Company":"MPO[Company]","Product Group":"Product[ProductGroup]","Product":"Product[ProductLabel]","Level":"Level[Level] (field parameter) - SINGLE SELECT, default Region","Anchor Year":"'Month Anchor'[Year] - SINGLE SELECT (NOT synced with DimDate Year)","Anchor Month":"'Month Anchor'[Month Short] (sorted by Month Number) - SINGLE SELECT (NOT synced with DimDate Month)","Metric":"Metric[Metric] (field parameter, dax/field_parameters.tmdl) - SINGLE SELECT, default Not Executed"}
def slicers(names):
    if not names: return []
    n=len(names); x0=16; wtot=1280-32-48-8; w=(wtot-(n-1)*8)//n
    return [dict(id=f"S{i+1}",type="Slicer (dropdown)",title=nm,x=x0+i*(w+8),y=64,w=w,h=40,fields=SL[nm],kind="slicer") for i,nm in enumerate(names)]
INFO=lambda: dict(id="INFO",type="Button (Information icon)",title="Info",x=1224,y=12,w=40,h=32,fields="Action: Page navigation > Glossary; tooltip 'How to read this page'",kind="info")
RESET=lambda: dict(id="RESET",type="Button (Reset)",title="Reset",x=1224,y=64,w=40,h=40,fields="Action: Bookmark > 'BM Reset - <page>' (clears slicers on this page)",kind="reset")
C0=116
PD=" - SVG"
pages=[]
def page(n,name,sub,sl,vis,notes): pages.append(dict(n=n,name=name,sub=sub,sl=sl,vis=vis,notes=notes))

PN=""  # 8. Comparison measures verified in measures.dax 13:22 SAST (untested in Power BI)
FB_="[SVG Floating Bar Gap to Plan] (140x20)"; DB="[SVG Dumbbell CY vs PY] (120x20)"; MB="[SVG MoM Change Bar] (130x20)"
PR=""  # all four SVG measures confirmed in measures.dax 13:16 SAST
BUL="[SVG Bullet Executed vs Planned]"; RB="[SVG Bullet Execution Rate vs Plan]"
NEXT=lambda tgt: dict(id="NEXT",type="Button (Blank, text 'Next >')",title="Next",x=1168,y=12,w=52,h=32,fields=f"Action: Page navigation > {tgt}; synced slicers carry the selection forward",kind="next")
STORY=["Year","Month","BU","Region","Branch"]
kpi=lambda i,x,title,base,py,mom,img,w=192: dict(id=f"K{i}",type="Card (new) + SVG image"+(PD if "[SVG" in img else "")+(PR if "[SVG Bullet" in img else ""),title=title,x=x,y=C0,w=w,h=100,fields=f"Value: [{base}]; Reference labels: [{py}] (label 'PY'), [{mom}] (label 'MoM'); Image (fx > Field value): {img}",kind="kpi")
A=lambda m: f"[SVG KPI Arrow {m} MoM] (80x18)"
page("01","Exec Overview","Are we on plan? Target = Planned",STORY,[
 kpi(1,16,"Planned Activities","Planned Activities","Planned PY","Planned MoM %",A("Planned")),
 kpi(2,216,"Executed Activities","Executed Activities","Executed PY","Executed MoM %",A("Executed")),
 kpi(3,416,"Not Executed","Not Executed","Not Executed PY","Not Executed MoM %",A("Not Executed")+" (reversed colours)"),
 dict(id="K6",type="Card (new) + SVG image"+PD+PN,title="Gap to Plan",x=616,y=C0,w=192,h=100,fields="Value: [Gap to Plan]; Reference label: [Gap to Plan %] (label '% of plan'); Image (fx > Field value): "+FB_+"; Title fx: [Title - Executed vs PY]; click cross-filters page",kind="kpi"),
 kpi(4,816,"Execution Rate %","Execution Rate %","Execution Rate PY","Execution Rate MoM pp",RB+" (120x20) + [SVG Status Pill] (80x20, % of plan)",w=248),
 dict(id="K5",type="Card (new) + SVG image - PROVISIONAL"+PD,title="Sales Count (provisional)",x=1072,y=C0,w=192,h=100,fields="Value: [Sales Count]; Reference labels: [Sales Count PY], [Sales Count MoM %]; Image: [SVG KPI Arrow Sales Count MoM] (80x18)",kind="kpi"),
 dict(id="V1",type="Waterfall chart"+PN,title="Plan bridge: Planned - Not Executed = Executed",x=16,y=224,w=300,h=240,fields="Category: 'Plan Bridge'[Step] (disconnected table, dax/plan_bridge.tmdl; sorted by hidden 'Plan Bridge'[Order]); Y: [Plan Bridge Value]; Total on, renamed 'Executed'; increase #006341, decrease #9AA5AB, total #006341; tooltip [Execution Rate %], [Gap to Plan]; replaces the funnel; cross-filtered by slicers and V5",kind="waterfall"),
 dict(id="V2",type="Line and stacked column chart"+PD,title="Executed vs not executed by month [fx: Title - Executed vs PY]",x=324,y=224,w=620,h=240,fields="Title fx: [Title - Executed vs PY]; X: DimDate[YEAR_MONTH_KEY] (drill YEAR > MONTH_NAME); Columns: [Executed Activities], [Not Executed]; Lines: [Executed PY], [Planned PY]",kind="combo"),
 dict(id="V5",type="Stacked bar chart",title="By business unit: executed vs not executed",x=952,y=224,w=312,h=240,fields="Y: MPO[BusinessUnit]; X: [Executed Activities], [Not Executed]; sort [Not Executed] desc; click cross-filters page; entry to Business Unit page",kind="hbarstack"),
 dict(id="V7",type="Line chart",title="Execution rate % by month vs PY",x=16,y=472,w=300,h=240,fields="X: DimDate[YEAR_MONTH_KEY]; Y: [Execution Rate %], [Execution Rate PY] (dashed); secondary Y [Executed (Exec Date)]",kind="line2"),
 dict(id="V8",type="Waterfall chart"+PN,title="Monthly change in executed (MoM)",x=324,y=472,w=460,h=240,fields="Category: DimDate[YEAR_MONTH_KEY] (drill YEAR > MONTH_NAME); Y: [Executed MoM Diff]; increase #006341, decrease #B03A2E, total off; click a month filters the page; sits under V2",kind="wfmom"),
 dict(id="V4T",type="Table (bookmark 'BM Exec - Table')"+PD+PR,title="Top 15 branches by not executed - table",x=792,y=472,w=472,h=240,fields="MPO[Branch], [Planned Activities], [Executed Activities], [Not Executed], [SVG Execution Progress], [SVG Status Pill]; Top N 15 by [Not Executed]; same position as V4",kind="svgtable",alt=True),
 dict(id="TOG",type="Button pair (Chart / Table)",title="Chart|Table",x=1124,y=476,w=136,h=20,fields="Bookmarks 'BM Exec - Chart' (V4 shown) / 'BM Exec - Table' (V4T shown); Display only, Selected visuals V4+V4T",kind="toggle"),
 dict(id="V4",type="Clustered bar chart (bookmark 'BM Exec - Chart', default)",title="Top 15 branches by not executed",x=792,y=472,w=472,h=240,fields="Y: MPO[Branch]; X: [Not Executed], [Executed Activities]; Top N 15 by [Not Executed]; tooltip TT Branch",kind="hbar"),
 NEXT("Business Unit"),INFO(),RESET()],
 "Plan Bridge waterfall V1 replaces the funnel (it shows the drop from plan as Not Executed; the funnel's with-sales step is provisional and conversion lives on Product). Donut dropped (the bridge shows the same split). K6 Gap to Plan sits next to K3. Absorbs the former Execution page (stacked months -> V2, rate line V7, top branches V4/V4T toggle). Smart narrative optional (spec only). K-card variance colours up #006341 / down #B03A2E.")
page("02","Business Unit","Which BU misses plan, and is it worsening?",["Anchor Year","Anchor Month","BU","Region","Branch","Metric"],[
 dict(id="K1",type="Card (new)",title="Planned",x=16,y=C0,w=200,h=100,fields="Value: [Anchor Planned] (10. L12M, dax/l12m_measures.dax; follows the Month Anchor slicers; nothing selected = latest data month)",kind="kpi"),
 dict(id="K2",type="Card (new)",title="Executed",x=224,y=C0,w=200,h=100,fields="Value: [Anchor Executed] (10. L12M, dax/l12m_measures.dax; follows the Month Anchor slicers; nothing selected = latest data month)",kind="kpi"),
 dict(id="K3",type="Card (new)",title="Executed (exec date)",x=432,y=C0,w=200,h=100,fields="Value: [Anchor Executed (Exec Date)] (10. L12M, dax/l12m_measures.dax; follows the Month Anchor slicers; nothing selected = latest data month)",kind="kpi"),
 dict(id="K4",type="Card (new) - PROVISIONAL",title="Activities with sales (prov.)",x=640,y=C0,w=200,h=100,fields="Value: [Anchor Activities With Sales] (10. L12M, dax/l12m_measures.dax; follows the Month Anchor slicers; nothing selected = latest data month)",kind="kpi"),
 dict(id="K5",type="Card (new) - PROVISIONAL",title="Sales count (prov.)",x=848,y=C0,w=200,h=100,fields="Value: [Anchor Sales Count] (10. L12M, dax/l12m_measures.dax; follows the Month Anchor slicers; nothing selected = latest data month)",kind="kpi"),
 dict(id="K6",type="Card (new)",title="Execution %",x=1056,y=C0,w=200,h=100,fields="Value: [Anchor Execution %] (10. L12M, dax/l12m_measures.dax; follows the Month Anchor slicers; nothing selected = latest data month)",kind="kpi"),

 dict(id="V1",type="Matrix (drill-down)"+PD+PR,title="BU > Region vs plan [fx: Title - Business Unit]",x=16,y=224,w=1248,h=184,fields=f"Title fx: [Title - Business Unit] (Format > Title > fx > Field value; untested, check in QA); Rows: MPO[BusinessUnit] > MPO[Region] (+/- on, expand to Region); Values: [Planned Activities], [Executed Activities], [Not Executed], [Gap to Plan], {BUL} (120x20), {FB_}, {DB} (tooltip [Execution Rate YoY pp]; blank for 2025 - no 2024 data), [SVG Status Pill] (80x20), [SVG Sparkline Executed] (120x20)",kind="svgtable"),
 dict(id="V2",type="Decomposition tree",title="Selected metric by BU > Region > MicroMarket > Branch > BankerName",x=16,y=416,w=400,h=296,fields="Analyze: Metric[Metric] (field parameter, single select slicer, default Not Executed; fallback bookmarks); Explain by: MPO[BusinessUnit], MPO[Region], MPO[MicroMarket], MPO[Branch], MPO[BankerName]",kind="decomp"),
 dict(id="V3",type="Line chart (small multiples)",title="Execution rate % vs PY per BU",x=424,y=416,w=400,h=296,fields="X: DimDate[YEAR_MONTH_KEY]; Y: [Execution Rate %], [Execution Rate PY]; Small multiples: MPO[BusinessUnit]",kind="smallmult"),
 dict(id="V4",type="Clustered column chart - PROVISIONAL",title="Rolling 12 months [fx: L12M Title]",x=832,y=416,w=432,h=296,fields="Title fx: [L12M Title] (Format > Title > fx > Field value); X: 'L12M Axis'[Axis Label] (month names only; sorted by hidden Month Sort Key ascending; not a date hierarchy; drill off); Y: [L12M Planned], [L12M Executed], [L12M Activities With Sales] (PROVISIONAL); Tooltip: [L12M Month Label] (month + year); visual-level filter [L12M Visible Flag] is 1; Columns colour per series fx > Field value: Planned = [L12M Bar Colour Planned] (#BFBFBF, #7F7F7F selected), Executed = [L12M Bar Colour Executed] (#7FB19F, #006341 selected), Sales = [L12M Bar Colour Sales] (#A9B4C2, #4A5A6E selected); window driven by the Month Anchor slicers (both tables disconnected, dax/l12m_measures.dax); Aug 2026 selected = Sep 2025-Aug 2026; nothing selected = 12 months to latest data month; untested in Power BI, check in QA",kind="l12m"),
 NEXT("Region"),INFO(),RESET()],
 "Matrix column headers white on #006341. Matrix rows drill-through to Banker Detail at banker level not available (BU/Region only); use the decomposition tree.")
page("03","Region","Within the BU, which regions and micro-markets drive the gap?",STORY+["Level"],[
 dict(id="V1",type="Line chart (small multiples)",title="Planned vs executed by month, per region",x=16,y=C0,w=620,h=596,fields="X: DimDate[YEAR_MONTH_KEY]; Y: [Planned Activities], [Executed Activities]; Small multiples: MPO[Region]",kind="smallmult"),
 dict(id="V2",type="Stacked bar chart",title="Executed + gap to plan (= Planned) by selected level",x=644,y=C0,w=620,h=292,fields="Y: Level[Level] (field parameter; slicer single select, default Region; use Region / MicroMarket); X: [Executed Activities] (#006341), [Gap to Plan] (#9AA5AB); sort [Gap to Plan] desc; tooltip [Execution Rate %], [Gap to Plan %]; replaces the rate bar; click filters V1/V3",kind="hbarstack"),
 dict(id="V3",type="Table"+PD+PR,title="Selected level vs plan [fx: Title - Region]",x=644,y=416,w=620,h=296,fields=f"Title fx: [Title - Region] (Format > Title > fx > Field value; untested, check in QA); Columns: Level[Level], [Planned Activities], [Executed Activities], [Not Executed], {BUL} (120x20), [SVG Status Pill] (80x20), [SVG Sparkline Executed] (120x20)",kind="svgtable"),
 NEXT("Branch"),INFO(),RESET()],
 "Chose the native stacked bar over a floating-bar table: V3 is already an SVG table beside it, a native bar cross-filters and drills natively, and Executed + Gap reads directly as Planned. Outliers: amber/red pill (below 100% / below 90% of plan) with a falling sparkline. V2 click filters V1/V3.")
page("04","Branch","Which branches have the most non-executed activities and fall furthest below plan?",STORY,[
 dict(id="V4T",type="Table (bookmark 'BM Branch - Table')"+PD+PR,title="Top 15 branches by not executed - table [fx: Title - Branch]",x=16,y=C0,w=760,h=596,fields=f"Title fx: [Title - Branch] (Format > Title > fx > Field value; untested, check in QA); Columns: MPO[Branch], [Planned Activities], [Executed Activities], [Not Executed], [SVG Execution Progress] (120x20), [SVG Status Pill] (80x20), [SVG Sparkline Executed] (120x20), {BUL} (120x20), {FB_}, {MB} (adapts to any level incl. the Level parameter), [Executed MoM Diff]; Top N 15 by [Not Executed]; drill-through Branch Detail (optional) / Banker Detail via bankers",kind="svgtable",alt=True),
 dict(id="TOG",type="Button pair (Chart / Table)",title="Chart|Table",x=440,y=120,w=136,h=20,fields="Bookmarks 'BM Branch - Chart' (V4) / 'BM Branch - Table' (V4T); Display only, Selected visuals V4+V4T",kind="toggle"),
 dict(id="V4",type="Clustered bar chart (bookmark 'BM Branch - Chart', default)",title="Top 15 branches by not executed [fx: Title - Branch]",x=16,y=C0,w=760,h=596,fields="Y: MPO[Branch]; X: [Not Executed], [Executed Activities]; Top N 15 by [Not Executed]; tooltip TT Branch",kind="hbar"),
 dict(id="V3",type="Ribbon chart",title="Branch rank by executed activities per month",x=784,y=C0,w=480,h=292,fields="X: DimDate[YEAR_MONTH_KEY]; Y: [Executed Activities]; Legend: MPO[Branch]; Top N 10",kind="ribbon"),
 dict(id="V5",type="Clustered bar chart",title="Top / bottom 10 branches: executed MoM change",x=784,y=416,w=480,h=296,fields="Y: MPO[Branch]; X: [Executed MoM Diff]; visual-level filter [MoM Top Bottom Flag] is 1; colour by field value / rules on [MoM Top Bottom Group]: 'Top 10' #006341, 'Bottom 10' #B03A2E; sort [Executed MoM Diff] desc; cross-filters page; tooltip TT Branch, [Executed MoM Diff Rank (Up)], [Executed MoM Diff Rank (Down)]; ranks work at any level; blank changes excluded; with fewer than 20 rows a row can be in both groups and shows as Top; untested in Power BI, check in QA",kind="hbardiv"),
 NEXT("Banker (Individual)"),INFO(),RESET()],
 "Default view Chart (V4); Table (V4T) holds the storyline columns. Tooltip TT Branch on V4/V4T/V3.")
page("05","Banker (Individual)","Who plans but doesn't execute? Who is on plan?",STORY,[
 dict(id="V1",type="Stacked bar chart",title="Bankers: executed + gap to plan (= Planned)",x=16,y=C0,w=400,h=596,fields="Y: MPO[BankerName]; X: [Executed Activities] (#006341), [Gap to Plan] (#9AA5AB); sort [Planned Activities] desc; tooltip TT Banker; drill-through Banker Detail",kind="hbarstack"),
 dict(id="V4",type="Table"+PD+PR,title="Banker scorecard",x=424,y=C0,w=840,h=292,fields=f"Columns: MPO[BankerName], [Planned Activities], [Executed Activities], [Not Executed], {RB} (120x20), {DB} (blank for 2025 - no 2024 data), {FB_}, [SVG Status Pill] (80x20), [SVG Sparkline Executed] (120x20); sort [Not Executed] desc; drill-through Banker Detail",kind="svgtable"),
 dict(id="V2",type="Scatter chart",title="Execution rate vs conversion % by banker",x=424,y=416,w=416,h=296,fields="Details: MPO[BankerName]; X: [Execution Rate %]; Y: [Conversion %] (provisional); Size: [Planned Activities]; Legend: MPO[Region]",kind="scatter"),
 dict(id="V3",type="Line chart",title="Selected banker(s): executed vs not executed by month",x=848,y=416,w=416,h=296,fields="X: DimDate[YEAR_MONTH_KEY]; Y: [Executed Activities], [Not Executed]",kind="line2"),
 NEXT("Product (PROVISIONAL)"),INFO(),RESET()],
 "Rate bullet so bankers of different sizes compare fairly.")
page("05a","Banker Detail","Drill-through target: MPO[BankerName] - hidden page",[],[
 dict(id="V1",type="Card (new)"+PD,title="Banker KPIs [fx: Title - Banker Detail]",x=16,y=C0,w=1248,h=100,fields="Title fx: [Title - Banker Detail]; [Planned Activities], [Executed Activities], [Not Executed], [Execution Rate %], [Conversion %] (provisional, number only - no gauge)",kind="kpi"),
 dict(id="V2",type="Line and stacked column chart",title="Monthly executed vs not executed",x=16,y=224,w=816,h=240,fields="X: DimDate[YEAR_MONTH_KEY]; Columns: [Executed Activities], [Not Executed]; Line: [Execution Rate %]",kind="combo"),
 dict(id="V4",type="Waterfall chart",title="Plan bridge for this banker",x=16,y=472,w=400,h=240,fields="Category: 'Plan Bridge'[Step] (sorted by hidden Order); Y: [Plan Bridge Value]; Total on, renamed 'Executed'; drill-through context MPO[BankerName]",kind="waterfall"),
 dict(id="V5",type="Waterfall chart",title="Monthly change in executed (MoM)",x=424,y=472,w=408,h=240,fields="Category: DimDate[YEAR_MONTH_KEY]; Y: [Executed MoM Diff]; increase #006341, decrease #B03A2E; sits under V2",kind="wfmom"),
 dict(id="V3",type="Table"+PD+PR,title="Companies visited",x=840,y=224,w=424,h=488,fields="Columns: MPO[Company], [Planned Activities], [Executed Activities], [Not Executed], [SVG Status Pill] (80x20, execution vs plan), [SVG Floating Bar Gap to Plan] (140x20), [Executed No Sale] (separate number column, header 'Executed No Sale (provisional)'); Top N 15 by [Planned Activities]",kind="svgtable"),
 dict(id="BACK",type="Button (Back)",title="Back",x=1224,y=64,w=40,h=40,fields="Back to previous page",kind="reset"),INFO()],
 "Drill-through field MPO[BankerName], keep all filters on. No SVG Conversion Gauge on this page.")
page("06","Product (PROVISIONAL)","PROVISIONAL - product visuals pending the product mapping (#11)",STORY+["Product Group","Product"],[
 dict(id="V1",type="Line and clustered column chart - PROVISIONAL"+PD,title="Conversion by month [fx: Title - Conversion]",x=16,y=C0,w=600,h=292,fields="Title fx: [Title - Conversion]; X: DimDate[YEAR_MONTH_KEY]; Columns: [Executed Activities], [Activities With Sales]; Line: [Conversion %]",kind="combo"),
 dict(id="G1",type="Card (new) image - PROVISIONAL"+PD,title="Conversion gauge (provisional)",x=624,y=C0,w=208,h=292,fields="Image: [SVG Conversion Gauge] (120x70); reference labels [Conversion YoY pp], [Conversion MoM pp]",kind="gauge"),
 dict(id="V2",type="Clustered bar chart - PROVISIONAL",title="Sales by product group (provisional)",x=840,y=C0,w=424,h=292,fields="Y: Product[ProductGroup]; X: [Sales Count (Product)] - STUB (commented out); placeholder 'Pending product mapping'",kind="hbar"),
 dict(id="V3",type="Treemap - PROVISIONAL",title="Sales by product (provisional)",x=16,y=416,w=600,h=296,fields="Category: Product[ProductLabel]; Values: [Sales Count (Product)] - STUB; placeholder",kind="treemap"),
 dict(id="V4",type="Scatter chart - PROVISIONAL",title="Executed activities vs sales by branch",x=624,y=416,w=640,h=296,fields="Details: MPO[Branch]; X: [Executed Activities]; Y: [Sales Count]; Size: [Planned Activities]; Legend: MPO[BusinessUnit]",kind="scatter"),
 NEXT("Company"),INFO(),RESET()],
 "Former Sales Conversion page. Product slicers change nothing until Sales Count (Product) is active.")
page("07","Company","Where do visits produce nothing?",STORY+["Company"],[
 dict(id="V1T",type="Table (bookmark 'BM Company - Table', optional)"+PD,title="Top 20 companies vs plan - table [fx: Title - Company]",x=16,y=C0,w=600,h=596,fields="Title fx: [Title - Company]; Columns: MPO[Company], [Planned Activities], [Executed Activities], [Not Executed], [SVG Floating Bar Gap to Plan] (140x20), [SVG Status Pill] (80x20, vs plan); Top N 20 by [Planned Activities]; drill-through Banker Detail; same position as V1",kind="svgtable",alt=True),
 dict(id="TOG",type="Button pair (Chart / Table)",title="Chart|Table",x=476,y=120,w=136,h=20,fields="Bookmarks 'BM Company - Chart' (V1) / 'BM Company - Table' (V1T); Display only, Selected visuals V1+V1T",kind="toggle"),
 dict(id="V1",type="Stacked bar chart (bookmark 'BM Company - Chart', default)",title="Top 20 companies: executed + gap to plan [fx: Title - Company]",x=16,y=C0,w=600,h=596,fields="Title fx: [Title - Company] (Format > Title > fx > Field value; untested, check in QA); Y: MPO[Company]; X: [Executed Activities] (#006341), [Gap to Plan] (#9AA5AB); Top N 20 by [Planned Activities]; drill-through Banker Detail",kind="hbarstack"),
 dict(id="V2",type="Scatter chart - PROVISIONAL",title="Visits vs sales by company",x=624,y=C0,w=640,h=292,fields="Details: MPO[Company]; X: [Executed Activities]; Y: [Sales Count]; Size: [Planned Activities]",kind="scatter"),
 dict(id="K1",type="Card (new) - PROVISIONAL",title="Repeat no-sale companies",x=624,y=416,w=200,h=296,fields="Value: [Repeat No-Sale Companies]",kind="kpi"),
 dict(id="V3",type="Clustered bar chart - PROVISIONAL",title="Executed no sale by company",x=832,y=416,w=432,h=296,fields="Y: MPO[Company]; X: [Executed No Sale]; Top N 15",kind="hbar"),
 NEXT("Daily"),INFO(),RESET()],
 "Company is free text when Store = 'Other' (#7) - footnote on V1.")
page("S1","Daily (supporting)","Day-level pattern and 7-day trend",["Year","Month","Day","BU","Region","Branch"],[
 dict(id="V1",type="Matrix (calendar heatmap)",title="Calendar heatmap: executed activities",x=16,y=C0,w=520,h=292,fields="Rows: DimDate[WEEK]; Columns: DimDate[DAY_SHORT_NAME] (sort by DAY_IN_WEEK); Values: [Executed Activities]; background colour scale white -> #006341; font colour rule: white when value high",kind="heat"),
 dict(id="V2",type="Line chart",title="Daily planned and executed with 7-day average",x=544,y=C0,w=720,h=292,fields="X: DimDate[ACTUAL_DATE] (continuous); Y: [Planned Activities] (light grey), [Executed Activities] (lime #7AB800), [Executed 7D Avg] (green #006341, 2px), [Not Executed 7D Avg] (grey dashed)",kind="daily"),
 dict(id="V3",type="Clustered column chart",title="Weekday pattern",x=16,y=416,w=620,h=296,fields="X: DimDate[DAY_SHORT_NAME] (sort by DAY_IN_WEEK); Y: [Executed Activities], [Not Executed]",kind="cols"),
 dict(id="V4",type="Line chart",title="Executed (exec date) per day vs PY",x=644,y=416,w=620,h=296,fields="X: DimDate[ACTUAL_DATE]; Y: [Executed (Exec Date)], [Executed (Exec Date) PY], [Executed (Exec Date) 7D Avg]",kind="line2"),
 INFO(),RESET()],
 "Heatmap matrix: column headers white on #006341 (theme), 0 padding. Default Day slicer to the last 90 days (relative date slicer on DimDate[ACTUAL_DATE]).")
page("S2","Glossary (supporting)","How to read this report",[],[
 dict(id="T1",type="Text box",title="How to use this report",x=16,y=72,w=616,h=300,fields="Paste glossary_page.md 'How to use this report' + 'Key rules'",kind="text"),
 dict(id="T2",type="Table (static, from text) or Text box",title="Measure definitions",x=648,y=72,w=616,h=640,fields="Paste glossary_page.md 'Measure definitions' (incl. the 3-band pill line: green >= 100% of plan, amber 90% to under 100%, red below 90%) + measures_guide.md 'Glossary additions' (Execution Rate %, Conversion %, YoY %, 7D Avg)",kind="text"),
 dict(id="T3",type="Text box",title="How to read trends and KPI cards",x=16,y=384,w=616,h=328,fields="Paste glossary_page.md 'How to read the trend charts' + 'How to read KPI cards'",kind="text"),
 dict(id="BACK",type="Button (Back)",title="Back",x=1224,y=12,w=40,h=32,fields="Back to previous page",kind="reset")],
 "No slicers. Section headers white on #006341.")

def hexrgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def background(p):
    im=Image.new("RGB",(1280,720),BG); d=ImageDraw.Draw(im)
    d.rectangle([0,0,1280,56],fill=G); d.rectangle([0,56,1280,59],fill=LIME)
    t=p["name"]; d.text((16,10),t,font=fnt(22,True),fill=W); d.text((16,36),p["sub"],font=fnt(12),fill="#DDEEE6")
    if p["sl"]: d.rectangle([0,60,1280,110],fill="#E9EDEF")
    for v in p["vis"]:
        if v["kind"] in("slicer","info","reset","toggle","optional","next") or v.get("alt"): continue
        d.rectangle([v["x"],v["y"],v["x"]+v["w"],v["y"]+v["h"]],fill=W,outline=GR3)
    return im
def draw_vis(d,v):
    x,y,w,h=v["x"],v["y"],v["w"],v["h"]; k=v["kind"]
    if k=="slicer":
        d.rectangle([x,y,x+w,y+h],fill=W,outline=GR2); d.text((x+6,y+3),v["title"],font=fnt(10,True),fill="#000"); d.text((x+6,y+20),("Not Executed  v" if v["title"]=="Metric" else "2026  v" if v["title"]=="Anchor Year" else "Aug  v" if v["title"]=="Anchor Month" else "All  v"),font=fnt(10),fill="#000"); return
    if k=="next":
        d.rectangle([x,y+4,x+w,y+h-4],fill=W); d.text((x+7,y+10),"Next >",font=fnt(10,True),fill=G); return
    if k=="toggle":
        d.rectangle([x,y,x+w/2,y+h],fill=G); d.text((x+14,y+4),"Chart",font=fnt(10,True),fill=W)
        d.rectangle([x+w/2,y,x+w,y+h],fill=W,outline=G); d.text((x+w/2+14,y+4),"Table",font=fnt(10),fill="#000"); return
    if k=="optional":
        for i in range(0,w,8): d.line([x+i,y,x+i+4,y],fill=GR2); d.line([x+i,y+h,x+i+4,y+h],fill=GR2)
        d.text((x+8,y+6),"OPTIONAL smart narrative",font=fnt(10,True),fill=GR); d.text((x+8,y+26),"Execution rate is 71.4%, +2.1 pp vs PY.",font=fnt(10),fill="#000"); return
    if k=="info":
        d.ellipse([x+6,y+2,x+34,y+30],fill=W); d.text((x+17,y+6),"i",font=fnt(16,True),fill=G); return
    if k=="reset":
        d.rectangle([x,y,x+w,y+h],fill=W,outline=G); d.text((x+4,y+h//2-6),v["title"][:5],font=fnt(10),fill=G); return
    d.text((x+8,y+5),v["title"],font=fnt(11,True),fill="#000")
    tags=[t for t in ("PROVISIONAL","SVG","PENDING DAX REVIEW","PENDING DAX") if t in v["type"].split(" - ")]
    tx=x+w-8
    for t in tags[::-1]:
        t={"PROVISIONAL":"PROV.","PENDING DAX REVIEW":"PENDING","PENDING DAX":"PENDING"}.get(t,t) if w<300 else t; tw=d.textlength(t,font=fnt(9,True)); tx-=tw+10; d.rectangle([tx-3,y+4,tx+tw+3,y+17],fill="#FFF4CC" if t.startswith("PEND") else W,outline=RED if t.startswith("PROV") else ("#B7950B" if t.startswith("PEND") else G)); d.text((tx,y+5),t,font=fnt(9,True),fill=RED if t.startswith("PROV") else ("#7D6608" if t.startswith("PEND") else G))
    ax=(x+36,y+26,x+w-12,y+h-22)
    def bars(n,stack=True,horiz=False,cols=(G,GR2)):
        if horiz:
            bh=(ax[3]-ax[1])/n
            for i in range(n):
                a=random.uniform(.3,1)*(1-i/(n*1.6)); b=a*random.uniform(.2,.6); L=ax[2]-ax[0]-30
                yy=ax[1]+i*bh; d.text((x+4,yy),f"Item {i+1}",font=fnt(9),fill="#000")
                d.rectangle([ax[0]+20,yy+2,ax[0]+20+a*L*.7,yy+bh-3],fill=cols[0])
                d.rectangle([ax[0]+20+a*L*.7,yy+2,ax[0]+20+(a*.7+b*.6)*L,yy+bh-3],fill=cols[1])
        else:
            bw=(ax[2]-ax[0])/n; pts=[]
            for i in range(n):
                a=random.uniform(.4,.75); b=random.uniform(.1,.25); H=ax[3]-ax[1]
                xx=ax[0]+i*bw+3; d.rectangle([xx,ax[3]-a*H,xx+bw-6,ax[3]],fill=cols[0])
                if stack: d.rectangle([xx,ax[3]-(a+b)*H,xx+bw-6,ax[3]-a*H],fill=cols[1])
                pts.append((xx+bw/2-3,ax[1]+random.uniform(.05,.35)*H))
                d.text((xx,ax[3]+3),(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] if n==7 else ["J","F","M","A","M","J","J","A","S","O","N","D","J","F","M","A","M","J","J","A","S","O"])[i%(7 if n==7 else 22)],font=fnt(9),fill="#000")
            return pts
    def line(n,col,lo=.2,hi=.8,width=2,dash=False):
        m=(lo+hi)/2; a=(hi-lo)/2; ph=random.uniform(0,6)
        pts=[(ax[0]+i*(ax[2]-ax[0])/(n-1),ax[3]-(m+a*(.6*math.sin(i/2.5+ph)+.4*random.uniform(-1,1)))*(ax[3]-ax[1])) for i in range(n)]
        for i in range(n-1):
            if dash and i%2: continue
            d.line([pts[i],pts[i+1]],fill=col,width=width)
        return pts
    if k=="kpi":
        n=5 if w>1000 else 1; cw=w/n
        for i in range(n):
            xx=x+i*cw
            AV={"Planned":"9,140","Executed":"8,040","Executed (exec date)":"8,110","Activities with sales (prov.)":"2,090","Sales count (prov.)":"2,410","Execution %":"88.0%"}
            if "Anchor" in v["fields"]: d.text((xx+12,y+24),AV.get(v["title"],"0"),font=fnt(26,True),fill="#000")
            else: d.text((xx+12,y+24),f"{random.randint(1,40)*1000+random.randint(0,999):,}" if not ("%" in v["title"] or (n==5 and i==3)) else "71.4%",font=fnt(26,True),fill="#000")
            if "Anchor" not in v["fields"]: d.text((xx+12,y+62),"PY 18,204",font=fnt(10),fill="#000"); d.text((xx+12,y+78),"MoM +4.2%",font=fnt(10,True),fill=G)
            else: d.text((xx+12,y+66),"Aug 2026 (anchor)",font=fnt(10),fill="#000")
            if "[SVG Bullet" in v["fields"]:
                bx=xx+110; d.rectangle([bx,y+62,bx+120,y+72],fill="#E6E9EB"); d.rectangle([bx,y+64,bx+84,y+70],fill=G); d.line([bx+112,y+59,bx+112,y+75],fill="#000",width=2); d.line([bx+76,y+60,bx+76,y+74],fill=GR2,width=2)
            if "[SVG Floating Bar" in v["fields"]:
                bx=xx+100; d.rectangle([bx,y+62,bx+80,y+72],fill="#E6E9EB"); d.rectangle([bx,y+62,bx+57,y+72],fill=G); d.rectangle([bx+57,y+64,bx+80,y+70],outline=RED); d.line([bx+80,y+59,bx+80,y+75],fill="#000",width=2)
            if "[SVG KPI Arrow" in v["fields"]:
                bx=xx+130; d.polygon([(bx,y+96-4),(bx+6,y+84),(bx+12,y+92)],fill=G); d.text((bx+16,y+82),"+4.2% MoM",font=fnt(9),fill="#000")
            if "[SVG Status Pill" in v["fields"]:
                bx=xx+150; d.rounded_rectangle([bx,y+80,bx+78,y+96],radius=8,fill="#C98A1A"); d.text((bx+8,y+82),"94% of plan",font=fnt(9),fill=W)
            if "[SVG" not in v["fields"] and "GAP" in v["fields"]:
                d.rectangle([xx+150,y+64,xx+232,y+82],outline=GR3); d.text((xx+154,y+67),"slot (gap)",font=fnt(9),fill=GR2)
    elif k=="funnel":
        for i,(lab,f) in enumerate([("Planned Activities",1),("Executed Activities",.71),("Activities With Sales",.24)]):
            st=(h-60)/3; bw=(w-40)*f; yy=y+40+i*st; d.rectangle([x+w/2-bw/2,yy,x+w/2+bw/2,yy+st-20],fill=[G,G3,LIME][i])
            d.text((x+w/2-60,yy+st/2-16),f"{lab}  {int(f*100)}%",font=fnt(10,True),fill=W if i<2 else "#000")
    elif k=="l12m":
        ML=["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"]
        CL=[("#BFBFBF","#7F7F7F"),("#7FB19F","#006341"),("#A9B4C2","#4A5A6E")]
        n=12; bw=(ax[2]-ax[0])/n; H=ax[3]-ax[1]-14
        for i in range(n):
            p_=random.uniform(.7,.9); vals=[p_,p_*random.uniform(.8,.95),p_*random.uniform(.2,.3)]
            for j,vv in enumerate(vals):
                xx=ax[0]+i*bw+2+j*(bw-4)/3; d.rectangle([xx,ax[3]-vv*H,xx+(bw-4)/3-1,ax[3]],fill=CL[j][1 if i==n-1 else 0])
            d.text((ax[0]+i*bw+2,ax[3]+3),ML[i],font=fnt(8),fill="#000")
        lx=ax[0]
        for (c0,c1),lab in zip(CL,["Planned","Executed","With sales (prov.)"]):
            d.rectangle([lx,ax[1]-4,lx+8,ax[1]+4],fill=c1); d.text((lx+11,ax[1]-5),lab,font=fnt(8),fill="#000"); lx+=d.textlength(lab,font=fnt(8))+24
        d.text((ax[0],ax[1]+8),"Aug 2026 selected: darker = selected month",font=fnt(8),fill="#000")
    elif k=="combo": bars(22 if w>800 else 12); line(22 if w>800 else 12,LIME,.5,.85); line(22 if w>800 else 12,GR,.4,.7,dash=True)
    elif k=="line2": line(22,G,.4,.8); line(22,GR2,.3,.7,dash=True)
    elif k=="stack": bars(22)
    elif k=="cols": bars(7,stack=False)
    elif k in("hbar","hbarstack"): bars(15 if (h<400 or "Top N 15" in v["fields"]) else 25,horiz=True,cols=(G,GR2))
    elif k=="gauge":
        cx,cy,r=x+w/2,y+150,80; d.pieslice([cx-r,cy-r,cx+r,cy+r],180,360,fill="#E6E9EB"); d.pieslice([cx-r,cy-r,cx+r,cy+r],180,180+180*.34,fill=LIME)
        d.ellipse([cx-r*.6,cy-r*.6,cx+r*.6,cy+r*.6],fill=W); d.rectangle([cx-r,cy,cx+r,cy+r],fill=W)
        a=math.radians(180+180*.30); d.line([cx+r*.62*math.cos(a),cy+r*.62*math.sin(a),cx+r*math.cos(a),cy+r*math.sin(a)],fill=GR,width=3)
        d.text((cx-22,cy-20),"34.0%",font=fnt(16,True),fill="#000"); d.text((cx-40,cy+14),"PY 30.0% (grey tick)",font=fnt(9),fill="#000")
        d.text((x+12,y+200),"+4.0 pp YoY",font=fnt(10,True),fill=G); d.text((x+12,y+218),"-0.6 pp MoM",font=fnt(10,True),fill=RED)
    elif k=="svgtable":
        hdr=["Name","Planned","Executed","Not Exec"]; f=v["fields"]
        extra=[c for c,key in (("Progress","SVG Execution Progress"),("Status","SVG Status Pill"),("Sparkline","SVG Sparkline"),("Bullet vs plan","SVG Bullet Executed vs Planned"),("Rate bullet","SVG Bullet Execution Rate vs Plan"),("Gap bar","SVG Floating Bar Gap to Plan"),("Dumbbell","SVG Dumbbell CY vs PY"),("MoM bar","SVG MoM Change Bar"),("No Sale","[Executed No Sale]")) if key in f]
        if "Matrix" in v["type"]: hdr[0]="BU > Region"
        cols=hdr+extra; tx=x+4; tw=w-8; nf=.18 if len(cols)>7 or tw<500 else .26; cw=[tw*nf]+[(tw*(1-nf))/(len(cols)-1)]*(len(cols)-1)
        yy=y+24; d.rectangle([tx,yy,tx+tw,yy+18],fill=G); cx=tx
        for c,wc in zip(cols,cw): d.text((cx+3,yy+3),c,font=fnt(10,True),fill=W); cx+=wc
        rows=int((h-50)/20)
        if "[SVG Status Pill]" in f: rows=min(rows,int((h-80)/20))
        if "Top N 15" in f: rows=min(rows,15)
        if "Top N 20" in f: rows=min(rows,20)
        for r in range(rows):
            ry=yy+20+r*20; cx=tx
            if r%2: d.rectangle([tx,ry,tx+tw,ry+20],fill="#F4F6F7")
            lab=(("+ " if r<3 else "   + ") if "Matrix" in v["type"] else "")+f"Item {r+1}"
            vals=[lab]+[f"{random.randint(50,900):,}" for _ in range(3)]
            for c,wc,val in zip(cols[:4],cw,vals): d.text((cx+3,ry+4),val,font=fnt(10),fill="#000"); cx+=wc
            for c,wc in zip(extra,cw[4:]):
                q=random.uniform(.4,.95); bw=min(80,wc-30)
                if c=="Progress": d.rectangle([cx+3,ry+6,cx+3+bw,ry+14],fill="#E6E9EB"); d.rectangle([cx+3,ry+6,cx+3+bw*q,ry+14],fill=G); d.text((cx+bw+6,ry+4),f"{int(q*100)}%",font=fnt(9),fill="#000")
                elif c=="Sparkline":
                    pts=[(cx+3+i*(min(wc-8,110))/11,ry+16-random.uniform(0,12)) for i in range(12)]; d.line(pts,fill=G,width=1); d.line([(p[0],min(ry+18,p[1]+6)) for p in pts],fill=GR2,width=1)
                elif c in("Bullet vs plan","Rate bullet"): d.rectangle([cx+3,ry+6,cx+3+bw,ry+14],fill="#E6E9EB"); d.rectangle([cx+3,ry+8,cx+3+bw*q,ry+12],fill=G); d.line([cx+3+bw*.7,ry+4,cx+3+bw*.7,ry+16],fill=GR,width=2)
                elif c=="Gap bar": a=bw*q; d.rectangle([cx+3,ry+6,cx+3+bw,ry+14],fill="#E6E9EB"); d.rectangle([cx+3,ry+6,cx+3+a,ry+14],fill=G); d.rectangle([cx+3+a,ry+8,cx+3+bw,ry+12],outline=RED); d.line([cx+3+bw,ry+3,cx+3+bw,ry+17],fill="#000",width=2)
                elif c=="Dumbbell": p1=cx+3+bw*random.uniform(.3,.9); p0=cx+3+bw*random.uniform(.3,.9); d.line([p0,ry+10,p1,ry+10],fill=GR3,width=2); d.ellipse([p0-4,ry+6,p0+4,ry+14],fill="#5E6A71"); d.ellipse([p1-4,ry+6,p1+4,ry+14],fill=G)
                elif c=="MoM bar": m0=cx+3+bw/2; dv=random.uniform(-.5,.5)*bw; d.line([m0,ry+3,m0,ry+17],fill=GR,width=1); d.rectangle([min(m0,m0+dv),ry+6,max(m0,m0+dv),ry+14],fill=G if dv>0 else RED)
                elif c.startswith("No Sale"): d.text((cx+3,ry+4),str(random.randint(0,40)),font=fnt(10),fill="#000")
                elif c=="Status":
                    pv=random.choice([random.randint(100,112),random.randint(90,99),random.randint(60,89)]); col=G if pv>=100 else ("#C98A1A" if pv>=90 else RED)
                    d.rounded_rectangle([cx+3,ry+3,cx+min(60,wc-4),ry+17],radius=7,fill=col); d.text((cx+12,ry+4),f"{pv}%",font=fnt(9),fill=W)
                cx+=wc
        if "Status" in extra:
            ly=y+h-34; lx=x+8
            for col,lab in ((G,">= 100% of plan"),("#C98A1A","90% to <100%"),(RED,"< 90%")):
                d.rounded_rectangle([lx,ly,lx+18,ly+10],radius=5,fill=col); d.text((lx+22,ly-1),lab,font=fnt(9),fill="#000"); lx+=d.textlength(lab,font=fnt(9))+36
    elif k=="waterfall":
        H=ax[3]-ax[1]; bw=(ax[2]-ax[0])/3-16; vals=[("Planned",1.0,0,G),("Not Executed",1.0,.71,GR2),("Executed",.71,0,G)]
        for i,(lab,top,bot,col) in enumerate(vals):
            xx=ax[0]+i*(bw+16); d.rectangle([xx,ax[3]-top*H*.9,xx+bw,ax[3]-bot*H*.9],fill=col); d.text((xx,ax[3]+3),lab,font=fnt(9),fill="#000"); d.text((xx+2,ax[3]-top*H*.9-12),["1,240","-354","886"][i],font=fnt(9,True),fill="#000")
    elif k=="wfmom":
        n=12; bw=(ax[2]-ax[0])/n; H=ax[3]-ax[1]; lvl=.5; mn="JFMAMJJASOND"
        for i in range(n):
            dv=random.uniform(-.12,.12); a,b=lvl,lvl+dv; xx=ax[0]+i*bw+2; d.rectangle([xx,ax[3]-max(a,b)*H,xx+bw-4,ax[3]-min(a,b)*H],fill=G if dv>0 else RED); d.text((xx+2,ax[3]+3),mn[i],font=fnt(9),fill="#000"); lvl=min(.9,max(.1,b))
    elif k=="hbardiv":
        n=20; bh=(ax[3]-ax[1])/n; m0=(ax[0]+ax[2])/2+20
        d.line([m0,ax[1],m0,ax[3]],fill=GR,width=1)
        for i in range(n):
            yy=ax[1]+i*bh; dv=(1-i/10)*random.uniform(.6,1) if i<10 else -((i-9)/10)*random.uniform(.6,1); L=(ax[2]-m0-8)*abs(dv)
            d.text((x+4,yy),("Top " if i<10 else "Bottom ")+str(i%10+1),font=fnt(9),fill="#000"); d.rectangle([m0 if dv>0 else m0-L,yy+2,m0+L if dv>0 else m0,yy+bh-2],fill=G if dv>0 else RED)
    elif k=="donut":
        cx,cy,r=x+w/2,y+h/2+8,min(w,h)/2-40; d.pieslice([cx-r,cy-r,cx+r,cy+r],-90,167,fill=G); d.pieslice([cx-r,cy-r,cx+r,cy+r],167,270,fill=GR2)
        d.ellipse([cx-r*.55,cy-r*.55,cx+r*.55,cy+r*.55],fill=W); d.text((cx-22,cy-6),"71% Yes",font=fnt(10,True),fill="#000")
    elif k=="scatter":
        for _ in range(40):
            px=random.uniform(ax[0],ax[2]); py=ax[3]-(px-ax[0])/(ax[2]-ax[0])*(ax[3]-ax[1])*random.uniform(.4,1); r=random.uniform(3,9)
            d.ellipse([px-r,py-r,px+r,py+r],fill=random.choice([G,LIME,G3,GR2]))
    elif k=="treemap":
        xs=ax[0]-28; ww=ax[2]-xs; hh=ax[3]-ax[1]; cols=[G,G3,LIME,G4,GR2,G2,LG,DK]
        for i,(fx,fy,fw,fh) in enumerate([(0,0,.45,1),(.45,0,.3,.6),(.75,0,.25,.6),(.45,.6,.2,.4),(.65,.6,.2,.4),(.85,.6,.15,.4)]):
            d.rectangle([xs+fx*ww,ax[1]+fy*hh,xs+(fx+fw)*ww-2,ax[1]+(fy+fh)*hh-2],fill=cols[i]); d.text((xs+fx*ww+4,ax[1]+fy*hh+4),f"Product {i+1}",font=fnt(9),fill=W if i in(0,1,5) else "#000")
    elif k=="decomp":
        for lvl in range(5):
            st=(w-30)/5; xx=x+14+lvl*st; d.text((xx,y+28),["BU","Region","MicroMkt","Branch","Banker"][lvl],font=fnt(10,True),fill="#000")
            for j in range(4 if lvl else 3):
                yy=y+50+j*50; L=random.uniform(.3,1)*(st-20); d.rectangle([xx,yy,xx+L,yy+16],fill=G if j==0 else GR3); d.text((xx,yy+18),f"Node {j+1}",font=fnt(9),fill="#000")
                if lvl<4 and j==0: d.line([xx+L,yy+8,xx+st,y+58],fill=GR2,width=1)
    elif k=="smallmult":
        cw=(w-16)/3; ch=(h-34)/3
        for i in range(9):
            cx=x+8+(i%3)*cw; cy=y+26+(i//3)*ch; d.rectangle([cx,cy,cx+cw-6,cy+ch-6],outline=GR3); d.text((cx+4,cy+2),("BU" if "BU" in v["title"] else "Region")+f" {i+1}",font=fnt(9),fill="#000")
            for col in (GR2,G):
                pts=[(cx+6+t*(cw-18)/9,cy+ch-12-random.uniform(.1,.7)*(ch-28)) for t in range(10)]; d.line(pts,fill=col,width=2)
    elif k=="ribbon":
        n=8; bw=(ax[2]-ax[0])/n; cols=[G,LIME,G3,G4,GR2,DK]
        for i in range(n):
            order=random.sample(range(6),6); yy=ax[1]
            for r in order:
                hh=(ax[3]-ax[1])/6*random.uniform(.6,1); d.rectangle([ax[0]+i*bw,yy,ax[0]+i*bw+bw*.6,yy+hh-2],fill=cols[r]); yy+=hh
    elif k=="heat":
        days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]; cw=(w-50)/7; rows=6; ch=(h-50)/rows
        for j,dn in enumerate(days):
            d.rectangle([x+42+j*cw,y+24,x+42+(j+1)*cw-1,y+40],fill=G); d.text((x+46+j*cw,y+26),dn,font=fnt(10),fill=W)
        for r in range(rows):
            d.text((x+6,y+44+r*ch),f"W{40+r}",font=fnt(9),fill="#000")
            for j in range(7):
                v=random.uniform(.05,.3) if j>4 else random.uniform(.3,1); c=tuple(int(255+(a-255)*v) for a in hexrgb(G))
                d.rectangle([x+42+j*cw,y+42+r*ch,x+42+(j+1)*cw-2,y+42+(r+1)*ch-2],fill=c)
    elif k=="daily":
        line(60,GR3,.3,.9,1); line(60,LIME,.2,.7,1); line(30,G,.4,.55,3); line(30,GR,.15,.25,1,True)
    elif k=="text":
        d.rectangle([x,y,x+w,y+22],fill=G); d.text((x+8,y+5),v["title"],font=fnt(11,True),fill=W)
        for i in range(int((h-40)/18)): d.text((x+10,y+32+i*18),"Lorem placeholder text line - paste from glossary_page.md"[:random.randint(30,58)],font=fnt(10),fill="#000")
def mock(p,alt=False,alt_hide=None):
    im=background(p); d=ImageDraw.Draw(im)
    for v in p["vis"]:
        if v.get("alt") and not alt: continue
        if alt and v["id"]==alt_hide: continue
        draw_vis(d,v)
    for v in p["vis"]:
        if v.get("alt") and not alt: continue
        if alt and v["id"]==alt_hide: continue
        if v["kind"] not in("slicer","info","reset","toggle","optional","next"): d.text((v["x"]+v["w"]-28,v["y"]+v["h"]-14),v["id"],font=fnt(9),fill=GR2)
    d.rectangle([900,14,1150,44],fill="#FFF4CC",outline=RED); d.text((910,21),"EXAMPLE DATA - not real values",font=fnt(12,True),fill=RED)
    return im
for p in pages: p["vis"]=slicers(p["sl"])+p["vis"]
def fn(p): return f"{p['n']}_{p['name'].split(' (')[0].replace(' ','_')}.png"
for p in pages:
    background(p).save(f"backgrounds/{fn(p)}"); mock(p).save(f"mockups/{fn(p)}")
    if any(v.get("alt") for v in p["vis"]):
        x0t=[v for v in p["vis"] if v.get("alt")][0]["x"]+6; aid=[v for v in p["vis"] if v.get("alt")][0]["id"]; im=mock(p,alt=True,alt_hide=aid[:-1]); ImageDraw.Draw(im).text((x0t,700),"Table view (Chart/Table bookmark)",font=fnt(9),fill=GR); im.save(f"mockups/{fn(p)[:-4]}_TableView.png")
# tooltip pages 320x240
TT=[("TT_Branch","MPO[Branch]"),("TT_Banker","MPO[BankerName]")]
for nm,fld in TT:
    im=Image.new("RGB",(320,240),W); d=ImageDraw.Draw(im); d.rectangle([0,0,320,24],fill=G); d.text((8,5),nm.replace("_"," ")+"  ("+fld+")",font=fnt(10,True),fill=W)
    for i,(lab,val) in enumerate([("Planned","1,240"),("Executed","886"),("Not Exec","354"),("Rate","71.4%")]):
        d.text((8+i*78,30),lab,font=fnt(9),fill="#000"); d.text((8+i*78,44),val,font=fnt(14,True),fill="#000")
    d.rectangle([8,70,312,86],fill="#FFF4CC",outline="#B7950B"); d.text((12,72),"[SVG Sparkline Executed] image",font=fnt(9,True),fill="#7D6608")
    pts=[(16+i*26,190-random.uniform(10,90)) for i in range(12)]; d.line(pts,fill=G,width=2); d.line([(p[0],min(200,p[1]+40)) for p in pts],fill=GR2,width=1)
    d.text((8,206),"Image 300x110 (or card image); grey = Not Executed",font=fnt(9),fill="#000")
    d.rectangle([190,222,318,238],fill="#FFF4CC",outline=RED); d.text((194,224),"EXAMPLE DATA",font=fnt(10,True),fill=RED)
    im.save(f"mockups/{nm}.png")
# spec md
o=["# GTM Dashboard - Visual layout spec","","Owner: Viz Designer. Canvas 1280 x 720 (16:9), page view 'Fit to page'. Theme: /workspace/corporate-theme/CorporateGreen.json (Arial 10, black text, 0 padding, column headers white on #006341). Coordinates are Format > General > Properties (x, y, width, height) in pixels. Backgrounds: viz/backgrounds/ (Canvas background > Image, Fit = Fit, transparency 0%). Mockups (EXAMPLE DATA): viz/mockups/. Generated by viz/build_viz.py - edit the script and re-run to change positions; the spec, backgrounds and mockups stay in sync.","",
"Names below are only those in dax/measures.dax and the MPO / DimDate / Product queries. Anything not yet available is listed under Gaps.","",
"## Shared rules","- Header band 0-56 px (green) with page title + subtitle baked into the background; lime rule at 56-59. Slicer strip y 64-104. Content area y 116-712, 16 px margins, 8 px gutters.",
"- Month axes: DimDate[YEAR_MONTH_KEY] (categorical, sorted ascending); display MONTH_SHORT_NAME via a hierarchy YEAR > MONTH_NAME if preferred. All dates are the planned date unless the measure says (Exec Date).",
"- Colours: Executed #006341, Not Executed #9AA5AB, Planned #C8D1D6, Sales/with sales #7AB800, PY lines grey #5E6A71 dashed. Positive variance #006341, negative #B03A2E (no #00A651).",
"- Every visual: title on, Arial 10 black, padding 0, border off (background panels supply the frame), tooltips default + report tooltip pages where noted.",
"- Info button (top-right, 1224,12,40,32) on every page navigates to Glossary. Reset button (1224,64,40,40) applies bookmark 'BM Reset - <page>' (Data only, current page).",
"- Slicers: dropdown, single-select off, 'Select all' on, Apply button on (DirectQuery).",""]
for p in pages:
    o+= [f"## Page {p['n']}: {p['name']}",f"_{p['sub']}_  ",f"Background: `backgrounds/{fn(p)}` | Mockup: `mockups/{fn(p)}`","",
         "| ID | Visual type | Title | Fields / measures | x | y | w | h |","|---|---|---|---|---|---|---|---|"]
    for v in p["vis"]:
        o.append(f"| {v['id']} | {v['type']} | {v['title']} | {v['fields']} | {v['x']} | {v['y']} | {v['w']} | {v['h']} |")
    o+=["",f"**Notes / formatting / interactions:** {p['notes']}",""]
o+=["## Story order and navigation",
"Exec Overview > Business Unit > Region > Branch > Banker (Individual) > [Banker Detail, drill-through] > Product (PROVISIONAL) > Company; supporting: Daily, Glossary; optional: Branch Detail. Drill spine BU > Region > MicroMarket > Branch > BankerName (MPO hierarchy + Level parameter).",
"- **Next >** button (1168,12,52,32) on each story page: Page navigation to the next page (Company -> Daily). Selections carry forward through synced slicers.",
"- Slicer sync: Year, Month, BU, Region, Branch synced and visible on all story pages (EXCEPT Business Unit, which uses Month Anchor Year/Month - NOT synced with DimDate; BU/Region/Branch still synced) + Daily (hidden-synced on Banker Detail, tooltip pages). Company on Company only. Product Group/Product on Product only. Metric (single select, default Not Executed) on Business Unit only. Level (single select, default Region) on Region only. Day on Daily only.","",
"## SVG image measures",
"Tag **SVG** = measure in dax/measures.dax folder 6. SVG. Re-checked 13:16 SAST: [SVG Bullet Executed vs Planned], [SVG Bullet Execution Rate vs Plan], revised [SVG Execution Progress] (plan end mark + PY tick) and revised [SVG Status Pill] (% of plan) are all in measures.dax with matching names, so no visual is pending DAX review.",
"- **Status pill legend (3 bands, user decision):** green #006341 >= 100% of plan; amber #C98A1A 90% to under 100%; red #B03A2E below 90%. Pill text = % of plan, white Arial 10. Show this legend as a text line under every table/matrix with a pill column (Exec Overview V4T, Business Unit V1, Region V3, Branch V4T, Banker V4, Banker Detail V3, Company V1) and on the Glossary page.",
"- Others: [SVG Sparkline Executed], [SVG Conversion Gauge] (provisional, Product page only), [SVG KPI Arrow Planned MoM], [SVG KPI Arrow Executed MoM], [SVG KPI Arrow Not Executed MoM], [SVG KPI Arrow Sales Count MoM] (provisional). Titles: [Title - Executed vs PY], [Title - Conversion], [Title - Banker Detail].",
"- **8. Comparison (verified in measures.dax 13:22 SAST, final per DAX Analyst, untested in Power BI):** [Gap to Plan], [Gap to Plan %], [Executed CY vs PY Diff], [Planned CY vs PY Diff], [Executed MoM Diff], [Plan Bridge Value], [Executed MoM Diff Rank (Up)], [Executed MoM Diff Rank (Down)], [MoM Top Bottom Flag] (1/0), [MoM Top Bottom Group] ('Top 10'/'Bottom 10'), [SVG Floating Bar Gap to Plan] (140x20), [SVG Dumbbell CY vs PY] (120x20, final), [SVG MoM Change Bar] (130x20; adapts to any level incl. the Level parameter). Every SVG measure: Data category = Image URL; table column width = image width + 6 px.",
"- **CY vs PY note:** [Executed CY vs PY Diff], [Planned CY vs PY Diff] and [SVG Dumbbell CY vs PY] are blank for 2025 because there is no 2024 data. Add a footnote on Business Unit V1 and Banker V4: 'PY comparison blank for 2025 (no 2024 data)'.",
"- **Plan Bridge waterfall:** disconnected table 'Plan Bridge' (dax/plan_bridge.tmdl, rows Planned / Not Executed). Category 'Plan Bridge'[Step] sorted by hidden 'Plan Bridge'[Order]; Y [Plan Bridge Value]; Total on, renamed 'Executed'.",
"- Target = Planned: bullet bar = Executed (or rate), black line = plan (Planned / 100%), grey tick = PY.",
"- Image sizes: progress, sparkline, bullets, dumbbell 120x20; floating gap bar 140x20; MoM change bar 130x20; pill 80x20; arrow 80x18; gauge 120x70. Grid image size H 20 / W 120.","",
"## Bookmarks",
"- BM Exec - Chart / BM Exec - Table (Exec Overview V4/V4T), BM Branch - Chart / BM Branch - Table (Branch V4/V4T), BM Company - Chart / BM Company - Table (Company V1/V1T, optional): Display only, Current page, Selected visuals.",
"- BM Reset - <page> per page (Data). Metric/Level fallback bookmarks only if field parameters fail in a visual.","",
"## Tooltip pages (hidden, 320 x 240). Mockups: mockups/TT_Branch.png, mockups/TT_Banker.png",
"| Page | Tooltip field | Visual | Fields | x | y | w | h |","|---|---|---|---|---|---|---|---|",
"| TT Branch | MPO[Branch] | Header text box | Branch name | 0 | 0 | 320 | 24 |",
"| TT Branch | | Multi-row card | [Planned Activities], [Executed Activities], [Not Executed], [Execution Rate %] | 8 | 28 | 304 | 40 |",
"| TT Branch | | Table image (SVG) | [SVG Sparkline Executed] 300x110 | 8 | 72 | 304 | 130 |",
"| TT Banker | MPO[BankerName] | same layout; card adds [Conversion %] (provisional) | | | | | |",
"Used by Exec Overview V4/V4T, Branch V4/V4T/V3, Product V4 (TT Branch); Banker V1/V2/V4 (TT Banker).","",
"## Drill-through",
"- **Banker Detail** (05a, hidden): MPO[BankerName], keep all filters. Sources: Banker V1/V2/V4, Business Unit V2 (banker node), Company V1.",
"- **Branch Detail** (OPTIONAL, hidden, same layout as Banker Detail): MPO[Branch]; V1 title fx: [Title - Branch Detail] (Format > Title > fx > Field value; untested, check in QA); V3 lists MPO[BankerName] with [Executed Activities], [Not Executed], [SVG Execution Progress], [SVG Status Pill]. Sources: Branch V4/V4T, Exec Overview V4. No title measure exists for it.","",
"## Interactions",
"- Default cross-filter. Waterfalls and the MoM bar cross-filter (all interactive). V5 BU bar filters page. Company V1/V1T and Branch V5 cross-filter. Region V2 filters V1/V3. Product gauge receives filters only.","",
"## Optional items",
"1. Branch Detail page (above). 2. Smart narrative on Exec Overview (e.g. in place of V7): 'Execution rate is [Execution Rate %], [Execution Rate YoY pp] vs PY.' 3. Metric swap also on Region V1 small multiples.","",
"## Gaps (for DAX Analyst / Data Modeler) - not invented here",
"1. (closed 13:16) Bullets and revised pill/progress are in measures.dax.",
"2. `Sales Count (Product)` still a stub; Product V2/V3 placeholders (#11, #3, #2).",
"3. (closed 13:17) Title measures now exist for Business Unit, Region, Branch, Company and Branch Detail; bound in this spec, not yet tested in Power BI.",
"4. Level parameter includes BankerName and Company; Region page uses only Region / MicroMarket (filter the Level slicer to those two items).",
"5. Open (user): sales date axis (#3), sales on not-executed rows (#2).",""]
open("layout_spec.md","w").write("\n".join(o))
# include slicers in spec for positions; also into mockups
