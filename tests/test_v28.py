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
  dnote:document.getElementById('dnote').textContent,blocks:out,sess:document.getElementById('sess').innerText};}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox","--autoplay-policy=no-user-gesture-required"])
    # (the rendered-view audit and the full guided runs moved to test_audit.py in the test redesign: one data-driven suite covers every week)
    # ---- flows: no READY prep left anywhere (pc-v30 clock mode)
    c,p=mk(b,"2026-10-13",{})
    bad=p.evaluate("""()=>{var S=__how.SESS,o=[];Object.keys(S).forEach(function(k){S[k].blocks.forEach(function(b){(b.segs||[]).forEach(function(g,i){if(g[0]=="READY")o.push(k+'/'+b.id+'@'+i);});});});return o;}""")
    ok("no READY segments in any block",not bad,bad[:5])
    # ---- strength rest timer: superset after the last move of a round, straight sets after each tick, off when auto-rest is off
    def tick(x,i):
        p.locator(f'.srow[data-x="{x}"] [data-tk]').nth(i).click();p.wait_for_timeout(30)
    ok("strength blocks have no guided timer button",p.locator('#sess .card.ex [data-t], #sess [data-t="aemom"], #sess [data-t="asb"]').count()==0)
    ok("A superset rows alternate A1, A2",[x.split("\n")[0] for x in p.locator('.blk').first.locator(".srow .sn").all_inner_texts()][:4]==["1 · A1","1 · A2","2 · A1","2 · A2"],p.locator('.blk').first.locator(".srow .sn").all_inner_texts()[:4])
    ok("A superset shows its count and rest range","2 · A · Superset · 4 rounds" in p.locator("#sess h2").all_text_contents() and "Each round: A1 → A2. Rest 60–90 s." in p.locator("#sess").inner_text())
    tick("incline-db-press",0);ok("no rest mid-round",p.locator("#rbar.show").count()==0)
    tick("prone-y-raise",0);ok("rest starts after the round at 1:15",p.locator("#rbar.show").count()==1 and p.locator("#rtime").inner_text()=="1:15",p.locator("#rtime").inner_text())
    ok("rest bar shows the next set",p.locator("#rlab").inner_text()=="Next: set 2 · Incline dumbbell press 6",p.locator("#rlab").inner_text())
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
    on=p.evaluate("()=>[...document.querySelectorAll('#sess .tk.on')].map(e=>e.dataset.tk)")
    ok("ticks still on the same moves",sorted(on)==["0_0","0_1","1_0"] and p.locator('[data-rp="0_1"]').inner_text()=="5",on)
    ok("weights still shown",p.locator('[data-kw="0_0"]').input_value()=="14")
    ok("warm-up done flag kept",p.locator("#c_awu.done").count()==1)
    opend("2026-10-16");ok("Fri tick on C1 kept",p.locator('.srow[data-x="db-rdl"] .tk.on').count()==1)
    opend("2026-10-17");p.click("#alt");p.wait_for_timeout(150)
    ok("Last: kg carries across sessions","Last: 16 kg (Tue 13 Oct)" in p.locator('.mvh[data-x="cs-row"]').text_content(),p.locator('.mvh[data-x="cs-row"]').text_content())
    ok("pull-up is one move, dips in its How-to",p.locator('.mvh[data-x="pullup-dip"] .mvn').inner_text()=="Assisted pull-up (feet on block)")
    p.locator('.mvh[data-x="pullup-dip"] .mvn').click();p.wait_for_timeout(200)
    ok("dips alternative in How-to","dips" in p.locator("#hs").inner_text().lower());p.click("#hs_x")
    p.select_option('#hist select[data-hd="2026-10-12"]',"backup");p.wait_for_timeout(150)
    e=[x for x in ls(p,"wo_log") if x["date"]=="2026-10-12"][0];ok("history Edit still works (→ Backup)",e["type"]=="backup" and e["name"]=="Backup · Zone 2 Row + Mobility",e)
    p.select_option('#hist select[data-hd="2026-10-12"]',"main");p.wait_for_timeout(150)
    e=[x for x in ls(p,"wo_log") if x["date"]=="2026-10-12"][0];ok("history Edit still works (→ Main)",e["type"]=="main" and e["name"]=="Zone 2 Run",e)
    ok("other entries untouched by edits",[x for x in ls(p,"wo_log") if x["date"]!="2026-10-12"]==[x for x in LOG if x["date"]!="2026-10-12"])
    c.close()
    src=open("index.html",encoding="utf8").read()
    ok("no navigator.vibrate in the app",".vibrate(" not in src)
    ok("no '≈m:ss' block estimates left",not re.search(r"'≈'\+mmss|≈\d+:\d\d",src))
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
