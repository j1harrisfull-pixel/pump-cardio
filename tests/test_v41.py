# pc-v41: the day screen focuses on what is left. A finished block (timer flag set, or every set ticked) folds to a
# one-line "✓ Done · name · show" that expands on tap; the first unfinished block carries an "Up next" pill; block
# headers never change. A backup line above Progress tells when the history was last exported and offers Back up now.
from playwright.sync_api import sync_playwright
from lib import *
D="2026-11-03"
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,D)
    H0=p.locator("#sess h2").all_inner_texts()
    ok("fresh day: nothing folded, no Up next",p.locator(".fold").count()==0 and p.locator(".upnext").count()==0)
    wu=p.evaluate("()=>document.querySelector('#sess [data-t]').dataset.t");R=run_block(p,wu)
    if p.locator("#bar.show").count(): p.click("#stop")
    ok("finished warm-up folds to one line naming the block",R["done"] and p.locator(".fold").all_inner_texts()==["✓ Done · Shoulder prep – upper · show"],p.locator(".fold").all_inner_texts())
    ok("its card is hidden, headers unchanged",p.locator("#sess .card.tcard").first.is_hidden() and p.locator("#sess h2").all_inner_texts()==H0)
    ok("Up next sits on block 2",p.evaluate("()=>{var u=document.querySelector('.upnext');return u&&u.textContent+'|'+u.nextElementSibling.textContent}")=="Up next|2 · A · Straight sets · 4 sets")
    p.locator(".fold").first.click();p.wait_for_timeout(60)
    ok("tap shows the finished block again (run again button visible)",p.locator(".fold").count()==0 and p.locator("#sess .card.tcard").first.is_visible() and p.locator(f'[data-t="{wu}"]').inner_text().startswith("✓ Done"))
    x=p.evaluate("()=>document.querySelector('.srow').dataset.x");n=p.locator(f'.srow[data-x="{x}"]').count()
    for i in range(n):
        tick(p,x,i)
        if p.locator("#rbar.show").count(): p.click("#rskip")
    ok("all sets ticked: the block you are in stays open (no fold under your thumb), Up next moves to block 3",p.locator(".fold").count()==0 and p.evaluate("()=>document.querySelector('.upnext').nextElementSibling.textContent").startswith("3 · "),p.locator(".fold").all_inner_texts())
    x2=p.evaluate("()=>document.querySelectorAll('.card.ex.blk')[1].querySelector('.srow').dataset.x");tick(p,x2,0)
    if p.locator("#rbar.show").count(): p.click("#rskip")
    ok("moving on to the next block folds the finished one",p.locator(".fold").all_inner_texts()==["✓ Done · Dumbbell bench press · show"],p.locator(".fold").all_inner_texts())
    p.locator(f'.srow[data-x="{x2}"] [data-tk]').first.click();p.wait_for_timeout(60)
    if p.locator("#rbar.show").count(): p.click("#rskip")
    ok("ticked rows stay in storage",len([k for k,v in (ls(p,"wo_"+D) or {}).get("t",{}).items() if v])==n)
    p.locator(".fold").first.click();p.wait_for_timeout(60);p.locator(f'.srow[data-x="{x}"] [data-tk]').last.click();p.wait_for_timeout(60)
    if p.locator("#rbar.show").count(): p.click("#rskip")
    ok("show, then untick a set: the block stays open and is no longer done",p.locator(".fold").count()==0 and p.locator(f'.srow[data-x="{x}"] .tk.on').count()==n-1)
    # ---- backup line ----
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("no logs: backup line hidden",p.locator("#bkn").is_hidden())
    fin(p);p.click("#o_done")
    ok("first log: 'No backup yet' with Back up now, not yet urgent",p.locator("#bkn").inner_text()=="No backup yet Back up now" and "due" not in (p.locator("#bkn").get_attribute("class") or ""))
    p.click("#bknow");p.wait_for_timeout(120)
    ok("Back up now opens the export and records the date",p.locator("#exs.show").count()==1 and ls(p,"wo_lastexport")==D and p.locator("#bkn").inner_text().startswith("Last backup Tue 3 Nov"),p.locator("#bkn").inner_text());p.click(".exx")
    c.close()
    L=[{"date":"2026-10-%02d"%d,"name":"x","type":"main","min":30} for d in (12,13,14,15,16,17)]
    c,p=view(b,"2026-11-07",seed={"wo_log":L});p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("5+ logs and never backed up → highlighted warning","due" in p.locator("#bkn").get_attribute("class") and "only lives on this phone" in p.locator("#bkn").inner_text())
    c.close();c,p=view(b,"2026-11-07",seed={"wo_log":L,"wo_lastexport":"2026-10-01"});p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("backup older than 30 days → highlighted with the age","due" in p.locator("#bkn").get_attribute("class") and "37 days ago" in p.locator("#bkn").inner_text(),p.locator("#bkn").inner_text())
    c.close();c,p=view(b,"2026-11-07",seed={"wo_log":L,"wo_lastexport":"2026-11-01"});p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("recent backup → plain line","due" not in (p.locator("#bkn").get_attribute("class") or "") and "6 days ago" in p.locator("#bkn").inner_text())
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
