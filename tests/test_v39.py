# pc-v39: weeks as data. A week is one JSON object (docs/week-format.md) built with the same builders as the code,
# validated (ids, How-to coverage, safety terms, effort words, run-instead totals), loaded from weeks/*.json at build
# time or imported on the phone (History → Import week). The sample week renders, audits clean, runs and logs.
import json, glob, os, copy
from playwright.sync_api import sync_playwright
from lib import *
SAMPLE=json.load(open(os.path.join(os.path.dirname(__file__),"..","docs","week-sample.json")))
def bar_off(p):
    if p.locator("#bar.show").count(): p.click("#stop");p.wait_for_timeout(40)
def seedw(w,extra=None): s={"wo_weeks":{w["week"]:w}}; s.update(extra or {}); return s
with sync_playwright() as pw:
    b=launch(pw)
    # ---------------- 1. validator ----------------
    c,p=view(b,"2026-11-07",open_day=False)
    V=lambda w:p.evaluate("w=>__app.validateWeek(w)",w)
    r=V(SAMPLE);ok("sample week validates with no errors",r["errors"]==[] and r["info"]["sess"]==4 and r["info"]["days"]==7,r)
    def bad(name,mut,want):
        w=copy.deepcopy(SAMPLE);mut(w);r=V(w);ok("rejects "+name,any(want in e for e in r["errors"]),r["errors"][:3])
    bad("a non-Monday week",lambda w:w.update(week="2027-01-05"),"not a Monday")
    bad("a reused built-in session id",lambda w:w["sess"].update(kb07=w["sess"]["kb0106"]),"already exists")
    bad("an unknown exercise id",lambda w:w["sess"]["up0105"]["blocks"][1]["items"][0].update(x="nope"),"unknown exercise id")
    bad("a move without a How-to",lambda w:w["sess"]["run0104"]["blocks"][0]["moves"].append(["Mystery stretch",30]),"no How-to")
    bad("a new exercise without a How-to",lambda w:w["x"].update(zz=["Zed press","10 kg","10",1]),"has no How-to")
    bad("a day outside the week",lambda w:w["days"].update({"2027-01-11":{"main":"run0104"}}),"outside the week")
    bad("a day pointing at an unknown session",lambda w:w["days"].update({"2027-01-07":{"main":"ghost"}}),"unknown session")
    bad("a duplicate block id",lambda w:w["sess"]["run0104"]["blocks"][2].update(id="s04wu"),"duplicate block id")
    bad("a banned term (barbell)",lambda w:w["sess"]["up0105"].update(safe="Barbell work today."),"banned term")
    bad("hard effort",lambda w:w["sess"]["run0104"]["blocks"][1].update(note="Hard pace."),"banned term")
    bad("RPE 8+",lambda w:w["sess"]["run0104"]["blocks"][1].update(note="Steady, RPE 8."),"RPE 8+")
    bad("a pace",lambda w:w["sess"]["run0104"]["blocks"][1].update(small="5:30 min/km."),"banned term")
    bad("a run-instead block with a different total",lambda w:w["ri"]["bk0105"]["s05bw"].update(sec=600),"differs")
    bad("a missing safety line",lambda w:w["sess"]["kb0106"].update(safe=""),"safe (safety line) missing")
    bad("a bad segment phase",lambda w:w["sess"]["kb0106"]["blocks"].append({"k":"timer","id":"zz","h":"Steady","name":"x","segs":[["SPRINT",60,"x"]]}),"bad segment")
    w=copy.deepcopy(SAMPLE);w["sess"]["kb0106"]["blocks"][2]["list"]=w["sess"]["kb0106"]["blocks"][2]["list"][:2];r=V(w)
    ok("warns (not blocks) on a circuit with fewer than 3 moves",r["errors"]==[] and any("fewer than 3" in x for x in r["warnings"]),r)
    ok("not JSON object → one clear error",V("nope")["errors"]==["Not a week object."])
    # built-in weeks: every weeks/*.json validates
    files=sorted(glob.glob(os.path.join(os.path.dirname(__file__),"..","weeks","*.json")))
    for f in files:
        r=V(json.load(open(f)));ok(f"weeks/{os.path.basename(f)} validates",r["errors"]==[],r["errors"][:3])
    print("built-in week files:",len(files))
    ok("Weeks list shows the coded weeks and the import button",p.evaluate("()=>{document.querySelector('details').open=true;return document.querySelectorAll('#wks li').length}")>=4 and p.locator("#imp").count()==1)
    c.close()
    # ---------------- 2. the sample week, imported, renders and audits clean ----------------
    c,p=view(b,"2027-01-05",seed=seedw(SAMPLE),open_day=False)
    W=p.evaluate("()=>__app.WEEKS");ok("imported week applied",W.get("2027-01-04",{}).get("src")=="import" and W["2027-01-04"]["errors"]==[],W)
    ok("week strip shows the imported sessions",[x.split("\n")[2] for x in p.locator("#week button.day").all_inner_texts()]==["Run","Upper","KB","Rest","Upper","KB","Rest"],p.locator("#week button.day").all_inner_texts())
    dev=[];views=week_views(p,"2027-01-04");ok("main, backup and run-instead views discovered",len(views)>=8 and any(t=="backup+run" for _,t,_ in views),views)
    for d,t,seed in views:
        c2,p2=view(b,d,seed=seedw(SAMPLE,seed));audit_view(f"{d} {t}",read_view(p2),dev);c2.close()
    ok("every view of the imported week passes the style audit",not dev,dev[:5])
    opend(p,"2027-01-05")
    ok("new exercise + How-to from the week file",p.locator('.mvn[data-h="db-floor-press"]').count()==1)
    p.click('.mvn[data-h="db-floor-press"]');p.wait_for_timeout(100);ok("How-to sheet opens for the new exercise",p.locator("#hs.show").count()==1 and "upper arms touch the floor" in p.locator("#hs").inner_text());p.click("#hs_x")
    R=run_block(p,"s05iv");ok("interval block from the file runs to the end with the right total (280 s + 10 s get-ready)",R["done"] and R["total"]==290,R);bar_off(p)
    tick(p,"db-floor-press",0)
    if p.locator("#rbar.show").count(): p.click("#rskip")
    fin(p);p.click("#o_done");e=ls(p,"wo_log")[0]
    ok("finishing an imported session logs normally",e["sid"]=="up0105" and e["sets"]==1 and e["name"]=="Strength · Upper (sample)",e)
    c.close();c,p=view(b,"2027-01-06",seed=seedw(SAMPLE))  # future days are read only, so each day is "today" in its own context
    R=run_block(p,"s06e");ok("EMOM from the file: 9 full minutes, done flag",R["done"] and R["total"]==550,R);bar_off(p)
    pl=p.evaluate("()=>__app.emomPlan(__how.SESS.kb0106.blocks[1])");ok("EMOM groups derived from the cycle",pl["p"]==3 and pl["reps"]==3 and pl["cycle"][0]["side"]=="left" and pl["cycle"][2]["mv"][0]["reps"]==12,pl)
    c.close();c,p=view(b,"2027-01-04",seed=seedw(SAMPLE));R=run_block(p,"s04run");bar_off(p);ok("run block with counter: walk break button and Actual card",R["done"] and p.locator("#r_d").count()==1 and p.locator("button:has-text('walk break')").count()>=1)
    ok("no page errors",not errs,errs);c.close()
    # ---------------- 3. import sheet on the phone ----------------
    c,p=view(b,"2027-01-04",open_day=False)
    ok("no plan yet: the day says so",p.locator("#week button.day").first.inner_text().endswith("Soon"))
    opend(p,"2027-01-04");ok("tbc note points at import","import it from History" in p.locator("#sess").inner_text())
    p.evaluate("()=>document.querySelector('details').open=true");p.click("#imp");p.wait_for_timeout(80)
    ok("import sheet opens",p.locator("#ims.show").count()==1 and p.locator("#im_ok").is_hidden())
    p.fill("#im_t","{not json");p.click("#im_chk");ok("bad JSON reported","Not valid JSON" in p.locator("#im_r").inner_text() and p.locator("#im_ok").is_hidden())
    w=copy.deepcopy(SAMPLE);w["days"]["2027-01-07"]={"main":"ghost"};p.fill("#im_t",json.dumps(w));p.click("#im_chk")
    ok("errors listed, save stays hidden","unknown session ghost" in p.locator("#im_r").inner_text() and p.locator("#im_ok").is_hidden())
    p.fill("#im_t",json.dumps(SAMPLE));p.click("#im_chk");ok("valid week: summary line and Save shown","4 sessions, 7 days" in p.locator("#im_r").inner_text() and p.locator("#im_ok").is_visible(),p.locator("#im_r").inner_text())
    p.click("#im_ok");p.wait_for_selector("#week button.day",timeout=10000);p.wait_for_timeout(200)
    ok("saved: page reloads with the week in place",(ls(p,"wo_weeks") or {}).get("2027-01-04",{}).get("week")=="2027-01-04" and p.locator("#week button.day").first.inner_text().endswith("Run"))
    p.click('button.day[data-d="2027-01-04"]');p.wait_for_timeout(150);p.evaluate("()=>document.querySelector('details').open=true")
    ok("Weeks list shows it as imported with Remove","imported" in p.locator("#wks").inner_text() and p.locator('[data-rmw="2027-01-04"]').count()==1,p.locator("#wks").inner_text())
    p.click('[data-rmw="2027-01-04"]');p.wait_for_selector("#week button.day",timeout=10000);p.wait_for_timeout(200)
    ok("removed: back to Plan coming Sunday, nothing else touched",not (ls(p,"wo_weeks") or {}) and p.locator("#week button.day").first.inner_text().endswith("Soon") and ls(p,"wo_ver")==12)
    c.close()
    # a bad stored week never breaks the app
    c,p=view(b,"2026-11-07",seed={"wo_weeks":{"2027-01-04":{"v":1,"week":"2027-01-04","sess":{},"days":{}}}})
    ok("a broken stored week is skipped and reported, the app still opens",p.locator("#sess h2").count()>3 and p.evaluate("()=>__app.WEEKS['2027-01-04'].errors.length")>0 and not errs,errs)
    c.close();b.close()
exit(done())
