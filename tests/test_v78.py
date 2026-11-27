# pc-v78: Lower · Step-Up Staircase moved to Fri 27 Nov (week file), recovery flow to Thu 26.
# A one-off on app open clears the old Edit plan rest flags / swaps for Thu 26 and Fri 27 (James's phone state)
# so the new plan shows. Logged entries and other days' flags are left alone, and it runs only once.
from playwright.sync_api import sync_playwright
from lib import *
LOG=[{"date":"2026-11-23","name":"Upper · Density Ladder","type":"main","sets":{}},
     {"date":"2026-11-24","name":"Tempo Triple","type":"main","sets":{}},
     {"date":"2026-11-25","name":"Run","type":"extra","extra":1,"act":"run","km":"5.13","time":"30:17","min":30.3}]
def week(b,seed):
    c,p=view(b,"2026-11-27",seed,hour=10,open_day=False)
    p.evaluate("()=>localStorage.removeItem('wo_flat')");p.reload();p.wait_for_selector("#tabbar",timeout=10000)
    p.click("#tabbar [data-tab=week]");p.wait_for_timeout(300);return c,p
def name(p,d): return p.locator(f'#wlist .wrow[data-d="{d}"] .wt').inner_text().strip()
def row(p,d): return p.locator(f'#wlist .wrow[data-d="{d}"]').inner_text()
with sync_playwright() as pw:
    b=launch(pw)
    c,p=week(b,{"wo_log":LOG,"wo_plan":{"2026-11-26":"Rest","2026-11-27":"Rest","2026-11-28":"Rest"}})
    ok("Fri 27 shows Lower · Step-Up Staircase",name(p,"2026-11-27")=="Lower · Step-Up Staircase",row(p,"2026-11-27"))
    ok("Fri 27 is Today","Today" in row(p,"2026-11-27") or "TODAY" in row(p,"2026-11-27"),row(p,"2026-11-27"))
    ok("Thu 26 shows the recovery flow",name(p,"2026-11-26")=="Recovery · Legs + Spine Reset",row(p,"2026-11-26"))
    pl=ls(p,"wo_plan") or {}
    ok("Thu/Fri rest flags cleared, Sat flag kept","2026-11-26" not in pl and "2026-11-27" not in pl and pl.get("2026-11-28")=="Rest",pl)
    ok("logged entries untouched",len(ls(p,"wo_log"))==3 and [e["date"] for e in ls(p,"wo_log")]==[e["date"] for e in LOG])
    ok("one-off flag set",ls(p,"wo_fix78")==1)
    p.screenshot(path="test-output/v78-week.png")
    # set Fri to rest again after the fix: a reload must not clear it a second time
    p.evaluate("()=>{var o=JSON.parse(localStorage.getItem('wo_plan')||'{}');o['2026-11-27']='Rest';localStorage.setItem('wo_plan',JSON.stringify(o));}")
    p.reload();p.wait_for_selector("#tabbar",timeout=10000);p.click("#tabbar [data-tab=week]");p.wait_for_timeout(300)
    ok("runs only once (a later rest choice stays)",name(p,"2026-11-27")=="Rest day")
    c.close()
    # today's session opens and can be started
    c,p=view(b,"2026-11-27",{"wo_plan":{"2026-11-27":"Rest"},"wo_daymap":{"2026-11-27":"2026-11-26","2026-11-26":"2026-11-27"}},hour=10)
    t=p.locator("#panel").inner_text()
    ok("today's panel is the Lower session (swap also cleared)","Carry ladder" in t and "hip airplane" in t.lower(),t[:800])
    ok("day swap for Thu/Fri cleared",not (ls(p,"wo_daymap") or {}),ls(p,"wo_daymap"))
    c.close()
    ok("no page errors",errs==[],errs)
    b.close()
raise SystemExit(done())
