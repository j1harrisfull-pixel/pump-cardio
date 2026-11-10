# pc-v61: a day opened from Week is just the workout (no week arrows, no strip), Back returns to the Week list at the
# same scroll position, and the Week tab stays selected while the day is open.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";WED="2026-11-11";THU="2026-11-12";SUN="2026-11-15"
vis=lambda p,*ids:[i for i in ids if p.locator(i).first.is_visible()]
with sync_playwright() as pw:
    b=launch(pw);c,p=tabs_app(b,THU)
    p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300)
    p.click(f'#wlist [data-d="{WED}"]');p.wait_for_timeout(300)
    ok("open day from Week: no week row, strip, swap row or hint",vis(p,".wk","#week","#swr","#hint","#wlist")==[],vis(p,".wk","#week","#swr","#hint","#wlist"))
    ok("it is the workout: title, Back and blocks",p.locator("#ttl").inner_text()=="Hill Hunter Run" and p.locator("#close").inner_text()=="‹ Back" and p.locator("#sess h2").count()>=4)
    ok("the Week tab stays selected",p.locator("#tabbar button.on").inner_text()=="Week" and p.evaluate("()=>document.body.classList.contains('t-week')"))
    ok("the session starts at the top",p.evaluate("scrollY")==0)
    p.click("#close");p.wait_for_timeout(300)
    ok("Back returns to the Week list",p.locator("#wlist").is_visible() and p.locator("#panel.open").count()==0 and p.locator("#ttl").inner_text()=="This week")
    c.close()
    # scroll position of the list is kept (short screen so the list scrolls)
    c,p=tabs_app(b,THU,h=520);p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300)
    p.evaluate("()=>window.scrollTo(0,document.body.scrollHeight)");p.wait_for_timeout(150);y=p.evaluate("scrollY")
    ok("the list scrolls on a short screen",y>100,y)
    p.click(f'#wlist [data-d="{SUN}"]');p.wait_for_timeout(300);ok("Sunday opens at the top",p.evaluate("scrollY")==0 and p.locator("#ttl").inner_text()!="This week")
    p.click("#close");p.wait_for_timeout(300);ok("Back restores the list position",abs(p.evaluate("scrollY")-y)<4,(y,p.evaluate("scrollY")))
    c.close()
    # editing still shows the strip, and swapping is untouched
    c,p=tabs_app(b,THU);p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300);p.click("#ed");p.wait_for_timeout(200)
    ok("Edit plan on the Week list shows the strip",p.locator("#week").is_visible() and p.locator("#swr").is_visible())
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
