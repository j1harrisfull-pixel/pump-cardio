# pc-v58: three screens instead of one page. A tab bar (Today · Week · Progress); Today is a home card (status, one big
# button, "I did something else", this week's line) with settings behind a cog; the session opens as its own screen with
# ‹ Back; Week keeps the strip with the day under it; Progress holds the numbers, History and the export. The old one
# page layout stays available with wo_flat=1 (what every older suite runs on), and the DOM is the same in both.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";WED="2026-11-11";THU="2026-11-12"
L=[{"date":MON,"name":"Upper · Slow Is Strong","type":"main","min":30,"sub":"Easy 5km","plan":"Upper · Slow Is Strong","act":"run","km":"5","time":"30:27","effort":"easy","oc":"modified","sid":"upb0911"},
   {"date":WED,"name":"Hill Hunter Run","type":"main","min":38,"km":"6.4","time":"38:12","effort":"steady","sid":"hill1111"}]
def app(b,d,seed=None,hour=9,scheme=None):
    y,m,dd=map(int,d.split("-"))
    kw={"color_scheme":scheme} if scheme else {}
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block",**kw)
    c.add_init_script(HOOK);p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda x:x.accept());p.clock.install(time=dt.datetime(y,m,dd,hour,0));p.goto(URL)
    p.evaluate("t=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');for(var k in t)localStorage.setItem(k,JSON.stringify(t[k]));}",seed or {})
    p.reload();p.wait_for_selector("#tabbar button",timeout=10000);p.wait_for_timeout(200);return c,p
