# pc-v67: Progress and History. Four tiles that line up (2 x 2), the last four weeks with bars, lifts as cards that open the
# exercise history, recent runs in columns, an empty state, History as cards with one actions button each (change type,
# Edit run, Delete behind it), and Export together with the backup line.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";WED="2026-11-11";THU="2026-11-12"
def mk():
    L=[{"date":MON,"name":"Upper · Slow Is Strong","type":"main","min":30,"sub":"Easy 5km","plan":"Upper · Slow Is Strong","act":"run","km":"5","time":"30:27","effort":"easy","oc":"modified","sid":"upb0911"},
       {"date":WED,"name":"Hill Hunter Run","type":"main","min":38,"km":"6.4","time":"38:12","effort":"steady","sid":"hill1111","feel":"6"},
       {"date":"2026-11-02","name":"Extra run","type":"extra","extra":1,"act":"run","min":20,"km":"3","time":"20:00","effort":"easy"}]
    for x in ["goblet-squat","db-rdl","kb-swing","db-row","pushup","plank","farmers"]:
        for d,kg in (("2026-11-03","16"),("2026-11-10","18")):
            L.append({"date":d,"name":"Lower · Test "+x,"type":"main","min":40,"sets":3,"of":3,"sid":"x","wt":{x:kg},"rp":{x:{"v":["7","7","7"],"u":"","k":[kg,kg,kg]}}})
    return sorted(L,key=lambda e:e["date"])
