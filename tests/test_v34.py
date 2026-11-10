import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v34: swap two day slots in the current week (BRIEF-day-swap.md). wo_daymap {calendar date: source date};
# backup / quick / run-instead follow the moved session; toggles, ticks and logs stay on the calendar date trained.
import datetime as dt, json
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
THU,FRI,MON,SAT,SUN="2026-11-05","2026-11-06","2026-11-02","2026-11-07","2026-11-08"
LOG=[{"date":MON,"name":"Zone 2 Run","type":"main","sid":"run02","min":40}]
def mk(b,d,seed=None):
    y,m,dd=map(int,d.split("-"))
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block");p=c.new_page()
    p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda x:x.accept());p.clock.install(time=dt.datetime(y,m,dd,9,0));p.goto(URL)
    p.evaluate("t=>{localStorage.clear();localStorage.setItem('wo_chg','1');localStorage.setItem('wo_flat','1');localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');for(var k in t)localStorage.setItem(k,JSON.stringify(t[k]));}",seed or {})
    p.reload();p.wait_for_timeout(150)
    if p.locator("#panel.open").count(): p.click("#close")
    return c,p
pl=lambda p,d:p.locator(f'button.day[data-d="{d}"] .pl').inner_text()
def opend(p,d):
    if p.locator("#panel.open").count(): p.click("#close")
    p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(200)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    c,p=mk(b,FRI,{"wo_log":LOG})
    N=p.evaluate("()=>{var S=__how.SESS,P=__wk.PROG,B=__wk.BK,o={};Object.keys(P).forEach(function(d){o[d]={main:P[d],name:S[P[d]].name,short:S[P[d]].short,bk:B[d]?S[B[d]].name:null,ri:S[P[d]].blocks.some(function(x){return x.ri;})};});return o;}")
    # ---- no wo_daymap: unchanged
    ok("old installs: no wo_daymap, labels as planned",ls(p,"wo_daymap") is None and pl(p,THU)==N[THU]["short"] and pl(p,FRI)==N[FRI]["short"])
    ok("swap row hidden outside Edit plan",not p.locator("#swr").is_visible())
    # ---- Edit plan → Swap days → Thu, Fri
    p.click("#ed");ok("Edit plan shows Swap days",p.locator("#swd").is_visible() and p.locator("#swd").inner_text()=="Swap days" and not p.locator("#swreset").is_visible())
    ok("'Swap today's session' (coach request) is a separate control",p.locator("#swap").inner_text()=="Swap today's session" if p.locator("#swap").count() else True)
    p.click("#swd");ok("swap mode asks for the first day",p.locator("#swh").inner_text()=="Tap the first day.")
    p.click(f'button.day[data-d="{THU}"]');ok("first day picked",p.locator(f'button.day[data-d="{THU}"].pick').count()==1 and "swap with Thu" in p.locator("#swh").inner_text())
    p.click(f'button.day[data-d="{FRI}"]');p.wait_for_timeout(100)
    ok("wo_daymap stores both directions",ls(p,"wo_daymap")=={THU:FRI,FRI:THU},ls(p,"wo_daymap"))
    ok("strip labels swapped",pl(p,THU)==N[FRI]["short"] and pl(p,FRI)==N[THU]["short"],(pl(p,THU),pl(p,FRI)))
    ok("swap confirmed, mode ends, Reset shown","Swapped Thu and Fri" in p.locator("#swh").inner_text() and p.locator("#swd").inner_text()=="Swap days" and p.locator("#swreset").is_visible())
    ok("no Rest toggled by the swap taps",not (ls(p,"wo_plan") or {}))
    p.click("#ed")
    # ---- Friday opens Thursday's Lower; backup travels with it; Finish logs Friday
    opend(p,FRI)
    ok("Fri opens Thu's main session",p.locator("#ttl").inner_text()==N[THU]["name"],p.locator("#ttl").inner_text())
    ok("day note says where it moved from","moved from Thu" in p.locator("#dnote").inner_text(),p.locator("#dnote").inner_text())
    ok("backup follows the moved session",N[THU]["bk"] is None or N[THU]["bk"].replace("Backup · ","") in p.locator("#alt").inner_text(),p.locator("#alt").inner_text())
    tk=p.locator("[data-tk]")
    if tk.count(): tk.first.click();p.wait_for_timeout(50);p.click("#rskip") if p.locator("#rbar.show").count() else None
    p.click("#fin");p.clock.fast_forward(1000);p.wait_for_timeout(100);p.click("#o_done")
    e=[x for x in ls(p,"wo_log") if x["date"]==FRI]
    ok("Finish logs the calendar date trained, with the moved session",len(e)==1 and e[0]["name"]==N[THU]["name"] and e[0]["sid"]==N[THU]["main"] and e[0]["type"]=="main",e)
    ok("ticks stay keyed by Friday",(ls(p,"wo_"+FRI) or {}).get("t") is not None and ls(p,"wo_"+THU) is None)
    ok("Mon log untouched",[x for x in ls(p,"wo_log") if x["date"]==MON]==LOG)
    opend(p,THU);ok("Thu shows Fri's session",p.locator("#ttl").inner_text()==N[FRI]["name"])
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("history Edit offers the moved session's backup",[o.split("|")[0] for o in p.locator(f'#hist select[data-hd="{FRI}"] option').evaluate_all("o=>o.map(x=>x.value+'|'+x.textContent)")][:2]==["main","backup"])
    p.click("#close")
    # ---- blocks: logged or started days stay put
    p.click("#ed");p.click("#swd");p.click(f'button.day[data-d="{MON}"]')
    ok("logged day can't be swapped","already logged" in p.locator("#swh").inner_text() and ls(p,"wo_daymap")=={THU:FRI,FRI:THU})
    p.click(f'button.day[data-d="{FRI}"]');ok("day with ticks (or now logged) can't be swapped","stays put" in p.locator("#swh").inner_text())
    p.click("#swd");ok("Cancel swap leaves swap mode",p.locator("#swd").inner_text()=="Swap days")
    p.click(f'button.day[data-d="{SUN}"]');ok("outside swap mode, Edit plan tap still toggles Rest",(ls(p,"wo_plan") or {}).get(SUN)=="Rest" and pl(p,SUN)=="Rest")
    p.click(f'button.day[data-d="{SUN}"]');ok("and back",SUN not in (ls(p,"wo_plan") or {}))
    p.click("#next");ok("other weeks: no swap controls",not p.locator("#swr").is_visible());p.click("#prev")
    ok("back on this week: swap row again",p.locator("#swr").is_visible());p.click("#ed")
    c.close()
    # ---- undo by swapping again; Reset week order; run instead follows the session
    c,p=mk(b,THU);p.click("#ed");p.click("#swd");p.click(f'button.day[data-d="{THU}"]');p.click(f'button.day[data-d="{FRI}"]')
    p.click("#swd");p.click(f'button.day[data-d="{FRI}"]');p.click(f'button.day[data-d="{THU}"]')
    ok("swapping the same pair again undoes it",(ls(p,"wo_daymap") or {})=={} and pl(p,THU)==N[THU]["short"])
    ri=[d for d in (SAT,SUN) if N[d]["ri"]];other=SAT if ri and ri[0]==SUN else SUN
    p.click("#swd");p.click(f'button.day[data-d="{THU}"]');p.click(f'button.day[data-d="{SAT}"]')
    p.click("#swreset");ok("Reset week order clears this week",(ls(p,"wo_daymap") or {})=={} and pl(p,SAT)==N[SAT]["short"] and not p.locator("#swreset").is_visible())
    if ri:
        src=ri[0];dst=other if other>=THU else THU
        p.click("#swd");p.click(f'button.day[data-d="{src}"]');p.click(f'button.day[data-d="{dst}"]');p.click("#ed")
        opend(p,dst);ok("Run instead follows the moved session",p.locator("#ri").is_visible(),(src,dst))
        p.click("#ri");p.wait_for_timeout(100);ok("run toggle saved on the calendar date",(ls(p,"wo_ri") or {}).get(dst)==1 and src not in (ls(p,"wo_ri") or {}))
        opend(p,src);ok("the other day has no run option unless its new session has one",p.locator("#ri").is_visible()==N[dst]["ri"])
    c.close()
    # ---- a stale / odd wo_daymap value is ignored
    c,p=mk(b,THU,{"wo_daymap":{THU:"not-a-date",FRI:42}})
    ok("bad wo_daymap values are ignored",pl(p,THU)==N[THU]["short"] and pl(p,FRI)==N[FRI]["short"]);c.close()
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
