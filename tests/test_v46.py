# pc-v46: one record of what actually happened. "something else" on any session without a run (type chips Run / Walk /
# Row / Gym session / Mobility / Other, distance, time, effort, details) saves ONE entry on the planned day with
# sub + plan; "+ Add an activity" on every day without an Actual card, rest and unplanned days included; a typed time
# wins over the wall clock for minutes; a skipped session is 0 min and gets no tick in the week strip; the header date
# follows the open day; the Swap button says "this session" on other days.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12"
with sync_playwright() as pw:
    b=launch(pw)
    # ---- Monday: ran instead of Upper ----
    c,p=view(b,MON)
    ok("strength day chips include 'something else'",p.locator("#oc .rc").all_inner_texts()==["as planned","something else","modified","cut short","skipped"])
    ok("header date is the open day's",p.locator("#date").inner_text()=="Monday 9 November")
    p.click('#oc [data-oc="something else"]');p.wait_for_timeout(80)
    ok("one form: type chips (Run on), distance, time, effort, details; Extra section gone",p.locator("#r_at .rc").all_inner_texts()==["Run","Walk","Row","Gym session","Mobility","Other"] and p.locator("#r_at .rc.on").inner_text()=="Run" and p.locator("#logsec #r_d").is_visible() and p.locator("#logsec #r_t").count()==1 and p.locator("#logsec #r_sl").count()==1 and p.locator("#addrun").count()==0)
    p.fill("#r_d","5");p.dispatch_event("#r_d","input");p.fill("#r_t","2940");p.dispatch_event("#r_t","change");p.click('#r_e [data-e="easy"]')
    ok("time normalised from the keypad",p.input_value("#r_t")=="29:40")
    fin(p);od=p.locator("#o_d").inner_text()
    ok("summary: one line, no sets or blocks noise, minutes from the typed time",od=="did Run 5 km 29:40 instead of Upper · Slow Is Strong" and p.locator("#o_t").inner_text()=="30 min",(od,p.locator("#o_t").inner_text()))
    p.click("#o_done");L=ls(p,"wo_log")
    ok("ONE entry on the planned day: sub, plan, act, km, time, modified",len(L)==1 and L[0]["sub"]=="Run 5 km 29:40" and L[0]["plan"]=="Upper · Slow Is Strong" and L[0]["act"]=="run" and L[0]["km"]=="5" and L[0]["time"]=="29:40" and L[0]["oc"]=="modified" and L[0]["min"]==30,L)
    ok("week strip ticks the day",p.locator(f'button.day[data-d="{MON}"] .ok').count()==1)
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("History: one line that says it","did Run 5 km 29:40 instead of Upper · Slow Is Strong" in p.locator("#hist li").first.inner_text() and p.locator("#hist li").count()==1)
    ok("Progress counts it as a run","1 run · 5 km" in p.locator("#prog_b").inner_text(),p.locator("#prog_b").inner_text())
    p.click('#r_at [data-at="gym"]');p.wait_for_timeout(60)
    ok("Gym session hides distance",p.locator("#logsec #r_d").is_hidden() and p.locator("#r_at .rc.on").inner_text()=="Gym session")
    p.fill("#r_sl","Hotel gym · pulls and carries");p.dispatch_event("#r_sl","input");fin(p);p.click("#o_done")
    ok("details text becomes the label, no km on a gym session",ls(p,"wo_log")[0]["sub"]=="Hotel gym · pulls and carries" and ls(p,"wo_log")[0]["act"]=="gym" and not ls(p,"wo_log")[0].get("km"),ls(p,"wo_log")[0])
    p.click('#oc [data-oc="planned"]');p.wait_for_timeout(60)
    ok("as planned clears the form and the Extra section returns",p.locator("#logsec #r_at").count()==0 and p.locator("#addrun").count()==1)
    c.close()
    # ---- Tuesday: a rest day takes an activity ----
    c,p=view(b,TUE)
    ok("rest day: '+ Add an activity', no Finish",p.locator("#addrun").inner_text()=="+ Add an activity" and p.locator("#acts").is_hidden())
    p.click("#addrun");p.wait_for_timeout(60);p.click('#r_at [data-at="walk"]');p.wait_for_timeout(60)
    ok("Walk keeps distance, Save activity button",p.locator("#runx #r_d").is_visible() and p.locator("#runsave").inner_text()=="Save activity")
    p.fill("#r_t","20");p.dispatch_event("#r_t","change");p.fill("#r_n","walk + stretch");p.dispatch_event("#r_n","input");p.click("#runsave");p.wait_for_timeout(120)
    e=ls(p,"wo_log")[0];ok("saved as a Walk entry on the rest day, 20 min, ticked in the strip",e["name"]=="Walk" and e["type"]=="extra" and e["act"]=="walk" and e["min"]==20 and e["notes"]=="walk + stretch" and p.locator(f'button.day[data-d="{TUE}"] .ok').count()==1,e)
    p.click('#r_at [data-at="mob"]');p.wait_for_timeout(60);ok("Mobility hides distance",p.locator("#runx #r_d").is_hidden())
    p.click("#runsave");p.wait_for_timeout(100);ok("re-saving updates the same entry and renames it",len(ls(p,"wo_log"))==1 and ls(p,"wo_log")[0]["name"]=="Mobility")
    c.close()
    # ---- unplanned future week also takes an activity ----
    c,p=view(b,"2026-11-16")
    ok("unplanned day: Add an activity available",p.locator("#addrun").count()==1 and "No plan yet" in p.locator("#sess").inner_text())
    c.close()
    # ---- skipped: 0 min, no tick ----
    c,p=view(b,THU);p.click('#oc [data-oc="skipped"]');fin(p)
    ok("skipped logs 0 min",p.locator("#o_t").inner_text()=="0 min" and ls(p,"wo_log")[0]["min"]==0);p.click("#o_done")
    ok("skipped day has no tick in the strip",p.locator(f'button.day[data-d="{THU}"] .ok').count()==0)
    opend(p,WED);ok("viewing another day: its date in the header, 'Swap this session'",p.locator("#date").inner_text()=="Wednesday 11 November" and p.locator("#swap").inner_text()=="Swap this session")
    c.close()
    # ---- typed time beats the wall clock ----
    c,p=view(b,WED);p.evaluate("d=>{var s=JSON.parse(localStorage.getItem('wo_'+d)||'{}');s.start=Date.now()-70000;localStorage.setItem('wo_'+d,JSON.stringify(s));}",WED)
    p.fill("#r_d","6.4");p.dispatch_event("#r_d","input");p.fill("#r_t","3812");p.dispatch_event("#r_t","change");fin(p)
    ok("run logged 70 s after the timer started still reads 38 min",p.locator("#o_t").inner_text()=="38 min" and ls(p,"wo_log")[0]["min"]==38 and ls(p,"wo_log")[0]["time"]=="38:12");p.click("#o_done")
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