vis=lambda p,*ids:[i for i in ids if p.locator(i).first.is_visible()]
with sync_playwright() as pw:
    b=launch(pw)
    c,p=app(b,THU,{"wo_log":L})
    # ---- Today ----
    ok("tab bar with three tabs, Today selected",p.locator("#tabbar button").all_inner_texts()==["Today","Week","Progress"] and p.locator("#tabbar button.on").inner_text().endswith("Today"),p.locator("#tabbar button").all_inner_texts())
    ok("Today shows the title, the home card and the cog; no week strip, no session, no history",vis(p,"#ttl","#home","#cog","#week","#panel","#more","#hist")==["#ttl","#home","#cog"],vis(p,"#ttl","#home","#cog","#week","#panel","#more"))
    ok("home card: length, one big Start, something else, this week",(lambda t:t[0]=="≈ 43 min · 6 blocks" and t[-3:]==["Start session","I did something else","This week · 2 of 5 sessions · 11.4 km ›"])(p.locator("#home").inner_text().split("\n")),p.locator("#home").inner_text())
    ok("the whole Today screen fits one screen (no scrolling)",p.evaluate("()=>document.getElementById('home').getBoundingClientRect().bottom")<760)
    p.click('#home [data-hm="start"]');p.wait_for_timeout(500)
    ok("Start opens the session as its own screen: no strip, ‹ Back, clock running",p.locator("#panel.open").count()==1 and vis(p,"#home","#week","#more")==[] and p.locator("#close").inner_text()=="‹ Back" and p.locator("#sclk").inner_text().replace("\n"," ").startswith("⏱ 0:0") and p.evaluate("()=>window.scrollY")==0)
    ok("the session screen has the blocks and Finish; settings tick boxes are not in it",p.locator("#sess h2").count()>=6 and p.locator("#fin").count()==1 and p.locator("#panel .setr").count()==0)
    ok("pills sit above the tab bar",p.evaluate("()=>document.getElementById('sclk').getBoundingClientRect().bottom<=document.getElementById('tabbar').getBoundingClientRect().top"))
    x=p.evaluate("()=>document.querySelector('.srow').dataset.x");tick(p,x,0);p.wait_for_timeout(120)
    p.click("#close");p.wait_for_timeout(400)
    ok("Back returns to Today; the card now says in progress with Continue",vis(p,"#home","#panel")==["#home"] and p.locator("#home .hline").inner_text()=="In progress · started 09:00 · 1 of 19 parts done" and p.locator("#home .btn").inner_text()=="Continue",p.locator("#home").inner_text())
    p.click('#home [data-hm="open"]');p.wait_for_timeout(300);fin(p);p.click("#o_done");p.wait_for_timeout(300)
    ok("after Finish the card says logged, with View today",p.locator("#home .hline").inner_text().startswith("✓ Logged") and p.locator('#home [data-hm="open"]').inner_text()=="View today",p.locator("#home").inner_text())
    # ---- Week ----
    p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300)
    ok("Week shows the day list and Edit plan, not the home card or history",vis(p,"#wlist","#ed","#home","#more")==["#wlist","#ed"])
    p.click(f'#wlist [data-d="{WED}"]');p.wait_for_timeout(400)
    ok("tapping a day opens just the workout: no strip, no week row",p.locator("#panel.open").count()==1 and p.locator("#week").is_hidden() and p.locator(".wk").is_hidden() and p.locator("#ttl").inner_text()=="Hill Hunter Run")
    p.click("#close");p.wait_for_timeout(300);p.click(f'#wlist [data-d="{MON}"]');p.wait_for_timeout(300);ok("another day: Back, then one tap",p.locator("#ttl").inner_text()=="Easy 5km")
    # ---- Progress ----
    p.click('#tabbar [data-tab="prog"]');p.wait_for_timeout(300)
    ok("Progress closes the day and shows its own title, the numbers open, History and export",p.locator("#panel.open").count()==0 and vis(p,".ptitle","#prog_b",".wkbig","#home","#week","#ttl")==[".ptitle","#prog_b",".wkbig"] and p.locator("#more details summary").nth(1).is_visible())
    p.locator("#more details").nth(1).locator("summary").click();p.wait_for_timeout(100)
    ok("History opens in place with entries, Edit and Delete",p.locator("#hist li").count()==3 and p.locator("#hist .hdel").first.is_visible() and p.locator("#exp").is_visible())
    p.click("#exp");p.wait_for_timeout(150);ok("export works from the Progress tab",p.locator("#exs.show").count()==1);p.click(".exx")
    # ---- settings ----
    p.click('#tabbar [data-tab="today"]');p.wait_for_timeout(200);p.click("#cog");p.wait_for_timeout(200)
    ok("the cog opens Settings with the three tick boxes and the Weeks list",p.locator("#sets.show").count()==1 and [p.locator("#sets "+i).is_visible() for i in ("#autorest","#cueon","#loud","#imp")]==[True]*4 and "w/c Mon 9 Nov" in p.locator("#sets #wks").inner_text())
    p.locator("label.setr:has(#autorest)").click();ok("a setting still saves",ls(p,"wo_autorest")==False)
    p.click("#imp");p.wait_for_timeout(150);ok("Import week opens its sheet and closes Settings",p.locator("#ims.show").count()==1 and p.locator("#sets.show").count()==0);p.click(".imx")
    c.close()
    # ---- other home states ----
    c,p=app(b,"2026-11-10");ok("rest day home: says so, offers to open today",p.locator("#home .hline").inner_text().startswith("Rest day") and p.locator('#home [data-hm="open"]').inner_text()=="Open today")
    ok("yesterday's prompt lives on Today",p.locator("#ynag").is_visible())
    p.click('#ynag [data-ng="log"]');p.wait_for_timeout(300);ok("Log it opens yesterday as a session screen; Back returns to Today",p.evaluate("()=>__app.sel")==MON and p.locator("#panel.open").count()==1 and not p.locator("#week").is_visible())
    p.click("#close");p.wait_for_timeout(300);ok("back on Today",p.locator("#home").is_visible())
    c.close();c,p=app(b,THU);p.click('#home [data-hm="else"]');p.wait_for_timeout(400)
    ok("I did something else: one tap to the short form",p.locator("#panel.open").count()==1 and p.locator("#toc .rc.on").inner_text()=="Something else" and p.locator("#r_at").count()==1 and p.locator("#fin2").is_visible())
    c.close();c,p=app(b,"2026-11-16");ok("unplanned week home",p.locator("#home .hline").inner_text()=="Nothing planned for this week yet.")
    c.close();c,p=app(b,"2026-11-15",{"wo_log":L},hour=18);ok("the Sunday week review shows on Today",p.locator("#wrev").is_visible())
    # the clock overlay hides the tab bar
    c.close();c,p=app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(300);p.locator("#sess [data-t]").first.click();p.clock.run_for(3000);p.wait_for_timeout(200)
    ok("the full screen clock covers the tab bar",p.locator("#tabbar").is_hidden() and p.locator("#bar.show").count()==1);p.click("#stop")
    c.close();c,p=app(b,THU,scheme="dark");ok("dark: tab bar and home card are dark surfaces",p.evaluate("()=>{var f=function(s){var m=getComputedStyle(document.querySelector(s)).backgroundColor.match(/\\d+/g);return +m[0]+ +m[1]+ +m[2]};return f('#tabbar')<200&&f('.hweek')<200}"))
    c.close()
    # ---- flat layout still there, same DOM ----
    c,p=view(b,THU);ok("wo_flat=1: the one page layout, no tab bar, settings in the page",p.locator("#tabbar").is_hidden() and p.locator("#home").is_hidden() and p.locator("#panel .setr").count()==3 and p.locator("#week").is_visible() and p.locator("#close").inner_text()=="Close")
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
