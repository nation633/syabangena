# Viz Designer v2 of Storyteller's build_baseline_mockups.py (PENDING tags, Gap arrow green on decrease). EXAMPLE DATA.
# Baseline-style enhanced mockups. ALL NUMBERS ARE EXAMPLE DATA.
import random
from PIL import Image, ImageDraw, ImageFont
random.seed(3)
G="#006341";LIME="#7AB800";GR="#9AA5AB";GR3="#E3E8EA";RED="#B03A2E";AMB="#C98A1A";K="#000000"
F="/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf";FB=F.replace("Regular","Bold")
f=lambda s,b=False:ImageFont.truetype(FB if b else F,s)
M=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov"]
def base(title):
    im=Image.new("RGB",(1280,720),"white");d=ImageDraw.Draw(im)
    d.rectangle([0,0,1280,40],fill=G);d.text((12,10),title,font=f(18,True),fill="white")
    d.text((900,12),"EXAMPLE DATA - not real figures",font=f(14,True),fill="#FFD7D7")
    d.text((12,46),"[PENDING N1/N2/N8] Data through 20 Nov (partial month)   |   until N3/N4 exist: partial month - the MoM % is not like-for-like",font=f(11),fill=AMB)
    return im,d
def panel(d,x,y,w,h,t):
    d.rectangle([x,y,x+w,y+h],outline=GR3);d.rectangle([x,y,x+w,y+20],fill=G);d.text((x+5,y+3),t,font=f(11,True),fill="white")
def pill(d,x,y,r):
    c=G if r>=1 else AMB if r>=.9 else RED;d.rounded_rectangle([x,y,x+56,y+14],7,fill=c);d.text((x+6,y+1),f"{int(r*100)}% plan",font=f(9,True),fill="white")
def prog(d,x,y,r,w=70):
    d.rectangle([x,y,x+w,y+10],fill=GR3);d.rectangle([x,y,x+int(w*r),y+10],fill=G);d.line([x+w,y-2,x+w,y+12],fill=K)
def floatbar(d,x,y,r,w=80):
    d.rectangle([x,y,x+w,y+10],fill=GR3);d.rectangle([x+int(w*r),y,x+w,y+10],fill=RED)
def dumb(d,x,y,a,b,w=70):
    xa,xb=x+int(w*a),x+int(w*b);d.line([min(xa,xb),y+5,max(xa,xb),y+5],fill=GR,width=2)
    d.ellipse([xb-4,y+1,xb+4,y+9],fill=GR);d.ellipse([xa-4,y+1,xa+4,y+9],fill=G)
def momcols(d,x,y,w,h,series,cols,partial=True,line=None):
    n=len(M);bw=(w-20)/n;mx=max(max(s) for s in series)
    for i in range(n):
        for j,s in enumerate(series):
            bh=s[i]/mx*(h-40);x0=x+10+i*bw+j*bw/len(series)*0.8
            fill=cols[j] if not(partial and i==n-1) else "#D5E5DC"
            d.rectangle([x0,y+h-15-bh,x0+bw/len(series)*0.75,y+h-15],fill=fill,outline=cols[j] if partial and i==n-1 else None)
        d.text((x+10+i*bw,y+h-13),M[i],font=f(9),fill=K)
    # label only Executed last full month
    i=n-2;d.text((x+10+i*bw,y+22),f"{series[1][i]:,}",font=f(9,True),fill=G)
    if line:
        pts=[(x+10+i*bw+bw/2,y+30+(1-v)*(h-60)) for i,v in enumerate(line)];d.line(pts,fill=K,width=2)
        d.text((pts[-2][0]-10,pts[-2][1]-14),f"{line[-2]:.0%}",font=f(9,True),fill=K)
def kpis(im,d,items,y=64):
    w=1256//len(items)
    for i,(t,v,dl) in enumerate(items):
        x=12+i*w;d.rectangle([x,y,x+w-8,y+70],outline=GR3);d.text((x+6,y+4),t,font=f(10),fill=K)
        d.text((x+6,y+20),v,font=f(20,True),fill=G)
        if dl is None: d.text((x+6,y+50),"Aug 2026 (Month Anchor)",font=f(9),fill=K); continue
        up=dl>=0;rev=("Gap" in t or "Not Exec" in t);good=(not up) if rev else up;c=G if good else RED
        d.text((x+6,y+50),("▲ " if up else "▼ ")+f"{dl:+.1%} vs PM",font=f(9),fill=c)
