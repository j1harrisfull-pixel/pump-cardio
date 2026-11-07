import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v35: (1) EMOM overview as per-minute groups derived from the session rotation, in step with the clock screen;
# (2) actual running: decimal km, elapsed time, effort, notes on run days; "Add a run" after other sessions (one entry,
# never a duplicate); edit from history; (3) training history export. Old logs without the new fields still work.
import datetime as dt, json, re
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
def mk(b,d,seed=None,hour=9):
    y,m,dd=map(int,d.split("-"))
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block");p=c.new_page()
    p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda x:x.accept());p.clock.install(time=dt.datetime(y,m,dd,hour,0));p.goto(URL)
    p.evaluate("t=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');for(var k in t)localStorage.setItem(k,JSON.stringify(t[k]));}",seed or {})
    p.reload();p.wait_for_timeout(150)
    if not p.locator("#panel.open").count(): p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(200)
    return c,p
from lib import fin  # shared: retries if the overlay is slow
def opend(p,d):
    if p.locator("#panel.open").count(): p.click("#close")
    p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(200)
NUM={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox","--autoplay-policy=no-user-gesture-required"])
    # ---------------- 1. EMOM groups: every EMOM block in the data ----------------
    c,p=mk(b,"2026-11-07")
    EM=p.evaluate("""()=>{var S=__how.SESS,o=[];Object.keys(S).forEach(function(k){S[k].blocks.forEach(function(bl){if(bl.k=="timer"&&/^EMOM/.test(bl.h||""))o.push({sid:k,id:bl.id,h:bl.h,segs:bl.segs,list:bl.list||[],plan:__app.emomPlan(bl)});});});return o;}""")
    ok("EMOM blocks found",len(EM)>=3,[x["id"] for x in EM])
    for e in EM:
        pl=e["plan"];w=e["segs"][0][1];n=len(e["segs"])
        ok(f"{e['id']}: plan derived from the rotation ({pl['p']} minute cycle × {pl['reps']})",pl and pl["p"]*pl["reps"]==n and n==int(re.search(r"× (\d+)",e["h"]).group(1)),pl and (pl["p"],pl["reps"],n))
        ok(f"{e['id']}: every minute incl. the last is a full {w} s",all(g[0]=="WORK" and g[1]==w for g in e["segs"]) and e["segs"][-1][1]==w)
        sides=[g["side"] for g in pl["cycle"]]
        ok(f"{e['id']}: left and right minutes alternate in the cycle",sides[:2]==["left","right"] or "left" not in sides,sides)
        reps=sorted(set(int(re.search(r"×(\d+)",x).group(1)) for x in e["list"]));used=sorted(set(m["reps"] for g in pl["cycle"] for m in g["mv"]))
        ok(f"{e['id']}: group reps come from the prescription, unchanged",used==reps,(used,reps))
        ok(f"{e['id']}: each sided minute carries the sided moves, the other minute the rest",all((len(g["mv"])==len([x for x in e["list"] if "each side" in x])) if g["side"] else (len(g["mv"])==len([x for x in e["list"] if "each side" not in x])) for g in pl["cycle"]))
        ok(f"{e['id']}: no 'each side' or 'no rest' in the groups",not re.search(r"each side|no rest",json.dumps(pl["cycle"])))
    # rendered overview for Sat 7 Nov (k07a) matches the brief's wording
    txt=p.locator("#c_k07a").inner_text()
    ok("overview: Minute 1 · Left / Minute 2 · Right / Minute 3 groups",re.search(r"MINUTE 1 · LEFT\n3 cleans, 3 front rack squats, 3 presses\.\nMINUTE 2 · RIGHT\n3 cleans, 3 front rack squats, 3 presses\.\nMINUTE 3\n15 swings, then 5 goblet squats\.",txt),txt)
    ok("overview: repeat line + start on the minute, rest for what remains","Repeat this three minute cycle five times." in txt and "Start each group on the minute. Rest for whatever remains of that minute." in txt)
    ok("overview: no 'each side', no 'Last round has no rest', no flat list","each side" not in txt and "no rest" not in txt and p.locator("#c_k07a .lst").count()==0)
    ok("overview: move names still open How-to",p.locator("#c_k07a .emm .mv").count()>=4)
    p.locator("#c_k07a .emm .mv").first.click();p.wait_for_timeout(100);ok("How-to sheet opens from a group",p.locator("#hs.show").count()==1 and len(p.locator("#hs").inner_text())>60);p.click("#hs_x")
    ok("header still shows the exact total",any(h.endswith("15:00") for h in p.locator("#sess h2").all_text_contents()))
    # clock agrees with the overview, minute by minute
    groups=[(a,b.capitalize(),t) for a,b,t in re.findall(r"MINUTE (\d+)(?: · (LEFT|RIGHT))?\n([^\n]+)",txt)];pl=[x for x in EM if x["id"]=="k07a"][0]["plan"]
    p.click('[data-t="k07a"]');p.wait_for_timeout(60)
    ok("get-ready shows the first minute next",p.locator("#ph").inner_text()=="GET READY" and p.locator("#sub").inner_text()=="Next: Left · 3 cleans, 3 front rack squats, 3 presses.",p.locator("#sub").inner_text())
    p.clock.run_for(10500);p.wait_for_timeout(60);agree=True;detail=[]
    for m in range(15):
        g=groups[m%3];side=g[1] or "";text=g[2]
        now=p.locator("#now").inner_text();nd=p.locator("#nowd").inner_text() if p.locator("#nowd").is_visible() else "";sub=p.locator("#sub").inner_text();ctr=p.locator("#cctr").inner_text()
        exp_now=side if side else text;exp_nd=text if side else ""
        ng=groups[(m+1)%3];exp_next=("Next: "+((ng[1]+" · ") if ng[1] else "")+ng[2]) if m<14 else "Last minute"
        good=now==exp_now and nd==exp_nd and sub==exp_next and ctr==f"Minute {m+1} of 15" and p.locator("#time").inner_text() in ("1:00","0:59")
        if not good: agree=False;detail.append((m+1,now,nd,sub,ctr))
        p.clock.run_for(60000);p.wait_for_timeout(40)
    ok("clock agrees with the overview on all 15 minutes (side, moves, next, counter, 60 s each)",agree,detail[:2])
    ok("block logged done after the final full minute",(ls(p,"wo_2026-11-07") or {}).get("s",{}).get("k07a")==1 and p.locator("#bar.ask").count()==0)
    p.click("#ctop") if p.locator("#bar.show").count() else None
    # other timer types untouched: intervals keep their own NOW text and no detail line
    opend(p,"2026-11-03");tid=p.evaluate("()=>[...document.querySelectorAll('#sess [data-t]')].map(e=>e.dataset.t).find(x=>/fl$/.test(x))")
    p.click(f'[data-t="{tid}"]');p.clock.run_for(10500);p.wait_for_timeout(60)
    ok("intervals unchanged: machine · time · effort, no minute detail",re.match(r"Row · \d:\d\d · moderate",p.locator("#now").inner_text()) and not p.locator("#nowd").is_visible(),p.locator("#now").inner_text());p.click("#stop")
    c.close()
    # ---------------- 2. actual running ----------------
    c,p=mk(b,"2026-11-02")
    ok("run day: actual fields (km, mm:ss, effort, feel, notes) and no Add a run",all(p.locator(x).count()==1 for x in ("#r_d","#r_t","#r_e","#r_f","#r_n")) and p.locator("#addrun").count()==0)
    ok("nothing prefilled from the prescription",p.locator("#r_d").input_value()=="" and p.locator("#r_t").input_value()=="" and p.locator("#r_e .rc.on").count()==0)
    note0=p.locator("#dnote").inner_text()
    p.fill("#r_d","6.87");p.dispatch_event("#r_d","input");p.fill("#r_t","34:20");p.dispatch_event("#r_t","input");p.click('#r_e [data-e="steady"]');p.fill("#r_n","windy");p.dispatch_event("#r_n","input")
    r=ls(p,"wo_run_2026-11-02");ok("decimal km, time, effort, notes saved as typed",r["d"]=="6.87" and r["t"]=="34:20" and r["e"]=="steady" and r["n"]=="windy",r)
    ok("prescription untouched: day note same, run block not ticked",p.locator("#dnote").inner_text()==note0 and not (ls(p,"wo_2026-11-02") or {}).get("s"))
    fin(p)
    ok("summary shows the actual run","6.87 km" in p.locator("#o_d").inner_text() and "34:20" in p.locator("#o_d").inner_text() and "steady effort" in p.locator("#o_d").inner_text(),p.locator("#o_d").inner_text());p.click("#o_done")
    L=ls(p,"wo_log");e=L[0]
    ok("one log entry with the actual values, old fields kept",len(L)==1 and e["km"]=="6.87" and e["time"]=="34:20" and e["effort"]=="steady" and e["notes"]=="windy" and e["type"]=="main" and "sid" in e and "feel" in e,e)
    ok("session minutes = actual elapsed time when nothing else is known",e["min"]==34,e["min"])
    p.fill("#r_t","41");p.dispatch_event("#r_t","input");fin(p);p.click("#o_done")
    ok("plain minutes normalise to mm:ss and update the same entry",ls(p,"wo_log")[0]["time"]=="41:00" and len(ls(p,"wo_log"))==1)
    p.evaluate("()=>document.querySelector('details').open=true")
    ok("history shows the run line",re.search(r"6\.87 km · 41:00 · steady",p.locator("#hist li").first.inner_text()),p.locator("#hist li").first.inner_text())
    # edit from history
    p.click("#hist .erun");p.wait_for_timeout(100);ok("Edit run sheet prefilled",p.locator("#ers.show").count()==1 and p.locator("#er_km").input_value()=="6.87" and p.locator("#er_t").input_value()=="41:00" and p.locator("#er_e .rc.on").inner_text()=="steady")
    p.fill("#er_km","7.01");p.click('#er_e [data-e="moderate"]');p.fill("#er_n","hilly");p.click("#er_ok");p.wait_for_timeout(100)
    e=ls(p,"wo_log")[0];ok("edit saves to the same entry and the day card",e["km"]=="7.01" and e["effort"]=="moderate" and e["notes"]=="hilly" and len(ls(p,"wo_log"))==1 and p.locator("#r_d").input_value()=="7.01" and ls(p,"wo_run_2026-11-02")["e"]=="moderate",e)
    c.close()
    # extra run after a strength day
    c,p=mk(b,"2026-11-03")
    ok("strength day: no run fields, small Add a run",p.locator("#r_d").count()==0 and p.locator("#addrun").is_visible())
    p.locator(".tk").first.click();p.wait_for_timeout(50)
    if p.locator("#rbar.show").count(): p.click("#rskip")
    fin(p);p.click("#o_done")
    p.click("#addrun");p.wait_for_timeout(60);ok("Add a run opens the same fields",p.locator("#runx #r_d").count()==1 and p.locator("#runsave").is_visible())
    p.fill("#r_d","5.2");p.dispatch_event("#r_d","input");p.fill("#r_t","28:10");p.dispatch_event("#r_t","input");p.click('#r_e [data-e="easy"]');p.click("#runsave");p.wait_for_timeout(100)
    L=ls(p,"wo_log");ex=[x for x in L if x.get("type")=="extra"];st=[x for x in L if x.get("type")!="extra"]
    ok("extra run is its own entry on the same date; strength log not duplicated",len(L)==2 and len(ex)==1 and len(st)==1 and ex[0]["date"]=="2026-11-03" and ex[0]["name"]=="Extra run" and ex[0]["km"]=="5.2" and ex[0]["time"]=="28:10" and ex[0]["effort"]=="easy" and ex[0]["min"]==28,L)
    ok("strength entry untouched",st[0]["name"]=="Strength A4 · Upper" or st[0]["type"]=="main",st[0]["name"])
    p.fill("#r_d","5.5");p.dispatch_event("#r_d","input");p.click("#runsave");p.wait_for_timeout(100)
    L=ls(p,"wo_log");ok("saving again updates, never duplicates",len(L)==2 and [x for x in L if x.get("type")=="extra"][0]["km"]=="5.5")
    p.reload();p.wait_for_timeout(200)
    if not p.locator("#panel.open").count(): p.click('button.day[data-d="2026-11-03"]');p.wait_for_timeout(200)
    ok("extra run card reopens with its values after reload",p.locator("#runx").count()==1 and p.locator("#r_d").input_value()=="5.5")
    ok("day still shows the strength session as logged",p.locator("#fin").inner_text()=="Update log" and "Logged" in p.locator("#dnote").inner_text() or p.locator("#dnote").inner_text().startswith("Today"))
    p.evaluate("()=>document.querySelector('details').open=true")
    items=p.locator("#hist li").all_inner_texts()
    ok("history lists both; extra run has Edit run but no type dropdown",len(items)==2 and any("Extra run" in x and "5.5 km · 28:10 · easy" in x for x in items) and p.locator('#hist li:has-text("Extra run") select').count()==0 and p.locator('#hist li:has-text("Extra run") .erun').count()==1,items)
    p.select_option('#hist select[data-hd="2026-11-03"]',"backup");p.wait_for_timeout(100)
    L=ls(p,"wo_log");ok("changing the strength entry's type leaves the extra run alone",[x for x in L if x.get("type")=="extra"][0]["name"]=="Extra run" and any(x.get("type")=="backup" for x in L),L)
    c.close()
    # ---------------- 3. export + old logs ----------------
    OLD=[{"date":"2026-10-12","name":"Easy Run","type":"main","sid":"easyrun12","min":34,"km":"4.1","feel":"6","notes":"","breaks":1},
         {"date":"2026-10-13","name":"Strength A · Upper","type":"main","sid":"strA","min":38,"sets":3,"of":24,"w":{},"wt":{"incline-db-press":"14"},"rp":{"incline-db-press":{"v":[6,5,"–","–"],"u":""}}},
         {"date":"2026-10-14","name":"Easy run 5 km","type":"run","sid":"row","ri":1,"custom":1,"mig":"v24","min":31,"km":"5","feel":"4","notes":"easy 5k outside","breaks":0},
         {"date":"2026-10-17","name":"15-min KB Flow (16 kg)","type":"quick","sid":"kbq17","min":15}]
    c,p=mk(b,"2026-11-07",{"wo_log":OLD})
    ok("old logs without time/effort load unchanged",ls(p,"wo_log")==OLD)
    p.evaluate("()=>document.querySelector('details').open=true")
    items=p.locator("#hist li").all_inner_texts()
    ok("old entries render (km, feel, strength line)",len(items)==4 and any("4.1 km" in x and "felt 6/10" in x for x in items) and any("Incline dumbbell press 14 kg · 6/5/–/–" in x for x in items),items)
    ok("Export button in History",p.locator("#exp").is_visible())
    p.click("#exp");p.wait_for_timeout(200)
    ok("export sheet shown when the share sheet is unavailable",p.locator("#exs.show").count()==1)
    t=p.locator("#ex_t").input_value()
    ok("export has dates, sessions, run km, notes and strength data",all(x in t for x in ("2026-10-12 · Easy Run (main)","4.1 km","2026-10-13 · Strength A · Upper (main)","Incline dumbbell press 14 kg · 6/5/–/–","notes: easy 5k outside","2026-10-17 · 15-min KB Flow (16 kg) (quick)")),t[:400])
    ok("export carries the raw log as JSON",json.loads(t.split("--- JSON (wo_log) ---")[1].strip())==OLD)
    ok("export changes nothing on the phone",ls(p,"wo_log")==OLD)
    p.click(".exx");ok("export sheet closes",p.locator("#exs.show").count()==0)
    # the new fields appear in the export once present
    p.click("#close") if p.locator("#panel.open").count() else None;p.click('button.day[data-d="2026-11-07"]');p.wait_for_timeout(150)
    p.click("#addrun");p.fill("#r_d","3.3");p.dispatch_event("#r_d","input");p.fill("#r_t","20:00");p.dispatch_event("#r_t","input");p.click('#r_e [data-e="steady"]');p.fill("#r_n","evening");p.dispatch_event("#r_n","input");p.click("#runsave");p.wait_for_timeout(100)
    t=p.evaluate("()=>__app.exportText()")
    ok("export includes actual running time, effort and notes","2026-11-07 · Extra run (extra) · 20 min · 3.3 km · 20:00 · steady" in t and "notes: evening" in t,t[:300])
    ok("old logs still intact after adding a run",[x for x in ls(p,"wo_log") if x.get("type")!="extra"]==OLD)
    c.close()
    src=open("index.html",encoding="utf8").read()
    ok("no network calls or sharing without a tap",not re.search(r"fetch\(|XMLHttpRequest",src.split("navigator.serviceWorker.register")[0]) and src.count("navigator.share(")==1)
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
