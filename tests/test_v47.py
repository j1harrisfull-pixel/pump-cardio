# pc-v47: honest strength logging. Per exercise "Note for next time" (saved as rp[id].n, shown under the move next
# time, exported); "Did a different exercise" (rp[id].sub: the log, History, Progress and the export say so, the real
# lift's weight history and suggestion are left alone); "Skip this exercise" (rows hidden, excluded from totals, logged
# as skx); "+ set / − set" per block (extra rounds in wo_<date>.xs, counted in sets/of and in the rest bar).
from playwright.sync_api import sync_playwright
from lib import *
D="2026-11-12"
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,D)
    xs=p.evaluate("d=>__how.SESS[__app.sid(d)].blocks.filter(b=>b.k=='ex').map(b=>({tid:b.tid,n:b.n,x:b.items.map(i=>i.x)}))",D)
    A=xs[0];x1=A["x"][0];x2=A["x"][1];B=xs[1];bx=B["x"];tot0=sum(b["n"]*len(b["x"]) for b in xs)
    ok("every strength block has + set, no − set yet",p.locator('[data-xs="1"]').count()==len(xs) and p.locator('[data-xs="-1"]').count()==0)
    p.locator('[data-xs="1"]').first.click();p.wait_for_timeout(60)
    ok("+ round adds a row for every move in the block and a − control",p.locator(f'.srow[data-x="{x1}"]').count()==A["n"]+1 and p.locator(f'.srow[data-x="{x2}"]').count()==A["n"]+1 and p.locator('[data-xs="-1"]').count()==1 and (ls(p,"wo_"+D) or {}).get("xs",{}).get(A["tid"])==1)
    p.locator('[data-xs="-1"]').first.click();p.wait_for_timeout(60);ok("− round removes it again",p.locator(f'.srow[data-x="{x1}"]').count()==A["n"] and not (ls(p,"wo_"+D) or {}).get("xs"))
    p.locator('[data-xs="1"]').first.click();p.wait_for_timeout(60)
    p.locator('.more[data-mo]').first.click();p.wait_for_timeout(60)
    ok("More panel: note, different exercise, skip",p.locator('[data-xn]').first.is_visible() and p.locator('[data-rx]').first.is_visible() and p.locator('[data-sk]').first.inner_text()=="Skip this exercise")
    p.locator('[data-xn]').first.fill("left knee twinge rep 6");p.locator('[data-xn]').first.dispatch_event("input")
    p.locator('[data-rx]').first.fill("Goblet squat");p.locator('[data-rx]').first.dispatch_event("input");p.locator('[data-rx]').first.dispatch_event("change");p.wait_for_timeout(80)
    ok("header shows the replacement over the planned lift",p.locator(".mvh .rxn").first.inner_text()=="Goblet squat" and "instead of" in p.locator(".mvh .hd").first.inner_text())
    ok("no suggestion for a replaced lift",p.locator(".mvh").first.locator(".sug").count()==0)
    p.locator(f'.srow[data-x="{x1}"] input.w').first.fill("16");p.locator(f'.srow[data-x="{x1}"] input.w').first.dispatch_event("change");p.wait_for_timeout(120)
    for i in range(A["n"]+1):
        tick(p,x1,i)
        if p.locator("#rbar.show").count(): p.click("#rskip")
    ok("the real lift's weight history is not written for a replacement",(ls(p,"wo_wt") or {}).get(x1) is None)
    ok("ring counts the extra round",p.locator("#pct").inner_text()!="0%")
    # skip B2
    p.locator('.more[data-mo]').nth(3).click();p.wait_for_timeout(60);p.locator('[data-sk]').nth(3).click();p.wait_for_timeout(60)
    ok("skipped move: rows gone, header struck through, Un-skip offered",p.locator(f'.srow[data-x="{bx[1]}"]').count()==0 and p.locator(".mvh.skp").count()==1 and "skipped" in p.locator(".mvh.skp .hd").inner_text() and p.locator('[data-sk]').nth(3).inner_text()=="Un-skip this exercise")
    for i in range(B["n"]):
        tick(p,bx[0],i)
        if p.locator("#rbar.show").count(): p.click("#rskip")
    ok("rest bar never names the skipped move",all("Single-leg calf raise" not in t for t in [p.locator("#rlab").inner_text()]))
    fin(p);od=p.locator("#o_d").inner_text()
    ok("summary: replacement, note, skipped move, honest sets total",f"{A['n']+1+B['n']} of {tot0+len(A['x'])-B['n']} sets ticked" in od and "Goblet squat (instead of Rear-foot-elevated split squat) 16 kg · 7/7/7/7 · note: left knee twinge rep 6" in od and "skipped: Single-leg calf raise" in od,od)
    p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("log: rp.sub, rp.n, per-set kg, skx, of",e["rp"][x1]["sub"]=="Goblet squat" and e["rp"][x1]["n"]=="left knee twinge rep 6" and e["rp"][x1]["k"][0]=="16" and e["skx"]==[bx[1]] and e["of"]==tot0+len(A["x"])-B["n"] and x1 not in (e.get("wt") or {}),e)
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("History says it",re.search(r"Goblet squat \(instead of Rear-foot-elevated split squat\) 16 kg · 7/7/7/7 · note: left knee twinge rep 6",p.locator("#hist li").first.inner_text()))
    ok("Progress marks the replacement and carries the note, no trend arrow","12 Nov: 7/7/7/7 @ 16 kg (as Goblet squat) · left knee twinge rep 6" in p.locator("#prog_b").inner_text() and "↑" not in p.locator("#prog_b").inner_text().split("Rear-foot-elevated split squat")[1].split("\n")[0],p.locator("#prog_b").inner_text())
    t=p.evaluate("()=>__app.exportText()")
    ok("export: planned → did <replacement>, skipped line, no dangling arrow","Rear-foot-elevated split squat: planned 3 × 7 each side → did Goblet squat · 16 kg · 7/7/7/7 · note: left knee twinge rep 6" in t and "  skipped: Single-leg calf raise" in t and "→ ·" not in t,[l for l in t.split("\n") if "→" in l][:3])
    ok("next time the suggestion ignores the replaced session",p.evaluate("a=>__app.suggest(a,{rp:7})",x1) is None)
    c.close()
    # the note shows under the move the next time it appears (same session id a week later via an imported copy of the day is overkill: reuse the date with a later 'today')
    e2=dict(e);e2["date"]="2026-11-05";c,p=view(b,D,seed={"wo_log":[e2]})
    ok("note from the last time shows under the move",p.locator(".lnote").first.inner_text()=="Last time: left knee twinge rep 6")
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
