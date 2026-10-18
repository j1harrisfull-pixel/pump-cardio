import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
import datetime as dt, json, sys
from playwright.sync_api import sync_playwright
BASE="http://localhost:8765/";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)))
def ls(p,k): return p.evaluate("k=>JSON.parse(localStorage.getItem(k)||'null')",k)
SEED="""()=>{localStorage.clear();localStorage.setItem('wo_startdate','"2026-10-10"');localStorage.setItem('wo_ver','12');}"""
def ctx(b): return b.new_context(viewport={"width":390,"height":844},device_scale_factor=3,is_mobile=True,has_touch=True,service_workers="block")
def pg(c,file,t):
    p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.clock.install(time=t);p.goto(BASE+file);return p
def run_day(p):
    p.click('button.day[data-d="2026-10-14"]');p.wait_for_timeout(250);p.click("#ri");p.wait_for_timeout(200)
    p.fill("#r_d","5");p.dispatch_event("#r_d","input");p.dispatch_event("#r_d","change");p.click("#fin");p.clock.fast_forward(1000);p.wait_for_timeout(200)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    T=dt.datetime(2026,10,14,17,0)
    if "--repro" in sys.argv:
        c=ctx(b);p=pg(c,"old23.html",T);p.evaluate(SEED);p.reload();run_day(p);e=ls(p,"wo_log")[-1]
        print("REPRO v23 log name:",e["name"],"| summary:",p.locator("#o_n").inner_text());c.close();sys.exit()
    # 1 run instead logs as run everywhere
    c=ctx(b);p=pg(c,"index.html",T);p.evaluate(SEED);p.reload();run_day(p);e=ls(p,"wo_log")[-1]
    ok("log name is run",e["name"]=="Run Intervals",e);ok("log type run + sid",e.get("type")=="run" and e.get("sid")=="row" and e.get("ri")==1,e)
    ok("log km 5",e.get("km")=="5",e)
    ok("finish summary run",p.locator("#o_n").inner_text()=="Run Intervals" and "run instead" in p.locator("#o_d").inner_text(),p.locator("#o_n").inner_text())
    p.click("#o_done");p.wait_for_timeout(150)
    ok("title run",p.locator("#ttl").inner_text()=="Run Intervals")
    ok("distance label km",p.locator("label:has(#r_d)").inner_text().startswith("Distance (km)"))
    ok("day shows logged","Logged" in p.locator("#dnote").inner_text() or "Today" in p.locator("#dnote").inner_text())
    p.click("#close");ok("strip says Run",p.locator('button.day[data-d="2026-10-14"] .pl').inner_text()=="Run")
    p.evaluate("()=>document.querySelector('details').open=true")
    h=p.locator("#hist li").first.inner_text();ok("history says run","Run Intervals" in h and "Rower" not in h,h)
    # history edit -> main -> run
    p.select_option('#hist select[data-hd="2026-10-14"]',"main");p.wait_for_timeout(150)
    e=ls(p,"wo_log")[-1];ok("edit to Main",e["name"]=="Rower Intervals" and e["type"]=="main" and "ri" not in e and not (ls(p,"wo_ri") or {}).get("2026-10-14"),e)
    ok("strip back to Row",p.locator('button.day[data-d="2026-10-14"] .pl').inner_text()=="Row")
    p.select_option('#hist select[data-hd="2026-10-14"]',"backup");p.wait_for_timeout(150)
    e=ls(p,"wo_log")[-1];ok("edit to Backup",e["name"]=="Backup · Runner Walk + Core" and e["type"]=="backup" and ls(p,"wo_alt").get("2026-10-14"),e)
    p.select_option('#hist select[data-hd="2026-10-14"]',"run");p.wait_for_timeout(150)
    e=ls(p,"wo_log")[-1];ok("edit to Run instead",e["name"]=="Run Intervals" and e["type"]=="run" and not (ls(p,"wo_alt") or {}).get("2026-10-14"),e)
    ok("one entry only for the day",len([x for x in ls(p,"wo_log") if x["date"]=="2026-10-14"])==1)
    c.close()
    # 2 backup toggle
    c=ctx(b);p=pg(c,"index.html",dt.datetime(2026,10,13,17,0));p.evaluate(SEED);p.reload()
    p.click('button.day[data-d="2026-10-13"]');p.wait_for_timeout(250);p.click("#alt");p.wait_for_timeout(200);p.click("#fin");p.clock.fast_forward(1000);p.wait_for_timeout(200)
    e=ls(p,"wo_log")[-1];ok("backup logs as backup",e["name"]=="Backup · Upper (KB + Bodyweight)" and e["type"]=="backup" and e["sid"]=="bk13",e)
    ok("backup finish summary",p.locator("#o_n").inner_text()=="Backup · Upper (KB + Bodyweight)")
    p.click("#o_done");p.evaluate("()=>document.querySelector('details').open=true");ok("backup history","Backup · Upper" in p.locator("#hist li").first.inner_text())
    c.close()
    # 2b backup + run instead (Wed backup)
    c=ctx(b);p=pg(c,"index.html",T);p.evaluate(SEED);p.reload()
    p.click('button.day[data-d="2026-10-14"]');p.wait_for_timeout(250);p.click("#alt");p.wait_for_timeout(200);p.click("#ri");p.wait_for_timeout(200)
    ok("backup run title",p.locator("#ttl").inner_text()=="Backup · Run/Walk + Core");p.click("#fin");p.clock.fast_forward(1000)
    e=ls(p,"wo_log")[-1];ok("backup run log",e["name"]=="Backup · Run/Walk + Core" and e["type"]=="run" and e["sid"]=="bk14",e);c.close()
    # 3 migration of James's real log
    OTHER=[{"date":"2026-10-12","name":"Easy Run","min":34,"feel":"6","km":""},{"date":"2026-10-13","name":"Strength A · Upper","min":36,"sets":20,"of":24}]
    ROW={"date":"2026-10-14","name":"Rower Intervals","min":31,"km":"5","feel":"4","notes":"easy 5k outside","breaks":0}
    for flag in (True,False):
        c=ctx(b);p=pg(c,"index.html",dt.datetime(2026,10,14,18,0))
        p.evaluate("""([lg,f])=>{localStorage.clear();localStorage.setItem('wo_startdate','"2026-10-10"');localStorage.setItem('wo_ver','12');localStorage.setItem('wo_log',JSON.stringify(lg));if(f)localStorage.setItem('wo_ri',JSON.stringify({'2026-10-14':1}));}""",[OTHER+[ROW],flag]);p.reload()
        L=ls(p,"wo_log");m=[x for x in L if x["date"]=="2026-10-14"][0]
        ok(f"migr(flag={flag}) relabelled",m["name"]=="Easy run 5 km" and m["type"]=="run" and m["ri"]==1,m)
        ok(f"migr(flag={flag}) rest intact",all(m[k]==ROW[k] for k in ROW if k!="name"),m)
        ok(f"migr(flag={flag}) others untouched",L[:2]==OTHER,L[:2])
        p.reload();p.reload();ok(f"migr(flag={flag}) idempotent",ls(p,"wo_log")==L)
        p.click('button.day[data-d="2026-10-14"]');p.wait_for_timeout(250)
        ok(f"migr(flag={flag}) day view run + logged",p.locator("#ttl").inner_text()=="Run Intervals" and p.locator("#fin").inner_text()=="Update log",p.locator("#fin").inner_text())
        p.click("#close");ok(f"migr(flag={flag}) strip Run",p.locator('button.day[data-d="2026-10-14"] .pl').inner_text()=="Run")
        if flag: p.screenshot(path="test-output/app-v24.png")
        c.close()
    # other dates' Rower entries untouched by migration
    c=ctx(b);p=pg(c,"index.html",T);x=[{"date":"2026-10-21","name":"Rower Intervals","min":30}]
    p.evaluate("lg=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');localStorage.setItem('wo_log',JSON.stringify(lg))}",x);p.reload()
    ok("migration ignores other dates",ls(p,"wo_log")==x);c.close()
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
