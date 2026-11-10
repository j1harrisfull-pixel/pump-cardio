# pc-v48: exercise history one tap from the move (History in More, or the "last …" chip) with the best set; carry /
# Every blocks end with the score sheet (rounds · kg · effort) and show last time's score on the card; "29.40" means
# 29:40; export names strength blocks by their moves; the suggestion never says "came up short"; Progress opens with
# this week's numbers against last week; the Rest timer pill hides when no day is open, on rest days and under sheets;
# an unplanned week says so under the strip.
from playwright.sync_api import sync_playwright
from lib import *
X="db-bench"
with sync_playwright() as pw:
    b=launch(pw)
    seed={"wo_log":[{"date":"2026-10-20","name":"Strength A · Upper","type":"main","min":40,"sets":6,"of":6,"wt":{X:"18"},"rp":{X:{"v":[6,6,6,6],"u":"","n":"felt heavy"}}},
                    {"date":"2026-10-27","name":"Strength A · Upper","type":"main","min":40,"sets":6,"of":6,"wt":{X:"20"},"rp":{X:{"v":[6,6,6,6],"u":""}}},
                    {"date":"2026-11-02","name":"Easy 5 km Run","type":"main","min":28,"km":"5","time":"28:30","effort":"easy","sid":"run02"}],"wo_wt":{X:{"2026-10-27":"20"}}}
    c,p=view(b,"2026-11-03",seed=seed)
    ok("rest timer pill shows on an open strength day",p.locator("#rbtn").is_visible())
    p.locator(".lchip").first.click();p.wait_for_timeout(80)
    ok("tapping the 'last' chip opens the exercise history with the best set",p.locator("#xhs.show").count()==1 and p.locator("#xh_t").inner_text()=="Dumbbell bench press" and p.locator("#xh_u").inner_text()=="Best: 20 kg × 6 (Tue 27 Oct)",p.locator("#xh_u").inner_text())
    ok("history rows newest first with notes",p.locator("#xh_b .prow").all_inner_texts()==["Tue 27 Oct · 20 kg · 6/6/6/6","Tue 20 Oct · 18 kg · 6/6/6/6 · note: felt heavy"],p.locator("#xh_b .prow").all_inner_texts())
    ok("pill hidden while a sheet is up",p.locator("#rbtn").is_hidden());p.click(".xhx");p.wait_for_timeout(50)
    p.locator('.more[data-mo]').first.click();p.wait_for_timeout(60);ok("History button in More",p.locator('button[data-xh]').first.is_visible())
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("Progress opens with this week's numbers against last week",p.locator(".wkbig").inner_text().replace("\n"," ")=="1/2 sessions 1 run 5 km last week 0 km 29 min last week 0 min",p.locator(".wkbig").inner_text().replace("\n"," "))
    p.click("#close");p.wait_for_timeout(100);ok("pill hidden with no day open",p.locator("#rbtn").is_hidden())
    opend(p,"2026-11-04");ok("pill hidden on a rest / mobility day",p.locator("#rbtn").is_hidden())
    c.close()
    # suggestion wording when the target changed
    c,p=view(b,"2026-11-03",seed={"wo_log":[{"date":"2026-10-27","name":"x","type":"main","min":40,"wt":{X:"20"},"rp":{X:{"v":[5,5,5,5],"u":""}}}],"wo_wt":{X:{"2026-10-27":"20"}}})
    ok("stay line states the facts, never 'came up short'",p.locator(".sug").first.inner_text()=="Stay at 20 kg · last time 5/5/5/5 at 20 kg, target 6",p.locator(".sug").first.inner_text())
    c.close()
    # carry medley: score sheet at the end, last time on the card, export
    c,p=view(b,"2026-11-12");R=run_block(p,"l12bmed",score=False)
    ok("Every block ends with the score sheet, rounds prefilled, not yet marked done",p.locator("#scs.show").count()==1 and p.input_value("#sc_r")=="4" and not R["done"])
    p.fill("#sc_k","32");p.click("#sc_ok");p.wait_for_timeout(100)
    ok("saving stores rounds and kg and marks the block done",(ls(p,"wo_2026-11-12") or {}).get("sc",{}).get("l12bmed")=={"r":4,"kg":"32","e":""} and (ls(p,"wo_2026-11-12") or {}).get("s",{}).get("l12bmed")==1)
    fin(p);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("log carries the score, export names the block by its moves and prints the score",e["sc"]["l12bmed"]["kg"]=="32" and "  l12bmed: 4 rounds · 32 kg" in p.evaluate("()=>__app.exportText()") and e["bk"]["d"]==["Carry medley"],e["bk"])
    c.close();c,p=view(b,"2026-11-19",seed={"wo_log":[dict(e,date="2026-11-05")]},open_day=False);p.click("#prev");p.wait_for_timeout(100);opend(p,"2026-11-12")
    ok("last time's score shows on the carry card",p.locator(".lnote").all_inner_texts()==["Last time: 4 rounds · 32 kg (Thu 5 Nov)"],p.locator(".lnote").all_inner_texts())
    c.close()
    # strength block names in the export
    c,p=view(b,"2026-11-03");x1=p.evaluate("()=>document.querySelector('.srow').dataset.x")
    for i in range(4):
        tick(p,x1,i)
        if p.locator("#rbar.show").count(): p.click("#rskip")
    fin(p);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("export block name is the move, not 'Straight sets sets'",e["bk"]["d"]==["Straight sets: Dumbbell bench press"],e["bk"])
    c.close()
    # time parsing and the unplanned-week hint
    c,p=view(b,"2026-11-11")
    T=lambda v:p.evaluate("v=>{var i=document.getElementById('r_t');i.value=v;i.dispatchEvent(new Event('change',{bubbles:true}));return i.value}",v)
    ok("29.40 → 29:40, 29.5 → 29:30, 2940 → 29:40, 29:40 kept",[T("29.40"),T("29.5"),T("2940"),T("29:40")]==["29:40","29:30","29:40","29:40"],[T("29.40"),T("29.5"),T("2940"),T("29:40")])
    ok("placeholder shows the three ways",p.get_attribute("#r_t","placeholder")=="29:40 · 29.40 · 2940")
    c.close();c,p=view(b,"2026-11-16",open_day=False)
    ok("unplanned week: hint says so and offers logging",p.locator("#hint").inner_text().startswith("Nothing planned for this week yet"))
    c.close();c,p=view(b,"2026-11-10",open_day=False);ok("planned week: normal hint",p.locator("#hint").inner_text()=="Tap a day to see its workout")
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
