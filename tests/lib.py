"""Shared test library for the Pump + Cardio Playwright suites.

Every suite imports from here instead of carrying its own copy of the page setup, the
style-standard audit and the timer runner. Fix something once and every suite gets it.

    from lib import *            # ok, ls, sec, view, opend, fin, run_block, audit, ...
    with sync_playwright() as pw:
        b=launch(pw)
        c,p=view(b,"2026-11-07",{"wo_alt":{"2026-11-07":1}})

Timers: run_block(p, tid) drives a guided block to the end the fast way. The app's engine is
timestamp based and loop() only renders, so the clock can jump inside a segment and then tick
across each boundary; every boundary beep, the countdown and the done flag are still verified,
but a 30 minute walk costs a fraction of a second instead of 30 s of 250 ms ticks.
"""
import os, re, json, datetime as dt
CHROME=os.environ.get("CHROME") or None  # CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
URL=os.environ.get("PC_URL") or "http://localhost:8765/index.html"
res=[];errs=[]
def ok(n,c,i=""):
    res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
def done():
    """Print the suite total; exit code 1 when anything failed (scripts/test.sh reads both)."""
    print(f"{sum(res)}/{len(res)} passed"); return 0 if all(res) else 1
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
def sec(s):
    m=re.search(r"(\d+):(\d\d)",s or ""); return int(m.group(1))*60+int(m.group(2)) if m else -1
HOOK="""window.__bp=[];window.__osc=0;window.__vib=0;
(function(){var C=window.AudioContext||window.webkitAudioContext;if(C){var o=C.prototype.createOscillator;C.prototype.createOscillator=function(){window.__osc++;return o.apply(this,arguments);};}
try{navigator.vibrate=function(){window.__vib++;return true;};}catch(e){}})();"""
def launch(pw): return pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox","--autoplay-policy=no-user-gesture-required"])
def view(b,d,seed=None,hour=9,open_day=True):
    """A fresh iPhone-sized context on date d (localStorage seeded with `seed`), with the day panel open."""
    y,m,dd=map(int,d.split("-"))
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block")
    c.add_init_script(HOOK);p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda x:x.accept())
    p.clock.install(time=dt.datetime(y,m,dd,hour,0));p.goto(URL)
    p.evaluate("t=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');for(var k in t)localStorage.setItem(k,JSON.stringify(t[k]));}",seed or {})
    p.reload();p.wait_for_selector("#week button.day",timeout=10000);p.wait_for_timeout(80)
    if open_day and not p.locator("#panel.open").count(): p.click(f'button.day[data-d="{d}"]');p.wait_for_selector("#panel.open",timeout=5000);p.wait_for_timeout(100)
    return c,p
def opend(p,d):
    if p.locator("#panel.open").count(): p.click("#close")
    p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(150)
def fin(p):
    """Finish workout and wait for the summary overlay (then its 700 ms tap guard). The app ignores a second tap
    within 1.5 s (finBusy), so if the overlay doesn't show, move the clock on and tap again."""
    for _ in range(3):
        p.click("#fin")
        try: p.wait_for_selector("#ov.show",timeout=1500);break
        except Exception: p.clock.run_for(2000);p.wait_for_timeout(80)
    p.clock.fast_forward(1000);p.wait_for_timeout(120)
def tick(p,x,i):
    """Tick set i of exercise x in list mode (closes the reps stepper if it opens)."""
    p.locator(f'.srow[data-x="{x}"] [data-tk]').nth(i).click();p.wait_for_timeout(30)
def run_block(p,tid,d=None):
    """Start guided block `tid` and drive it to the end quickly. Returns a dict with what was seen:
    segs, total, beeps (count), osc, done (flag written), ask (locked prompt shown), first (first time shown),
    drops (countdown advanced during the first seconds). Every segment boundary is crossed with real ticks."""
    d=d or p.evaluate("()=>__app.sel")
    p.evaluate("()=>{window.__bp=[];window.__osc=0}")
    p.locator(f'#sess [data-t="{tid}"]').first.click();p.wait_for_timeout(40)
    T=ls(p,"wo_timer");segs=T["segs"];tot=sum(x[1] for x in segs)
    first=p.locator("#time").inner_text();t0=sec(first)
    p.clock.run_for(1500);p.wait_for_timeout(20);t1=sec(p.locator("#time").inner_text())
    el=1.5;acc=0
    for g in segs:
        acc+=g[1];target=acc-1.0
        if target>el+0.5: p.clock.fast_forward(int((target-el)*1000));el=target
        p.clock.run_for(1500);el+=1.5;p.wait_for_timeout(15)
    p.clock.run_for(1200);p.wait_for_timeout(60)
    for _ in range(8):  # under heavy parallel load a tick can lag: give the engine a few more seconds of clock to finish
        st=ls(p,"wo_"+d) or {}
        if (st.get("s") or {}).get(tid)==1 or p.locator("#bar.ask").count(): break
        p.clock.run_for(1000);p.wait_for_timeout(40)
    st=ls(p,"wo_"+d) or {}
    return {"segs":segs,"total":tot,"beeps":p.evaluate("window.__bp.length"),"osc":p.evaluate("window.__osc"),
            "done":(st.get("s") or {}).get(tid)==1,"ask":p.locator("#bar.ask").count()==1,"first":first,"drops":t1<t0 or t0<=3}
