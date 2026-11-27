# pc-v77 (kept for the old one page layout, wo_flat=1): in Edit plan a tap that sets a day to rest says so ("Thu set to rest.
# Tap again to undo."), a second tap restores it ("Thu is back to …"), and a past day this week that was set to rest can be
# switched back. Other past days stay locked. (v79: the tabs layout has no Edit plan mode; see test_v79 for the new menu.)
from playwright.sync_api import sync_playwright
from lib import *
def flat(b,d,seed,hour=9):
    c,p=view(b,d,seed,hour=hour,open_day=False);p.click("#ed");p.wait_for_timeout(200);return c,p
def toast(p): return p.locator("#toast").inner_text() if p.locator("#toast.show").count() else ""
def rest(p,d): return (ls(p,"wo_plan") or {}).get(d)=="Rest"
with sync_playwright() as pw:
    b=launch(pw)
    c,p=flat(b,"2026-11-27",{"wo_plan":{"2026-11-26":"Rest","2026-11-27":"Rest"},"wo_fix78":1})
    ok("both days start as rest",rest(p,"2026-11-26") and rest(p,"2026-11-27"))
    p.click('#week button.day[data-d="2026-11-26"]');p.wait_for_timeout(200)
    ok("past Thu set to rest can be switched back",not rest(p,"2026-11-26"),ls(p,"wo_plan"))
    ok("message says it is back","Thu is back to Recovery · Legs + Spine Reset" in toast(p),toast(p))
    p.click('#week button.day[data-d="2026-11-26"]');p.wait_for_timeout(200)
    ok("a past day that is not rest stays locked (no second change)",not rest(p,"2026-11-26"))
    p.click('#week button.day[data-d="2026-11-27"]');p.wait_for_timeout(200)
    ok("today back from rest",not rest(p,"2026-11-27") and "Fri is back to" in toast(p),toast(p))
    p.click('#week button.day[data-d="2026-11-28"]');p.wait_for_timeout(200)
    ok("a tap that sets a day to rest says so","Sat set to rest. Tap again to undo." in toast(p) and rest(p,"2026-11-28"),toast(p))
    p.click('#week button.day[data-d="2026-11-28"]');p.wait_for_timeout(200)
    ok("tap again undoes it",not rest(p,"2026-11-28") and "Sat is back to" in toast(p))
    p.click('#week button.day[data-d="2026-11-24"]');p.wait_for_timeout(200)
    ok("an ordinary past day can't be set to rest",not rest(p,"2026-11-24"))
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
