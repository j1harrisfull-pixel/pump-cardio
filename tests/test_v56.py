# pc-v56/57: the session clock, bottom left. "Start session" before anything happens; it starts on its own with the first
# tick or guided timer; counts up (also over the full screen clock); tapping the time starts a lap, again clears it.
# pc-v57: a ■ button stops it ("⏸ 32:10 resume", tap to carry on without counting the pause); it stops by itself once
# the day has any log (Finish, Save, a skip) and after 3 hours; a stopped clock gives the log its minutes.
from playwright.sync_api import sync_playwright
from lib import *
TUE="2026-11-03";WED="2026-11-04"
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,TUE);p.wait_for_timeout(300)
    T=lambda:p.locator("#sclk").inner_text().replace("\n"," ") if p.locator("#sclk").is_visible() else None
    adv=lambda ms:(p.clock.run_for(ms),p.wait_for_timeout(300))
    ok("before anything: an orange 'Start session' pill, bottom left, 44 px",T()=="▶ Start session" and "idle" in p.get_attribute("#sclk","class") and p.evaluate("()=>{var r=document.getElementById('sclk').getBoundingClientRect();return r.left<40&&innerHeight-r.bottom<40&&r.height>=44}"))
    p.click('[data-sc="go"]');adv(65000)
    ok("tap: the session starts and counts up, with a stop button",T()=="⏱ 1:05 ■" and p.locator('[data-sc="stop"]').is_visible(),T())
    p.click('[data-sc="lap"]');adv(23000);ok("tap the time: a lap for timed exercises",T()=="⏱ 1:28 lap 0:23 ■",T())
    p.click('[data-sc="lap"]');adv(1000);ok("tap again: the lap clears, the session keeps running",T()=="⏱ 1:29 ■",T())
    p.click('[data-sc="stop"]');adv(60000)
    ok("■ stops it: paused, frozen, offers resume",re.match(r"⏸ 1:(29|30) resume$",T() or "") is not None and (ls(p,"wo_"+TUE) or {}).get("end"),T())
    p.click('[data-sc="resume"]');adv(5000);ok("resume carries on without counting the paused minute",re.match(r"⏱ 1:3[45] ■$",T() or "") is not None,T())
    tick(p,"db-bench",0);p.wait_for_timeout(200)
    ok("lifts above the rest bar",p.evaluate("()=>document.getElementById('sclk').getBoundingClientRect().bottom<=document.getElementById('rbar').getBoundingClientRect().top"));p.click("#rskip")
    p.locator("#sess [data-t]").first.click();adv(12000)
    ok("stays visible over the full screen clock",p.locator("#bar.show").count()==1 and T().startswith("⏱ 1:4"),T());p.click("#stop")
    p.evaluate("()=>document.querySelectorAll('.more[data-mo]')[0].click()");p.wait_for_timeout(60);p.click('.mvn[data-h="db-bench"]');p.wait_for_timeout(120)
    ok("hidden under a sheet",p.locator("#hs.show").count()==1 and p.locator("#sclk").is_hidden());p.click("#hs_x");p.wait_for_timeout(60)
    adv(60000*28);fin(p)
    ok("hidden under the Workout saved card, which shows the session minutes",p.locator("#sclk").is_hidden() and p.locator("#o_t").inner_text()=="30 min",p.locator("#o_t").inner_text())
    p.click("#o_done");adv(100)
    ok("Finish stops it: ✓ and the final time, no stop button",re.match(r"✓ (29|30):\d\d$",T() or "") is not None and p.locator('[data-sc="stop"]').count()==0,T())
    f0=T();adv(120000);ok("stays frozen afterwards",T()==f0,(f0,T()))
    opend(p,WED);ok("not on another day",T() is None)
    p.click("#close");p.wait_for_timeout(150);ok("not with no day open",T() is None)
    c.close()
    c,p=view(b,TUE);tick(p,"db-bench",0);p.wait_for_timeout(300);ok("starts on its own with the first tick",T()=="⏱ 0:00 ■",T())
    p.click('[data-sc="stop"]');p.clock.run_for(60000*20);p.wait_for_timeout(100);fin(p)
    ok("a clock stopped before Finish gives the log the stopped length, not the time since",ls(p,"wo_log")[0]["min"]==0 and p.locator("#o_t").inner_text()=="0 min",ls(p,"wo_log")[0]["min"]);p.click("#o_done")
    c.close();c,p=view(b,TUE);p.locator("#sess [data-t]").first.click();adv(3000);ok("starts on its own with the first guided timer",T().startswith("⏱ 0:0"),T());p.click("#stop")
    p.clock.run_for(3*3600000+60000);p.wait_for_timeout(300);ok("left running, it stops itself at 3 hours",T()=="⏸ 3:00:00 resume",T())
    c.close();c,p=view(b,TUE);p.click('[data-sc="go"]');adv(5000)
    p.evaluate("()=>{var l=[{date:'2026-11-03',name:'Something else',type:'main',min:30,oc:'modified'}];localStorage.setItem('wo_log',JSON.stringify(l));}");adv(500)
    ok("any log on the day stops it, even under another name",(T() or "").startswith("✓ ") or (T() or "").startswith("⏸"),T())
    p.click('#toc [data-toc="else"]');p.wait_for_timeout(200);ok("hidden when the day became something else",T() is None)
    c.close();c,p=view(b,"2026-11-10");ok("not on a rest day",T() is None)
    c.close();c,p=view(b,TUE,seed={"wo_log":[{"date":TUE,"name":"Strength A4 · Upper","type":"main","min":40,"sid":"up03"}]});ok("an already logged day without a start shows nothing",T() is None)
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