# ---------------- views in the data ----------------
def weeks(p):
    """Mondays of every programmed week in PROG (ascending)."""
    days=sorted(p.evaluate("()=>Object.keys(__wk.PROG)"))
    out=[]
    for d in days:
        y,m,dd=map(int,d.split("-"));x=dt.date(y,m,dd);mon=(x-dt.timedelta(days=x.weekday())).isoformat()
        if mon not in out: out.append(mon)
    return out
def week_views(p,monday):
    """All views a week offers: (date, type, seed) for main, backup, quick option and run-instead variants."""
    y,m,dd=map(int,monday.split("-"));days=[(dt.date(y,m,dd)+dt.timedelta(days=i)).isoformat() for i in range(7)]
    info=p.evaluate("""ds=>ds.map(function(d){var W=__wk,S=__how.SESS,mn=W.PROG[d],bk=W.BK[d],qk=(W.QK||{})[d];
      var ri=function(k){return !!(k&&S[k]&&S[k].blocks.some(function(b){return b.ri;}));};
      return {d:d,main:!!(mn&&S[mn]),bk:!!(bk&&S[bk]),qk:!!(qk&&S[qk]),rim:ri(mn),rib:ri(bk)};})""",days)
    out=[]
    for i in info:
        d=i["d"]
        if not i["main"]: continue
        out.append((d,"main",{}))
        if i["rim"]: out.append((d,"run",{"wo_ri":{d:1}}))
        if i["bk"]:
            out.append((d,"backup",{"wo_alt":{d:1}}))
            if i["rib"]: out.append((d,"backup+run",{"wo_alt":{d:1},"wo_ri":{d:1}}))
        if i["qk"]: out.append((d,"quick",{"wo_quick":{d:1}}))
    return out
# ---------------- app-style-standard.md audit (§1/§2/§3/§6/§9/§10/§11) ----------------
GUIDED=r"Warm-up|Every 2:00 × \d+|EMOM \d+ s × \d+|Intervals|Circuit × \d+|Steady|Flow|Cool-down"
STRENGTH=r"Straight sets|Superset|Tri-set"
HDR=re.compile(r"^\d+ · (?:([A-C]) · )?("+GUIDED+"|"+STRENGTH+r") · (?:(\d+:\d\d)|(\d+) (rounds|sets))$")
EW=r"\b(easy|steady|moderate|hard)\b"
BAND={"easy":(3,4),"steady":(5,6),"moderate":(7,7)}
def rpes(t): return [(int(a),int(b or a)) for a,b in re.findall(r"RPE (\d+)(?:–(\d+))?",t)]
def effort_ok(texts):
    """§6: every effort word comes with an RPE from its band, and every RPE written next to effort words sits in one of their bands."""
    t=" ".join(x for x in texts if x)
    words={w.lower() for w in re.findall(EW,t,re.I)}
    if "hard" in words: return False,"hard"
    if not words: return True,""
    rs=rpes(t)
    if not rs: return False,("no RPE",words)
    for w in words:
        lo,hi=BAND[w]
        if not any(lo<=a and b<=hi for a,b in rs): return False,(w,rs)
    for a,b in rs:
        if not any(BAND[w][0]<=a and b<=BAND[w][1] for w in words): return False,(rs,words)
    return True,""
