# pc-v52: Sunday week review (from 15:00: sessions, runs, km, minutes, what is not logged, next week, Send to Grok);
# readable dates in History (the export keeps ISO); Undo on the "Workout saved" card restores the log exactly, also
# after "It replaced …" and the one tap Skipped; dark mode follows the phone with readable text everywhere.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12";SUN="2026-11-15"
L=[{"date":MON,"name":"Upper · Slow Is Strong","type":"main","min":30,"sub":"Run 5 km 29:40","plan":"Upper · Slow Is Strong","act":"run","km":"5","time":"29:40","effort":"easy","oc":"modified","sid":"upb0911"},
   {"date":WED,"name":"Hill Hunter Run","type":"main","min":38,"km":"6.4","time":"38:12","effort":"steady","sid":"hill1111"},
   {"date":THU,"name":"Lower · Carry Medley","type":"main","min":0,"oc":"skipped","sid":"lob1211","sets":0,"of":16}]
def lum(rgb):
    v=[int(x)/255 for x in re.findall(r"\d+",rgb)[:3]];v=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in v];return 0.2126*v[0]+0.7152*v[1]+0.0722*v[2]
def ratio(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True);return (x+0.05)/(y+0.05)
with sync_playwright() as pw:
    b=launch(pw)
    # ---- Sunday review ----
    c,p=view(b,SUN,seed={"wo_log":L},hour=18,open_day=False)
    t=p.locator("#wrev").inner_text().replace("\n"," ")
    ok("Sunday evening: Your week card with the four numbers",p.locator("#wrev").is_visible() and t.startswith("YOUR WEEK 2/5 sessions 2 runs 11.4 km distance 68 min running"),t)
    ok("what is not logged, what was skipped, next week",("Not logged: Sat Swing EMOM + Fartlek 5 km · Sun Hill Push Walk + Stretch" in t) and "Skipped: Thu" in t and "Next week: not planned yet" in t,t)
    p.click("#rev_go");p.wait_for_timeout(150);ok("Send this week to Grok opens the export",p.locator("#exs.show").count()==1 and "SUMMARY" in p.locator("#ex_t").input_value() and ls(p,"wo_lastexport")==SUN);p.click(".exx")
    p.click("#rev_x");p.wait_for_timeout(80);ok("Done hides it for this week",p.locator("#wrev").is_hidden() and ls(p,"wo_rev")==MON)
    c.close();c,p=view(b,SUN,seed={"wo_log":L},hour=9,open_day=False);ok("not shown on Sunday morning",p.locator("#wrev").is_hidden())
    c.close();c,p=view(b,THU,seed={"wo_log":L[:2]},hour=18,open_day=False);ok("not shown on other days",p.locator("#wrev").is_hidden())
    # ---- readable History dates ----
    p.evaluate("()=>document.querySelectorAll('details').forEach(function(d){d.open=true})")
    ok("History shows 'Wed 11 Nov', the ISO date stays in the data attribute",p.locator("#hist li b").first.inner_text()=="Wed 11 Nov" and p.locator("#hist li b").first.get_attribute("data-d")==WED)
    ok("the export keeps ISO dates for the coach",f"{WED} · Hill Hunter Run (main)" in p.evaluate("()=>__app.exportText()"))
    c.close()
    # ---- Undo ----
    c,p=view(b,THU,seed={"wo_log":L[:2]});before=ls(p,"wo_log")
    p.click('#toc [data-toc="skip"]');p.wait_for_timeout(60);fin(p)
    ok("Undo offered on the saved card",p.locator("#o_undo").is_visible() and len(ls(p,"wo_log"))==3)
    p.click("#o_undo");p.wait_for_timeout(150)
    ok("Undo restores the log exactly and says so",ls(p,"wo_log")==before and p.locator("#ov.show").count()==0 and p.locator("#toast.show").count()==1 and "Undone" in p.locator("#toast").inner_text())
    c.close()
    X={"date":MON,"name":"Extra run","type":"extra","extra":1,"act":"run","km":"5","time":"29:40","effort":"easy","min":30}
    c,p=view(b,TUE,seed={"wo_log":[X]},open_day=False);opend(p,MON);p.click("#xconv");p.wait_for_selector("#ov.show",timeout=3000);p.clock.fast_forward(1000);p.click("#o_undo");p.wait_for_timeout(150)
    ok("Undo after 'It replaced …' brings the extra entry and the plan back",ls(p,"wo_log")==[X] and p.locator("#ttl").inner_text()=="Upper · Slow Is Strong" and p.locator("#toc .rc.on").inner_text()=="The plan" and p.locator(".conv").count()==1,ls(p,"wo_log"))
    c.close()
    c,p=view(b,TUE,open_day=False);p.evaluate("()=>localStorage.removeItem('wo_nag')");p.click('#ynag [data-ng="skip"]');p.wait_for_selector("#ov.show",timeout=3000);p.clock.fast_forward(1000);p.click("#o_undo");p.wait_for_timeout(150)
    ok("Undo after the one tap Skipped clears the skip",ls(p,"wo_log") in (None,[]) and not (ls(p,"wo_"+MON) or {}).get("oc"),(ls(p,"wo_log"),ls(p,"wo_"+MON)))
    c.close()
    # ---- dark mode ----
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block",color_scheme="dark")
    p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.clock.install(time=dt.datetime(2026,11,3,9,0));p.goto(URL)
    p.evaluate("()=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');}");p.reload();p.wait_for_selector("#week button.day");p.click('button.day[data-d="2026-11-03"]');p.wait_for_timeout(250)
    cs=lambda sel,prop:p.evaluate("a=>getComputedStyle(document.querySelector(a[0]))[a[1]]",[sel,prop])
    ok("dark: page background is dark, body text light",lum(cs("body","backgroundColor"))<0.02 and lum(cs("#ttl","color"))>0.8,(cs("body","backgroundColor"),cs("#ttl","color")))
    pairs=[("#sess .card","backgroundColor","#sess .card .name","color"),(".topq","backgroundColor",".topq .rc:not(.on)","color"),(".day:not(.today):not(.sel)","backgroundColor",".day:not(.today):not(.sel) .dd","color"),("#fin","backgroundColor","#fin","color"),(".day.today","backgroundColor",".day.today .dd","color")]
    bad=[(a,ratio(cs(a,pa),cs(bb,pb))) for a,pa,bb,pb in pairs if ratio(cs(a,pa),cs(bb,pb))<4.5]
    ok("dark: cards, chips, day pills and the orange buttons keep 4.5:1 text contrast",not bad,bad)
    ok("dark: the stop-signs line is still visible",p.locator(".safe .stop").is_visible() and ratio(cs("body","backgroundColor"),cs(".safe .stop","color"))>=4.5)
    tick(p,"db-bench",0);p.wait_for_timeout(150)
    ok("dark: rest bar text readable",ratio(cs("#rbar","backgroundColor").replace("rgba","rgb"),cs("#rtime","color"))>=7,(cs("#rbar","backgroundColor"),cs("#rtime","color")));p.click("#rskip")
    p.locator("#sess [data-t]").first.click();p.clock.run_for(12000);p.wait_for_timeout(100)
    ok("dark: clock digits and the NOW line are light on dark",lum(cs("#time","color"))>0.8 and lum(cs("#now","color"))>0.8,(cs("#time","color"),cs("#now","color")));p.click("#stop")
    c.close()
    c,p=view(b,"2026-11-03");ok("light stays light",lum(p.evaluate("()=>getComputedStyle(document.body).backgroundColor"))>0.8)
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
