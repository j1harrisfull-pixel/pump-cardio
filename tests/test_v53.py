# pc-v53: logging something different is three things and one button. What · Distance · Time · Save on one screen; name,
# effort, feel and notes wait behind "Add details" (with a one line summary once filled); no second row of chips, no
# Finish workout, auto-rest tick box or Reset on that screen; saving absorbs an extra entry of the same kind on that day.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";TUE="2026-11-10";THU="2026-11-12"
EXTRA={"date":MON,"name":"Extra run","type":"extra","extra":1,"act":"run","km":"5.00","time":"30:27","effort":"easy","min":30}
VIS="()=>[...document.querySelectorAll('#panel button, #panel input, #panel textarea')].filter(e=>e.offsetParent!==null&&!e.closest('#dctl')&&!e.closest('#topq')&&e.id!='close').map(e=>e.id||e.dataset.at||e.textContent.trim())"
with sync_playwright() as pw:
    b=launch(pw)
    # ---- James's Monday exactly as in his screenshots: extra run saved, Something else already on, details typed ----
    seed={"wo_log":[EXTRA],"wo_run_"+MON:{"b":0,"s":{},"d":"5.00","t":"30:27","e":"easy","f":"4","sl":"Easy 5km","sub":1,"at":"run"},"wo_"+MON:{"t":{},"rp":{},"s":{},"oc":"modified"}}
    c,p=view(b,TUE,seed=seed,open_day=False);opend(p,MON);p.wait_for_timeout(500)
    v=p.evaluate(VIS)
    ok("the whole screen is: six type chips, distance, time, the details line, Save, Show the planned session",v==["run","walk","row","gym","mob","other","r_d","r_t","moredet","fin2","showp"],v)
    ok("no second chip row, no Finish workout, no auto-rest tick box, no Reset",p.locator("#oc").count()==0 and p.locator("#fin").is_hidden() and p.locator(".setr").first.is_hidden() and p.locator("#rst").is_hidden())
    ok("the values he already typed are there",p.input_value("#r_d")=="5.00" and p.input_value("#r_t")=="30:27" and p.locator("#moredet").inner_text()=="Details: Easy 5km · easy · felt 4",p.locator("#moredet").inner_text())
    bottom=p.evaluate("()=>document.getElementById('fin2').getBoundingClientRect().bottom+window.scrollY")
    ok("Save is reachable with barely a scroll (under 1.8 screens from the top of the page)",bottom<1520,bottom)
    p.click("#fin2");p.wait_for_selector("#ov.show",timeout=3000)
    ok("one tap saves",p.locator("#o_d").inner_text()=="did Easy 5km instead of Upper · Slow Is Strong" and p.locator("#o_t").inner_text()=="30 min",p.locator("#o_d").inner_text())
    p.clock.fast_forward(1000);p.click("#o_done");p.wait_for_timeout(120);L=ls(p,"wo_log")
    ok("ONE entry: the extra run was absorbed, nothing typed was lost",len(L)==1 and L[0]["type"]=="main" and L[0]["sub"]=="Easy 5km" and L[0]["km"]=="5.00" and L[0]["time"]=="30:27" and L[0]["effort"]=="easy" and L[0]["feel"]=="4" and L[0]["min"]==30,L)
    ok("Monday reads as the run",p.locator("#ttl").inner_text()=="Easy 5km" and p.locator("#dnote").inner_text()=="Logged · Mon 9 Nov · 30 min" and p.locator(f'button.day[data-d="{MON}"]').inner_text().replace("\n"," ")=="MON 9 Run ✓")
    c.close()
    # ---- fresh day: three things and Save ----
    c,p=view(b,THU);p.click('#toc [data-toc="else"]');p.wait_for_timeout(80)
    ok("fresh: Add details is closed, no name / effort / feel / notes fields",p.locator("#moredet").inner_text()=="Add details" and all(p.locator(x).count()==0 for x in ("#r_sl","#r_e","#r_f","#r_n")))
    p.fill("#r_d","5");p.dispatch_event("#r_d","input");p.fill("#r_t","2940");p.dispatch_event("#r_t","change");p.click("#fin2");p.wait_for_selector("#ov.show",timeout=3000);p.clock.fast_forward(1000);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("distance, time, Save is a complete log",e["sub"]=="Run 5 km 29:40" and e["km"]=="5" and e["time"]=="29:40" and e["min"]==30 and e["oc"]=="modified",e)
    p.click("#moredet");p.wait_for_timeout(60);ok("Add details opens the four optional fields and reads Hide details",all(p.locator(x).count()==1 for x in ("#r_sl","#r_e","#r_f","#r_n")) and p.locator("#moredet").inner_text()=="Hide details")
    p.click('#r_e [data-e="steady"]');p.click("#moredet");p.wait_for_timeout(60);ok("closed again, the line summarises what is filled",p.locator("#moredet").inner_text()=="Details: steady")
    p.click("#showp");p.wait_for_timeout(80);ok("Show the planned session brings Finish workout and the settings back",p.locator("#fin").is_visible() and p.locator(".setr").first.is_visible() and p.locator("#sess .card.ex").count()>0)
    p.click('#toc [data-toc="skip"]');p.wait_for_timeout(80)
    ok("Skipped: a small card with a note box and one Save",p.locator("#sess h2").first.inner_text()=="HOW DID IT GO?" and p.locator("#fin2").inner_text()=="Save" and p.locator("#s_nt").count()==1 and p.locator("#sess .runc").count()==0)
    c.close()
    # ---- an extra of a different kind is kept ----
    W=dict(EXTRA,name="Walk",act="walk",km="2",time="25:00")
    c,p=view(b,TUE,seed={"wo_log":[W]},open_day=False);opend(p,MON);p.click('#toc [data-toc="else"]');p.wait_for_timeout(60);p.click('#r_at [data-at="gym"]');p.wait_for_timeout(60);p.fill("#r_t","40");p.dispatch_event("#r_t","change");p.click("#fin2");p.wait_for_selector("#ov.show",timeout=3000);p.clock.fast_forward(1000);p.click("#o_done")
    L=ls(p,"wo_log");ok("a walk logged earlier stays when the day is saved as a gym session",len(L)==2 and any(x["type"]=="extra" and x["act"]=="walk" for x in L) and any(x.get("act")=="gym" and x["type"]=="main" for x in L),L)
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
