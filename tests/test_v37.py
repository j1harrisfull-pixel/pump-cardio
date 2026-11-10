# pc-v37/38: (1) "Did a different run" on run days: the actual run replaces the prescription in the log (sub + plan),
# editable from History; (2) one-tap outcome on every session (as planned / modified / cut short / skipped) with notes
# on strength days, saved by Finish workout; (3) a SUMMARY at the top of the export: last weights and reps, runs by
# week, swapped days, different runs, outcomes, planned but not logged. Old logs without the new fields still work.
import re, json
from playwright.sync_api import sync_playwright
from lib import *
RUN="2026-11-02"; STR="2026-11-03"
with sync_playwright() as pw:
    b=launch(pw)
    # ---------------- 1. different run on a run day ----------------
    c,p=view(b,RUN)
    ok("run day: one set of outcome chips incl. different run, none on, no text field yet (pc-v42)",p.locator("#oc .rc").all_inner_texts()==["as planned","different run","modified","cut short","skipped"] and p.locator("#oc .rc.on").count()==0 and p.locator("#r_sl").count()==0 and p.locator("#r_sub").count()==0)
    ok("notes stay in the Actual card on a run day",p.locator("#s_nt").count()==0 and p.locator("#r_n").count()==1)
    p.click('#oc [data-oc="different run"]');p.wait_for_timeout(80)
    ok("different run chip: flag saved, outcome modified, text field appears and takes focus",(ls(p,"wo_run_"+RUN) or {}).get("sub")==1 and (ls(p,"wo_"+RUN) or {}).get("oc")=="modified" and p.locator("#r_sl").count()==1 and p.evaluate("()=>document.activeElement&&document.activeElement.id")=="r_sl")
    p.fill("#r_sl","5K easy run");p.dispatch_event("#r_sl","input");p.fill("#r_d","5");p.dispatch_event("#r_d","input");p.fill("#r_t","28:30");p.dispatch_event("#r_t","input");p.click('#r_e [data-e="easy"]')
    ok("what you ran instead is saved as typed",ls(p,"wo_run_"+RUN).get("sl")=="5K easy run")
    fin(p)
    od=p.locator("#o_d").inner_text()
    ok("summary says what replaced the plan","did 5K easy run instead of Easy run 5 km 31:00" in od,od);p.click("#o_done")
    L=ls(p,"wo_log");e=L[0]
    ok("log: sub + plan recorded, type still main, actual values kept",len(L)==1 and e.get("sub")=="5K easy run" and e.get("plan")=="Easy run 5 km 31:00" and e["type"]=="main" and e["km"]=="5" and e["time"]=="28:30" and e["effort"]=="easy",e)
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("history line shows the substitution","did 5K easy run instead of Easy run 5 km 31:00" in p.locator("#hist li").first.inner_text(),p.locator("#hist li").first.inner_text())
    # edit from History
    p.click("#hist .erun");p.wait_for_timeout(100)
    ok("Edit run: Plan chips shown with Did a different run on and the text prefilled",p.locator("#er_subw").is_visible() and p.locator("#er_sub .rc.on").inner_text()=="Did a different run" and p.locator("#er_sl").input_value()=="5K easy run")
    p.click('#er_sub [data-sub="0"]');p.wait_for_timeout(50)
    ok("As prescribed hides the text field",p.locator("#er_slw").is_hidden())
    p.click("#er_ok");p.wait_for_timeout(100);e=ls(p,"wo_log")[0]
    ok("saving As prescribed removes sub and plan from the entry and the day card",("sub" not in e) and ("plan" not in e) and ls(p,"wo_run_"+RUN).get("sub")==0 and e.get("oc")=="planned" and p.locator("#oc .rc.on").inner_text()=="as planned" and len(ls(p,"wo_log"))==1,e)
    p.click("#hist .erun");p.wait_for_timeout(100);p.click('#er_sub [data-sub="1"]');p.fill("#er_sl","parkrun");p.click("#er_ok");p.wait_for_timeout(100);e=ls(p,"wo_log")[0]
    ok("setting a different run from History writes sub and re-derives the plan",e.get("sub")=="parkrun" and e.get("plan")=="Easy run 5 km 31:00" and ls(p,"wo_run_"+RUN).get("sl")=="parkrun",e)
    ok("no page errors so far",not errs,errs)
    c.close()
    # a flagged run with no text still reads sensibly
    c,p=view(b,RUN);p.click('#oc [data-oc="different run"]');p.wait_for_timeout(50);fin(p);p.click("#o_done")
    ok("empty text falls back to 'a different run'",ls(p,"wo_log")[0].get("sub")=="a different run")
    c.close()
    # a run inside a mixed session (Sat 7 Nov: KB EMOM 15 + Zone 2 run) gets the same Actual card (pc-v38)
    c,p=view(b,"2026-11-07")
    ok("mixed session with a run block: Actual card, different run chip, no Add a run",p.locator("#r_d").count()==1 and p.locator('#oc [data-oc="different run"]').count()==1 and p.locator("#addrun").count()==0 and p.locator("#runx").count()==0)
    p.click('#oc [data-oc="different run"]');p.wait_for_timeout(60);p.fill("#r_sl","5K easy run");p.dispatch_event("#r_sl","input");p.fill("#r_d","5.1");p.dispatch_event("#r_d","input");p.fill("#r_t","30:00");p.dispatch_event("#r_t","input");p.click('#r_e [data-e="easy"]')
    fin(p);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("log: nothing else done, so the whole session was replaced (plan = session name)",e.get("sub")=="5K easy run" and e.get("plan")=="KB EMOM 15 · Round 2 + Run" and e.get("bk",{}).get("n")==4 and e["km"]=="5.1" and e["time"]=="30:00" and e["type"]=="main" and len(ls(p,"wo_log"))==1,e)
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("history: Edit run offered on the mixed session",p.locator("#hist .erun").count()==1)
    c.close()
    # ---------------- 2. outcome on a strength day ----------------
    c,p=view(b,STR)
    ok("strength day: How did it go? card with 5 chips (something else, no different run), none selected, and a notes box",p.locator("#oc .rc").count()==5 and p.locator("#oc .rc.on").count()==0 and p.locator("#s_nt").count()==1 and p.locator("#r_sub").count()==0)
    ok("chip wording",p.locator("#oc .rc").all_inner_texts()==["as planned","something else","modified","cut short","skipped"],p.locator("#oc .rc").all_inner_texts())
    p.click('#oc [data-oc="cut short"]');p.fill("#s_nt","knee niggle");p.dispatch_event("#s_nt","input");s=ls(p,"wo_"+STR)
    ok("outcome and notes saved on the day as you go",s.get("oc")=="cut short" and s.get("nt")=="knee niggle",s)
    p.click('#oc [data-oc="cut short"]');ok("tapping the same chip again clears it",ls(p,"wo_"+STR).get("oc")=="" and p.locator("#oc .rc.on").count()==0)
    p.click('#oc [data-oc="cut short"]')
    p.locator(".tk").first.click();p.wait_for_timeout(50)
    if p.locator("#rbar.show").count(): p.click("#rskip")
    fin(p);od=p.locator("#o_d").inner_text();ok("summary shows the outcome","cut short" in od,od);p.click("#o_done")
    e=ls(p,"wo_log")[0]
    ok("log: oc + notes, sets still counted",e.get("oc")=="cut short" and e.get("notes")=="knee niggle" and e["sets"]==1 and e["type"]=="main",e)
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("history shows cut short and the note","cut short" in p.locator("#hist li").first.inner_text() and "knee niggle" in p.locator("#hist li").first.inner_text())
    ok("chips and notes restored after re-render",p.locator("#oc .rc.on").inner_text()=="cut short" and p.locator("#s_nt").input_value()=="knee niggle")
    c.close()
    # skipped with nothing ticked still logs the day
    c,p=view(b,STR);p.click('#oc [data-oc="skipped"]');fin(p);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("skipped logs a 0-set day with the outcome",e.get("oc")=="skipped" and e["sets"]==0,e)
    ok("as planned is not written to history as a line","as planned" not in p.locator("#hist li").first.inner_text() if p.locator("#hist li").count() else True)
    c.close()
    # rest day has no outcome card
    c,p=view(b,"2026-11-07",open_day=False)
    rd=p.evaluate("()=>{var P=__wk.PROG,S=__how.SESS;return Object.keys(P).filter(function(d){return d>='2026-11-02'&&d<='2026-11-08'&&S[P[d]]&&S[P[d]].rest;})[0]||null;}")
    if rd:
        opend(p,rd);ok(f"rest day {rd}: no outcome card",p.locator("#oc").count()==0)
    c.close()
    # ---------------- 3. export summary ----------------
    c,p=view(b,"2026-11-07",open_day=False)
    xid=p.evaluate("()=>{var S=__how.SESS.up03,x=null;S.blocks.forEach(function(b){if(!x&&b.k=='ex')x=b.items[0].x;});return x;}")
    xnm=p.evaluate("x=>__how.X[x][0]",xid)
    seed={"wo_log":[
        {"date":"2026-10-20","name":"Old shape","type":"main","min":30,"sets":3,"of":6,"feel":"7"},                         # pre-v35 entry, no new fields
        {"date":"2026-10-27","name":"Strength A · Upper","type":"main","min":40,"sets":6,"of":6,"wt":{xid:"20"},"rp":{xid:{"v":[8,8,8],"u":""}}},
        {"date":"2026-10-29","name":"Zone 2 Run","type":"main","min":30,"km":"4.5","time":"30:00","effort":"easy","oc":"modified"},
        {"date":"2026-11-02","name":"Easy 5 km Run","type":"main","min":28,"km":"5","time":"28:30","effort":"easy","sub":"5K easy run","plan":"Easy run 5 km 31:00"},
        {"date":"2026-11-03","name":"Strength A4 · Upper","type":"main","min":42,"sets":5,"of":6,"wt":{xid:"22"},"rp":{xid:{"v":[8,7,"–"],"u":""}},"oc":"cut short","notes":"knee niggle"},
        {"date":"2026-11-03","name":"Extra run","type":"extra","extra":1,"min":20,"km":"3.2","time":"20:00","effort":"easy"}],
        "wo_daymap":{"2026-11-04":"2026-11-06","2026-11-06":"2026-11-04"}}
    c.close();c,p=view(b,"2026-11-07",seed=seed,open_day=False)
    t=p.evaluate("()=>__app.exportText()");lines=t.split("\n")
    ok("summary sits right under the title, before the entries",lines[2]=="SUMMARY" and t.index("SUMMARY")<t.index("2026-11-03 · Strength A4") and t.index("Planned but not logged")<t.index("--- JSON"),lines[:4])
    ok("last weights and reps: the latest entry per exercise wins",re.search(re.escape(xnm)+r" 22 kg · 8/7/– \(2026-11-03\)",t) and "20 kg" not in t.split("Runs by week")[0],t[:600])
    ok("runs by week: one line per Monday with count, km and minutes","w/c 2026-10-26: 1 run · 4.5 km · 30 min" in t and "w/c 2026-11-02: 2 runs · 8.2 km · 49 min" in t,[l for l in lines if "w/c" in l])
    ok("swapped days listed from wo_daymap","Swapped days: Wed 4 Nov ran Fri 6 Nov's session" in t and "Fri 6 Nov ran Wed 4 Nov's session" in t,[l for l in lines if "Swapped" in l])
    ok("different runs listed","Different runs: 2026-11-02: 5K easy run instead of Easy run 5 km 31:00" in t)
    ok("outcomes grouped by kind","Outcomes: modified 2026-10-29 · cut short 2026-11-03" in t,[l for l in lines if "Outcomes" in l])
    miss=[l for l in lines if l.startswith("Planned but not logged")]
    ok("planned but not logged: past programmed days without a log, not today, not rest days",miss and "Thu 5 Nov (" in miss[0] and "7 Nov" not in miss[0] and "3 Nov" not in miss[0] and "2 Nov" not in miss[0] and "11 Oct" not in miss[0],miss)
    ok("per-entry lines carry the substitution and the outcome","2026-11-02 · Easy 5 km Run (main) · 28 min · 5 km · 28:30 · easy · did 5K easy run instead of Easy run 5 km 31:00" in t and "cut short" in [l for l in lines if l.startswith("2026-11-03 · Strength")][0],[l for l in lines if l.startswith("2026-11-0")])
    ok("raw JSON still at the end, old entry untouched",json.loads(t.split("--- JSON (wo_log) ---\n")[1])[0]=={"date":"2026-10-20","name":"Old shape","type":"main","min":30,"sets":3,"of":6,"feel":"7"})
    opend(p,"2026-11-07");p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("history renders every entry incl. the old shape without errors",p.locator("#hist li").count()==6 and not errs,(p.locator("#hist li").count(),errs,p.locator("#hist li").all_inner_texts()))
    # empty log: summary degrades to just the heading
    c.close();c,p=view(b,"2026-11-07",open_day=False)
    t=p.evaluate("()=>__app.exportText()")
    ok("empty history: summary has no weights/runs/outcomes sections and no crash","SUMMARY" in t and "Last weights" not in t and "Runs by week" not in t and "Outcomes" not in t and not errs,errs)
    c.close();b.close()
exit(done())
