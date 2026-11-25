# pc-v75: Save activity saves for sure and says so (James, Wed 25 Nov: "It just flashes"). Writes to wo_log are read back
# before any confirmation; a failed write shows an error and keeps the form; Finish no longer shows "Workout saved" when the
# write failed; times over an hour (1:11 for 11.9 km, 1.11.00) are read as h:mm(:ss); old entries like that are corrected.
from playwright.sync_api import sync_playwright
from lib import *
STUB="()=>{window.__o=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k=='wo_log'){var e=new Error('full');e.name='QuotaExceededError';throw e;}return window.__o.apply(this,arguments)}}"
UNSTUB="()=>{Storage.prototype.setItem=window.__o}"
def tabs(b,d,seed=None,hour=22):
    c,p=view(b,d,seed,hour=hour,open_day=False)
    p.evaluate("()=>localStorage.removeItem('wo_flat')");p.emulate_media(color_scheme="dark");p.reload();p.wait_for_selector("#home",timeout=10000);p.wait_for_timeout(150)
    return c,p
def toast(p): return p.locator("#toast").inner_text() if p.locator("#toast.show").count() else ""
def fill25(p):
    p.fill("#r_d","5.13");p.fill("#r_t","30:17");p.click('#r_e [data-e="easy"]');p.fill("#r_f","5")
with sync_playwright() as pw:
    b=launch(pw)
    # 1. the exact entry from the video, tabs layout, dark mode, rest day
    c,p=tabs(b,"2026-11-25")
    p.click('#home [data-hm="open"]');p.wait_for_timeout(200);p.click("#addrun");p.wait_for_timeout(150);fill25(p)
    p.click("#runsave");p.wait_for_timeout(200)
    L=[e for e in ls(p,"wo_log") or [] if e["date"]=="2026-11-25"]
    ok("Save activity stores the run: 5.13 km, 30:17, 30 min, easy, felt 5",len(L)==1 and L[0]["km"]=="5.13" and L[0]["time"]=="30:17" and L[0]["min"]==30 and L[0]["effort"]=="easy" and L[0]["feel"]=="5",L)
    t=toast(p);ok("a visible 'Activity saved' toast after the write",t.startswith("Activity saved") and "5.13 km" in t and "30:17" in t,t)
    p.click("#tabbar [data-tab=prog]");p.wait_for_timeout(250);txt=p.locator("body").inner_text()
    ok("Progress lists it (5.13 km · 30:17)","5.13 km" in txt and "30:17" in txt)
    c.close()
    # 2. storage refuses the write: error, form kept, nothing claimed; then it saves
    c,p=tabs(b,"2026-11-25")
    p.click('#home [data-hm="open"]');p.wait_for_timeout(200);p.click("#addrun");p.wait_for_timeout(150);fill25(p)
    p.evaluate(STUB);p.click("#runsave");p.wait_for_timeout(200)
    t=toast(p);ok("failed write: 'Couldn't save' toast with the reason, no 'saved'","Couldn't save" in t and "QuotaExceededError" in t and "Activity saved" not in t,t)
    ok("failed write: the form keeps 5.13 and 30:17",p.input_value("#r_d")=="5.13" and p.input_value("#r_t")=="30:17")
    ok("failed write: nothing in wo_log",not [e for e in ls(p,"wo_log") or [] if e["date"]=="2026-11-25"])
    p.evaluate(UNSTUB);p.click("#runsave");p.wait_for_timeout(200)
    ok("after storage recovers the same tap saves",len([e for e in ls(p,"wo_log") or [] if e["date"]=="2026-11-25"])==1 and toast(p).startswith("Activity saved"))
    c.close()
    # 3. long runs: 1:11 with 11.9 km and 1.11.00 are 71 min; 30:17 stays 30 min
    c,p=tabs(b,"2026-11-25")
    p.click('#home [data-hm="open"]');p.wait_for_timeout(200);p.click("#addrun");p.wait_for_timeout(150)
    p.fill("#r_d","11.9");p.fill("#r_t","1:11");p.click("#runsave");p.wait_for_timeout(150)
    e=[e for e in ls(p,"wo_log") if e["date"]=="2026-11-25"][0];ok("1:11 for 11.9 km saves as 1:11:00, 71 min",e["time"]=="1:11:00" and e["min"]==71,e)
    p.fill("#r_t","1.11.00");p.click("#runsave");p.wait_for_timeout(150)
    e=[e for e in ls(p,"wo_log") if e["date"]=="2026-11-25"][0];ok("1.11.00 (iPhone number pad) saves as 1:11:00, 71 min",e["time"]=="1:11:00" and e["min"]==71,e)
    c.close()
    # 4. Finish: no 'Workout saved' card when the write fails
    c,p=tabs(b,"2026-11-24",hour=19)
    p.click('#home [data-hm="run"]');p.wait_for_timeout(250);p.fill("#r_d","6.2");p.fill("#r_t","31:05")
    p.evaluate(STUB);p.click("#fin_c");p.wait_for_timeout(300)
    ok("Finish with a failed write: no 'Workout saved' card, an error toast",not p.locator("#ov.show").count() and "Couldn't save" in toast(p),toast(p))
    ok("Finish with a failed write: nothing logged, fields kept",not [e for e in ls(p,"wo_log") or [] if e["date"]=="2026-11-24"] and p.input_value("#r_d")=="6.2")
    p.evaluate(UNSTUB);p.clock.run_for(2000);p.click("#fin_c");p.wait_for_timeout(300)
    ok("Finish after storage recovers shows 'Workout saved' and logs it",p.locator("#ov.show").count()==1 and len([e for e in ls(p,"wo_log") if e["date"]=="2026-11-24"])==1)
    c.close()
    # 5. the 18 Nov run saved as 1:11 (1 min) is corrected on load; normal runs untouched
    seed={"wo_log":[{"date":"2026-11-18","name":"Extra run","type":"extra","extra":1,"act":"run","km":"11.90","time":"1:11","effort":"steady","feel":"6","notes":"A","min":1},
                    {"date":"2026-11-09","name":"Upper · Slow Is Strong","type":"main","km":"5.00","time":"30:27","min":30}]}
    c,p=tabs(b,"2026-11-25",seed)
    L={e["date"]:e for e in ls(p,"wo_log")}
    ok("18 Nov 11.9 km in 1:11 becomes 1:11:00 / 71 min",L["2026-11-18"]["time"]=="1:11:00" and L["2026-11-18"]["min"]==71,L["2026-11-18"])
    ok("a normal 5 km in 30:27 is untouched",L["2026-11-09"]["time"]=="30:27" and L["2026-11-09"]["min"]==30)
    c.close()
    ok("no page errors",errs==[],errs)
    b.close()
raise SystemExit(done())
