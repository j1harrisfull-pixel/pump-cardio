import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v33: beauty pass, white + orange (BRIEF-beauty-pass.md). Visual chrome only: theme tokens, week pills,
# cards, clock and rest bar colours, ≥44 px tap targets. Behaviour is covered by the other suites.
import datetime as dt
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
WHITE="rgb(255, 255, 255)";BG="rgb(245, 245, 247)";TEXT="rgb(17, 17, 17)";ORANGE="rgb(255, 138, 61)";MUTED="rgb(107, 107, 112)"
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block");p=c.new_page()
    p.on("pageerror",lambda e:errs.append(str(e)));p.clock.install(time=dt.datetime(2026,11,3,8,0));p.goto(URL)
    p.evaluate("()=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');}");p.reload();p.wait_for_timeout(200)
    cs=lambda sel,prop:p.locator(sel).first.evaluate(f"e=>getComputedStyle(e).{prop}")
    h=lambda sel:p.locator(sel+":visible").first.evaluate("e=>e.getBoundingClientRect().height")
    ok("page background #F5F5F7",cs("body","backgroundColor")==BG,cs("body","backgroundColor"))
    ok("text #111111",cs("body","color")==TEXT)
    ok("browser chrome colour is light",p.locator('meta[name="theme-color"]').get_attribute("content")=="#F5F5F7")
    ok("today pill solid orange, white text",cs(".day.today","backgroundColor")==ORANGE and cs(".day.today .dd","color")==WHITE)
    ok("other days are white pills with a hairline",cs('.day:not(.today):not(.pre)',"backgroundColor")==WHITE and cs('.day:not(.today):not(.pre)',"borderTopColor")=="rgb(232, 232, 237)")
    ok("progress ring: orange fill on a hairline track",cs("#rg","stroke")==ORANGE and cs(".ring .bg","stroke")=="rgb(232, 232, 237)")
    ok("week arrows ≥44 px",h("#prev")>=44 and h("#ed")>=44)
    if not p.locator("#panel.open").count(): p.click('button.day[data-d="2026-11-03"]');p.wait_for_timeout(250)
    ok("cards white, soft rounded (16–20 px)",cs(".card","backgroundColor")==WHITE and 16<=float(cs(".card","borderTopLeftRadius")[:-2])<=20)
    ok("muted notes #6B6B70",cs(".card .note","color")==MUTED)
    ok("primary button orange",cs(".btn:not(.ghost)","backgroundColor")==ORANGE)
    ok("stop-signs line still shown",p.locator(".safe .stop").is_visible() and "sudden or severe headache" in p.locator(".safe .stop").inner_text())
    p.locator(".more").first.click();p.wait_for_timeout(60)
    for sel in (".close",".more",".how",".tk",".rpb",".srow input.w","#swap"):
        if p.locator(sel).count(): ok(f"{sel} tap height ≥44 px",h(sel)>=44,h(sel))
    p.locator("[data-tk]").first.click();p.wait_for_timeout(80)
    ok("rest bar light, Skip orange",cs("#rbar","backgroundColor").startswith("rgba(255, 255, 255") and cs("#rskip","backgroundColor")==ORANGE and cs("#rtime","color")==TEXT)
    ok("rest bar buttons ≥44 px",all(h(x)>=44 for x in ("#rm15","#rp15","#rskip")));p.click("#rskip")
    p.locator('#sess [data-t]').first.click();p.clock.run_for(11000);p.wait_for_timeout(80)
    ok("clock: near-black countdown on a light screen",cs("#time","color")==TEXT and cs("#bar","backgroundImage")!="none" or cs("#bar","backgroundColor") in (WHITE,BG))
    ok("clock: Pause orange, WORK label orange",cs("#tpause","backgroundColor")==ORANGE and cs("#ph","color")==ORANGE,(cs("#tpause","backgroundColor"),cs("#ph","color")))
    ok("clock controls ≥44 px",all(h(x)>=44 for x in ("#tback","#tpause","#tnext","#stop","#tlock")))
    p.click("#stop");ok("no page errors",not errs,errs[:3]);b.close()
print(f"{sum(res)}/{len(res)} passed")
