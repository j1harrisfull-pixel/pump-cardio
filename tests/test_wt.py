import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
import datetime as dt, sys
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(c); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    p=b.new_context(viewport={"width":390,"height":844},service_workers="block").new_page(); p.on("pageerror",lambda e:errs.append(str(e)))
    p.clock.install(time=dt.datetime(2026,10,11,10,0,0)); p.goto(URL)
    # migration from v9 per-date weights
    p.evaluate("""()=>{localStorage.clear();localStorage.setItem('wo_ver','9');localStorage.setItem('wo_startdate','"2026-10-10"');
      localStorage.setItem('wo_2026-10-10',JSON.stringify({t:{'0_0':true},w:{'0':'18','4':'12'},r:1,s:{},start:1}));
      localStorage.setItem('wo_plan',JSON.stringify({'2026-10-11':'Pump','2026-10-12':'Pump'}));}""")
    p.reload()
    wt=ls(p,"wo_wt"); ok("migration db-bench", wt["db-bench"]["2026-10-10"]=="18" and wt["db-shoulder-press"]["2026-10-10"]=="12", wt); ok("ver 12", ls(p,"wo_ver")==12)
    p.click('button.day[data-d="2026-10-11"]'); p.wait_for_timeout(300)
    inp=p.locator('input[data-w="0"]'); ok("prefill from previous date", inp.input_value()=="18" and "pf" in inp.get_attribute("class"))
    ok("Last line", "Last: 18 kg (Sat 10 Oct)" in p.locator("#sess .card[data-x]").nth(0).text_content(), p.locator("#sess .card[data-x]").nth(0).text_content())
    ok("prefill not saved yet", "2026-10-11" not in ls(p,"wo_wt")["db-bench"])
    ok("no prefill when none", p.locator('[data-a="1"]').count()==1 and p.locator('input[data-w="1"]').count()==0 and "Suggested: 14–18 kg each" in p.locator("#sess .card[data-x]").nth(1).text_content())
    p.click('[data-k="4_0"]'); ok("tick saves prefill", ls(p,"wo_wt")["db-shoulder-press"].get("2026-10-11")=="12")
    p.locator('input[data-w="0"]').fill("20"); p.locator('input[data-w="0"]').dispatch_event("change"); p.wait_for_timeout(100)
    ok("update after change", ls(p,"wo_wt")["db-bench"]["2026-10-11"]=="20")
    ok("trend arrow", p.locator("#sess .card[data-x]").nth(0).locator(".up").count()==1)
    p.locator('[data-a="1"]').click(); p.locator('input[data-w="1"]').fill("16")
    ok("new weight saved by id", ls(p,"wo_wt")["cs-row"]["2026-10-11"]=="16")
    p.click("#fin"); p.clock.fast_forward(1000); p.click("#o_done")
    e=ls(p,"wo_log")[-1]; ok("log has weights by id", e["wt"]["db-bench"]=="20" and e["w"]["0"]=="20", e)
    # next day picks most recent
    p.click("#close"); p.click("#next"); p.click('button.day[data-d="2026-10-13"]'); p.wait_for_timeout(300)
    ok("Tue cs-row carries Last from Pump", "Last: 16 kg (Sun 11 Oct)" in p.locator('#sess .mvh[data-x="cs-row"]').text_content())
    p.click("#close"); p.click("#prev"); p.click('button.day[data-d="2026-10-11"]'); p.wait_for_timeout(300)
    ok("same-day shows earlier last", "Last: 18 kg (Sat 10 Oct)" in p.locator("#sess .card[data-x]").nth(0).text_content() and p.locator('input[data-w="0"]').input_value()=="20")
    p.reload(); p.click('button.day[data-d="2026-10-11"]'); p.wait_for_timeout(300)
    ok("persist after reload", p.locator('input[data-w="0"]').input_value()=="20" and "pf" not in p.locator('input[data-w="0"]').get_attribute("class"))
    p.on("dialog",lambda d:d.accept()); p.click("#rst"); p.wait_for_timeout(100)
    ok("reset clears day weights", "2026-10-11" not in ls(p,"wo_wt")["db-bench"] and ls(p,"wo_wt")["db-bench"]["2026-10-10"]=="18")
    ok("no JS errors", not errs, errs); b.close()
print(f"{sum(res)}/{len(res)} passed"); sys.exit(0 if all(res) else 1)
