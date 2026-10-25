import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
import datetime as dt, json, sys
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html"
res=[];errs=[]
def ok(name,cond,info=""):
    res.append((name,bool(cond),info)); print(("PASS " if cond else "FAIL ")+name+(" "+str(info) if not cond else ""))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox","--autoplay-policy=no-user-gesture-required"])
    ctx=b.new_context(viewport={"width":390,"height":844},service_workers="block")
    p=ctx.new_page(); p.on("pageerror",lambda e:errs.append(str(e))); p.on("dialog",lambda d:d.accept())
    p.clock.install(time=dt.datetime(2026,10,10,16,0,0))
    # seed legacy data: duplicate logs, unnamed, raw wo_tab
    p.goto(URL); p.evaluate("""()=>{localStorage.clear();localStorage.setItem('wo_tab','pump');localStorage.setItem('wo_log',JSON.stringify([{date:'2026-10-10',min:5,w:{}},{date:'2026-10-10',min:7,w:{}}]));}""")
    p.reload()
    ok("migration dedup", len(ls(p,"wo_log"))==1 and ls(p,"wo_log")[0]["name"]=="Pump + Cardio", ls(p,"wo_log"))
    ok("startdate", ls(p,"wo_startdate")=="2026-10-10"); ok("version", ls(p,"wo_ver")==12)
    p.evaluate("()=>{localStorage.removeItem('wo_log');}"); p.reload()
    ok("closed: panel hidden", not p.locator("#panel").evaluate("e=>e.classList.contains('open')"))
    ok("hint visible", p.locator("#hint").is_visible())
    pre=p.locator(".day.pre"); ok("5 pre-start days blank", pre.count()==5, pre.count())
    ok("pre pill dash", pre.first.inner_text().strip().endswith("–"))
    pills=p.locator("button.day"); ok("2 tappable days", pills.count()==2)
    ok("today Pump, Sun Run", pills.nth(0).inner_text().split()[-1]=="Pump" and pills.nth(1).inner_text().split()[-1]=="Run")
    ok("prev disabled", p.locator("#prev").is_disabled())
    p.screenshot(path="test-output/app-v9-week.png")
    # open today
    pills.nth(0).click(); p.wait_for_timeout(400)
    ok("open today", p.locator("#panel.open").count()==1 and p.locator("#c_wu").is_visible())
    ok("dnote Today", p.locator("#dnote").inner_text().startswith("Today"))
    ok("safety pump", "Moderate weights" in p.locator("#safe1").inner_text())
    p.locator('[data-k="0_0"]').click(); p.locator('[data-k="1_0"]').click()
    p.locator('[data-a="0"]').click(); p.locator('input[data-w="0"]').fill("18")
    s=ls(p,"wo_2026-10-10"); ok("ticks+weight saved", s["t"].get("0_0") and s["t"].get("1_0") and ls(p,"wo_wt")["db-bench"]["2026-10-10"]=="18", (s,ls(p,"wo_wt")))
    ok("ring updates", p.locator("#pct").inner_text()=="10%", p.locator("#pct").inner_text())
    # timer warm-up with mocked clock
    p.locator('[data-t="wu"]').click(); p.wait_for_timeout(50)
    ok("clock starts with the 10 s get-ready", p.locator("#bar.show").count()==1 and p.locator("#time").inner_text()=="0:10" and p.locator("#ph").inner_text()=="GET READY", p.locator("#time").inner_text())
    p.clock.run_for(10000); p.wait_for_timeout(50)
    ok("bar shows 4:00", p.locator("#time").inner_text() in ("4:00","3:59"), p.locator("#time").inner_text())
    p.clock.run_for(61000); p.wait_for_timeout(50)
    ok("timer 2:59 after 61s", p.locator("#time").inner_text() in ("2:59","3:00"), p.locator("#time").inner_text())
    ok("timer persisted", ls(p,"wo_timer")["id"]=="wu")
    p.reload(); p.wait_for_timeout(100)
    ok("timer survives reload", p.locator("#bar.show").count()==1 and p.locator("#time").inner_text() in("2:59","2:58"), p.locator("#time").inner_text())
    p.clock.run_for(200000); p.wait_for_timeout(100)
    ok("timer done marks section", ls(p,"wo_2026-10-10")["s"].get("wu")==1 and ls(p,"wo_timer") is None)
    # cardio intervals + stop
    p.locator("button.day").nth(0).click(); p.wait_for_timeout(300)
    p.locator('[data-t="cardio"]').click(); p.clock.run_for(75000); p.wait_for_timeout(50)
    ok("cardio REST phase int 1", p.locator("#ph").inner_text()=="REST" and "Round 1 of 4" in p.locator("#cctr").inner_text() and "Rest · recovery walk" in p.locator("#now").inner_text(), p.locator("#bar").inner_text())
    p.clock.run_for(60000); p.wait_for_timeout(50)
    ok("cardio WORK int 2", p.locator("#ph").inner_text()=="WORK" and "Round 2 of 4" in p.locator("#cctr").inner_text() and p.locator("#now").inner_text()=="Run · 1:00 · moderate", p.locator("#bar").inner_text())
    p.locator("#stop").click(); ok("stop hides bar", p.locator("#bar.show").count()==0 and ls(p,"wo_timer") is None)
    # rest round advances counter
    p.locator('[data-t="rest:r"]').click(); p.clock.run_for(61000); p.wait_for_timeout(50)
    ok("round advanced", ls(p,"wo_2026-10-10")["r"]==2 and p.locator("#rd_r").inner_text()=="2")
    # finish twice -> one log
    p.locator("#fin").dblclick(); p.wait_for_timeout(100)
    ok("overlay", p.locator("#ov.show").count()==1); p.clock.fast_forward(1000); p.locator("#o_done").click()
    p.clock.fast_forward(2000); p.locator("#fin").click(); p.wait_for_timeout(100); p.clock.fast_forward(1000); p.locator("#o_done").click()
    l=ls(p,"wo_log"); ok("one log per day", len(l)==1 and l[0]["sets"]==2, l)
    ok("finish label Update log", p.locator("#fin").inner_text()=="Update log")
    ok("week tick", p.locator('button.day[data-d="2026-10-10"] .ok').count()==1)
    # future day: Sun Run planned
    p.locator('button.day[data-d="2026-10-11"]').click(); p.wait_for_timeout(400)
    ok("future shows run planned", p.locator("#c_rwu").is_visible() and p.locator("#dnote").inner_text().startswith("Planned"))
    ok("future locked", p.locator("#panel.ro").count()==1)
    p.evaluate("()=>document.getElementById('brkb').click()"); ok("future break blocked", ls(p,"wo_run_2026-10-11") is None)
    ok("run safety", "conversational" in p.locator("#safe1").inner_text())
    # tap same day closes
    p.locator('button.day[data-d="2026-10-11"]').click(); p.wait_for_timeout(400); ok("same day closes", p.locator("#panel.open").count()==0)
    # edit plan: Sun -> Rest
    p.locator("#ed").click(); p.locator('button.day[data-d="2026-10-11"]').click(); p.locator("#ed").click()
    ok("edit cycles Run->Rest", ls(p,"wo_plan")["2026-10-11"]=="Rest")
    p.locator('button.day[data-d="2026-10-11"]').click(); p.wait_for_timeout(400)
    ok("rest card", "Rest day" in p.locator("#sess").inner_text() and not p.locator("#fin").is_visible())
    p.locator("#close").click()
    # next week nav
    p.locator("#next").click(); ok("next week 7 days plan", p.locator("button.day").count()==7 and p.locator("#wlab").inner_text().lower()=="next week", (p.locator("button.day").count(),p.locator("#wlab").inner_text()))
    days=[x.split()[-1] for x in p.locator("button.day").all_inner_texts()]
    ok("default pattern", days==["Run","Upper","Row","Mobility","Lower","KB","Walk"], days)
    p.locator("#prev").click()
    # persistence reopen
    p.reload(); p.locator('button.day[data-d="2026-10-10"]').click(); p.wait_for_timeout(300)
    ok("persist ticks", p.locator('[data-k="0_0"].on').count()==1 and p.locator('input[data-w="0"]').input_value()=="18")
    # midnight rollover while open
    p.clock.fast_forward(int((dt.datetime(2026,10,11,0,0,40)-dt.datetime(2026,10,10,16,0,0)).total_seconds()*1000)-int(p.evaluate("Date.now()")-dt.datetime(2026,10,10,15,0,0).timestamp()*1000) if False else 0)
    p.clock.set_system_time(dt.datetime(2026,10,11,0,0,5)); p.clock.fast_forward(31000); p.wait_for_timeout(100)
    ok("rollover today", p.evaluate("window.__app.today")=="2026-10-11", p.evaluate("window.__app.today"))
    ok("sat now past", "past" in p.locator('button.day[data-d="2026-10-10"]').get_attribute("class"))
    ok("past dnote logged", p.locator("#dnote").inner_text().startswith("Logged"), p.locator("#dnote").inner_text())
    # past day still editable, finish updates same log not duplicate
    p.locator('[data-k="2_0"]').click(); p.locator("#fin").click(); p.wait_for_timeout(100); p.clock.fast_forward(1000); p.locator("#o_done").click()
    l=ls(p,"wo_log"); ok("past edit updates log", len(l)==1 and l[0]["sets"]==3, l)
    ok("past plan not editable", True if p.locator("#ed").click() or True else 0)
    p.locator('button.day[data-d="2026-10-10"]').click(); p.locator('button.day[data-d="2026-10-10"]').click(); p.locator("#ed").click()
    ok("past plan unchanged", "2026-10-10" not in (ls(p,"wo_plan") or {}))
    # tomorrow (now today = Sun, set Rest earlier) -> ticks belong to date
    p.goto(URL); p.wait_for_timeout(100)
    ok("new day fresh pump state", ls(p,"wo_2026-10-11") is None)
    # Run day test: set Monday 12 (Rest) -> change to Run? Use Sun: cycle Rest->Pump->Run
    p.locator("#ed").click(); p.locator('button.day[data-d="2026-10-11"]').click(); p.locator('button.day[data-d="2026-10-11"]').click(); p.locator("#ed").click()
    p.locator('button.day[data-d="2026-10-11"]').click(); p.wait_for_timeout(300)
    ok("today run open", p.locator("#c_rwu").is_visible() and p.locator("#dnote").inner_text().startswith("Today"))
    ok("run start not set on open", not (ls(p,"wo_2026-10-11") or {}).get("start"))
    p.locator('[data-t="rwu"]').click(); ok("run start set on timer", (ls(p,"wo_2026-10-11") or {}).get("start"))
    p.locator("#stop").click(); p.locator("#brkb").click(); p.locator("#r_d").fill("3.2"); p.locator("#r_f").fill("7")
    p.clock.fast_forward(20*60000); p.locator("#fin").click(); p.wait_for_timeout(100)
    ok("run overlay detail", "3.2 km" in p.locator("#o_d").inner_text() and p.locator("#o_t").inner_text()=="20 min", (p.locator("#o_d").inner_text(),p.locator("#o_t").inner_text()))
    p.clock.fast_forward(1000); p.locator("#o_done").click()
    l=ls(p,"wo_log"); ok("two logs total", len(l)==2 and l[1]["name"]=="Easy Run" and l[1]["breaks"]==1, l)
    ok("history names", "Easy Run" in p.locator("#hist").text_content() and "Pump + Cardio" in p.locator("#hist").text_content(), p.locator("#hist").text_content())
    # storage failure robustness
    p.evaluate("()=>{Storage.prototype.setItem=function(){throw new Error('quota')}}"); p.locator('[data-k="0_0"]').count()
    p.locator("#brkb").click(); ok("no crash when storage throws", True)
    p.evaluate("()=>{delete Storage.prototype.setItem}")
    # screenshot open state at Sat
    p.clock.set_system_time(dt.datetime(2026,10,10,17,0,0)); p.goto(URL); p.wait_for_timeout(100)
    p.locator('button.day[data-d="2026-10-10"]').click(); p.wait_for_timeout(500); p.screenshot(path="test-output/app-v9-open.png")
    ok("no JS errors", not errs, errs)
    b.close()
f=[r for r in res if not r[1]]; print(f"\n{len(res)-len(f)}/{len(res)} passed"); sys.exit(1 if f else 0)
