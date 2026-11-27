# pc-v79: simpler moving of sessions between days. A tap on a day only ever opens it. Each Week row has a ... menu (and the
# session screen has the same actions under Change session): Move to another day (a 7 day picker, swap with confirm, Undo),
# Make this a rest day (Undo), Do a different session today (plan untouched), Reset week to plan. No Edit plan mode.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-23";TUE="2026-11-24";WED="2026-11-25";THU="2026-11-26";FRI="2026-11-27";SAT="2026-11-28";SUN="2026-11-29"
PLAN={"wo_fix78":1}
def week(b,d=THU,seed=None,hour=9,scheme=None):
    c,p=tabs_app(b,d,dict(PLAN,**(seed or {})),hour=hour,scheme=scheme);p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300);return c,p
def row(p,d,sel=".wt"): return p.locator(f'#wlist [data-d="{d}"] {sel}').first.inner_text().strip()
def toast(p): return p.locator("#toast").inner_text() if p.locator("#toast.show").count() else ""
def menu(p,d): p.locator(f'.wmore[data-wm="{d}"]').click();p.wait_for_timeout(250)
rect=lambda p,s:p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}",s)
with sync_playwright() as pw:
    b=launch(pw)
    c,p=week(b)
    ok("no Edit plan mode: no button, no strip, no Swap days",p.locator("#ed2").count()==0 and p.locator("#ed").is_hidden() and p.locator("#week").is_hidden() and p.locator("#swr").is_hidden())
    ok("every row has a 44 px ... menu and the row itself opens the day",p.locator("#wlist .wmore").count()==7 and p.evaluate("()=>[].every.call(document.querySelectorAll('#wlist .wmore'),function(b){var r=b.getBoundingClientRect();return r.width>=44&&r.height>=44})"))
    p.click(f'#wlist [data-d="{FRI}"]');p.wait_for_timeout(300)
    ok("tapping a day opens it and changes nothing",p.locator("#panel.open").count()==1 and not ls(p,"wo_plan") and not ls(p,"wo_daymap"));p.click("#close");p.wait_for_timeout(300)
    menu(p,FRI)
    ok("the menu offers Move, Rest",p.locator('#dms [data-dm="move"]').count()==1 and p.locator('#dms [data-dm="rest"]').count()==1 and p.locator('#dms [data-dm="do"]').count()==0)
    p.click('#dms [data-dm="move"]');p.wait_for_timeout(250)
    st=p.evaluate("()=>[].map.call(document.querySelectorAll('#dms .dmrow'),function(b){return [b.dataset.t,b.disabled,b.querySelector('small').textContent]})")
    ok("the 7 day picker: past days and the day itself are disabled with a reason, today and later days can be chosen",len(st)==7 and [s[1] for s in st]==[True,True,True,False,True,False,False] and st[4][2]=="This is the day it is on." and st[0][2]=="That day is over.",st)
    p.click(f'#dms [data-t="{SAT}"]');p.wait_for_timeout(250)
    ok("onto a day that has a session it asks: Swap with …?","Swap with Bell Circuit + Gentle Hills 5K?" in p.locator("#dm_t").inner_text() and p.locator('#dms [data-dm="swap"]').count()==1)
    p.click('#dms [data-dm="swap"]');p.wait_for_timeout(350)
    ok("swapped: Fri shows Sat's session, Sat shows Fri's",row(p,FRI)=="Bell Circuit + Gentle Hills 5K" and row(p,SAT)=="Lower · Step-Up Staircase")
    ok("moved rows say Moved from",row(p,FRI,"small").endswith("Moved from Sat") and row(p,SAT,"small").endswith("Moved from Fri"),(row(p,FRI,"small"),row(p,SAT,"small")))
    ok("a toast with Undo",("Moved Lower · Step-Up Staircase to Sat." in toast(p)) and p.locator("#toast .tact").inner_text()=="Undo",toast(p))
    ok("Reset week to plan shows because the week changed",p.locator("#wreset").is_visible())
    p.click("#toast .tact");p.wait_for_timeout(300)
    ok("Undo puts both back",row(p,FRI)=="Lower · Step-Up Staircase" and row(p,SAT)=="Bell Circuit + Gentle Hills 5K" and p.locator("#wreset").count()==0 and not (ls(p,"wo_daymap") or {}))
    # onto a rest day: no question, the rest day takes the old slot
    menu(p,FRI);p.click('#dms [data-dm="move"]');p.wait_for_timeout(250);p.click(f'#dms [data-t="{THU}"]');p.wait_for_timeout(350)
    ok("onto a rest day it just moves (no question)",row(p,THU)=="Lower · Step-Up Staircase" and row(p,FRI)=="Recovery · Legs + Spine Reset" and "Moved Lower · Step-Up Staircase to Thu." in toast(p),(row(p,THU),row(p,FRI),toast(p)))
    # Make this a rest day, with undo
    menu(p,SAT);p.click('#dms [data-dm="rest"]');p.wait_for_timeout(300)
    ok("Make this a rest day: says so with Undo",row(p,SAT)=="Rest day" and "Sat is now a rest day." in toast(p) and (ls(p,"wo_plan") or {}).get(SAT)=="Rest")
    menu(p,SAT);ok("a rest day offers Back to the session",p.locator('#dms [data-dm="back"]').inner_text()=="Back to Bell Circuit + Gentle Hills 5K" and p.locator('#dms [data-dm="move"]').count()==0)
    p.click('#dms [data-dm="back"]');p.wait_for_timeout(300)
    ok("Back to the session restores it",row(p,SAT)=="Bell Circuit + Gentle Hills 5K" and "Sat is back to" in toast(p))
    p.click("#toast .tact");p.wait_for_timeout(300);ok("Undo of that sets rest again",row(p,SAT)=="Rest day")
    # Reset week to plan
    ok("Reset week to plan is offered",p.locator("#wreset").is_visible())
    p.click("#wreset");p.wait_for_timeout(350)
    ok("it undoes every move and rest change this week",row(p,THU)=="Recovery · Legs + Spine Reset" and row(p,FRI)=="Lower · Step-Up Staircase" and row(p,SAT)=="Bell Circuit + Gentle Hills 5K" and not (ls(p,"wo_plan") or {}) and not (ls(p,"wo_daymap") or {}) and p.locator("#wreset").count()==0 and "Week back to plan." in toast(p),(row(p,THU),row(p,FRI),row(p,SAT),toast(p)))
    p.click("#toast .tact");p.wait_for_timeout(300);ok("and that has an Undo too",row(p,THU)=="Lower · Step-Up Staircase" and row(p,SAT)=="Rest day");c.close()
    # session screen: same actions under Change session
    c,p=tabs_app(b,THU,PLAN);p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(250);p.click(f'#wlist [data-d="{FRI}"]');p.wait_for_timeout(350);p.click("#chg");p.wait_for_timeout(200)
    ok("the session screen has Move to another day and Make this a rest day under Change session",p.locator("#mvb").is_visible() and p.locator("#rsb").is_visible() and p.locator("#dob").is_hidden() and p.locator("#rsb").inner_text()=="Make this a rest day")
    p.click("#mvb");p.wait_for_timeout(250);p.click(f'#dms [data-t="{SUN}"]');p.wait_for_timeout(250);p.click('#dms [data-dm="swap"]');p.wait_for_timeout(400)
    ok("moving from the session screen closes it and shows the Week list with the result",p.locator("#panel.open").count()==0 and row(p,SUN)=="Lower · Step-Up Staircase" and row(p,FRI)=="Landmark Walk + Hip Reset",(row(p,SUN),row(p,FRI)));c.close()
    # logged or started days can't move and show why
    L=[{"date":TUE,"name":"Tempo Triple","type":"main","min":40,"sid":"x"}]
    c,p=week(b,THU,{"wo_log":L})
    ok("a logged day has no menu",p.locator(f'.wmore.z').count()>=1 and p.locator(f'.wmore[data-wm="{TUE}"]').count()==0)
    menu(p,FRI);p.click('#dms [data-dm="move"]');p.wait_for_timeout(250)
    ok("a logged day is a disabled target with the reason",p.evaluate("()=>{var b=document.querySelector('#dms [data-t=\"%s\"]');return b.disabled&&b.querySelector('small').textContent.indexOf('That day is over')>=0}"%TUE));c.close()
    # past, unlogged day: can be moved onto a rest day but not onto a session
    c,p=week(b,THU);menu(p,TUE);p.click('#dms [data-dm="move"]');p.wait_for_timeout(250)
    st=p.evaluate("()=>[].map.call(document.querySelectorAll('#dms .dmrow'),function(b){return [b.dataset.t,b.disabled,b.querySelector('small').textContent]})")
    ok("a missed session can go to a rest day later in the week but not onto another session (it would land on a day that is over)",st[3][1]==False and st[5][1]==True and "day that is over" in st[5][2],st)
    p.click(f'#dms [data-t="{THU}"]');p.wait_for_timeout(350);ok("it lands on today and today's rest slot goes to Tue",row(p,THU)=="Tempo Triple" and row(p,TUE)=="Recovery · Legs + Spine Reset");c.close()
    # Do a different session today
    c,p=tabs_app(b,FRI,PLAN)
    ok("on a planned day Today offers Do a different session",p.locator('#home [data-hm="dif"]').inner_text()=="Do a different session")
    p.click('#home [data-hm="dif"]');p.wait_for_timeout(300)
    names=p.evaluate("()=>[].map.call(document.querySelectorAll('#dms [data-dm=pick] .wn'),function(e){return e.firstChild.textContent})")
    ok("it lists the other sessions of this week (not rest days, not today)",names==["Upper · Density Dash","Tempo Triple","Bell Circuit + Gentle Hills 5K","Landmark Walk + Hip Reset"],names)
    p.click(f'#dms [data-dm=pick][data-id]:nth-child(2)');p.wait_for_timeout(350)
    ok("today now shows that session; the plan is unchanged",bool((ls(p,"wo_do") or {}).get(FRI)),ls(p,"wo_do"))
    ok("Today says what it is instead of",p.locator("#ttl").inner_text()=="Tempo Triple" and "instead of Lower · Step-Up Staircase" in p.locator("#date").inner_text(),(p.locator("#ttl").inner_text(),p.locator("#date").inner_text()))
    p.click('#home [data-hm="dback"]');p.wait_for_timeout(300)
    ok("Back to the plan in one tap",not (ls(p,"wo_do") or {}) and p.locator("#ttl").inner_text()=="Lower · Step-Up Staircase")
    p.click('#home [data-hm="dif"]');p.wait_for_timeout(250);p.click('#dms [data-dm=pick]:nth-child(1)');p.wait_for_timeout(350)
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);x=p.evaluate("()=>document.querySelector('.srow')&&document.querySelector('.srow').dataset.x")
    if x: tick(p,x,0)
    fin(p);p.wait_for_timeout(300)
    lg=ls(p,"wo_log") or []
    ok("logging it keeps the real session and remembers what was planned",len(lg)==1 and lg[0]["date"]==FRI and lg[0].get("plan")=="Lower · Step-Up Staircase" and lg[0]["name"]!="Lower · Step-Up Staircase" and not lg[0].get("sub"),lg and {k:lg[0].get(k) for k in ("name","plan","sid")})
    p.click("#o_done");p.wait_for_timeout(300)
    ok("Today's summary and the Week row say instead of","instead of Lower · Step-Up Staircase" in p.locator("#home .hsum").inner_text(),p.locator("#home .hsum").inner_text())
    p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300);ok("the Week row says it too","instead of Lower · Step-Up Staircase" in row(p,FRI,"small"),row(p,FRI,"small"))
    ok("a day that is done has no menu",p.locator(f'.wmore[data-wm="{FRI}"]').count()==0)
    p.click('#tabbar [data-tab="prog"]');p.wait_for_timeout(300)
    ok("History shows the entry and the export names the swap","Different sessions:" in p.evaluate("()=>__app.exportText()"));c.close()
    # dark and a11y: the sheet is a dark surface; rows have names
    c,p=week(b,THU,scheme="dark");menu(p,FRI);p.click('#dms [data-dm="move"]');p.wait_for_timeout(250)
    ok("dark: the picker sheet and rows are dark surfaces",p.evaluate("()=>{var f=function(s){var m=getComputedStyle(document.querySelector(s)).backgroundColor.match(/\\d+/g);return +m[0]+ +m[1]+ +m[2]};return f('#dms .sh')<200&&f('#dms .dmrow:not(:disabled)')<200}"))
    ok("the ... buttons have names","Actions for" in p.locator(".wmore").first.get_attribute("aria-label"))
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
