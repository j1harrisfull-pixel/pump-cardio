# pc-v49: the question sits at the top of the day. "What did you do? The plan / Something else / Skipped" right under
# the day controls; off-plan days lead with the log card and a Save button, the planned blocks fold behind "Show the
# planned session"; once logged the day reads as what was done (title, date line, strip label, ring, header); an extra
# activity on a day with nothing else done converts to "it replaced <session>" in one tap; History entries can be deleted.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12"
EXTRA={"date":MON,"name":"Extra run","type":"extra","extra":1,"act":"run","km":"5","time":"29:40","effort":"easy","feel":"6","notes":"river loop","min":30}
with sync_playwright() as pw:
    b=launch(pw)
    # ---- James's Monday: an extra run already saved, looked at on Tuesday ----
    c,p=view(b,TUE,seed={"wo_log":[EXTRA],"wo_run_"+MON:{"b":0,"s":{},"d":"5","t":"29:40","e":"easy"}},open_day=False);opend(p,MON)
    ok("top question with three chips, The plan on",p.locator("#toc .rc").all_inner_texts()==["The plan","Something else","Skipped"] and p.locator("#toc .rc.on").inner_text()=="The plan")
    ok("chips fit one row at iPhone width",len(set(round(e.bounding_box()["y"]) for e in p.locator("#toc .rc").all()))==1)
    ok("header says an extra is logged, not 'Not logged'",p.locator("#dnote").inner_text().startswith("Extra logged · Mon 9 Nov"))
    ok("offer to convert the extra, naming it and the session",p.locator(".conv").inner_text().replace("\n"," ")=="You logged Extra run · 5 km · 29:40 · easy on this day. It replaced Upper · Slow Is Strong",p.locator(".conv").inner_text())
    p.click("#xconv");p.wait_for_selector("#ov.show",timeout=3000)
    ok("one tap saves it: summary says what replaced what",p.locator("#o_d").inner_text()=="did Run 5 km 29:40 instead of Upper · Slow Is Strong" and p.locator("#o_t").inner_text()=="30 min",p.locator("#o_d").inner_text())
    p.clock.fast_forward(1000);p.click("#o_done");p.wait_for_timeout(150);L=ls(p,"wo_log");e=L[0]
    ok("ONE entry now: the extra is merged into Monday's record with its feel and note",len(L)==1 and e["type"]=="main" and e["sub"]=="Run 5 km 29:40" and e["plan"]=="Upper · Slow Is Strong" and e["act"]=="run" and e["km"]=="5" and e["time"]=="29:40" and e["effort"]=="easy" and e["feel"]=="6" and e["notes"]=="river loop" and e["oc"]=="modified" and e["min"]==30,L)
    ok("the day reads as what was done: title, date line, strip, ring, header",p.locator("#ttl").inner_text()=="Run 5 km 29:40" and p.locator("#date").inner_text()=="Monday 9 November · instead of Upper · Slow Is Strong" and p.locator(f'button.day[data-d="{MON}"]').inner_text().replace("\n"," ")=="MON 9 Run ✓" and p.locator("#pct").inner_text()=="100%" and p.locator("#dnote").inner_text()=="Logged · Mon 9 Nov · 30 min",(p.locator("#ttl").inner_text(),p.locator("#date").inner_text(),p.locator(f'button.day[data-d="{MON}"]').inner_text(),p.locator("#dnote").inner_text()))
    ok("planned blocks folded away, the log card leads, the offer is gone",p.locator("#sess h2").all_inner_texts()==["HOW DID IT GO?"] and p.locator("#showp").inner_text()=="Show the planned session" and p.locator(".conv").count()==0 and p.locator("#toc .rc.on").inner_text()=="Something else")
    ok("session safety note hidden, stop-signs line stays",p.locator("#safe1").is_hidden() and p.locator(".safe .stop").is_visible())
    ok("rest timer pill out of the way on an off-plan day",p.locator("#rbtn").is_hidden())
    p.click("#showp");p.wait_for_timeout(80);ok("Show the planned session brings the blocks back",p.locator("#sess h2").count()>=6 and p.locator("#showp").inner_text()=="Hide the planned session")
    p.click("#showp");p.wait_for_timeout(60)
    opend(p,TUE);ok("another day keeps its own title",p.locator("#ttl").inner_text()!="Run 5 km 29:40")
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    li=p.locator("#hist li").first.inner_text()
    ok("History: one line, no '0/20 sets' noise, Delete offered","did Run 5 km 29:40 instead of Upper · Slow Is Strong" in li and "sets" not in li and p.locator("#hist .hdel").count()==1,li)
    ok("Progress counts one run, not two","1 run · 5 km" in p.locator("#prog_b").inner_text() or p.locator(".wkbig").inner_text().replace("\n"," ").startswith("1/"),p.locator(".wkbig").inner_text())
    p.locator("#hist .hdel").first.click();p.wait_for_timeout(150);opend(p,MON)
    ok("Delete removes the entry and the day goes back to the plan",ls(p,"wo_log")==[] and p.locator("#ttl").inner_text()=="Upper · Slow Is Strong" and p.locator("#toc .rc.on").inner_text()=="The plan" and p.locator(f'button.day[data-d="{MON}"]').inner_text().replace("\n"," ")=="MON 9 Upper" and p.locator("#sess h2").count()>=6)
    c.close()
    # ---- fresh strength day: Something else at the top, Save right there ----
    c,p=view(b,THU)
    H0=p.locator("#sess h2").all_inner_texts()
    p.click('#toc [data-toc="else"]');p.wait_for_timeout(80)
    ok("Something else: the form leads the day with a Save button, plan folded",p.locator("#sess h2").first.inner_text()=="HOW DID IT GO?" and p.locator("#logsec #r_at .rc.on").inner_text()=="Run" and p.locator("#fin2").inner_text()=="Save this day" and p.locator("#sess .card.ex").count()==0 and p.locator("#oc .rc.on").inner_text()=="something else")
    top=p.evaluate("()=>document.getElementById('fin2').getBoundingClientRect().bottom+window.scrollY")
    ok("Save sits within about two screens of the top (no long scroll)",top<1900,top)
    p.fill("#r_d","5");p.dispatch_event("#r_d","input");p.fill("#r_t","2940");p.dispatch_event("#r_t","change");p.click('#r_e [data-e="easy"]');p.click("#fin2");p.wait_for_selector("#ov.show",timeout=3000)
    ok("Save this day logs it",p.locator("#o_d").inner_text()=="did Run 5 km 29:40 instead of Lower · Carry Medley");p.clock.fast_forward(1000);p.click("#o_done");p.wait_for_timeout(120)
    ok("today reads as the run",p.locator("#ttl").inner_text()=="Run 5 km 29:40" and p.locator(f'button.day[data-d="{THU}"]').inner_text().replace("\n"," ")=="THU 12 Run ✓" and p.locator("#dnote").inner_text()=="Logged today · 30 min")
    p.click('#toc [data-toc="skip"]');p.wait_for_timeout(80)
    ok("Skipped: outcome skipped, substitution cleared, plan still folded",(ls(p,"wo_"+THU) or {}).get("oc")=="skipped" and ls(p,"wo_run_"+THU).get("sub")==0 and p.locator("#oc .rc.on").inner_text()=="skipped" and p.locator("#sess .card.ex").count()==0 and p.locator("#fin2").count()==1)
    p.click('#toc [data-toc="plan"]');p.wait_for_timeout(80)
    ok("The plan: everything back as prescribed, outcome cleared",p.locator("#sess h2").all_inner_texts()==H0 and not (ls(p,"wo_"+THU) or {}).get("oc") and p.locator("#fin2").count()==0 and p.locator("#safe1").is_visible())
    ok("the bottom chips still work and agree with the top",(p.click('#oc [data-oc="something else"]'),p.wait_for_timeout(60),p.locator("#toc .rc.on").inner_text())[-1]=="Something else")
    c.close()
    # ---- run day: Something else shows the Actual card first, with the type row ----
    c,p=view(b,WED);p.click('#toc [data-toc="else"]');p.wait_for_timeout(80)
    ok("run day off-plan: Actual card then the outcome card, type chips, one distance field",p.locator("#sess h2").all_inner_texts()[:2]==["ACTUAL","HOW DID IT GO?"] and p.locator("#r_at .rc").count()==6 and p.locator("#r_d").count()==1 and p.locator("#oc .rc.on").inner_text()=="different run")
    p.click('#r_at [data-at="row"]');p.wait_for_timeout(60);p.fill("#r_d","4");p.dispatch_event("#r_d","input");p.fill("#r_t","20");p.dispatch_event("#r_t","change");fin(p);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("a row instead of the run is logged with its type",e["act"]=="row" and e["sub"]=="Row 4 km 20:00" and e["km"]=="4" and e["time"]=="20:00",e)
    ok("strip says Row",p.locator(f'button.day[data-d="{WED}"]').inner_text().replace("\n"," ")=="WED 11 Row ✓")
    c.close()
    # ---- not offered where it makes no sense ----
    c,p=view(b,TUE);ok("rest day: no top question",p.locator("#topq").is_hidden());opend(p,THU);ok("future day: no top question",p.locator("#topq").is_hidden())
    c.close();c,p=view(b,TUE,seed={"wo_log":[EXTRA,{"date":MON,"name":"Upper · Slow Is Strong","type":"main","min":40,"sets":20,"of":20,"sid":"upb0911","oc":"planned"}]},open_day=False);opend(p,MON)
    ok("no convert offer when the session itself was done",p.locator(".conv").count()==0 and p.locator("#dnote").inner_text().startswith("Logged · "))
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
