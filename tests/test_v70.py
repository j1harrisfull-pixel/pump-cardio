# pc-v70: fixes from the pc-v69 walkthrough. The something else form lays out in one column, the clock fits landscape,
# an empty Finish is not praised and asks on any past day, History is newest date first, edit plan ends when you leave Week,
# the rest bar never hides the next set, a notes only entry is not a run, Export counts as a backup only once it left the app,
# plus short screen, dock, prompt and wording tidy ups.
from playwright.sync_api import sync_playwright
from lib import *
import datetime as dt
MON="2026-11-09";TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12";SUN="2026-11-15"
rect=lambda p,s:p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}",s)
with sync_playwright() as pw:
    b=launch(pw)
    c,p=tabs_app(b,THU);p.click('#home [data-hm="else"]');p.wait_for_timeout(300)
    tq=rect(p,"#topq");f2=rect(p,"#fin2");sess=rect(p,"#sess")
    ok("something else: one column, full width, Save above the tab bar",tq[0]<30 and tq[2]>350 and tq[3]-tq[1]<140 and sess[0]<30 and f2[3]<=rect(p,"#tabbar")[1],(tq,f2,sess))
    p.fill("#r_d","5");p.fill("#r_t","29.40");p.locator("#r_t").blur();fin(p);p.wait_for_timeout(300)
    ok("and it saves one record",len(ls(p,"wo_log"))==1 and ls(p,"wo_log")[0]["time"]=="29:40");p.click("#o_done");c.close()
    # landscape clock
    c,p=tabs_app(b,THU,w=844,h=390);p.click('#home [data-hm="start"]');p.wait_for_timeout(300);p.locator("#sess [data-t]").first.click();p.clock.run_for(14000);p.wait_for_timeout(300)
    rr=p.evaluate("()=>[].map.call(document.querySelectorAll('#tback,#tpause,#tnext,#tlock,#stop'),function(e){var r=e.getBoundingClientRect();return [e.id,Math.round(r.left),Math.round(r.right),Math.round(r.top),Math.round(r.bottom)]})")
    ok("landscape clock: every control is on screen",all(x[1]>=0 and x[2]<=844 and x[4]<=390 for x in rr),rr)
    ok("landscape clock: Pause is still the biggest control",rr[1][2]-rr[1][1]>rr[0][2]-rr[0][1]);c.close()
    # empty Finish: neutral card; past day asks and logs 0 minutes
    c,p=tabs_app(b,THU);msgs=[];p.remove_listener("dialog",p.listeners("dialog")[0]) if False else None
    p.on("dialog",lambda d:msgs.append(d.message))
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);fin(p);p.wait_for_timeout(300)
    ok("an empty Finish is not praised",("nothing ticked" in p.locator("#o_e").inner_text()) and "Strong work" not in p.locator("#o_e").inner_text() and "Nicely done" not in p.locator("#o_e").inner_text(),p.locator("#o_e").inner_text())
    p.click("#o_done");p.wait_for_timeout(200)
    p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(250);p.click(f'#wlist [data-d="{WED}"]');p.wait_for_timeout(300);msgs.clear();fin(p);p.wait_for_timeout(300)
    lg=[e for e in ls(p,"wo_log") if e["date"]==WED]
    ok("a past day asks first and logs 0 minutes when nothing was done",any("Finish with only 0 of" in m for m in msgs) and lg and lg[0]["min"]==0,(msgs,lg and lg[0].get("min")));c.close()
    # History order
    L=[{"date":"2026-11-09","name":"B","type":"main","min":10},{"date":"2026-11-12","name":"A newest","type":"main","min":20},{"date":"2026-10-30","name":"C oldest","type":"main","min":30}]
    c,p=tabs_app(b,THU,{"wo_log":L});p.click('#tabbar [data-tab="prog"]');p.wait_for_timeout(300)
    ok("History is newest date first",p.evaluate("()=>[].map.call(document.querySelectorAll('#hist .hnm'),function(e){return e.textContent})")==["A newest","B","C oldest"])
    p.locator("#hist .hmore").first.click();p.wait_for_timeout(250);p.click("#acs [data-del]");p.wait_for_timeout(300)
    ok("deleting the top entry removes that one",[e["name"] for e in ls(p,"wo_log")]==["B","C oldest"],[e["name"] for e in ls(p,"wo_log")]);c.close()
    # edit plan ends when you leave Week
    c,p=tabs_app(b,THU);p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(250);p.click("#ed2");p.wait_for_timeout(200)
    p.click('#tabbar [data-tab="today"]');p.wait_for_timeout(250)
    ok("leaving Week ends edit mode everywhere",not p.evaluate("()=>document.body.classList.contains('ed')") and p.locator("#ehint").is_hidden())
    p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(250);ok("and Week is back to the list",p.locator("#wlist").is_visible() and p.locator("#week").is_hidden())
    # today caption, short screen, idle dock pill, escape on the stop dialog
    ok("the Today ring says This week",p.locator("header .rcap").count()==1);p.click('#tabbar [data-tab="today"]');p.wait_for_timeout(200)
    ok("the ring caption is visible on Today",p.locator(".rcap").is_visible() and p.locator(".rcap").inner_text()=="This week");c.close()
    c,p=tabs_app(b,THU,w=375,h=667)
    ok("375 x 667: Start session is above the tab bar and the preview is shortened",rect(p,'#home [data-hm="start"]')[3]<=rect(p,"#tabbar")[1] and "+2 more blocks" in p.locator("#home .hprev").inner_text(),rect(p,'#home [data-hm="start"]'));c.close()
    c,p=tabs_app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(300)
    bgc=p.evaluate("()=>[getComputedStyle(document.getElementById('sclk')).backgroundColor,getComputedStyle(document.getElementById('sclk')).borderTopColor]") if p.locator("#sclk.idle").count() else None
    p.locator("#sess [data-t]").first.click();p.clock.run_for(12000);p.wait_for_timeout(250)
    p.click("#stop");p.wait_for_timeout(150);p.keyboard.press("Escape");p.wait_for_timeout(150)
    ok("Escape closes the stop confirm and the timer keeps running",p.locator("#stq").is_hidden() and p.locator("#bar.show").count()==1)
    ok("the session time says Session",p.locator("#sct").inner_text().startswith("Session "));c.close()
    c,p=tabs_app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(300)
    ok("the Start session pill is outlined, not a second orange button",p.locator("#sclk.idle").count()==0 or p.evaluate("()=>getComputedStyle(document.getElementById('sclk')).backgroundColor")!="rgb(255, 138, 61)");c.close()
    # rest bar and the next set
    c,p=tabs_app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(300)
    xs=p.evaluate("()=>{var o=[];[].forEach.call(document.querySelectorAll('.srow'),function(r){if(o.indexOf(r.dataset.x)<0)o.push(r.dataset.x)});return o.slice(0,2)}")
    p.evaluate("()=>{var r=document.querySelectorAll('.srow')[2];window.scrollTo(0,window.scrollY+r.getBoundingClientRect().top-420)}");p.wait_for_timeout(150)
    tick(p,xs[0],0);tick(p,xs[1],0);p.wait_for_timeout(500)
    nx=rect(p,".srow.nx");rb=rect(p,"#rbar")
    ok("after a tick the next set stays above the rest bar",p.locator("#rbar.show").count()==1 and nx[3]<=rb[1]+1,(nx,rb));c.close()
    # notes only is not a run
    c,p=tabs_app(b,THU);p.click('#home [data-hm="else"]');p.wait_for_timeout(300);det(p);p.fill("#r_n","Took the dog out for a long walk");fin(p);p.wait_for_timeout(300)
    lg=ls(p,"wo_log")[0] if ls(p,"wo_log") else {}
    ok("a notes only entry is not a run",lg.get("act")=="other" and "dog" in lg.get("sub","") and not lg.get("km"),lg);c.close()
    # export counts as a backup only when it left the app
    c,p=tabs_app(b,THU,{"wo_log":L});p.click('#tabbar [data-tab="prog"]');p.wait_for_timeout(300);p.click("#bknow");p.wait_for_timeout(300)
    ok("opening Export does not mark a backup",p.locator("#exs.show").count()==1 and ls(p,"wo_lastexport") is None);c.close()
    # wording
    c,p=tabs_app(b,THU);p.click("#cog");p.wait_for_timeout(200);p.click("#imp");p.wait_for_timeout(250)
    ok("Import sheet does not point at a repo file","docs/" not in p.locator("#ims").inner_text())
    p.click(".imx");p.wait_for_timeout(150);p.click("#sets .swx") if p.locator("#sets.show").count() else None
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);p.evaluate("scrollTo(0,99999)");p.wait_for_timeout(100)
    ok("the Notes placeholder is plain",p.locator("#s_nt").get_attribute("placeholder")=="Anything worth remembering");c.close()
    # review no longer lists today
    c,p=tabs_app(b,SUN,{"wo_log":[{"date":MON,"name":"x","type":"main","min":10}]},hour=18)
    ok("the Sunday review does not list today's session as not logged",p.locator("#wrev").is_visible() and "Hill Push Walk" not in p.locator("#wrev").inner_text(),p.locator("#wrev").inner_text());c.close()
    # extra logged: the replace link is a button
    c,p=tabs_app(b,THU,{"wo_log":[{"date":THU,"name":"Extra run","type":"extra","extra":1,"act":"run","min":30,"km":"5","time":"29:40"}]})
    ok("It replaced this session is drawn as a button",p.evaluate("()=>parseFloat(getComputedStyle(document.querySelector('.hlink.cv')).borderTopWidth)")>=1);c.close()
    ok("no page errors",not errs,errs);b.close()
exit(done())
