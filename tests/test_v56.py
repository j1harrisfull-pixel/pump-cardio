# pc-v56: a small session clock, bottom left. "Start session" before anything happens; it starts on its own with the
# first tick or guided timer; counts up while you train (also over the full screen clock); a tap starts a lap for timed
# exercises and a second tap clears it; Finish stops it ("✓ 30:13", stored as wo_<date>.end); hidden under sheets,
# on other days, rest days and off-plan days; lifts above the rest bar.
from playwright.sync_api import sync_playwright
from lib import *
TUE="2026-11-03";WED="2026-11-04"
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,TUE);p.wait_for_timeout(300)
    T=lambda:p.locator("#sclk").inner_text().replace("\n"," ") if p.locator("#sclk").is_visible() else None
    adv=lambda ms:(p.clock.run_for(ms),p.wait_for_timeout(300))
    ok("before anything: an orange 'Start session' pill, bottom left, 44 px",T()=="▶ Start session" and "idle" in p.get_attribute("#sclk","class") and p.evaluate("()=>{var r=document.getElementById('sclk').getBoundingClientRect();return r.left<40&&innerHeight-r.bottom<40&&r.height>=44}"))
    p.click("#sclk");adv(65000)
    ok("tap: the session starts and counts up",T()=="⏱ 1:05" and (ls(p,"wo_"+TUE) or {}).get("start"),T())
    p.click("#sclk");adv(23000);ok("tap while running: a lap for timed exercises",T()=="⏱ 1:28 lap 0:23",T())
    p.click("#sclk");adv(1000);ok("tap again: the lap clears, the session keeps running",T()=="⏱ 1:29",T())
    tick(p,"db-bench",0);p.wait_for_timeout(200)
    ok("lifts above the rest bar",p.evaluate("()=>document.getElementById('sclk').getBoundingClientRect().bottom<=document.getElementById('rbar').getBoundingClientRect().top"));p.click("#rskip")
    p.locator("#sess [data-t]").first.click();adv(12000)
    ok("stays visible over the full screen clock",p.locator("#bar.show").count()==1 and T().startswith("⏱ 1:4"),T());p.click("#stop")
    p.evaluate("()=>document.querySelectorAll('.more[data-mo]')[0].click()");p.wait_for_timeout(60);p.click('.mvn[data-h="db-bench"]');p.wait_for_timeout(120)
    ok("hidden under a sheet",p.locator("#hs.show").count()==1 and p.locator("#sclk").is_hidden());p.click("#hs_x");p.wait_for_timeout(60)
    adv(60000*28);fin(p)
    ok("hidden under the Workout saved card, which shows the session minutes",p.locator("#sclk").is_hidden() and p.locator("#o_t").inner_text()=="30 min")
    p.click("#o_done");adv(100)
    ok("Finish stops it: ✓ and the final time, stored as the end",re.match(r"✓ (29|30):\d\d$",T() or "") is not None and (ls(p,"wo_"+TUE) or {}).get("end"),T())
    f0=T();adv(120000);ok("stays frozen afterwards",T()==f0,(f0,T()))
    opend(p,WED);ok("not on another day",T() is None)
    p.click("#close");p.wait_for_timeout(150);ok("not with no day open",T() is None)
    c.close()
    c,p=view(b,TUE);tick(p,"db-bench",0);p.wait_for_timeout(300);ok("starts on its own with the first tick",T()=="⏱ 0:00",T())
    c.close();c,p=view(b,TUE);p.locator("#sess [data-t]").first.click();adv(3000);ok("starts on its own with the first guided timer",T().startswith("⏱ 0:0"),T());p.click("#stop")
    p.click('#toc [data-toc="else"]');p.wait_for_timeout(200);ok("hidden when the day became something else",T() is None)
    c.close();c,p=view(b,"2026-11-10");ok("not on a rest day",T() is None)
    c.close();c,p=view(b,TUE,seed={"wo_log":[{"date":TUE,"name":"Strength A4 · Upper","type":"main","min":40,"sid":"up03"}]});ok("an already logged day without a start shows nothing",T() is None)
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
