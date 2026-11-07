# pc-v42: fixes from the user walkthroughs. The elapsed time field takes what the iPhone keypad can type ("30",
# "30.5", "3005") and shows mm:ss at once; Progress keeps the weight for per-set-kg logs and the arrow needs clean sets;
# the rest bar clears when a block is complete and its label leads with reps @ kg; Edit run only on run logs; one set
# of outcome chips (different run lives there); a different run with nothing else done replaces the whole session and
# the log records blocks done (bk); the ring and header reflect a log; a Log ↓ shortcut; Reset is a small link.
from playwright.sync_api import sync_playwright
from lib import *
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,"2026-11-07")
    T=lambda v:p.evaluate("v=>{var i=document.getElementById('r_t');i.value=v;i.dispatchEvent(new Event('change',{bubbles:true}));return i.value}",v)
    ok("time field: decimal keypad, format hint",p.get_attribute("#r_t","inputmode")=="decimal" and "3005" in p.get_attribute("#r_t","placeholder"))
    ok("30 → 30:00, 30.5 → 30:30, 3005 → 30:05, 30:05 kept, 105 → 1:45:00? no: 105 minutes → 105:00",[T("30"),T("30.5"),T("3005"),T("30:05"),T("105")]==["30:00","30:30","30:05","30:05","105:00"],[T("30"),T("30.5"),T("3005"),T("30:05"),T("105")])
    ok("normalised value is what gets stored",ls(p,"wo_run_2026-11-07")["t"]=="105:00")
    ok("Log ↓ shortcut shown today, Swap still there",p.locator("#tolog").is_visible() and p.locator("#swap").is_visible())
    y0=p.evaluate("()=>window.scrollY");p.click("#tolog");p.wait_for_timeout(1200)
    ok("Log ↓ scrolls down to the How did it go card",p.evaluate("()=>window.scrollY")>y0+500 and p.evaluate("()=>document.getElementById('logsec').getBoundingClientRect().top")<844,(y0,p.evaluate("()=>window.scrollY"),p.evaluate("()=>document.getElementById('logsec').getBoundingClientRect().top")))
    ok("Reset is a small link away from Finish, Finish alone in the actions",p.locator("#acts button").all_inner_texts()==["Finish workout"] and p.locator("#rst").inner_text()=="Reset this day…" and p.locator("#rst").evaluate("e=>getComputedStyle(e).fontSize")=="15px")
    T("30:05");p.fill("#r_d","5.02");p.dispatch_event("#r_d","input");p.click('#r_e [data-e="easy"]');p.fill("#r_f","5");p.dispatch_event("#r_f","input")
    p.click('#oc [data-oc="different run"]');p.wait_for_timeout(60);p.fill("#r_sl","5K easy run");p.dispatch_event("#r_sl","input")
    ok("different run chip is on and stored as modified + sub",p.locator("#oc .rc.on").inner_text()=="different run" and ls(p,"wo_run_2026-11-07")["sub"]==1 and ls(p,"wo_2026-11-07")["oc"]=="modified")
    p.click('#oc [data-oc="planned"]');p.wait_for_timeout(60)
    ok("as planned clears the different run flag and the text field",ls(p,"wo_run_2026-11-07")["sub"]==0 and p.locator("#r_sl").count()==0 and p.locator("#oc .rc.on").inner_text()=="as planned")
    p.click('#oc [data-oc="different run"]');p.wait_for_timeout(60);p.fill("#r_sl","5K easy run");p.dispatch_event("#r_sl","input")
    fin(p);od=p.locator("#o_d").inner_text()
    ok("summary: whole session replaced, blocks done counted, no 'modified' duplicate, no '0 walk breaks'","did 5K easy run instead of KB EMOM 15 · Round 2 + Run" in od and "0 of 4 blocks done" in od and "modified" not in od and "walk break" not in od,od)
    ok("feel 5 is not a flat day",p.locator("#o_e").inner_text()!="Showing up on a flat day is the win.")
    p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("log: sub, plan = session, oc modified, bk {d:[], n:4}, time 30:05",e["sub"]=="5K easy run" and e["plan"]=="KB EMOM 15 · Round 2 + Run" and e["oc"]=="modified" and e["bk"]=={"d":[],"n":4} and e["time"]=="30:05",e)
    ok("header and ring reflect the log",p.locator("#dnote").inner_text()=="Logged today · 30 min" and p.locator("#pct").inner_text()=="100%",(p.locator("#dnote").inner_text(),p.locator("#pct").inner_text()))
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("history line: substitution once, not 'modified' as well","did 5K easy run instead of KB EMOM 15 · Round 2 + Run" in p.locator("#hist li").first.inner_text() and "modified" not in p.locator("#hist li").first.inner_text())
    c.close()
    # the run piece is replaced (not the session) when other blocks were done
    c,p=view(b,"2026-11-07");wu=p.evaluate("()=>document.querySelector('#sess [data-t]').dataset.t");R=run_block(p,wu)
    if p.locator("#bar.show").count(): p.click("#stop")
    emom=p.evaluate("()=>[...document.querySelectorAll('#sess [data-t]')].map(e=>e.dataset.t).find(x=>x=='k07a')");R=run_block(p,"k07a")
    if p.locator("#bar.show").count(): p.click("#stop")
    p.click('#oc [data-oc="different run"]');p.wait_for_timeout(60);p.fill("#r_sl","5K easy run");p.dispatch_event("#r_sl","input");fin(p);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("EMOM done + different run: plan is the run piece, bk lists the done blocks",e["plan"]=="Zone 2 run 12:00" and e["bk"]["d"]==["Kettlebell warm-up","Single-bell EMOM"] and e["bk"]["n"]==4,e)
    c.close()
    # strength: rest bar label and clearing; Progress weight; Edit run only on run logs
    seed={"wo_log":[{"date":"2026-10-27","name":"Strength A · Upper","type":"main","min":40,"sets":6,"of":6,"wt":{"db-bench":"20"},"rp":{"db-bench":{"v":[6,6,6,6],"u":"","k":["20","20","20","20"]}}}],"wo_wt":{"db-bench":{"2026-10-27":"20"}}}
    c,p=view(b,"2026-11-03",seed=seed)
    tick(p,"db-bench",0);ok("rest bar leads with reps @ kg, no exercise name on a single-move block",p.locator("#rlab").inner_text()=="Next: set 2 · 6 @ 20 kg",p.locator("#rlab").inner_text())
    tick(p,"db-bench",1);tick(p,"db-bench",2);ok("still running before the last set",p.locator("#rbar.show").count()==1)
    tick(p,"db-bench",3);ok("last set of the block clears the rest bar",p.locator("#rbar.show").count()==0 and ls(p,"wo_rest") is None)
    x2=p.evaluate("()=>document.querySelectorAll('.card.ex.blk')[1].querySelectorAll('.srow')[0].dataset.x");x3=p.evaluate("()=>document.querySelectorAll('.card.ex.blk')[1].querySelectorAll('.srow')[1].dataset.x")
    tick(p,x2,0);tick(p,x3,0);ok("superset: label carries the lab of the next move",re.match(r"Next: set 2 · \S+( \S+)? · B1$",p.locator("#rlab").inner_text()) is not None,p.locator("#rlab").inner_text())
    p.click("#rskip")
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("Progress shows the weight for a per-set-kg log","27 Oct: 6/6/6/6 @ 20 kg" in p.locator("#prog_b").inner_text(),p.locator("#prog_b").inner_text())
    ok("no Edit run on a strength log",p.locator("#hist .erun").count()==0)
    fin(p);p.click("#o_done");p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("a heavier session with a short set gets no up arrow",p.evaluate("()=>{var l=JSON.parse(localStorage.wo_log);l[l.length-1].rp['db-bench']={v:[6,6,5,'–'],u:'',k:['22','22','22','–']};l[l.length-1].wt={'db-bench':'22'};localStorage.wo_log=JSON.stringify(l);return 1}") and p.evaluate("()=>{__app.sid;return 1}") and (p.click("#close"),opend(p,"2026-11-03"),p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})"),"↑" not in p.locator("#prog_b").inner_text().split("Dumbbell bench press")[1].split("\n")[0])[-1])
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
