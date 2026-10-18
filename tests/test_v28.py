import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v28: automated audit of app-style-standard.md (§1/§2/§6/§9/§10/§11) on all 19 session views, guided-window fit,
# strength rest timer, saved-log compatibility and a full guided run of every day type. Replaces the one-off audit script.
import datetime as dt, re, json
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
HOOK="""window.__bp=[];window.__osc=0;window.__vib=0;
(function(){var C=window.AudioContext||window.webkitAudioContext;if(C){var o=C.prototype.createOscillator;C.prototype.createOscillator=function(){window.__osc++;return o.apply(this,arguments);};}
try{navigator.vibrate=function(){window.__vib++;return true;};}catch(e){}})();"""
# the 19 views: 7 main, 7 backup, 1 quick option, 4 run instead (Wed main + backup, Sat backup, Sun main)
DAYS=["2026-10-%d"%d for d in range(12,19)]
VIEWS=[(d,"main",{}) for d in DAYS]+[(d,"backup",{"wo_alt":{d:1}}) for d in DAYS]+[("2026-10-17","quick",{"wo_quick":{"2026-10-17":1}})]
VIEWS+=[("2026-10-14","run",{"wo_ri":{"2026-10-14":1}}),("2026-10-14","backup+run",{"wo_alt":{"2026-10-14":1},"wo_ri":{"2026-10-14":1}}),
        ("2026-10-17","backup+run",{"wo_alt":{"2026-10-17":1},"wo_ri":{"2026-10-17":1}}),("2026-10-18","run",{"wo_ri":{"2026-10-18":1}})]
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
    # ---- flows: GET READY only on position change (positions from the app's posOf)
    c,p=mk(b,"2026-10-13",{})
    bad=p.evaluate("""()=>{var S=__how.SESS,P=__app.posOf,o=[];Object.keys(S).forEach(function(k){S[k].blocks.forEach(function(b){if(!b.flow)return;var g=b.segs;
      for(var i=0;i<g.length;i++){if(g[i][0]!="READY")continue;var prev=null;for(var j=i-1;j>=0;j--)if(g[j][0]!="READY"){prev=g[j];break;}
       if(prev&&P(String(prev[2]).replace(/ · .*$/,""))==P(String(g[i+1][2]).replace(/ · .*$/,"")))o.push(k+'/'+b.id+'@'+i);}});});return o;}""")
    ok("flows: GET READY only on a position change",not bad,bad)
    # ---- strength rest timer: superset after the last move of a round, straight sets after each tick, off when auto-rest is off
    def tick(x,i):
        p.locator(f'.card[data-x="{x}"] .pill').nth(i).click()
        if p.locator(".step").count(): p.click('[data-st="x"]')
    ok("strength blocks have no guided timer button",p.locator('#sess .card.ex [data-t], #sess [data-t="aemom"], #sess [data-t="asb"]').count()==0)
    ok("A superset shows its count and rest range","2 · A · Superset · 4 rounds" in p.locator("#sess h2").all_text_contents() and "Each round: A1 → A2. Rest 60–90 s." in p.locator("#sess").inner_text())
    tick("incline-db-press",0);ok("no rest mid-round",p.locator("#rbar.show").count()==0)
    tick("prone-y-raise",0);ok("rest starts after the round at 1:15",p.locator("#rbar.show").count()==1 and p.locator("#rtime").inner_text()=="1:15",p.locator("#rtime").inner_text())
    p.click("#rskip")
    tick("assisted-chinup",0);tick("lateral-raise",0);tick("hammer-curl",0)
    ok("tri-set 60–90 s rest starts at 1:15",p.locator("#rbar.show").count()==1 and p.locator("#rtime").inner_text()=="1:15");p.click("#rskip")
    p.evaluate("""()=>{var S=__how.SESS.strA;S.blocks.push({k:"ex",h:"Z · Straight sets",mode:"sup",n:3,rr:[45,75],rest:60,unit:"Set",items:[{x:"goblet-squat",lab:"Z1",rp:6,gi:900}]});}""")
    p.click("#close");p.click('button.day[data-d="2026-10-13"]');p.wait_for_timeout(200)
    ok("straight sets header + line","7 · Z · Straight sets · 3 sets" in p.locator("#sess h2").all_text_contents() and "Each set: Z1. Rest 45–75 s." in p.locator("#sess").inner_text() and "Tick a set to start the rest timer." in p.locator("#sess").inner_text())
    tick("goblet-squat",0);ok("straight set: rest after one tick at 1:00",p.locator("#rbar.show").count()==1 and p.locator("#rtime").inner_text()=="1:00");p.click("#rskip")
    tick("goblet-squat",1);ok("straight set: rest after set 2",p.locator("#rbar.show").count()==1);p.click("#rskip")
    tick("goblet-squat",2);ok("straight set: no rest after the last set",p.locator("#rbar.show").count()==0)
    p.locator("#autorest").uncheck();tick("incline-db-press",1);tick("prone-y-raise",1)
    ok("auto-rest off: ticking a round starts nothing",p.locator("#rbar.show").count()==0)
    ok("auto-rest off: rest-timer small print hidden","start the rest timer" not in p.locator("#sess").inner_text())
    ok("manual rest timer button stays",p.locator("#rbtn").is_visible())
    c.close()
    # ---- saved logs from pc-v27 are untouched by the upgrade
    LOG=[{"date":"2026-10-12","name":"Easy Run","type":"main","sid":"easyrun12","min":34,"km":"4.1","feel":"6","notes":"","breaks":1},
         {"date":"2026-10-13","name":"Strength A · Upper","type":"main","sid":"strA","min":38,"sets":3,"of":24,"w":{},"wt":{"incline-db-press":"14","cs-row":"16"},"rp":{"incline-db-press":{"v":[6,5,"–","–"],"u":""}}},
         {"date":"2026-10-14","name":"Easy run 5 km","type":"run","sid":"row","ri":1,"custom":1,"mig":"v24","min":31,"km":"5","feel":"4","notes":"easy 5k outside","breaks":0},
         {"date":"2026-10-15","name":"Backup · Easy Walk + Breathing","type":"backup","sid":"bk15","min":15},
         {"date":"2026-10-16","name":"Strength B · Lower + Core","type":"main","sid":"strB","min":36,"sets":10,"of":20,"w":{},"wt":{"goblet-squat":"18"}},
         {"date":"2026-10-17","name":"15-min KB Flow (16 kg)","type":"quick","sid":"kbq17","min":15}]
    SEED={"wo_log":LOG,"wo_2026-10-13":{"t":{"0_0":True,"1_0":True,"0_1":True},"rp":{"0_0":6,"1_0":6,"0_1":5},"w":{},"r":1,"s":{"awu":1,"aemom":1,"afl":1},"start":1},
          "wo_2026-10-16":{"t":{"4_0":True},"w":{},"r":1,"s":{"bwu":1}},"wo_wt":{"incline-db-press":{"2026-10-13":"14"},"cs-row":{"2026-10-13":"16"},"goblet-squat":{"2026-10-16":"18"}},
          "wo_alt":{"2026-10-15":1},"wo_ri":{"2026-10-14":1},"wo_quick":{"2026-10-17":1},"wo_plan":{},"wo_run_2026-10-12":{"b":1,"s":{"rmain":1},"d":"4.1","f":"6"}}
    c,p=mk(b,"2026-10-18",SEED,9)
    for k,v in SEED.items(): ok(f"log compat: {k} unchanged after upgrade",ls(p,k)==v,(ls(p,k),v))
    p.evaluate("()=>document.querySelector('details').open=true")
    hist=p.locator("#hist li").all_inner_texts()
    ok("history lists every entry under its saved name",[h.split(" · ",1)[1].split(" – ")[0] for h in hist]==[x["name"] for x in LOG[::-1]],hist)
    opts=p.locator('#hist select[data-hd="2026-10-14"] option:checked').inner_text();ok("history Edit keeps the saved type",opts=="Run instead",opts)
    p.click("#close") if p.locator("#panel.open").count() else None
    def opend(d):
        if p.locator("#panel.open").count(): p.click("#close")
        p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(200)
    opend("2026-10-12");ok("renamed Mon session still shows its old log",p.locator("#ttl").inner_text()=="Zone 2 Run" and p.locator("#dnote").inner_text().startswith("Logged") and p.locator("#fin").inner_text()=="Update log",(p.locator("#ttl").inner_text(),p.locator("#dnote").inner_text()))
    ok("Mon done flag kept",p.locator("#c_rmain.done").count()==1)
    p.click("#fin");p.clock.fast_forward(1000);p.wait_for_timeout(100);p.click("#o_done")
    L=[x for x in ls(p,"wo_log") if x["date"]=="2026-10-12"];ok("updating the old log keeps one entry and its name",len(L)==1 and L[0]["name"]=="Easy Run",L)
    opend("2026-10-13")
    on=p.evaluate("()=>[...document.querySelectorAll('#sess .pill.on')].map(e=>e.dataset.k)")
    ok("ticks still on the same moves",sorted(on)==["0_0","0_1","1_0"] and p.locator('.card[data-x="incline-db-press"] .pill').nth(1).inner_text()=="✓ 5",on)
    ok("weights still shown",p.locator('.card[data-x="incline-db-press"] input').input_value()=="14")
    ok("warm-up done flag kept",p.locator("#c_awu.done").count()==1)
    opend("2026-10-16");ok("Fri tick on C1 kept",p.locator('.card[data-x="db-rdl"] .pill.on').count()==1)
    opend("2026-10-17");p.click("#alt");p.wait_for_timeout(150)
    ok("Last: kg carries across sessions","Last: 16 kg (Tue 13 Oct)" in p.locator('.card[data-x="cs-row"]').text_content(),p.locator('.card[data-x="cs-row"]').text_content())
    ok("pull-up is one move, dips in its How-to",p.locator('.card[data-x="pullup-dip"] .name').inner_text().endswith("Assisted pull-up (feet on block)"))
    p.click('.card[data-x="pullup-dip"] .more');p.locator('.card[data-x="pullup-dip"] .how').click();p.wait_for_timeout(200)
    ok("dips alternative in How-to","dips" in p.locator("#hs").inner_text().lower());p.click("#hs_x")
    p.select_option('#hist select[data-hd="2026-10-12"]',"backup");p.wait_for_timeout(150)
    e=[x for x in ls(p,"wo_log") if x["date"]=="2026-10-12"][0];ok("history Edit still works (→ Backup)",e["type"]=="backup" and e["name"]=="Backup · Zone 2 Row + Mobility",e)
    p.select_option('#hist select[data-hd="2026-10-12"]',"main");p.wait_for_timeout(150)
    e=[x for x in ls(p,"wo_log") if x["date"]=="2026-10-12"][0];ok("history Edit still works (→ Main)",e["type"]=="main" and e["name"]=="Zone 2 Run",e)
    ok("other entries untouched by edits",[x for x in ls(p,"wo_log") if x["date"]!="2026-10-12"]==[x for x in LOG if x["date"]!="2026-10-12"])
    c.close()
    # ---- full guided run on the quick option and the 4 run-instead views (main + backup days run in test_v25)
    for d,ty,tg in VIEWS[14:]:
        c,p=mk(b,d,tg);nm=p.locator("#ttl").inner_text()
        ids=p.evaluate("[...document.querySelectorAll('#sess [data-t]')].map(e=>e.dataset.t)")
        ok(f"{d} {ty} ({nm}) has guided blocks",len(ids)>0,ids)
        for tid in ids:
            p.evaluate("()=>{window.__bp=[];window.__osc=0}");p.locator(f'#sess [data-t="{tid}"]').first.click();p.wait_for_timeout(40)
            segs=ls(p,"wo_timer")["segs"];tot=sum(x[1] for x in segs)
            t0=sec(p.locator("#time").inner_text());p.clock.run_for(3000);p.wait_for_timeout(20);t1=sec(p.locator("#time").inner_text())
            ok(f"{d} {ty}/{tid} counts down",t1<t0 or t0<=3,(t0,t1))
            p.clock.run_for(tot*1000+2000);p.wait_for_timeout(60)
            bp=p.evaluate("window.__bp.length");osc=p.evaluate("window.__osc")
            ok(f"{d} {ty}/{tid} beeps on every segment ({len(segs)}) via AudioContext",bp>=len(segs) and osc>=len(segs),(bp,osc))
            ok(f"{d} {ty}/{tid} logged done",(ls(p,"wo_"+d) or {}).get("s",{}).get(tid)==1 and p.locator("#bar.ask").count()==0)
        ok(f"{d} {ty} no navigator.vibrate calls",p.evaluate("window.__vib")==0)
        c.close()
    src=open("index.html",encoding="utf8").read()
    ok("no navigator.vibrate in the app",".vibrate(" not in src)
    ok("no '≈m:ss' block estimates left",not re.search(r"'≈'\+mmss|≈\d+:\d\d",src))
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