DOM="""()=>{var V=__app.view(),out=[],cur=null,bi=0,ex=V.blocks.filter(function(b){return b.k=="timer"||b.k=="ex";});
 [].forEach.call(document.getElementById('sess').children,function(el){
  var h=el.tagName=="H2"?el:(el.classList.contains("bh")?el.querySelector("h2"):null);
  if(h&&/^(Optional|Actual|Extra|How did it go\?)$/.test(h.textContent)){cur=null;return;}
  if(h){var b=ex[bi++];cur={hdr:h.textContent,kind:b.k,id:b.id||"",flow:!!b.flow,segs:b.segs||[],items:(b.items||[]).map(function(i){return i.lab;}),n:b.n||0,rr:b.rr||null,rest:b.rest||0,title:"",note:"",small:[],list:[],sm:0,btns:[],names:[],gn:[]};out.push(cur);return;}
  if(!cur)return;
  if(el.classList.contains("gn"))cur.gn.push(el.textContent);
  if(el.classList.contains("sp"))cur.small.push(el.textContent);
  if(el.classList.contains("card")){var n=el.querySelector(".hd .name, :scope > .name");
   if(el.classList.contains("ex")){el.querySelectorAll(".mvh .mvn").forEach(function(x){cur.names.push(x.textContent);});cur.rows=el.querySelectorAll(".srow").length;}
   else{cur.title=n.textContent;var nt=el.querySelector(":scope > .note");cur.note=nt?nt.textContent:"";
    el.querySelectorAll(":scope > .sp").forEach(function(x){cur.small.push(x.textContent);});
    el.querySelectorAll(".lst li").forEach(function(x){cur.list.push(x.textContent);});
    cur.sm=el.querySelectorAll("[data-sm]").length;}
   el.querySelectorAll("[data-t]").forEach(function(x){cur.btns.push(x.textContent);});}
  if(el.matches&&el.matches("button[data-t]"))cur.btns.push(el.textContent);});
 return {name:V.name,safe:document.getElementById('safe1').textContent,stop:document.querySelector('.safe .stop').textContent,stopVis:!document.querySelector('.safe .stop').hidden,
  dnote:document.getElementById('dnote').textContent,blocks:out,sess:document.getElementById('sess').innerText,
  tids:[...document.querySelectorAll('#sess [data-t]')].map(function(e){return e.dataset.t;}).filter(function(x){return x.indexOf('rest:')!=0;})};}"""