def matrix(d,x,y,rows,hdr,cw):
    d.rectangle([x,y,x+sum(cw),y+16],fill=G);cx=x
    for h,w in zip(hdr,cw):d.text((cx+3,y+2),h,font=f(9,True),fill="white");cx+=w
    for r,row in enumerate(rows):
        yy=y+18+r*18;cx=x
        for c,(val,w) in enumerate(zip(row,cw)):
            if callable(val):val(d,cx+3,yy+3)
            else:d.text((cx+3,yy+2),str(val),font=f(9,r==len(rows)-1 and row[0]=="Total"),fill=K)
            cx+=w
def ex(n):return [int(random.uniform(.8,1.2)*n) for _ in M]

# 1 Exec Overview
im,d=base("Executive Overview  (enhanced baseline)")
kpis(im,d,[("Planned Activities","12,480",.031),("Executed Activities","10,912",.024),("Gap to Plan | 12.6%","1,568",-.04),("Activities with a Sale","2,904",.012),("Sales Made During Activities","3,377",-.018),("Execution Rate %","87.4%",.006),("Exec. Activities Conversion %","26.6%",-.004)])
d.text((12+5*179+6,64+36),"",font=f(9));pill(d,12+5*179+110,90,.874);prog(d,12+5*179+110,108,.874,56)
panel(d,12,145,620,250,"Planned vs Executed MoM + Execution %  (labels: last full month only; Nov light = PENDING N2)")
P=ex(12000);E=[int(p*random.uniform(.82,.95)) for p in P];momcols(d,12,165,620,230,[P,E],[GR,G],line=[e/p for e,p in zip(E,P)])
panel(d,642,145,626,250,"Plan Bridge waterfall: Planned > Not Executed > Executed")
bars=[("Planned",12480,0,GR),("Not Executed",1568,10912,RED),("Executed",10912,0,G)]
for i,(n,v,b,c) in enumerate(bars):
    x=700+i*180;sc=190/12480;d.rectangle([x,385-(b+v)*sc,x+110,385-b*sc],fill=c);d.text((x,388-(b+v)*sc-14),f"{v:,}",font=f(10,True),fill=K);d.text((x,388),n,font=f(10),fill=K)
panel(d,12,405,800,305,"BU matrix: + progress, floating gap bar, pill, CY vs PY dumbbell")
bus=["BU A","BU B","BU C","BU D","ROUTE 99 (grey: PENDING N5)"];rows=[]
for b in bus:
    p=random.randint(1500,4000) if "ROUTE" not in b else 12;e=int(p*random.uniform(.8,1.0));r=e/p
    rows.append([b,f"{p:,}",f"{e:,}",(lambda d,x,y,r=r:prog(d,x,y,r)),(lambda d,x,y,r=r:floatbar(d,x,y,r)),f"{p-e:,}",f"{int(e*.27):,}",f"{int(e*.31):,}",(lambda d,x,y,r=r:pill(d,x,y,r)),(lambda d,x,y,r=r:dumb(d,x,y,r,r-.04))])
matrix(d,20,430,rows,["Business Unit","Planned","Executed","Progress","Gap to Plan","Not Exec.","Act. w Sale","Sales","Status","CY vs PY"],[150,60,60,80,90,60,65,55,70,90])
d.text((20,560),"Legend: pill green >=100% of plan, amber 90-<100%, red <90%; dumbbell green = CY rate, grey = PY rate",font=f(9),fill=GR)
panel(d,822,405,446,145,"Executed MoM change (waterfall, Executed MoM Diff)")
v=0
for i in range(10):
    dd=random.randint(-300,400);c=G if dd>=0 else RED;x=835+i*42;y0=500-v*0.1;y1=500-(v+dd)*0.1;d.rectangle([x,min(y0,y1),x+30,max(y0,y1)],fill=c);v+=dd;d.text((x,535),M[i+1],font=f(9),fill=K)
