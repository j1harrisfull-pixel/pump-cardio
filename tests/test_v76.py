# pc-v76: the Week list says what was actually done. A day with only an added activity shows "✓ Run · 5.1 km" (Walk / Row the
# same; types without distance show minutes, e.g. "✓ Mobility · 20 min"); a planned day that is done keeps its name and shows
# the logged distance in the small line; more than one thing on a day adds "+1". The pill never wraps on a 320 px iPhone.
from playwright.sync_api import sync_playwright
from lib import *
LOG=[{"date":"2026-11-25","name":"Extra run","type":"extra","extra":1,"act":"run","km":"5.13","time":"30:17","effort":"easy","feel":"5","notes":"","min":30},
     {"date":"2026-11-24","name":"Tempo Triple","type":"main","sid":"fls2411","km":"6.24","time":"34:10","min":34},
     {"date":"2026-11-23","name":"Upper · Density Dash","type":"main","sets":20,"of":20,"min":41},
     {"date":"2026-11-23","name":"Walk","type":"extra","extra":1,"act":"walk","km":"3","time":"35:00","min":35},
     {"date":"2026-11-27","name":"Mobility","type":"extra","extra":1,"act":"mob","km":"","time":"20:00","min":20}]
def wk(b,w=390):
    c,p=view(b,"2026-11-27",{"wo_log":LOG},hour=21,open_day=False)
    p.evaluate("()=>localStorage.removeItem('wo_flat')");p.set_viewport_size({"width":w,"height":844});p.reload();p.wait_for_selector("#tabbar",timeout=10000)
    p.click("#tabbar [data-tab=week]");p.wait_for_timeout(250)
    R=p.evaluate("""()=>{var o={};document.querySelectorAll('#wlist .wrow').forEach(function(r){var s=r.querySelector('.ws'),n=r.querySelector('.wn');
      o[r.dataset.d]={ws:s?s.textContent:'',sm:(n.querySelector('small')||{}).textContent||'',h:s?Math.round(s.getBoundingClientRect().height):0,
      over:s?s.scrollWidth>s.clientWidth+1:false,right:Math.round(r.getBoundingClientRect().right),sr:s?Math.round(s.getBoundingClientRect().right):0};});return o;}""")
    return c,p,R
with sync_playwright() as pw:
    b=launch(pw)
    c,p,R=wk(b)
    ok("rest day with a run: '✓ Run · 5.1 km' instead of '✓ Extra'",R["2026-11-25"]["ws"]=="✓ Run · 5.1 km",R["2026-11-25"])
    ok("planned run day done: '✓ Done', the session name kept, 6.2 km in the small line",R["2026-11-24"]["ws"]=="✓ Done" and R["2026-11-24"]["sm"].startswith("6.2 km"),R["2026-11-24"])
    ok("planned day done plus an added walk: '✓ Done +1'",R["2026-11-23"]["ws"]=="✓ Done +1",R["2026-11-23"])
    ok("activity without distance shows minutes: '✓ Mobility · 20 min'",R["2026-11-27"]["ws"]=="✓ Mobility · 20 min",R["2026-11-27"])
    ok("no row says just 'Extra' any more","Extra" not in p.locator("#wlist").inner_text())
    c.close()
    for w in (320,375):
        c,p,R=wk(b,w)
        ok(f"{w} px: every status pill on one line, inside its row",all(v["h"]<=32 and v["sr"]<=v["right"] for v in R.values() if v["ws"]),{k:(v["ws"],v["h"]) for k,v in R.items()})
        ok(f"{w} px: '✓ Mobility · 20 min' and '✓ Run · 5.1 km' shown in full",not R["2026-11-27"]["over"] and not R["2026-11-25"]["over"])
        if w==320: p.screenshot(path="test-output/v76-week-320.png")
        c.close()
    ok("no page errors",errs==[],errs)
    b.close()
raise SystemExit(done())