def read_view(p): return p.evaluate(DOM)
def audit_view(vw,V,dev):
    """Check one rendered view against the standard; append every deviation to `dev`."""
    def chk(where,rule,cond,info=""):
        if not cond: dev.append(f"{where} · {rule} · {info}")
    chk(vw,"§11 safety ≤160",len(V["safe"])<=160,len(V["safe"]))
    chk(vw,"stop-signs line visible",V["stopVis"] and "sudden or severe headache" in V["stop"])
    e=effort_ok([V["safe"]]);chk(vw,"§6 safety effort",e[0],(V["safe"],e[1]))
    chk(vw,"no head-down / breath-hold advice",not re.search(r"head-down position(?!s)|hold your breath(?!.)",V["sess"]))
    hasEx=any(x["kind"]=="ex" for x in V["blocks"])
    chk(vw,"day total ≈ only when strength estimates are included",("≈" in V["dnote"])==hasEx,V["dnote"])
    for bl in V["blocks"]:
        where=f"{vw} · {bl['hdr']}"
        m=HDR.match(bl["hdr"])
        chk(where,"§1 header format",m and len(bl["hdr"])<=32,bl["hdr"])
        if not m: continue
        fmt=m.group(2);tot=sum(x[1] for x in bl["segs"])
        if bl["kind"]=="ex":
            chk(where,"strength header: count, no time",m.group(3) is None and m.group(4)==str(bl["n"]) and m.group(5)==("sets" if len(bl["items"])==1 else "rounds"),bl["hdr"])
            chk(where,"strength format",re.fullmatch(STRENGTH,fmt),fmt)
            chk(where,"strength has no guided timer button",not bl["btns"],bl["btns"])
            ins=bl["gn"][0] if bl["gn"] else ""
            exp="Each "+("set" if len(bl["items"])==1 else "round")+": "+" → ".join(bl["items"])+f". Rest {bl['rr'][0]}–{bl['rr'][1]} s."
            chk(where,"§2 strength instruction line",ins==exp and len(ins)<=60,(ins,exp))
            chk(where,"rest timer = middle of prescribed range",bl["rr"] and bl["rest"]==(bl["rr"][0]+bl["rr"][1])/2,(bl["rr"],bl["rest"]))
            for nm in bl["names"]: chk(where,"§11 move name ≤36",len(nm)<=36,nm)
            for nm in bl["names"]: chk(where,"R5 kettlebell/dumbbell spelt out, one move per name",not re.search(r"\b(KB|DB)\b| or ",nm),nm)
        else:
            chk(where,"guided format",re.fullmatch(GUIDED,fmt),fmt)
            chk(where,"header time = timer total",m.group(3) and sec(m.group(3))==tot,(bl["hdr"],tot))
            chk(where,"§11 title ≤30",len(bl["title"])<=30,bl["title"])
            note=bl["note"]
            if bl["flow"]: pat=r"Each move: time shown · sides cued\."
            elif fmt=="Intervals": pat=r"Each round: \d+:\d\d work · \d+:\d\d rest\. (Easy|Steady|Moderate) pace, RPE \d(–\d)?\."
            elif fmt.startswith("Circuit"): pat=r"Each round: [\d–]+ s per move · \d+ s rest\."
            elif fmt.startswith("Every") or fmt.startswith("EMOM"): pat=r"Each (round|\d+ s): .+\."
            else: pat=r"(Easy|Steady|Moderate) (pace|walk|row|run)(, Zone \d(–\d)?)?, RPE \d(–\d)?\."
            chk(where,"§2 instruction line",re.fullmatch(pat,note) and len(note)<=60,note)
            for x in bl["small"]: chk(where,"§2 small print ≤70",len(x)<=70,x)
            labels=[str(x[2]) if len(x)>2 else "" for x in bl["segs"]]
            e=effort_ok([bl["title"],note]+bl["small"]+labels);chk(where,"§6 effort word ↔ RPE band",e[0],e[1])
            btn=[x for x in bl["btns"] if "walk break" not in x]
            want=("Start guided flow" if bl["flow"] else "Start guided timer")+" · "+(m.group(3) or "")
            chk(where,"§9 button label",len(btn)==1 and btn[0] in (want,"✓ Done · run guided timer again · "+(m.group(3) or "")),(btn,want))
            if bl["flow"]: chk(where,"§10 flow moves collapsed",bl["sm"]==1 and not bl["list"])
            elif fmt.startswith("Circuit"): chk(where,"§10 circuit moves expanded",bl["sm"]==0 and len(bl["list"])>=3,bl["list"])
            for x in bl["list"]: chk(where,"§11 move line ≤36",len(x)<=36,x)
            for x in bl["list"]+labels: chk(where,"§3 'each side' spelled out",not re.search(r"per side|/side|\bL/R\b",x),x)
            g=bl["segs"]
            if len(g)>1:
                chk(where,"no trailing REST/READY",g[-1][0] not in ("REST","READY"),g[-1])
                chk(where,"no READY segments (one 10 s get-ready is added at start)",not [x for x in g if x[0]=="READY"])
                chk(where,"no combined switch / round labels",not [x for x in labels if re.search(r"switch →|round \d|Interval \d|set \d",x)],labels[:3])
                left=[x for x in labels if x.endswith(" · left")];right=[x for x in labels if x.endswith(" · right")]
                chk(where,"sides written as left / right moves",len(left)==len(right) or fmt.startswith("EMOM") or fmt.startswith("Every"),(len(left),len(right)))
                if not (fmt.startswith("EMOM") or fmt.startswith("Every")): chk(where,"'each side' only inside an EMOM minute",not [x for x in labels if "each side" in x])
                rests=[x[1] for x in g if x[0]=="REST"]
                chk(where,"every rest ≥10 s",all(r>=10 for r in rests),rests)
                if fmt.startswith("Every") or fmt.startswith("EMOM"):
                    win=sec(fmt) if ":" in fmt else int(re.search(r"(\d+) s",fmt).group(1));n=int(re.search(r"× (\d+)",fmt).group(1))
                    chk(where,f"EMOM/Every = {n} segments of {win} s, all WORK",len(g)==n and all(x[0]=="WORK" and x[1]==win for x in g),[x[:2] for x in g][:4])
            if bl["flow"]: chk(where,"flow has its moves list",len(bl["segs"])>1)
    txt=V["sess"]+" "+V["safe"]
    chk(vw,"§6 no combined effort terms",not re.search(r"(easy|steady|moderate|hard)\s*[-–/(]+\s*(easy|steady|moderate|hard)|steady-state",txt,re.I))
    chk(vw,"§6 no 'hard'",not re.search(r"\bhard\b",txt,re.I))
    chk(vw,"§6 no numeric paces",not re.search(r"min/km|km/h|/500|drag factor|\d:\d\d–\d:\d\d/",txt))
    notsmall=[x for bl in V["blocks"] for x in [bl["title"],bl["note"]]+bl["gn"]+[str(s[2]) for s in bl["segs"] if len(s)>2]]
    chk(vw,"§6 stroke rate only in small print",not [x for x in notsmall if "s/m" in x],[x for x in notsmall if "s/m" in x][:2])