panel(d,822,560,446,150,"Daily Executed Vol + Executed 7D Avg line")
pts=[]
for i in range(20):
    h=random.randint(40,100);x=835+i*21;d.rectangle([x,700-h,x+14,700],fill=G);pts.append((x+7,700-h+random.randint(-10,10)))
d.line(pts,fill=LIME,width=2)
im.save("viz/baseline/mockups/01_Exec_Overview_enhanced_v2.png")

# 2 Business Unit
im,d=base("Business Unit  (enhanced baseline)")
kpis(im,d,[("Anchor Planned","9,140",None),("Anchor Executed","8,040",None),("Anchor Executed (Exec Date)","8,110",None),("Anchor Act. With Sales (prov.)","2,090",None),("Anchor Sales Count (prov.)","2,410",None),("Anchor Execution %","88.0%",None)])
for i,(t,v) in enumerate([("Year (Month Anchor)","2026"),("Month (Month Anchor)","Aug")]):
    x=800+i*235;d.rectangle([x,43,x+228,59],outline=GR,fill="white");d.text((x+4,45),f"{t}: {v}  v  single, NOT synced",font=f(9),fill=K)
panel(d,12,145,620,250,"[fx: L12M Title] Planned, executed and activities with sales, Sep 2025 - Aug 2026")
L12=["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"]
CL=[("#BFBFBF","#7F7F7F"),("#7FB19F","#006341"),("#A9B4C2","#4A5A6E")]
P=[random.randint(6500,9000) for _ in L12];mx=max(P);bw=600/12
for i,pv in enumerate(P):
    for j,vv in enumerate([pv,int(pv*.88),int(pv*.88*.26)]):
        bh=vv/mx*180;x0=22+i*bw+j*bw*0.27;d.rectangle([x0,380-bh,x0+bw*0.25,380],fill=CL[j][1 if i==11 else 0])
    d.text((26+i*bw,382),L12[i],font=f(9),fill=K)
lx=20
for (c0,c1),lab in zip(CL,["Planned","Executed","Activities With Sales (prov.)"]):
    d.rectangle([lx,170,lx+9,179],fill=c1);d.text((lx+12,169),lab,font=f(9),fill=K);lx+=int(d.textlength(lab,font=f(9)))+30
d.text((lx,169),"Aug 2026 selected = darker; tooltip shows year",font=f(9),fill=K)
panel(d,642,145,626,250,"Executed split: with Sale vs No Sale per BU (stacked 100%, replaces donut)")
for i,b in enumerate(["BU A","BU B","BU C","BU D"]):
    y=180+i*48;r=random.uniform(.2,.35);d.text((652,y+8),b,font=f(10),fill=K);d.rectangle([720,y,1240,y+28],fill=GR);d.rectangle([720,y,720+520*r,y+28],fill=LIME);d.text((725,y+8),f"{r:.0%} with sale",font=f(9,True),fill=K);d.text((1150,y+8),f"{1-r:.0%} no sale",font=f(9,True),fill="white")
panel(d,12,405,860,305,"BU table (title: Title - Business Unit): bullet, gap bar, dumbbell, pill, sparkline, MoM change")
rows=[]
for b in ["BU A","BU B","BU C","BU D"]:
    p=random.randint(1500,4000);e=int(p*random.uniform(.85,1.0));r=e/p;m=random.uniform(-1,1)
    rows.append([b,f"{p:,}",f"{e:,}",(lambda d,x,y,r=r:prog(d,x,y,r)),(lambda d,x,y,r=r:floatbar(d,x,y,r)),(lambda d,x,y,r=r:dumb(d,x,y,r,r-.03)),f"{random.randint(-120,150):+}",(lambda d,x,y,r=r:pill(d,x,y,r)),(lambda d,x,y:d.line([(x+i*8,y+10-random.randint(0,10)) for i in range(9)],fill=G,width=2)),(lambda d,x,y,m=m:(d.line([x+50,y-2,x+50,y+12],fill=K),d.rectangle([min(x+50,x+50+m*45),y,max(x+50,x+50+m*45),y+10],fill=G if m>0 else RED)))])
