# pc-v40: progression inside the app. A suggestion per weighted exercise from the last logged sets (all sets hit the
# target → one step up, 2 kg dumbbells / 4 kg kettlebells; a short set → same weight), always qualified "only if it
# felt RPE 6–7", with a one-tap "Use N kg" that fills the unticked sets. A Progress screen: last 4 weeks (done of
# planned, runs, km), strength by exercise with a trend arrow, recent runs. Nothing is prefilled from the plan.
from playwright.sync_api import sync_playwright
from lib import *
X="db-bench";D="2026-11-03"
def seed(v,kg="20",k=None,extra=None):
    rp={"v":v,"u":""}
    if k: rp["k"]=k
    s={"wo_log":[{"date":"2026-10-27","name":"Strength A · Upper","type":"main","min":40,"sets":6,"of":6,"wt":{X:kg},"rp":{X:rp}}],"wo_wt":{X:{"2026-10-27":kg}}}
    s.update(extra or {});return s
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,D)
    ok("no history: no suggestion, kg empty, nothing from the plan",p.locator(".sug").count()==0 and p.locator(f'.srow[data-x="{X}"] input.w').first.input_value()=="" and p.evaluate("()=>__app.suggest('db-bench',{rp:6})") is None)
    c.close()
    # all sets hit → step up
    c,p=view(b,D,seed=seed([6,6,6,6]))
    ok("suggestion: all sets hit → try +2 kg (dumbbell), RPE 6–7 caveat",re.match(r"Use 22 kg\s*all 4 sets hit 6 at 20 kg last time · only if it felt RPE 6–7$",p.locator(".sug").first.inner_text()),p.locator(".sug").first.inner_text())
    ok("last weight prefilled as a dashed hint, not as today's weight",p.locator(f'.srow[data-x="{X}"] input.w.pf').count()==4 and (ls(p,"wo_wt") or {}).get(X,{}).get(D) is None)
    p.locator(".sfill").first.click();p.wait_for_timeout(80)
    ok("Use 22 kg fills every unticked set and saves today's weight",[e.input_value() for e in p.locator(f'.srow[data-x="{X}"] input.w').all()]==["22"]*4 and ls(p,"wo_wt")[X][D]=="22" and (ls(p,"wo_"+D) or {}).get("kg",{}).get("0_0")=="22")
    ok("suggestion disappears once it is in use",p.locator(".sug").count()==0)
    tick(p,X,0)
    if p.locator("#rbar.show").count(): p.click("#rskip")
    fin(p);p.click("#o_done");e=ls(p,"wo_log")[-1]
    ok("the log carries the new weight",e["wt"][X]=="22" and e["rp"][X]["k"][0]=="22",e)
    c.close()
    # a short set → same weight; kettlebell step 4 kg; timed/distance items never get a suggestion
    c,p=view(b,D,seed=seed([6,6,5,"–"]))
    ok("a short set → stay at the weight, no button (pc-v43)",p.locator(".sug").first.inner_text()=="Stay at 20 kg · last time 6/6/5/– at 20 kg, target 6" and p.locator(".sug .sfill").count()==0,p.locator(".sug").first.inner_text())
    ok("kettlebell step is 4 kg",p.evaluate("()=>__app.suggest('kb-swing',{rp:15})") is None and p.evaluate("()=>{var l=JSON.parse(localStorage.wo_log);l.push({date:'2026-10-28',rp:{'kb-swing':{v:[15,15],u:''}},wt:{'kb-swing':'16'}});localStorage.wo_log=JSON.stringify(l);return __app.suggest('kb-swing',{rp:15}).kg}")==20)
    ok("distance / timed items get no suggestion",p.evaluate("()=>__app.suggest('farmers-carry',{rp:50,ru:'m'})") is None)
    # per-set kg uses the heaviest set
    p.evaluate("()=>{var l=JSON.parse(localStorage.wo_log);l[0].rp['db-bench']={v:[6,6,6,6],u:'',k:['18','20','20','20']};localStorage.wo_log=JSON.stringify(l);}")
    ok("mixed per-set kg: steps up from the heaviest",p.evaluate("()=>__app.suggest('db-bench',{rp:6}).kg")==22)
    c.close()
    # ---------------- Progress screen ----------------
    L=[{"date":"2026-10-20","name":"Strength A · Upper","type":"main","min":40,"sets":6,"of":6,"wt":{X:"18"},"rp":{X:{"v":[6,6,6,6],"u":""}}},
       {"date":"2026-10-27","name":"Strength A · Upper","type":"main","min":40,"sets":6,"of":6,"wt":{X:"20"},"rp":{X:{"v":[6,6,6,6],"u":""}}},
       {"date":"2026-10-29","name":"Zone 2 Run","type":"main","min":30,"km":"4.5","time":"30:00","effort":"easy"},
       {"date":"2026-10-30","name":"Mobility","type":"main","min":20,"oc":"skipped","sets":0},
       {"date":"2026-11-02","name":"Easy 5 km Run","type":"main","min":28,"km":"5","time":"28:30","effort":"easy","sub":"5K easy run","plan":"Easy run 5 km 31:00"},
       {"date":"2026-11-02","name":"Extra run","type":"extra","extra":1,"min":20,"km":"3.2","time":"20:00","effort":"easy"}]
    c,p=view(b,"2026-11-07",seed={"wo_log":L})
    p.evaluate("()=>document.getElementById('prg').open=true");t=p.locator("#prog_b").inner_text()
    ok("Progress: a details section before History",p.locator("#prg summary").inner_text()=="Progress" and p.evaluate("()=>document.getElementById('prg').nextElementSibling.querySelector('summary').textContent")=="History")
    ok("last 4 weeks: done of planned (mobility days are rest days; skipped and extra runs not counted as done), runs and km","w/c 2 Nov · 1 of 4 sessions · 2 runs · 8.2 km · 49 min" in t and re.search(r"w/c 26 Oct · 2 of \d sessions · 1 run · 4.5 km · 30 min",t),t)
    ok("strength by exercise with the last entries and an up arrow","Dumbbell bench press ↑" in t and "20 Oct: 6/6/6/6 @ 18 kg · 27 Oct: 6/6/6/6 @ 20 kg" in t,t)
    ok("recent runs, newest first, substitutions and extras marked",t.index("2 Nov · 3.2 km · 20:00 · easy · extra")<t.index("2 Nov · 5 km · 28:30 · easy · instead of Easy run 5 km 31:00")<t.index("29 Oct · 4.5 km"),t)
    W=p.evaluate("()=>__app.weekRows(1)[0]");ok("weekRows counts only programmed days up to today",W["pl"]==4 and W["dn"]==1,W)
    c.close()
    c,p=view(b,"2026-11-07");p.evaluate("()=>document.getElementById('prg').open=true")
    ok("empty history: Progress still renders",("Nothing logged" in p.locator("#prog_b").inner_text()) or ("of" in p.locator("#prog_b").inner_text()))
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
