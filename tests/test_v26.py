import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v26: Sat 17 Oct quick option "15-min KB Flow (16 kg)"
import datetime as dt, re
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
def ls(p,k): return p.evaluate("k=>JSON.parse(localStorage.getItem(k)||'null')",k)
SEED="""()=>{localStorage.clear();localStorage.setItem('wo_startdate','"2026-10-10"');localStorage.setItem('wo_ver','12');}"""
HOOK="window.__bp=[];window.__vib=0;try{navigator.vibrate=function(){window.__vib++;return true}}catch(e){}"
def sec(s): m=re.search(r"(\d+):(\d\d)",s); return int(m.group(1))*60+int(m.group(2)) if m else -1
Q="15-min KB Flow (16 kg)"
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block");c.add_init_script(HOOK)
    p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda d:d.accept());p.clock.install(time=dt.datetime(2026,10,17,19,30));p.goto(URL)
    p.evaluate(SEED);p.reload();p.wait_for_timeout(200)
    if not p.locator("#panel.open").count(): p.click('button.day[data-d="2026-10-17"]');p.wait_for_timeout(250)
    ok("main unchanged by default",p.locator("#ttl").inner_text()=="KB + Carry Flow")
    ok("backup toggle unchanged",p.locator("#alt").is_visible() and "Dumbbell Flow" in p.locator("#alt").inner_text())
    ok("quick option button next to backup",p.locator("#qk").is_visible() and p.locator("#qk").inner_text()=="Quick option: "+Q,p.locator("#qk").inner_text())
    p.click("#qk");p.wait_for_timeout(200)
    ok("quick session shown",p.locator("#ttl").inner_text()==Q and ls(p,"wo_quick")=={"2026-10-17":1})
    ok("button flips to back to main",p.locator("#qk").inner_text().startswith("↩ Back to main"))
    ok("header 15 min","15 min" in p.locator("#dnote").inner_text(),p.locator("#dnote").inner_text())
    hs=p.locator("#sess h2").all_inner_texts();ts=[sec(h.split("·")[-1]) for h in hs]
    ok("blocks 3:00 + 9:40 + 2:20 = 15:00 exactly",ts==[180,580,140] and sum(ts)==900,hs)
    S=p.evaluate("()=>{var S=__how.SESS.kbq17;return{tot:S.tot,b:S.blocks.map(function(b){return{id:b.id,segs:b.segs,list:b.list}})}}")
    ok("SESS total 900 s",S["tot"]==900)
    for bl in S["b"]:
        g=bl["segs"]
        ok(f"{bl['id']} no trailing rest",g[-1][0] not in("REST","READY"))
        ok(f"{bl['id']} sides cued",not [x for x in g if re.search("each side|per side",x[2])] and any("switch → right side" in x[2] for x in g))
    mn=S["b"][1]["segs"];w=[x for x in mn if x[0]=="WORK"]
    ok("main = 5 rounds of 45 s left + 45 s right, 20 s rest",len(w)==10 and all(x[1]==45 for x in w) and [x[1] for x in mn if x[0]=="REST"]==[20]*4)
    ok("every round is 2:00 except last",all(sum(x[1] for x in mn[i*4:i*4+4])==120 for i in range(4)))
    txt=p.locator("#sess").inner_text()+" "+p.locator("#safe1").inner_text()+" "+" ".join(" ".join(x[2] for x in bl["segs"]) for bl in S["b"])+" "+" ".join(" ".join(bl["list"]) for bl in S["b"])
    ok("one 16 kg bell, no second implement",not re.search(r"dumbbell|barbell|two bells|bench|\b(20|24|12) kg",txt,re.I),re.findall(r"dumbbell|barbell|bench",txt,re.I))
    ok("no snatch / head-down / breath-hold",not re.search(r"snatch|head-down|inver|hold your breath(?! )",txt.replace("never hold your breath",""),re.I))
    ok("RPE 6–7 + single effort words","RPE 6–7" in txt and not re.search(r"(easy|steady|moderate|hard)[- ](easy|steady|moderate|hard)",txt,re.I))
    ok("no numeric paces",not re.search(r"min/km|km/h|/500|drag factor|s/m",txt))
    ok("stop signs shown",p.locator(".safe .stop").is_visible() and "headache" in p.locator(".safe .stop").inner_text())
    # How-to for every move in every block
    for bid in ("q17wu","q17a","q17fin"):
        sm=p.locator(f"#c_{bid} [data-sm]")
        if sm.count(): sm.click();p.wait_for_timeout(80)
        n=len(S["b"][["q17wu","q17a","q17fin"].index(bid)]["list"]);mv=p.locator(f"#c_{bid} .mv")
        ok(f"{bid} every move has a How-to ({n})",mv.count()==n,mv.count())
        for i in range(mv.count()):
            mv.nth(i).click();p.wait_for_timeout(60);good=p.locator("#hs.show").count()==1 and len(p.locator("#hs").inner_text())>60
            if not good: ok(f"{bid} how-to {i}",False,mv.nth(i).inner_text())
            p.click("#hs_x");p.wait_for_timeout(40)
    ok("flow card: short line + grouped rounds expanded",p.locator("#c_q17a .note").inner_text()=="Each round: 45 s left · 45 s right · 20 s rest. RPE 6–7." and p.locator("#c_q17a .rgh").all_inner_texts()==["ROUNDS 1 · 3 · 5 each side","ROUNDS 2 · 4 each side"] or [x.lower() for x in p.locator("#c_q17a .rgh").all_inner_texts()]==["rounds 1 · 3 · 5 each side","rounds 2 · 4 each side"],p.locator("#c_q17a .rgh").all_inner_texts())
    ok("no repeated 'rounds' per move, no hidden list",p.locator("#c_q17a [data-sm]").count()==0 and "rounds 1, 3, 5" not in p.locator("#c_q17a").inner_text())
    p.locator('#sess [data-t="q17a"]').click();p.wait_for_timeout(60);ok("Now/Next shows round moves + reps","Swing ×5, Clean ×3, Press ×3" in p.locator("#sub").inner_text(),p.locator("#sub").inner_text())
    p.clock.run_for(100500);p.wait_for_timeout(60);ok("rest shows next round moves","Front-rack squat ×4, Row ×6" in p.locator("#sub").inner_text(),p.locator("#sub").inner_text());p.click("#stop")
    # guided timer through each block
    for bid in ("q17wu","q17a","q17fin"):
        p.evaluate("()=>{window.__bp=[]}");p.locator(f'#sess [data-t="{bid}"]').click();p.wait_for_timeout(50)
        ok(f"{bid} controls",all(p.locator(x).is_visible() for x in ("#tpause","#tback","#tnext","#stop")))
        t0=sec(p.locator("#time").inner_text());p.clock.run_for(3000);t1=sec(p.locator("#time").inner_text());ok(f"{bid} counts down",t1<t0,(t0,t1))
        segs=ls(p,"wo_timer")["segs"];sw=False
        for i in range(sum(x[1] for x in segs)+3):
            p.clock.run_for(1000)
            if i%5==0 and p.locator("#bar.show").count() and p.locator("#ph").inner_text()=="SWITCH SIDES": sw=True
        ok(f"{bid} switch-sides cue shown",sw)
        ok(f"{bid} beeps each segment",p.evaluate("window.__bp.length")>=len(segs))
        ok(f"{bid} logged done",ls(p,"wo_2026-10-17")["s"].get(bid)==1)
    ok("no vibrate",p.evaluate("window.__vib")==0)
    # persistence
    p.reload();p.wait_for_timeout(200)
    if not p.locator("#panel.open").count(): p.click('button.day[data-d="2026-10-17"]');p.wait_for_timeout(250)
    ok("saved per day across reload",p.locator("#ttl").inner_text()==Q)
    # log
    p.click("#fin");p.clock.fast_forward(1000);p.wait_for_timeout(200)
    e=ls(p,"wo_log")[-1];ok("logs under own name + type",e["name"]==Q and e["type"]=="quick" and e["sid"]=="kbq17",e)
    ok("summary name",p.locator("#o_n").inner_text()==Q);p.click("#o_done");p.wait_for_timeout(100)
    p.click("#close");ok("strip says KB 15",p.locator('button.day[data-d="2026-10-17"] .pl').inner_text()=="KB 15")
    p.evaluate("()=>document.querySelector('details').open=true")
    ok("history shows quick name",Q in p.locator("#hist li").first.inner_text())
    opts=p.locator('#hist select[data-hd="2026-10-17"] option').evaluate_all("o=>o.map(x=>x.value+'|'+x.textContent)")
    ok("history Edit has 4 options incl quick",[o.split("|")[0] for o in opts]==["main","backup","run","quick"] or [o.split("|")[0] for o in opts]==["main","backup","quick"],opts)
    p.select_option('#hist select[data-hd="2026-10-17"]',"main");p.wait_for_timeout(150);e=ls(p,"wo_log")[-1]
    ok("edit to Main",e["name"]=="KB + Carry Flow" and e["type"]=="main" and not (ls(p,"wo_quick") or {}).get("2026-10-17"),e)
    p.select_option('#hist select[data-hd="2026-10-17"]',"backup");p.wait_for_timeout(150);e=ls(p,"wo_log")[-1]
    ok("edit to Backup",e["type"]=="backup" and "Dumbbell" in e["name"],e)
    p.select_option('#hist select[data-hd="2026-10-17"]',"quick");p.wait_for_timeout(150);e=ls(p,"wo_log")[-1]
    ok("edit back to quick",e["name"]==Q and e["type"]=="quick" and ls(p,"wo_quick").get("2026-10-17") and not (ls(p,"wo_alt") or {}).get("2026-10-17"),e)
    ok("one log entry for the day",len([x for x in ls(p,"wo_log") if x["date"]=="2026-10-17"])==1)
    # toggles are exclusive
    p.click('button.day[data-d="2026-10-17"]');p.wait_for_timeout(200);p.click("#alt");p.wait_for_timeout(150)
    ok("backup button from quick → backup",p.locator("#ttl").inner_text().startswith("Backup") and not (ls(p,"wo_quick") or {}).get("2026-10-17"))
    p.click("#qk");p.wait_for_timeout(150);ok("quick from backup → quick, backup off",p.locator("#ttl").inner_text()==Q and not (ls(p,"wo_alt") or {}).get("2026-10-17"))
    p.click("#qk");p.wait_for_timeout(150);ok("back to main",p.locator("#ttl").inner_text()=="KB + Carry Flow")
    p.click("#close");p.click('button.day[data-d="2026-10-16"]');p.wait_for_timeout(200);ok("no quick option on other days",not p.locator("#qk").is_visible())
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