rect=lambda p,s:p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}",s)
def go(p): p.click('#tabbar [data-tab="prog"]');p.wait_for_timeout(300)
with sync_playwright() as pw:
    b=launch(pw)
    c,p=tabs_app(b,THU);go(p)
    ok("empty state: one friendly line, no tiles, no History, no backup card",p.locator(".pempty").is_visible() and "Nothing logged yet." in p.locator(".pempty").inner_text() and p.locator(".wkbig").count()==0 and p.locator("#hsd").is_hidden() and p.locator("#bkn").is_hidden());c.close()
    c,p=tabs_app(b,THU,{"wo_log":mk(),"wo_lastexport":"2026-11-08"});go(p)
    tl=p.evaluate("()=>[].map.call(document.querySelectorAll('.wkbig.t4 > div'),function(e){var r=e.getBoundingClientRect(),q=function(s){return e.querySelector(s).getBoundingClientRect().top-r.top};return [Math.round(r.width),Math.round(r.height),Math.round(q('.tl')),Math.round(q('b')),Math.round(q('.tc')),e.querySelector('.tl').textContent,e.querySelector('.tc').textContent]})")
    ok("four tiles of one size with label, number and comparison in the same places",len(tl)==4 and len({(t[0],t[1]) for t in tl})==1 and len({t[2] for t in tl})==1 and len({t[3] for t in tl})==1 and len({t[4] for t in tl})==1,tl)
    ok("tiles: Sessions, Runs, Distance, Running with last week comparisons",[t[5] for t in tl]==["Sessions","Runs","Distance","Running"] and all(t[6].startswith("last week") for t in tl),[t[6] for t in tl])
    ok("the numbers",p.locator(".wkbig.t4").inner_text().replace("\n"," ").startswith("SESSIONS 3 / 5") and "11.4 km" in p.locator(".wkbig.t4").inner_text().replace("\n"," ") and "68 min" in p.locator(".wkbig.t4").inner_text().replace("\n"," "))
    w4=p.evaluate("()=>[].map.call(document.querySelectorAll('.prow.wk4'),function(e){return [e.querySelector('.bar i').style.width,e.textContent.slice(0,22)]})")
    ok("last four weeks: text kept, a bar for sessions done of planned",len(w4)==4 and w4[0][0]=="60%" and w4[1][0]=="20%" and w4[0][1].startswith("w/c 9 Nov · 3 of 5") and p.locator(".prow.wk4 .bar").first.get_attribute("aria-hidden")=="true",w4)
    ok("lifts: five cards and Show all",p.locator(".xcard").count()==5 and p.locator(".xall").inner_text()=="Show all 7")
    p.click(".xall");p.wait_for_timeout(150);ok("Show all lists all seven; Show fewer goes back",p.locator(".xcard").count()==7 and p.locator(".xall").inner_text()=="Show fewer");p.click(".xall");p.wait_for_timeout(100)
    p.locator(".xcard").first.click();p.wait_for_timeout(250)
    ok("a lift card opens the exercise history sheet",p.locator("#xhs.show").count()==1 and p.locator("#xh_b").inner_text().strip()!="");p.click(".xhx");p.wait_for_timeout(150)
    rr=p.evaluate("()=>[].map.call(document.querySelectorAll('.rtab .rrow'),function(r){return [].map.call(r.children,function(c){return c.textContent})})")
    ok("recent runs in four columns: date, distance, time, effort",rr[0]==["11 Nov","6.4 km","38:12","steady"] and rr[1]==["9 Nov","5 km","30:27","easy"],rr)
    ok("a different run and an extra are noted under their row","instead of Upper · Slow Is Strong" in p.locator(".rtab").inner_text() and "extra" in p.locator(".rtab .rnote").last.inner_text())
    # backup and export
    ok("Export and the backup line sit in one card",p.locator("#bkn").inner_text().startswith("Last backup Sun 8 Nov · 4 days ago") and p.locator("#bknow").inner_text()=="Export history" and p.locator("#exp").is_hidden())
    p.click("#bknow");p.wait_for_timeout(200);ok("Export history opens the export",p.locator("#exs.show").count()==1);p.click(".exx");p.wait_for_timeout(100)
    # history
    ok("History is open, with a heading and no disclosure triangle",p.locator("#hsd").evaluate("e=>e.open") and p.locator("#hsd > summary").inner_text().lower()=="history" and p.evaluate("()=>getComputedStyle(document.querySelector('#hsd > summary')).listStyleType")=="none")
    hc=p.evaluate("()=>[].map.call(document.querySelectorAll('#hist li.hcard'),function(e){return [e.querySelector('b[data-d]').dataset.d,e.querySelector('.hnm').textContent,e.querySelector('.hmn').textContent,e.querySelector('.hmore').getBoundingClientRect().width,!!e.querySelector('.hdel'),!!e.querySelector('select')]})")
    ok("History cards: ISO date kept, name, minutes, one 44 px button; no select or Delete inline",len(hc)==17 and hc[0][0]==WED and hc[0][1]=="Hill Hunter Run" and hc[0][2]=="38 min" and all(h[3]>=44 and not h[4] and not h[5] for h in hc),hc[0])
    p.locator("#hist .hmore").first.click();p.wait_for_timeout(250)
    ok("the actions sheet: Change type, Edit run, Delete",p.locator("#acs.show").count()==1 and p.locator("#ac_t").inner_text()=="Hill Hunter Run" and p.locator("#acs [data-ty]").count()>=2 and p.locator("#acs [data-er]").count()==1 and p.locator("#acs [data-del]").count()==1)
    p.click('#acs [data-ty="backup"]');p.wait_for_timeout(300)
    lg=[e for e in ls(p,"wo_log") if e["date"]==WED][0]
    ok("Change type works from the sheet and closes it",lg["type"]=="backup" and p.locator("#acs.show").count()==0,lg.get("type"))
    p.locator("#hist .hmore").first.click();p.wait_for_timeout(200);p.click('#acs [data-ty="main"]');p.wait_for_timeout(250)
    p.locator("#hist .hmore").first.click();p.wait_for_timeout(200);p.click("#acs [data-er]");p.wait_for_timeout(250)
    ok("Edit run opens its sheet from the actions sheet",p.locator("#ers.show").count()==1 and p.locator("#acs.show").count()==0);p.click(".erx");p.wait_for_timeout(150)
    n0=len(ls(p,"wo_log"));p.locator("#hist .hmore").first.click();p.wait_for_timeout(200);p.click("#acs [data-del]");p.wait_for_timeout(300)
    ok("Delete still confirms (the test accepts) and deletes that entry",len(ls(p,"wo_log"))==n0-1 and not [e for e in ls(p,"wo_log") if e["date"]==WED] and p.locator("#acs.show").count()==0)
    p.locator("#hist .hmore").last.scroll_into_view_if_needed();p.locator("#hist .hmore").last.click();p.wait_for_timeout(250)
    ok("an extra has no change type, only delete and Edit run",p.locator("#ac_t").inner_text()=="Extra run" and p.locator("#acs [data-ty]").count()==0 and p.locator("#acs [data-del]").count()==1 and p.locator("#acs [data-er]").count()==1)
    p.click(".acx") if p.locator("#acs.show").count() else None
    c.close()
    c,p=tabs_app(b,THU,{"wo_log":mk(),"wo_lastexport":"2026-11-08"},scheme="dark");go(p)
    col=p.evaluate("()=>[getComputedStyle(document.querySelector('.xcard')).backgroundColor,getComputedStyle(document.querySelector('.rtab')).backgroundColor,getComputedStyle(document.querySelector('#bkn')).backgroundColor,getComputedStyle(document.querySelector('.hcard')).backgroundColor]")
    ok("dark: every card is a dark surface",all(sum(map(int,__import__("re").findall(r"\d+",x)[:3]))<200 for x in col),col)
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
