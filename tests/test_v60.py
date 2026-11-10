# pc-v60: Week is one list. The strip only shows once a day is open (for hopping) or while editing the plan; the Week
# header is about the week; rows say what happened (logged minutes, moved days); Finish asks before saving a barely
# started session; the session clock's stop hides while the full screen clock is up.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12"
L=[{"date":MON,"name":"Upper · Slow Is Strong","type":"main","min":30,"sub":"Easy 5km","plan":"Upper · Slow Is Strong","act":"run","km":"5","time":"30:27","oc":"modified","sid":"upb0911"},
   {"date":WED,"name":"Hill Hunter Run","type":"main","min":38,"km":"6.4","time":"38:12","effort":"steady","sid":"hill1111"}]
with sync_playwright() as pw:
    b=launch(pw);c,p=tabs_app(b,THU,{"wo_log":L,"wo_daymap":{"2026-11-13":"2026-11-14","2026-11-14":"2026-11-13"}})
    p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300)
    ok("Week with no day open: the list only, no strip, no ring",p.locator("#wlist").is_visible() and p.locator("#week").is_hidden() and p.locator(".ring").is_hidden() and p.locator("#prev").is_visible() and p.locator("#ed").is_visible())
    ok("the header is about the week",p.locator("#ttl").inner_text()=="This week" and p.locator("#date").inner_text()=="2 of 5 sessions · 2 runs · 11.4 km",(p.locator("#ttl").inner_text(),p.locator("#date").inner_text()))
    ok("a done row shows the logged minutes",p.locator(f'#wlist [data-d="{WED}"] small').inner_text()=="38 min" and p.locator(f'#wlist [data-d="{MON}"] small').inner_text()=="30 min · instead of Upper · Slow Is Strong",p.locator("#wlist").inner_text())
    ok("a moved day says so",p.locator('#wlist [data-d="2026-11-13"] small').inner_text().endswith("⇄ moved from Sat"),p.locator('#wlist [data-d="2026-11-13"]').inner_text())
    p.click("#next");p.wait_for_timeout(200);ok("another week: its own title and dates",p.locator("#ttl").inner_text()=="Next week" and p.locator("#date").inner_text()=="Mon 16 Nov to Sun 22 Nov",p.locator("#date").inner_text());p.click("#prev");p.wait_for_timeout(200)
    p.click("#ed");p.wait_for_timeout(200);ok("Edit plan brings the strip back",p.locator("#week").is_visible());p.click("#ed");p.wait_for_timeout(200)
    p.click(f'#wlist [data-d="{WED}"]');p.wait_for_timeout(300)
    ok("an open day is just the workout with its own title",p.locator("#week").is_hidden() and p.locator("#wlist").is_hidden() and p.locator("#ttl").inner_text()=="Hill Hunter Run" and p.locator("#sbar").is_visible())
    p.click("#close");p.wait_for_timeout(300);ok("Back returns to the list",p.locator("#wlist").is_visible() and p.locator("#week").is_hidden() and p.locator("#ttl").inner_text()=="This week")
    c.close()
    # Finish asks first when barely started
    msgs=[]
    c=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,service_workers="block");c.add_init_script(HOOK);p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));ans=[False]
    p.on("dialog",lambda d:(msgs.append(d.message),d.accept() if ans[0] else d.dismiss()));p.clock.install(time=dt.datetime(2026,11,12,9,0));p.goto(URL)
    p.evaluate("()=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');}");p.reload();p.wait_for_selector("#tabbar button");p.wait_for_timeout(200)
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);x=p.evaluate("()=>document.querySelector('.srow').dataset.x");tick(p,x,0)
    p.click("#fin_c");p.wait_for_timeout(300)
    ok("Finish on a barely started session asks; No saves nothing",msgs==["Finish with only 1 of 19 parts done?"] and p.locator("#ov.show").count()==0 and not ls(p,"wo_log"),msgs)
    ans[0]=True;p.clock.run_for(2000);p.click("#fin_c");p.wait_for_selector("#ov.show",timeout=3000);ok("Yes saves it",len(ls(p,"wo_log"))==1)
    c.close();c,p=tabs_app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(300);p.locator("#sess [data-t]").first.click();p.clock.run_for(3000);p.wait_for_timeout(200)
    ok("on the full screen clock the session time shows without its stop",p.locator("#sclk .sc_t").is_visible() and p.locator("#sclk .sc_x").is_hidden());p.click("#stop")
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
