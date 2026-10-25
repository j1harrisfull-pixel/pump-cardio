import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v29: week 2 (Mon 19 – Sun 25 Oct). Same app-style-standard audit as test_v28 on every week-2 view, plus
# week-1 history intact, programme mapping, How-to coverage, medical rules, timings and a full guided run of every week-2 view.
import datetime as dt, re, json
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
HOOK="""window.__bp=[];window.__osc=0;window.__vib=0;
(function(){var C=window.AudioContext||window.webkitAudioContext;if(C){var o=C.prototype.createOscillator;C.prototype.createOscillator=function(){window.__osc++;return o.apply(this,arguments);};}
try{navigator.vibrate=function(){window.__vib++;return true;};}catch(e){}})();"""
# the 17 week-2 views: 7 main, 7 backup, 3 run instead (Wed backup, Sat backup, Sun main)
DAYS=["2026-10-%d"%d for d in range(19,26)]
VIEWS=[(d,"main",{}) for d in DAYS]+[(d,"backup",{"wo_alt":{d:1}}) for d in DAYS]
VIEWS+=[("2026-10-21","backup+run",{"wo_alt":{"2026-10-21":1},"wo_ri":{"2026-10-21":1}}),("2026-10-24","backup+run",{"wo_alt":{"2026-10-24":1},"wo_ri":{"2026-10-24":1}}),("2026-10-25","run",{"wo_ri":{"2026-10-25":1}})]
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
def sec(s): m=re.search(r"(\d+):(\d\d)",s); return int(m.group(1))*60+int(m.group(2)) if m else -1
def mk(b,d,toggles,hour=8):
    y,m,dd=map(int,d.split("-"))
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block")
    c.add_init_script(HOOK);p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda x:x.accept())
    p.clock.install(time=dt.datetime(y,m,dd,hour,0));p.goto(URL)
    p.evaluate("t=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');for(var k in t)localStorage.setItem(k,JSON.stringify(t[k]));}",toggles)
    p.reload();p.wait_for_timeout(150)
    if not p.locator("#panel.open").count(): p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(200)
    return c,p
