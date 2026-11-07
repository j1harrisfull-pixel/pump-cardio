# pc-v43: the second round of walkthrough fixes. Compact suggestion line; Progress / History / Weeks visible with no
# day open; unplanned week wording; import Check lists the days and Save lands on that week with a toast; coach
# export with planned → actual, blocks done, feel, recent misses only and a next-week line.
import json, copy
from playwright.sync_api import sync_playwright
from lib import *
X="db-bench"
SAMPLE=json.load(open(os.path.join(os.path.dirname(__file__),"..","docs","week-sample.json")))
def shifted():
    w=copy.deepcopy(SAMPLE);w["week"]="2026-11-09";w["days"]={}
    for i,(k,v) in enumerate(sorted(SAMPLE["days"].items())): w["days"]["2026-11-%02d"%(9+i)]=v
    return w
with sync_playwright() as pw:
    b=launch(pw)
    L=[{"date":"2026-10-27","name":"Strength A · Upper","type":"main","min":40,"sets":6,"of":6,"wt":{X:"20"},"rp":{X:{"v":[6,6,6,6],"u":""}},"feel":"7","sid":"up27"},
       {"date":"2026-10-29","name":"Zone 2 Run","type":"main","min":30,"km":"4.5","time":"30:00","effort":"easy","feel":"6"},
       {"date":"2026-11-03","name":"Strength A4 · Upper","type":"main","min":42,"sets":5,"of":14,"wt":{X:"22"},"rp":{X:{"v":[6,6,5,"–"],"u":"","k":["22","22","22","–"]}},"oc":"cut short","notes":"knee niggle","sid":"up03","bk":{"d":["Shoulder prep – upper","Straight sets sets"],"n":6}},
       {"date":"2026-11-07","name":"KB EMOM 15 · Round 2 + Run","type":"main","min":30,"km":"5.02","time":"30:05","effort":"easy","feel":"5","sub":"5K easy run","plan":"KB EMOM 15 · Round 2 + Run","oc":"modified","sid":"kb07","bk":{"d":[],"n":4}}]
    c,p=view(b,"2026-11-08",seed={"wo_log":L,"wo_daymap":{"2026-11-04":"2026-11-06","2026-11-06":"2026-11-04"}},open_day=False)
    ok("Progress, History and the backup line are visible with no day open",p.locator("#panel.open").count()==0 and p.locator("#more").is_visible() and p.locator("#prg").is_visible() and p.locator("#bkn").is_visible())
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("Progress has content without opening a day","Dumbbell bench press" in p.locator("#prog_b").inner_text() and p.locator("#hist li").count()==4)
    t=p.evaluate("()=>__app.exportText()");S=t.split("--- JSON")[0]
    ok("export: planned → actual per exercise from the logged session","Dumbbell bench press: planned 4 × 6 → 22 kg · 6/6/5/–" in S,S)
    ok("export: blocks done line","blocks: Shoulder prep – upper, Straight sets sets (2 of 6)" in S and "blocks: none of 4 done" in S,[l for l in S.split("\n") if "blocks" in l])
    ok("export: feel average over the last 4 weeks","Feel (last 4 weeks): average 6/10 over 3 sessions" in S,[l for l in S.split("\n") if "Feel" in l])
    ok("export: misses limited to the last 3 weeks with readable dates",re.search(r"Planned but not logged \(last 3 weeks\): .*Thu 5 Nov \(Strength B4",S) and "2026-10-12" not in S and "Mon 12 Oct" not in S,[l for l in S.split("\n") if "Planned but" in l])
    ok("export: next week line","Next week (w/c Mon 9 Nov): not planned yet" in S)
    ok("export: swapped days with names","Swapped days: Wed 4 Nov ran Fri 6 Nov's session" in S,[l for l in S.split("\n") if "Swapped" in l])
    ok("export: substitution line without a duplicate 'modified'","did 5K easy run instead of KB EMOM 15 · Round 2 + Run" in S and S.count("modified")==0,S)
    # unplanned week
    p.click("#next");p.wait_for_timeout(100);opend(p,"2026-11-09")
    ok("unplanned week: 'No plan yet', names the week, points at Import week, hides Swap and Log",p.locator("#ttl").inner_text()=="No plan yet" and "Nothing planned for w/c Mon 9 Nov" in p.locator("#sess").inner_text() and "Import week" in p.locator("#sess").inner_text() and p.locator("#swap").is_hidden() and p.locator("#tolog").is_hidden())
    ok("week strip still says Soon",p.locator("#week button.day").first.inner_text().endswith("Soon"))
    # import: days listed, toast, landing week
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})");p.click("#imp");p.fill("#im_t",json.dumps(shifted()));p.click("#im_chk");p.wait_for_timeout(100)
    ok("Check lists the days of the week","Mon Run · Tue Upper (+ backup) · Wed KB · Thu Rest · Fri Upper · Sat KB · Sun Rest" in p.locator("#im_r").inner_text() and "1 How-to entry." in p.locator("#im_r").inner_text(),p.locator("#im_r").inner_text())
    p.click("#im_ok");p.wait_for_selector("#week button.day",timeout=10000);p.wait_for_timeout(300)
    ok("after Save the app lands on the saved week with a toast",p.locator("#wlab").inner_text().lower()=="next week" and [x.split("\n")[2] for x in p.locator("#week button.day").all_inner_texts()]==["Run","Upper","KB","Rest","Upper","KB","Rest"] and p.locator("#toast.show").count()==1 and p.locator("#toast").inner_text().startswith("Week of Mon 9 Nov saved · Mon Run"),(p.locator("#wlab").inner_text(),p.locator("#toast").inner_text()))
    ok("flash is one-shot",ls(p,"wo_flash") is None)
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("weeks list: built in / imported with the title","w/c Mon 2 Nov · built in" in p.locator("#wks").inner_text() and "w/c Mon 9 Nov · Sample week (format demo) · imported · 7 days" in p.locator("#wks").inner_text(),p.locator("#wks").inner_text())
    ok("export now says next week is planned","Next week (w/c Mon 9 Nov): planned" in p.evaluate("()=>__app.exportText()"))
    c.close()
    # suggestion line
    c,p=view(b,"2026-11-03",seed={"wo_log":L[:1],"wo_wt":{X:{"2026-10-27":"20"}}})
    ok("suggestion: button first, one line",p.locator(".sug .sfill").first.inner_text()=="Use 22 kg" and p.locator(".sug span").first.inner_text()=="all 4 sets hit 6 at 20 kg last time · only if it felt RPE 6–7")
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
