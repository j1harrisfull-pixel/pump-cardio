# pc-v51 (updated for pc-v53): one logging form, `runCard`. Doing the plan on a run day and "+ Add an activity" show
# every field in one order; a day that became something else shows the same card in its quick shape: What · Distance ·
# Time · Save, with the same remaining fields (Name it · Effort · How it felt · Notes) behind "Add details".
from playwright.sync_api import sync_playwright
from lib import *
TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12"
LAB="()=>[...document.querySelectorAll('#sess .runc .l')].filter(e=>!e.hidden).map(e=>e.childNodes[0].textContent.trim())"
CORE=["Distance (km)","Elapsed time","Effort","How it felt (1–10)","Notes"]
QUICK=["What","Distance (km)","Time"];MORE=["Name it (optional)","Effort","How it felt (1–10)","Notes"]
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,WED)
    ok("run day, as planned: the five core fields in order",p.evaluate(LAB)==CORE,p.evaluate(LAB))
    p.click('#toc [data-toc="else"]');p.wait_for_timeout(80)
    ok("run day, something else: What, Distance, Time",p.evaluate(LAB)==QUICK,p.evaluate(LAB))
    det(p);ok("Add details reveals the same remaining fields, in order",p.evaluate(LAB)==QUICK+MORE,p.evaluate(LAB))
    c.close()
    c,p=view(b,THU);p.click('#toc [data-toc="else"]');p.wait_for_timeout(80)
    ok("strength day, something else: the very same card",p.locator("#sess h2").all_inner_texts()==["ACTUAL"] and p.evaluate(LAB)==QUICK,p.evaluate(LAB))
    p.click('#r_at [data-at="gym"]');p.wait_for_timeout(60)
    ok("a type without distance hides only that field",p.evaluate(LAB)==["What","Time"],p.evaluate(LAB))
    det(p);ok("one Notes box only",p.locator("#s_nt").count()==0 and p.locator("#r_n").count()==1)
    p.fill("#r_t","45");p.dispatch_event("#r_t","change");p.fill("#r_f","7");p.dispatch_event("#r_f","input");p.fill("#r_n","hotel gym, pulls and carries");p.dispatch_event("#r_n","input");p.click("#fin2");p.wait_for_selector("#ov.show",timeout=3000);p.clock.fast_forward(1000);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("feel and notes from the details are logged on a replaced strength day",e["sub"]=="Gym session 45:00" and e["feel"]=="7" and e["notes"]=="hotel gym, pulls and carries" and e["min"]==45 and e["act"]=="gym",e)
    p.click('#toc [data-toc="plan"]');p.wait_for_timeout(80)
    ok("back on the plan: the session Notes box returns, no Actual card",p.locator("#s_nt").count()==1 and p.locator("#sess .runc").count()==0)
    c.close()
    c,p=view(b,TUE);p.click("#addrun");p.wait_for_timeout(80)
    ok("+ Add an activity: What, then the five core fields, then Save activity",p.evaluate(LAB)==["What"]+CORE and p.locator("#runsave").inner_text()=="Save activity",p.evaluate(LAB))
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
