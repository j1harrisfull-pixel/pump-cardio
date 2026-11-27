# pc-v77: in Edit this week's plan a tap that sets a day to rest says so ("Thu set to rest. Tap again to undo."), a second tap
# restores it ("Thu is back to …"), and a past day this week that was set to rest can be switched back. Other past days stay locked.
from playwright.sync_api import sync_playwright
from lib import *
def tabs(b,d,seed,hour=9):
    c,p=view(b,d,seed,hour=hour,open_day=False)
    p.evaluate("()=>localStorage.removeItem('wo_flat')");p.reload();p.wait_for_selector("#tabbar",timeout=10000)
    p.click("#tabbar [data-tab=week]");p.wait_for_timeout(200);p.click("#ed2");p.wait_for_timeout(200);return c,p
def toast(p): return p.locator("#toast").inner_text() if p.locator("#toast.show").count() else ""
def name(p,d): return p.locator(f'#wlist .wrow[data-d="{d}"] .wt').inner_text().strip()
with sync_playwright() as pw:
    b=launch(pw)
    # Thu 26 set to rest the day before, now Fri 27 (the state on James's phone)
    c,p=tabs(b,"2026-11-27",{"wo_plan":{"2026-11-26":"Rest","2026-11-27":"Rest"}})
    ok("both days start as rest",name(p,"2026-11-26")=="Rest day" and name(p,"2026-11-27")=="Rest day")
    p.click('#week button.day[data-d="2026-11-26"]');p.wait_for_timeout(200)
    ok("past Thu set to rest can be switched back",name(p,"2026-11-26")=="Lower · Step-Up Staircase" and "2026-11-26" not in (ls(p,"wo_plan") or {}),ls(p,"wo_plan"))
    ok("message says it is back","Thu is back to Lower · Step-Up Staircase" in toast(p),toast(p))
    p.click('#week button.day[data-d="2026-11-26"]');p.wait_for_timeout(200)
    ok("a past day that is not rest stays locked (no second change)",name(p,"2026-11-26")=="Lower · Step-Up Staircase" and "2026-11-26" not in (ls(p,"wo_plan") or {}))
    p.click('#week button.day[data-d="2026-11-27"]');p.wait_for_timeout(200)
    ok("today back from rest",name(p,"2026-11-27")=="Recovery · Legs + Spine Reset" and "Fri is back to" in toast(p),toast(p))
    p.click('#week button.day[data-d="2026-11-28"]');p.wait_for_timeout(200)
    ok("a tap that sets a day to rest says so","Sat set to rest. Tap again to undo." in toast(p) and name(p,"2026-11-28")=="Rest day",toast(p))
    p.screenshot(path="test-output/v77-msg.png")
    p.click('#week button.day[data-d="2026-11-28"]');p.wait_for_timeout(200)
    ok("tap again undoes it",name(p,"2026-11-28")=="Bell Circuit + Gentle Hills 5K" and "Sat is back to" in toast(p))
    p.click('#week button.day[data-d="2026-11-24"]');p.wait_for_timeout(200)
    ok("an ordinary past day can't be set to rest","2026-11-24" not in (ls(p,"wo_plan") or {}) and name(p,"2026-11-24")=="Tempo Triple")
    c.close()
    # a past day in an earlier week stays locked even if it was rest
    c,p=tabs(b,"2026-11-27",{"wo_plan":{"2026-11-19":"Rest"}})
    p.evaluate("()=>{}");p.click("#prev");p.wait_for_timeout(200)
    if p.locator('#week button.day[data-d="2026-11-19"]').count(): p.click('#week button.day[data-d="2026-11-19"]');p.wait_for_timeout(200)
    ok("last week's rest day stays as it was",(ls(p,"wo_plan") or {}).get("2026-11-19")=="Rest")
    c.close()
    ok("no page errors",errs==[],errs)
    b.close()
raise SystemExit(done())