matrix(d,20,430,rows,["BU","Planned","Executed","Bullet","Gap to Plan","CY vs PY","Exec CY-PY","Status","Trend","MoM change"],[70,60,60,80,90,85,70,70,80,110])
panel(d,882,405,386,305,"BU Executed vs Sale + conversion % (one label per circle)")
for i in range(4):
    x=900+i*90;e=random.randint(120,200);s=int(e*.27);d.rectangle([x,690-e,x+30,690],fill=G);d.rectangle([x+32,690-s,x+62,690],fill=LIME);d.ellipse([x+14,690-e-40,x+48,690-e-6],outline=G,width=2);d.text((x+18,690-e-30),"27%",font=f(9,True),fill=K)
im.save("viz/baseline/mockups/02_Business_Unit_enhanced_v2.png")

# 3 Region
im,d=base("Region  (enhanced baseline)")
panel(d,12,64,620,240,"Planned vs Executed vs Sale MoM (Nov light = PENDING N2)")
P=ex(6000);E=[int(p*.87) for p in P];S=[int(e*.25) for e in E];momcols(d,12,84,620,220,[P,E,S],[GR,G,LIME])
panel(d,642,64,626,240,"Executed + Gap to Plan by BU (floating bar, replaces Not Executed bar)")
for i,b in enumerate(["BU A","BU B","BU C","BU D"]):
    y=100+i*48;r=random.uniform(.8,.97);d.text((652,y+8),b,font=f(10),fill=K);d.rectangle([720,y,720+500*r,y+28],fill=G);d.rectangle([720+500*r,y,1220,y+28],fill=RED);d.text((1225,y+8),f"{int((1-r)*900)}",font=f(9,True),fill=RED)
panel(d,12,314,620,396,"MTD product matrix by Region (report's own columns) + data bars + progress")
prods=["Credit Card","Funeral","Invest.","Overdraft","Pers. Loans","Transact."]
rows=[]
for rg in ["Region 1","Region 2","Region 3","Region 4","Region 5","Region 6"]:
    r=random.uniform(.8,1.0);vals=[random.randint(5,120) for _ in prods]
    rows.append([rg]+[(lambda d,x,y,v=v:(d.rectangle([x,y,x+v*0.5,y+10],fill="#CFE6B0"),d.text((x+2,y-1),str(v),font=f(9),fill=K))) for v in vals]+[(lambda d,x,y,r=r:prog(d,x,y,r,60))])
matrix(d,20,340,rows,["Region"]+prods+["Progress"],[70,75,65,65,75,75,75,80])
panel(d,642,314,626,396,"Region table (Title - Region): pill, dumbbell, MoM change, Top/Bottom 10")
rows=[]
for rg in ["Region 1","Region 2","Region 3","Region 4","Region 5","Region 6"]:
    r=random.uniform(.82,1.0);m=random.uniform(-1,1)
    rows.append([rg,f"{random.randint(600,2000):,}",(lambda d,x,y,r=r:pill(d,x,y,r)),(lambda d,x,y,r=r:dumb(d,x,y,r,r-.05)),(lambda d,x,y,m=m:(d.line([x+55,y-2,x+55,y+12],fill=K),d.rectangle([min(x+55,x+55+m*50),y,max(x+55,x+55+m*50),y+10],fill=G if m>0 else RED))),"Top 10" if m>0 else "Bottom 10"])
matrix(d,650,340,rows,["Region","Executed","Status","CY vs PY","MoM change","Group"],[90,80,80,100,130,90])
d.text((650,480),"Region sales % donut -> stacked 100% bar of Sales Count share by Region:",font=f(10,True),fill=K)
x=650
for i,s in enumerate([.24,.2,.18,.15,.13,.10]):
    w=600*s;d.rectangle([x,500,x+w,530],fill=[G,LIME,GR,"#4D8B70","#A3C9B8","#5E6A71"][i]);d.text((x+3,508),f"R{i+1} {s:.0%}",font=f(9,True),fill="white" if i in(0,3,5) else K);x+=w
im.save("viz/baseline/mockups/03_Region_enhanced_v2.png")
print("ok")