DOM="""()=>{var V=__app.view(),out=[],cur=null,bi=0,ex=V.blocks.filter(function(b){return b.k=="timer"||b.k=="ex";});
 [].forEach.call(document.getElementById('sess').children,function(el){
  var h=el.tagName=="H2"?el:(el.classList.contains("bh")?el.querySelector("h2"):null);
  if(h&&h.textContent=="Optional"){cur=null;return;}
  if(h){var b=ex[bi++];cur={hdr:h.textContent,kind:b.k,id:b.id||"",flow:!!b.flow,segs:b.segs||[],items:(b.items||[]).map(function(i){return i.lab;}),n:b.n||0,rr:b.rr||null,rest:b.rest||0,title:"",note:"",small:[],list:[],sm:0,btns:[],names:[],gn:[]};out.push(cur);return;}
  if(!cur)return;
  if(el.classList.contains("gn"))cur.gn.push(el.textContent);
  if(el.classList.contains("sp"))cur.small.push(el.textContent);
  if(el.classList.contains("card")){var n=el.querySelector(".hd .name, :scope > .name");
   if(el.classList.contains("ex"))cur.names.push(n.textContent.replace(/^[A-Z]\\d/,""));
   else{cur.title=n.textContent;var nt=el.querySelector(":scope > .note");cur.note=nt?nt.textContent:"";
    el.querySelectorAll(":scope > .sp").forEach(function(x){cur.small.push(x.textContent);});
    el.querySelectorAll(".lst li").forEach(function(x){cur.list.push(x.textContent);});
    cur.sm=el.querySelectorAll("[data-sm]").length;}
   el.querySelectorAll("[data-t]").forEach(function(x){cur.btns.push(x.textContent);});}
  if(el.matches&&el.matches("button[data-t]"))cur.btns.push(el.textContent);});
 return {name:V.name,safe:document.getElementById('safe1').textContent,stop:document.querySelector('.safe .stop').textContent,stopVis:!document.querySelector('.safe .stop').hidden,
  dnote:document.getElementById('dnote').textContent,blocks:out,sess:document.getElementById('sess').innerText};}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox","--autoplay-policy=no-user-gesture-required"])
    dev=[]  # every deviation from the standard, reported together
    def chk(view,rule,cond,info=""):
        if not cond: dev.append(f"{view} · {rule} · {info}")
    seen=set()
    for d,ty,tg in VIEWS:
        c,p=mk(b,d,tg);V=p.evaluate(DOM);c.close()
        vw=f"{d} {ty} ({V['name']})"
        ok(f"{vw} renders",len(V["blocks"])>0)
        # safety line + stop signs (§7/§11, hard rules)
        chk(vw,"§11 safety ≤160",len(V["safe"])<=160,len(V["safe"]))
        chk(vw,"stop-signs line visible",V["stopVis"] and "sudden or severe headache" in V["stop"])
        e=effort_ok([V["safe"]]);chk(vw,"§6 safety effort",e[0],(V["safe"],e[1]))
        chk(vw,"no head-down / breath-hold advice",not re.search(r"head-down position(?!s)|hold your breath(?!.)",V["sess"]))
        hasEx=any(x["kind"]=="ex" for x in V["blocks"])
        chk(vw,"day total ≈ only when strength estimates are included",("≈" in V["dnote"])==hasEx,V["dnote"])
        for bl in V["blocks"]:
            key=(bl["hdr"].split(" · ",1)[1] if " · " in bl["hdr"] else bl["hdr"])+"|"+bl["id"]+"|"+bl["title"]+"|"+json.dumps(bl["segs"])[:200]
            where=f"{vw} · {bl['hdr']}"
            m=HDR.match(bl["hdr"])
            chk(where,"§1 header format",m and len(bl["hdr"])<=32,bl["hdr"])
            if not m: continue
            fmt=m.group(2);tot=sum(x[1] for x in bl["segs"])
            if bl["kind"]=="ex":
                # (b)1 strength/carry: no guided timer, no time, count + "Rest X–Y s", rest timer at the prescribed rest
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
                # guided blocks: only EMOM / Every / intervals / flows (+ the steady and circuit timed formats of §1)
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
                # §9 buttons
                btn=[x for x in bl["btns"] if "walk break" not in x]
                want=("Start guided flow" if bl["flow"] else "Start guided timer")+" · "+(m.group(3) or "")
                chk(where,"§9 button label",len(btn)==1 and btn[0] in (want,"✓ Done · run guided timer again · "+(m.group(3) or "")),(btn,want))
                # §10 flows collapsed, interval/circuit moves expanded
                if bl["flow"]: chk(where,"§10 flow moves collapsed",bl["sm"]==1 and not bl["list"])
                elif fmt.startswith("Circuit"): chk(where,"§10 circuit moves expanded",bl["sm"]==0 and len(bl["list"])>=3,bl["list"])
                for x in bl["list"]: chk(where,"§11 move line ≤36",len(x)<=36,x)
                for x in bl["list"]+labels: chk(where,"§3 'each side' spelled out",not re.search(r"per side|/side|\bL/R\b",x),x)
                # (b)2 window fit: no trailing rest, ≥15 s of real rest, sides cued, GET READY only on position change
                g=bl["segs"]
                if len(g)>1:
                    chk(where,"no trailing REST/READY",g[-1][0] not in ("REST","READY"),g[-1])
                    left=[x for x in g if x[0] not in ("READY","REST") and "left side" in str(x[2:3])];sw=[x for x in labels if "switch → right side" in x]
                    chk(where,"sided moves cued (switch sides after every left side)",len(left)==len(sw),(len(left),len(sw)))
                    chk(where,"no un-cued 'each side' in timer",not [x for x in labels if "each side" in x])
                    rests=[x[1] for x in g if x[0]=="REST"]
                    chk(where,"every rest ≥15 s",all(r>=15 for r in rests),rests)
                    if fmt.startswith("Every") or fmt.startswith("EMOM"):
                        win=sec(fmt) if ":" in fmt else int(re.search(r"(\d+) s",fmt).group(1));acc=0;wins=[];cur=[]
                        for x in g:
                            cur.append(x)
                            if x[0]=="REST": wins.append(cur);cur=[]
                        wins.append(cur)
                        for i,wd in enumerate(wins):
                            work=sum(x[1] for x in wd if x[0]!="REST");full=sum(x[1] for x in wd)
                            chk(where,f"window {i+1}: set-up + work ≤ window − 15 s",work<=win-15,(work,win))
                            if i<len(wins)-1: chk(where,f"window {i+1} = {win} s",full==win,full)
                if bl["flow"]: chk(where,"flow has its moves list",len(bl["segs"])>1)
        # whole-view text rules (§6/§7): single words, no paces, no "hard", s/m only in small print
        txt=V["sess"]+" "+V["safe"]
        chk(vw,"§6 no combined effort terms",not re.search(r"(easy|steady|moderate|hard)\s*[-–/(]+\s*(easy|steady|moderate|hard)|steady-state",txt,re.I))
        chk(vw,"§6 no 'hard'",not re.search(r"\bhard\b",txt,re.I))
        chk(vw,"§6 no numeric paces",not re.search(r"min/km|km/h|/500|drag factor|\d:\d\d–\d:\d\d/",txt))
        notsmall=[x for bl in V["blocks"] for x in [bl["title"],bl["note"]]+bl["gn"]+[str(s[2]) for s in bl["segs"] if len(s)>2]]
        chk(vw,"§6 stroke rate only in small print",not [x for x in notsmall if "s/m" in x],[x for x in notsmall if "s/m" in x][:2])
    ok(f"standard audit: 0 deviations across {len(VIEWS)} views",not dev,len(dev))
    for x in dev[:40]: print("   DEVIATION",x)
    W1P={"2026-10-12":"easyrun12","2026-10-13":"strA","2026-10-14":"row","2026-10-15":"mob","2026-10-16":"strB","2026-10-17":"kb","2026-10-18":"walk"}
    W2P={"2026-10-19":"mob19","2026-10-20":"up20","2026-10-21":"run21","2026-10-22":"mob22","2026-10-23":"lo23","2026-10-24":"kb24","2026-10-25":"walk25"}
    c,p=mk(b,"2026-10-19",{})
    D=p.evaluate("""()=>{var S=__how.SESS,o={};Object.keys(S).forEach(function(k){o[k]={name:S[k].name,tot:S[k].tot,rest:!!S[k].rest,blocks:S[k].blocks.map(function(b){return {k:b.k,id:b.id||b.tid||"",flow:!!b.flow,
      names:(b.items||[]).map(function(i){return i.x;}),list:b.list||[],segs:(b.segs||[]).map(function(g){return String(g[2]||"");})};})};});return o;}""")
    P=p.evaluate("()=>__wk.PROG");B=p.evaluate("()=>__wk.BK")
    ok("week-1 programme unchanged",all(P[d]==k for d,k in W1P.items()),P)
    ok("week-1 backups unchanged",all(B["2026-10-%d"%d]=="bk%d"%d for d in range(12,19)),B)
    ok("week-2 programme mapped",all(P.get(d)==k for d,k in W2P.items()),P)
    ok("week-2 backups mapped",all(B.get("2026-10-%d"%d)=="bk%d"%d for d in range(19,26)),B)
    W1=set(W1P.values())|{"bk%d"%d for d in range(12,19)}|{"kbq17"};W2=set(W2P.values())|{"bk%d"%d for d in range(19,26)}
    ids1={bl["id"] for k in W1 for bl in D[k]["blocks"] if bl["id"]};ids2=[bl["id"] for k in W2 for bl in D[k]["blocks"] if bl["id"]]
    ok("week-2 block ids unique and new",len(ids2)==len(set(ids2)) and not (set(ids2)&ids1),set(ids2)&ids1)
    ok("week-2 session names new",not ({D[k]["name"] for k in W2}&{D[k]["name"] for k in W1}))
    def moves(k): return sorted([n for bl in D[k]["blocks"] for n in bl["names"]]+[x.split(" – ")[0] for bl in D[k]["blocks"] for x in bl["list"]])
    for d,k in W2P.items():
        d1="2026-10-%d"%(int(d[-2:])-7);ok(f"{d} differs from week 1 ({W1P[d1]})",moves(k)!=moves(W1P[d1]))
    lim={"mob19":(14,16),"mob22":(14,16),"run21":(36,40),"bk19":(10,16),"bk22":(10,16),"bk25":(10,16)}
    for k in W2:
        lo,hi=lim.get(k,(20 if k.startswith("bk") else 32,38));m=D[k]["tot"]/60;ok(f"{k} time {m:.1f} min in {lo}–{hi}",lo<=m<=hi)
    # How-to for every new move: exercise cards, timer lists, flow moves
    miss=p.evaluate("""()=>{var S=__how.SESS,H=__how.HT,o=[];%s.forEach(function(k){S[k].blocks.forEach(function(b){(b.items||[]).forEach(function(i){if(!H[i.x])o.push(i.x);});
      (b.list||[]).forEach(function(x){if(!H[__how.hkey(x)])o.push(x);});});});return o;}"""%json.dumps(sorted(W2)))
    ok("How-to covers every week-2 move",not miss,miss)
    carry=lambda k:[n for bl in D[k]["blocks"] for n in bl["names"] if "carry" in n]
    ok("carries: Tue farmer's only, Fri suitcase only, none Sat",carry("up20")==["farmers-carry"] and carry("lo23")==["suitcase-carry"] and not carry("kb24") and not carry("bk24"))
    ok("Sat: single 16 kg bell","16 kg" in p.evaluate("()=>__how.SESS.kb24.safe"))
    txt=json.dumps({k:D[k] for k in W2})
    ok("medical: no barbell, back squat, conventional deadlift, snatch, inversion",not re.search(r"barbell|back squat|conventional|snatch|handstand|headstand|inverted|valsalva",txt,re.I))
    p.click("#next");p.wait_for_timeout(150)
    ok("week 3 follows (26 Oct = Upper)",p.locator('button.day[data-d="2026-10-26"] .pl').inner_text()=="Upper")
    c.close()
    # full guided run of every week-2 view
    for d,ty,tg in VIEWS:
        c,p=mk(b,d,tg);nm=p.locator("#ttl").inner_text()
        ids=p.evaluate("[...document.querySelectorAll('#sess [data-t]')].map(e=>e.dataset.t)")
        ok(f"{d} {ty} ({nm}) has guided blocks",len(ids)>0,ids)
        for tid in ids:
            p.evaluate("()=>{window.__bp=[];window.__osc=0}");p.locator(f'#sess [data-t="{tid}"]').first.click();p.wait_for_timeout(40)
            segs=ls(p,"wo_timer")["segs"];tot=sum(x[1] for x in segs)
            p.clock.run_for(tot*1000+2000);p.wait_for_timeout(60)
            bp=p.evaluate("window.__bp.length")
            ok(f"{d} {ty}/{tid} beeps on every segment ({len(segs)}) and logs done",bp>=len(segs) and (ls(p,"wo_"+d) or {}).get("s",{}).get(tid)==1,(bp,len(segs)))
        c.close()
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
