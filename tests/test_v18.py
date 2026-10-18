import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
import datetime as dt, re
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
CTX=[]
def page(b,t):
    if not CTX: CTX.append(b.new_context(viewport={"width":390,"height":844},service_workers="block"))
    p=CTX[0].new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda d:d.accept());p.clock.install(time=t);p.goto(URL);return p
def opend(p,d):
    if p.locator('#panel.open').count(): p.click('#close')
    p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(250)
NEW=["easyrun12","strA","row","mob","strB","kb","walk"]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    p=page(b,dt.datetime(2026,10,12,9,0))
    p.evaluate("""()=>{localStorage.clear();localStorage.setItem('wo_startdate','"2026-10-10"');localStorage.setItem('wo_ver','12');
     localStorage.setItem('wo_wt',JSON.stringify({'goblet-squat':{'2026-10-10':'18'},'farmers-carry':{'2026-10-10':'22'},'cs-row':{'2026-10-10':'16'}}));}""");p.reload()
    # ---- data checks: timings and switch time
    D=p.evaluate("""()=>{var S=__how.SESS,o={};%s.forEach(function(k){var s=S[k];o[k]={tot:s.tot,blocks:s.blocks.map(function(b){var t=b.timer||b;return{h:b.h||b.k,k:b.k,mode:b.mode||'',segs:t.segs||[],list:!!b.list}})}});return o;}""" % str(NEW))
    for k,s in D.items():
        m=s["tot"]/60
        ok(f"{k} total {m:.1f} min within 15-38",(15<=m<=38) if k=="mob" else (30<=m<=38),m)
        for bl in s["blocks"]:
            g=bl["segs"]
            if len(g)<2: continue
            bad=[i for i in range(1,len(g)) if g[i][0] not in("READY","REST") and g[i-1][0] not in("READY","REST")]
            if bl["h"] in("Intervals","Conditioning finisher"): bad=[i for i in bad if not(g[i][0]=="REST" or g[i-1][0]=="WORK")]  # steady/easy alternation on same machine is fine
            if bl["list"]: bad=[]  # flows: GET READY only on position change (checked in test_v25)
            bad=[i for i in bad if "switch → right side" not in str(g[i][2])]
            ok(f"{k}/{bl['h']} switch time before every move",not bad,bad[:3])
            if bl["list"]: ok(f"{k}/{bl['h']} 10 s ready on position changes",all(x[1]>=10 for x in g if x[0]=="READY"))
    sa=D["strA"]["blocks"][1]["segs"];ok("every 2:00 rounds = 120 s",all(sum(x[1] for x in sa[i:i+5])==120 for i in (0,5,10)),[x[1] for x in sa])
    kb=D["kb"]["blocks"][2]["segs"];st=[kb[i:i+3] for i in range(0,len(kb),3)]
    ok("Sat every 75 s = ready+work+rest, 20 s before farmers, no trailing rest",all(sum(x[1] for x in q)==75 for q in st[:-1]) and st[3][0][1]==20 and kb[-1][0]=="WORK" and len(kb)==35,[x[:2] for x in kb[:8]])
    wi=D["row"]["blocks"][2]["segs"];ok("row intervals 5 s ready, no trailing rest",wi[0]==["READY",5,wi[0][2]] and len(wi)==17 and wi[-1][0]=="WORK")
    ok("Sun walk 25:00",D["walk"]["blocks"][1]["segs"][0][1]==1500)
    ok("Thu 15:00",sum(x[1] for x in D["mob"]["blocks"][1]["segs"])==900)
    # ---- strip + rendering
    pl=lambda d:p.locator(f'button.day[data-d="{d}"] .pl').inner_text()
    exp={"2026-10-12":"Run","2026-10-13":"Upper","2026-10-14":"Row","2026-10-15":"Mobility","2026-10-16":"Lower","2026-10-17":"KB","2026-10-18":"Walk"}
    ok("week strip names",all(pl(d)==v for d,v in exp.items()))
    p.click("#prev");ok("Sat 10 / Sun 11 unchanged",pl("2026-10-10")=="Pump" and pl("2026-10-11")=="Run");p.click("#next")
    p.click("#next");ok("19 Oct Soon",pl("2026-10-19")=="Soon");opend(p,"2026-10-19");ok("Plan coming Sunday","Plan coming Sunday" in p.locator("#sess").inner_text());p.click("#close");p.click("#prev")
    for d,(t,c) in {"2026-10-12":("Easy Run","c_rmain"),"2026-10-13":("Strength A","c_aemom"),"2026-10-14":("Rower","c_wiv"),"2026-10-15":("Mobility","c_mob"),"2026-10-16":("Strength B","c_bemom"),"2026-10-17":("KB + Carry","c_kcirc"),"2026-10-18":("Long Walk","c_swalk")}.items():
        opend(p,d);ok(f"{d} renders {t}",t in p.locator("#ttl").inner_text() and p.locator("#"+c).count()==1)
        hs=p.locator("#sess h2").all_inner_texts();tot=sum(int(m.group(1))*60+int(m.group(2)) for x in hs for m in [re.search(r"(\d+):(\d\d)$",x)] if m)
        mins=int(re.search(r"(\d+) min",p.locator("#dnote").inner_text()).group(1));ok(f"{d} labelled block times add up to header total",abs(tot/60-mins)<1,(tot,mins))
    opend(p,"2026-10-13")
    ok("compact: cue/Last hidden until More",not p.locator('.card[data-x="cs-row"] .mx').is_visible() and "Last: 16 kg (Sat 10 Oct)" in p.locator('.card[data-x="cs-row"]').text_content())
    hts=p.evaluate("[...document.querySelectorAll('#sess .card.ex')].map(c=>c.getBoundingClientRect().height)");ok("cards compact <=190px",max(hts)<=190,hts)
    ok("tempo chip + meaning per move",p.locator('.card[data-x="incline-db-press"] .chip').inner_text()=="3011" and p.locator('.card[data-x="incline-db-press"] .tm').inner_text()=="3 s down · 1 s up · 1 s hold")
    ok("4 pills with default reps",p.locator('.card[data-x="incline-db-press"] .pill').all_inner_texts()==["6"]*4)
    p.click('.card[data-x="cs-row"] .more');ok("More shows cue + How to",p.locator('.card[data-x="cs-row"] .mx').is_visible() and p.locator('.card[data-x="cs-row"] .how').is_visible())
    ok("warm-up collapsed",p.locator("#c_awu .lst").count()==0 and "Show 5 moves" in p.locator("#c_awu").inner_text())
    p.click('#c_awu [data-sm]');ok("show moves list",p.locator("#c_awu .lst li").count()==5)
    p.locator("#c_awu .mv").first.click();ok("tap move name opens how-to",p.locator("#hs.show").count()==1);p.click("#hs_x")
    opend(p,"2026-10-16");ok("Fri goblet Last","Last: 18 kg" in p.locator('.card[data-x="goblet-squat"]').text_content())
    opend(p,"2026-10-17");ok("Sat farmers Last + 3 rounds in metres","Last: 22 kg" in p.locator('.card[data-x="farmers-carry"]').text_content() and p.locator('.card[data-x="farmers-carry"] .pill').all_inner_texts()==["30m"]*3)
    p.click("#close");p.click("#ed");p.click('button.day[data-d="2026-10-13"]');ok("edit Tue -> Rest",pl("2026-10-13")=="Rest");p.click('button.day[data-d="2026-10-13"]');ok("edit back",pl("2026-10-13")=="Upper");p.click("#ed")
    opend(p,"2026-10-15");ok("Thu recovery + flow","Recovery day" in p.locator("#sess").inner_text() and "Show 8 moves" in p.locator("#c_mob").inner_text() and p.locator("#pct").inner_text()=="–")
    p.close()
    # ---- Tuesday as today: reps, timers, finish
    p=page(b,dt.datetime(2026,10,13,18,0));opend(p,"2026-10-13")
    ok("cs-row prefilled 16",p.locator('.card[data-x="cs-row"] input').input_value()=="16")
    k0=p.locator('.card[data-x="incline-db-press"] .pill').nth(0).get_attribute("data-k")
    p.locator('.card[data-x="incline-db-press"] .pill').nth(0).click();ok("tap pill = done + stepper",ls(p,"wo_2026-10-13")["t"][k0] and ls(p,"wo_2026-10-13")["rp"][k0]==6 and p.locator(".step").count()==1)
    p.click('[data-st="-1"]');ok("minus to 5",ls(p,"wo_2026-10-13")["rp"][k0]==5 and "5 reps" in p.locator("#stv").inner_text())
    p.screenshot(path="test-output/app-v18-c.png")
    p.click('[data-st="x"]');ok("OK closes stepper, pill shows ✓ 5",p.locator(".step").count()==0 and p.locator('.card[data-x="incline-db-press"] .pill').nth(0).inner_text()=="✓ 5")
    for i in (1,2):p.locator('.card[data-x="incline-db-press"] .pill').nth(i).click();p.click('[data-st="x"]')
    p.locator('.card[data-x="incline-db-press"] [data-a]').click();p.locator('.card[data-x="incline-db-press"] input').fill("14")
    p.locator('.card[data-x="incline-db-press"] .pill').nth(1).click();p.click('[data-st="-1"]');p.click('[data-st="-1"]');ok("edit done set again",ls(p,"wo_2026-10-13")["rp"][p.locator('.card[data-x="incline-db-press"] .pill').nth(1).get_attribute("data-k")]==4);p.click('[data-st="x"]')
    p.locator('.card[data-x="cs-row"] .pill').nth(0).click();p.click('[data-st="u"]');ok("undo unticks",not ls(p,"wo_2026-10-13")["t"].get(p.locator('.card[data-x="cs-row"] .pill').nth(0).get_attribute("data-k")))
    # every 2:00 timer
    p.click('[data-t="aemom"]');p.wait_for_timeout(60)
    ok("guided controls shown",all(p.locator(x).is_visible() for x in ("#tpause","#tback","#tnext","#stop")))
    ok("GET READY first with Next",p.locator("#ph").inner_text()=="GET READY" and "Next: A1 Incline dumbbell press" in p.locator("#sub").inner_text() and p.locator("#time").inner_text()=="0:10")
    p.clock.run_for(10500);p.wait_for_timeout(60);ok("WORK shows Now · Next",p.locator("#ph").inner_text()=="WORK" and "Next: A2 Incline prone Y-raise" in p.locator("#sub").inner_text(),p.locator("#sub").inner_text())
    p.clock.run_for(35000);p.wait_for_timeout(60);ok("15 s switch before A2",p.locator("#ph").inner_text()=="GET READY" and p.locator("#time").inner_text()=="0:15")
    p.evaluate("window.scrollTo(0,0)");p.screenshot(path="test-output/app-v18-b.png")
    p.clock.run_for(45000);p.wait_for_timeout(60);ok("rest after A2 then next round",p.locator("#ph").inner_text()=="REST" and "Next: A1" in p.locator("#sub").inner_text())
    p.click("#stop")
    ok("superset has no guided timer",p.locator('[data-t="asb"]').count()==0)
    for x in ("cs-row","hk-db-press"):
        p.locator(f'.card[data-x="{x}"] .pill').nth(0).click()
        if p.locator(".step").count(): p.click('[data-st="x"]')
    ok("rest bar 1:15 after last move of round, with filler",p.locator("#rbar.show").count()==1 and p.locator("#rtime").inner_text()=="1:15" and "hip flexor" in p.locator("#rlab").inner_text(),p.locator("#rlab").inner_text())
    p.click("#rskip");ok("skip hides rest bar",p.locator("#rbar.show").count()==0)
    p.click("#fin");p.clock.fast_forward(1000);e=ls(p,"wo_log")[-1]
    ok("log has reps per set",e["rp"]["incline-db-press"]["v"]==[5,4,6,"–"] and e["wt"]["incline-db-press"]=="14",e.get("rp"))
    ok("finish summary rep line","Incline dumbbell press 14 kg · 5/4/6/–" in p.locator("#o_d").inner_text(),p.locator("#o_d").inner_text())
    p.click("#o_done");ok("history rep line","Incline dumbbell press 14 kg · 5/4/6/–" in p.locator("#hist").text_content())
    p.close()
    # ---- Wed + Sat + Thu timers
    p=page(b,dt.datetime(2026,10,14,7,0));opend(p,"2026-10-14")
    p.click('[data-t="wiv"]');p.wait_for_timeout(60);ok("row 5 s ready",p.locator("#ph").inner_text()=="GET READY" and p.locator("#time").inner_text()=="0:05")
    p.clock.run_for(5500);p.wait_for_timeout(60);ok("row interval work","Interval 1/6" in p.locator("#sub").inner_text() and p.locator("#ph").inner_text()=="WORK")
    p.clock.run_for(60000);p.wait_for_timeout(60);ok("row easy","light paddle 18–20 s/m" in p.locator("#sub").inner_text())
    p.clock.run_for(700000);p.wait_for_timeout(100);ok("intervals done",ls(p,"wo_2026-10-14")["s"].get("wiv")==1)
    cs=lambda sel,prop:p.locator(sel).first.evaluate(f"e=>getComputedStyle(e).{prop}")
    ok("orange accent",cs(".btn","backgroundColor")=="rgb(255, 138, 61)" and cs(".day.today","borderColor")=="rgb(255, 138, 61)")
    p.fill("#r_d","2800");ok("row distance saved",ls(p,"wo_run_2026-10-14")["d"]=="2800");p.close()
    p=page(b,dt.datetime(2026,10,17,9,0));opend(p,"2026-10-17");p.click('[data-t="kcirc"]');p.wait_for_timeout(60)
    ok("EMOM ready 15 then swing",p.locator("#time").inner_text()=="0:15" and "B1 Kettlebell swing" in p.locator("#sub").inner_text())
    p.clock.run_for(15500);p.wait_for_timeout(60);ok("swing 35 s work, next rest",p.locator("#time").inner_text() in("0:35","0:34") and "Next: Rest" in p.locator("#sub").inner_text(),(p.locator("#time").inner_text(),p.locator("#sub").inner_text()))
    p.click("#stop");p.locator('.card[data-x="farmers-carry"] .pill').nth(0).click();p.click('[data-st="1"]');ok("metres step +5",ls(p,"wo_2026-10-17")["rp"][p.locator('.card[data-x="farmers-carry"] .pill').nth(0).get_attribute("data-k")]==35 and ls(p,"wo_wt")["farmers-carry"].get("2026-10-17")=="22")
    p.close()
    p=page(b,dt.datetime(2026,10,15,9,0));opend(p,"2026-10-15");p.click('[data-t="mob"]');p.wait_for_timeout(60)
    ok("flow starts with 10 s ready",p.locator("#ph").inner_text()=="GET READY" and "Shoulder CARs · left side" in p.locator("#sub").inner_text(),p.locator("#sub").inner_text())
    p.clock.run_for(70500);p.wait_for_timeout(60);ok("side switch cued",p.locator("#ph").inner_text()=="SWITCH SIDES" and "right side" in p.locator("#sub").inner_text())
    p.clock.run_for(900000);p.wait_for_timeout(100);ok("flow done",ls(p,"wo_2026-10-15")["s"].get("mob")==1);p.close()
    # ---- how-to coverage
    p=page(b,dt.datetime(2026,10,13,9,0))
    miss=p.evaluate("""()=>{var H=window.__how,m=[];Object.keys(H.X).forEach(function(k){var h=H.HT[k];if(!h||!h.u||h.s.length<3||h.s.length>5||h.c.length<2||h.c.length>3||!h.m||h.s.some(function(x){return x.split(/\\s+/).length>12;}))m.push(k);});
      Object.keys(H.SESS).forEach(function(sk){H.SESS[sk].blocks.forEach(function(b){(b.list||[]).forEach(function(x){if(!H.HT[H.hkey(x)])m.push(sk+':'+x);});});});return m;}""")
    ok("every exercise/move has how-to",not miss,miss)
    opend(p,"2026-10-16");p.click('.card[data-x="db-rdl"] .more');p.locator('.card[data-x="db-rdl"] .how').click();p.wait_for_timeout(300)
    ok("sheet + demo link",p.locator("#hs.show").count()==1 and p.locator("#hs_l").get_attribute("href")=="https://www.youtube.com/results?search_query=dumbbell+romanian+deadlift+how+to")
    p.click("#hs_x");ok("sheet closes",p.locator("#hs.show").count()==0)
    opend(p,"2026-10-13");p.screenshot(path="test-output/app-v18-a.png");p.close()
    ok("no page errors",not errs,errs)
    print(f"{sum(res)}/{len(res)} passed")
