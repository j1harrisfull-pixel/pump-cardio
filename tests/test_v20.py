import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
import datetime as dt, re, urllib.parse as U
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
DAYS=["2026-10-%d"%d for d in range(12,19)]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    c=b.new_context(viewport={"width":390,"height":844},service_workers="block")
    p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.clock.install(time=dt.datetime(2026,10,13,9,0));p.goto(URL)
    p.evaluate("""()=>{localStorage.clear();localStorage.setItem('wo_startdate','"2026-10-10"');localStorage.setItem('wo_ver','12');
      localStorage.setItem('wo_log',JSON.stringify([{date:'2026-10-12',name:'Easy Run',min:34,feel:6}]))}""");p.reload()
    D=p.evaluate("""()=>{var W=__wk,H=__how,o={};Object.keys(W.BK).forEach(function(d){var k=W.BK[d],s=H.SESS[k],ids=[],mv=[];
      s.blocks.forEach(function(b){(b.items||b.ex||[]).forEach(function(e){if(e.x)ids.push(e.x)});var t=b.timer||b;(t.segs||[]).forEach(function(g){if(g[0]!="READY"&&g[0]!="REST")mv.push(g[2])})});
      o[d]={k:k,name:s.name,main:H.SESS[W.PROG[d]].name,tot:s.tot,g0:s.g0,
       segs:s.blocks.map(function(b){var t=b.timer||b;return {h:b.h||b.k,s:t.segs||[]}}),
       noHow:ids.filter(function(x){return !H.X[x]||!H.HT[x]}),
       noHowMv:mv.filter(function(n){return !H.HT[H.hkey(String(n))]})}});return o}""")
    ok("one backup per day Mon-Sun",sorted(D)==DAYS,sorted(D))
    ok("backups all distinct and differ from main",len({v["name"] for v in D.values()})==7 and all(v["name"]!=v["main"] for v in D.values()))
    for d,v in D.items():
        m=v["tot"]/60;lim=(10,25) if d in("2026-10-15","2026-10-18") else (28,38)
        ok(f"{v['k']} {m:.1f} min",lim[0]<=m<=lim[1],m)
        ok(f"{v['k']} g0 offset",v["g0"]==100)
        ok(f"{v['k']} how-to for every exercise id",not v["noHow"],v["noHow"])
        for bl in v["segs"]:
            g=bl["s"]
            if len(g)<2: continue
            ok(f"{v['k']}/{bl['h']} starts with READY",g[0][0]=="READY")
            bad=[i for i in range(1,len(g)) if g[i][0] not in("READY","REST") and g[i-1][0] not in("READY","REST") and g[i][2]!=g[i-1][2] and not(g[i-1][0]=="WORK")]
            if any(x[0] in ("STRETCH","MOBILITY","FLOW") for x in g): bad=[]  # flows: READY only on position change (test_v25)
            ok(f"{v['k']}/{bl['h']} switch time between moves",not bad,bad[:3])
    # toggle on today (Tue)
    p.click('button.day[data-d="2026-10-13"]');p.wait_for_timeout(250)
    ok("toggle + swap visible",p.locator("#alt").is_visible() and p.locator("#swap").is_visible())
    ok("toggle label",p.locator("#alt").inner_text().startswith("Use backup session: Upper (KB"),p.locator("#alt").inner_text())
    p.screenshot(path="test-output/app-v20.png")
    p.click("#alt");p.wait_for_timeout(200)
    ok("backup renders",p.locator("#ttl").inner_text()==D["2026-10-13"]["name"] and p.locator('.card[data-x="kb-floor-press"]').count()==1)
    ok("back label",p.locator("#alt").inner_text().startswith("↩ Back to main"))
    ok("saved per day",ls(p,"wo_alt").get("2026-10-13") and not ls(p,"wo_alt").get("2026-10-14"))
    p.reload();p.click('button.day[data-d="2026-10-13"]');p.wait_for_timeout(250)
    ok("persists after reload",p.locator("#ttl").inner_text()==D["2026-10-13"]["name"])
    p.click("#fin");p.clock.fast_forward(1000);e=ls(p,"wo_log")[-1]
    ok("logged under backup name",e["name"]==D["2026-10-13"]["name"] and e["date"]=="2026-10-13",e)
    p.keyboard.press("Escape")
    for s in ["#o_done","#close"]:
        if p.locator(s).is_visible(): p.click(s)
    p.click('button.day[data-d="2026-10-13"]');p.wait_for_timeout(250);p.click("#alt");p.wait_for_timeout(200)
    ok("switch back to main",p.locator("#ttl").inner_text()==D["2026-10-13"]["main"])
    # swap
    p.click("#swap");ok("swap sheet open",p.locator("#swp.show").count()==1)
    ok("5 chips",p.locator("#sw_c .rc").all_inner_texts()==["Shorter","Feeling rough","No running","Different kit","Something else"])
    p.click('#sw_c [data-r="Shorter"]');p.click('#sw_c [data-r="No running"]');p.fill("#sw_n","Knee a bit sore");p.dispatch_event("#sw_n","input")
    h=p.evaluate("()=>{var a=document.getElementById('sw_go');a.dispatchEvent(new Event('mouseover'));return __wk.swapHref('2026-10-13')}")
    ok("mailto address",h.startswith("mailto:jamesharris+workout@mail.grokbot.com?"),h[:60])
    q=U.parse_qs(h.split("?",1)[1]);sub=q["subject"][0];body=q["body"][0]
    ok("subject",sub=="Workout swap request 2026-10-13",sub)
    ok("body fields","2026-10-13" in body and D["2026-10-13"]["main"] in body and "Shorter" in body and "No running" in body and "Knee a bit sore" in body and "Easy Run" in body,body)
    p.evaluate("()=>{var a=document.getElementById('sw_go');a.addEventListener('click',e=>e.preventDefault());a.click()}");p.wait_for_timeout(200)
    ok("confirmation",p.locator("#sw_ok").inner_text().strip().startswith("Sent to your coach. A new session usually lands within 10 to 20 minutes; use the backup meanwhile."),p.locator("#sw_ok").inner_text())
    ok("swap saved",ls(p,"wo_swaps")[-1]["reasons"]==["Shorter","No running"])
    # override one day
    n=p.evaluate("()=>{__wk.OVR['2026-10-16']='bk16';var o={};['2026-10-15','2026-10-16','2026-10-17'].forEach(function(d){o[d]=__wk.PROG[d]});return o}")
    p.reload();p.evaluate("()=>{}")
    p.evaluate("()=>{__wk.OVR['2026-10-16']='bk12'}");p.click('button.day[data-d="2026-10-16"]');p.wait_for_timeout(250)
    ok("OVR replaces Fri",p.locator("#ttl").inner_text()==D["2026-10-12"]["name"],p.locator("#ttl").inner_text())
    p.click("#close");p.click('button.day[data-d="2026-10-17"]');p.wait_for_timeout(250)
    ok("OVR leaves Sat alone",p.locator("#ttl").inner_text()=="KB + Carry" or "KB" in p.locator("#ttl").inner_text())
    src=open("index.html",encoding="utf8").read()
    for w in ["brisk","Brisk","jog","cooked"," mph","mile"]: ok(f"v21 no '{w}'",w not in src)
    import re as _r
    for pat in [r"/km",r"km/h",r"/500m",r"drag factor",r"\d:\d\d–\d:\d\d/",r"≈\d"]: ok(f"v22 no pace pattern {pat}",not _r.search(pat,src))
    md=open("docs/programme-week1.md",encoding="utf8").read()
    E=r"(easy|steady|moderate|hard)"
    for nm,txt in [("app",src),("md",md),("audit",open("docs/terminology-audit.md",encoding="utf8").read().split("## Glossary")[0].split("**pc-v23 change:**")[0])]:
        bad=_r.findall(E+r"[\s]*[-–/]+[\s]*"+E+r"|"+E+r"\s*\(\s*"+E+r"\s*\)|"+r"\b(easy|steady|moderate|hard)[- ](easy|steady|moderate|hard)\b|steady-state",txt,_r.I)
        ok(f"v23 no combined effort terms in {nm}",not bad,bad[:3])
    ok("v23 bans steady-hard","steady-hard" not in src.lower() and "steady-hard" not in md.lower())
    ok("v23 row intervals moderate pace","6 × 1:00 moderate pace, 24–26 s/m, RPE 7" in src)
    ok("v22 md has no paces",not _r.search(r"/km|km/h|/500m|drag factor",md))
    ok("v22 terms kept","Easy run (Zone 2)" in src and "steady run" in src and "power walk" in src and "recovery walk" in src and "Warm-up walk" in src and "24–26 s/m" in src and "damper 4–5" in src and "light paddle" in src and "2 RIR" in src)
    # v23 run instead (Wed main row, Sun walk; Wed/Sat backups)
    p.clock.set_system_time(dt.datetime(2026,10,14,9,0));p.reload()
    p.click('button.day[data-d="2026-10-14"]');p.wait_for_timeout(250)
    ok("v23 Run instead visible Wed",p.locator("#ri").is_visible() and "Run instead" in p.locator("#ri").inner_text())
    t0=p.locator("#dnote").inner_text()
    p.click("#ri");p.wait_for_timeout(200)
    ok("v23 Wed run version renders","Run/walk intervals 6 × (1:00 / 1:00)" in p.locator("#c_wiv").inner_text() and "moderate pace" in p.locator("#c_wiv").inner_text())
    ok("v23 same total time",p.locator("#dnote").inner_text()==t0,(t0,p.locator("#dnote").inner_text()))
    ok("v23 back label","Back to row" in p.locator("#ri").inner_text())
    ok("v23 saved per day",ls(p,"wo_ri")=={"2026-10-14":1},ls(p,"wo_ri"))
    p.screenshot(path="test-output/app-v23.png")
    p.click("#ri");p.wait_for_timeout(200);ok("v23 back to row","Row intervals" in p.locator("#c_wiv").inner_text())
    p.click("#close");p.click('button.day[data-d="2026-10-18"]');p.wait_for_timeout(250)
    ok("v23 Run instead on Sun",p.locator("#ri").is_visible());p.click("#ri");p.wait_for_timeout(200)
    ok("v23 Sun easy run + walk-break counter","Easy run (Zone 2)" in p.locator("#c_swalk").inner_text() and p.locator("#brkb").count()==1)
    p.click("#ri");p.click("#close");p.click('button.day[data-d="2026-10-13"]');p.wait_for_timeout(250)
    ok("v23 no Run instead on strength day",not p.locator("#ri").is_visible())
    RIc=p.evaluate("()=>{var S=__how.SESS,o=[];Object.keys(S).forEach(function(k){S[k].blocks.forEach(function(b){if(b.ri)o.push(k+'/'+b.id)})});return o}")
    ok("v23 run versions on Wed/Sat/Sun blocks",sorted(RIc)==sorted(["row/wwu","row/wiv","row/wst","bk14/x14iv","bk17/x17fl","walk/swalk"]),RIc)
    ok("no page errors",not errs,errs)
    b.close()
print(f"{sum(res)}/{len(res)} passed")
