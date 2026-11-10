# pc-v51: one logging form. The run day's Actual card, a day that became something else, and "+ Add an activity" all
# use the same card with the same fields in the same order: (What · Name it, only when it is not the plan) · Distance ·
# Time · Effort · How it felt · Notes. No second Notes box, no separate form inside the outcome card.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12"
LAB="()=>[...document.querySelectorAll('#sess .runc .l')].filter(e=>!e.hidden).map(e=>e.childNodes[0].textContent.trim())"
CORE=["Distance (km)","Elapsed time","Effort","How it felt (1–10)","Notes"]
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,WED)
    ok("run day, as planned: the five core fields in order",p.evaluate(LAB)==CORE,p.evaluate(LAB))
    p.click('#toc [data-toc="else"]');p.wait_for_timeout(80)
    ok("run day, something else: What and Name it lead, then the same five",p.evaluate(LAB)==["What","Name it (optional)"]+CORE,p.evaluate(LAB))
    ok("the outcome card holds only the chips and Save",p.locator("#logsec .l").count()==0 and p.locator("#logsec #fin2").count()==1)
    c.close()
    c,p=view(b,THU);p.click('#toc [data-toc="else"]');p.wait_for_timeout(80)
    ok("strength day, something else: the very same card",p.locator("#sess h2").all_inner_texts()[:2]==["ACTUAL","HOW DID IT GO?"] and p.evaluate(LAB)==["What","Name it (optional)"]+CORE,p.evaluate(LAB))
    ok("one Notes box only",p.locator("#s_nt").count()==0 and p.locator("#r_n").count()==1)
    p.click('#r_at [data-at="gym"]');p.wait_for_timeout(60)
    ok("a type without distance hides only that field",p.evaluate(LAB)==["What","Name it (optional)"]+CORE[1:],p.evaluate(LAB))
    p.fill("#r_t","45");p.dispatch_event("#r_t","change");p.fill("#r_f","7");p.dispatch_event("#r_f","input");p.fill("#r_n","hotel gym, pulls and carries");p.dispatch_event("#r_n","input");p.click("#fin2");p.wait_for_selector("#ov.show",timeout=3000);p.clock.fast_forward(1000);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("feel and notes from the form are logged on a replaced strength day",e["sub"]=="Gym session 45:00" and e["feel"]=="7" and e["notes"]=="hotel gym, pulls and carries" and e["min"]==45 and e["act"]=="gym",e)
    p.click('#toc [data-toc="plan"]');p.wait_for_timeout(80)
    ok("back on the plan: the session Notes box returns, no Actual card",p.locator("#s_nt").count()==1 and p.locator("#sess .runc").count()==0)
    c.close()
    c,p=view(b,TUE);p.click("#addrun");p.wait_for_timeout(80)
    ok("+ Add an activity: What, then the same five, then Save activity",p.evaluate(LAB)==["What"]+CORE and p.locator("#runsave").inner_text()=="Save activity",p.evaluate(LAB))
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
