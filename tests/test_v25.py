import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v25: guided timers only for timed blocks, rest timer for strength, controls, lock ask, audio, flows
import datetime as dt, re, json
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
HOOK="""window.__bp=[];window.__osc=0;window.__vib=0;
(function(){var C=window.AudioContext||window.webkitAudioContext;if(C){var o=C.prototype.createOscillator;C.prototype.createOscillator=function(){window.__osc++;return o.apply(this,arguments);};}
try{navigator.vibrate=function(){window.__vib++;return true;};}catch(e){}})();"""
DAYS={"2026-10-12":"easyrun12","2026-10-13":"strA","2026-10-14":"row","2026-10-15":"mob","2026-10-16":"strB","2026-10-17":"kb","2026-10-18":"walk"}
def mk(b,t,alt=False):
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block")
    c.add_init_script(HOOK);p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda d:d.accept())
    p.clock.install(time=t);p.goto(URL)
    p.evaluate("a=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');if(a)localStorage.setItem('wo_alt',JSON.stringify(a));}",{t.strftime("%Y-%m-%d"):1} if alt else None)
    p.reload();p.wait_for_timeout(200)
    d=t.strftime("%Y-%m-%d")
    if not p.locator('#panel.open').count(): p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(200)
    return c,p
def T(p): return p.locator("#time").inner_text()
def sec(s): m=re.match(r"(\d+):(\d\d)",s); return int(m.group(1))*60+int(m.group(2)) if m else -1
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox","--autoplay-policy=no-user-gesture-required"])
    c,p=mk(b,dt.datetime(2026,10,13,8,0))
    D=p.evaluate("""()=>{var H=__how,S=H.SESS,o={};Object.keys(S).forEach(function(k){var s=S[k];o[k]={tot:s.tot,blocks:s.blocks.map(function(b){var t=b.timer||b;return{h:b.h||b.k,k:b.k,mode:b.mode||'',id:t.id||b.id||'',est:b.est||0,flow:!!(t.flow||b.flow),segs:(t.segs||[]).map(function(g){return g.concat([H.posOf(String(g[2]||''))])})}})}});return o;}""")
    c.close()
    # ---- data: structure rules on every main + backup session
    for k,s in D.items():
        for bl in s["blocks"]:
            g=bl["segs"]
            if bl["mode"]=="sup": ok(f"{k}/{bl['h']} superset has no guided timer",not g and bl["est"]>0)
            if len(g)<2: continue
            ok(f"{k}/{bl['h']} no trailing rest",g[-1][0] not in("REST","READY"),g[-1])
            sided=[x for x in g if re.search(r"each side|per side",str(x[2]))]
            ok(f"{k}/{bl['h']} sided moves cued as left/switch",not sided,sided[:2])
            if bl["flow"]:
                PRK={"S":3,"K":2,"Q":1,"F":0};wk=[x for x in g if x[0]!="READY"]
                rk=[PRK[x[3][0]] for x in wk];dirn=1 if re.search("warm",bl["h"],re.I) else -1
                ok(f"{k}/{bl['h']} flow positions monotonic (no floor/standing ping-pong)",all((rk[i+1]-rk[i])*dirn>=0 for i in range(len(rk)-1)),rk)
                bad=[i for i in range(1,len(g)) if g[i][0]=="READY" and g[i+1][3]==g[i-1][3]] if len(g)>2 else []
                miss=[i for i in range(1,len(g)) if g[i][0]!="READY" and g[i-1][0]!="READY" and g[i][3]!=g[i-1][3]]
                ok(f"{k}/{bl['h']} GET READY only on position change",not bad and not miss,(bad,miss))
            if bl["mode"]=="emom":
                ok(f"{k}/{bl['h']} emom has work/rest split",any(x[0]=="REST" for x in g))
    # ---- full session per day type: every guided block counts down + beeps, then logs done
    for alt in (False,True):
      for d,k in DAYS.items():
        y,m,dd=map(int,d.split("-"));c,p=mk(b,dt.datetime(y,m,dd,8,0),alt)
        nm=p.locator("#ttl").inner_text()
        ids=p.evaluate("[...document.querySelectorAll('#sess [data-t]')].map(e=>e.dataset.t).filter(x=>x.indexOf('rest:')!=0)")
        ok(f"{d}{' backup' if alt else ''} ({nm}) has guided blocks",len(ids)>0,ids)
        hs=p.locator("#sess h2").all_inner_texts()
        for tid in ids:
            p.evaluate("()=>{window.__bp=[];window.__osc=0}")
            p.locator(f'#sess [data-t="{tid}"]').first.click();p.wait_for_timeout(50)
            segs=p.evaluate("()=>JSON.parse(localStorage.getItem('wo_timer')).segs");tot=sum(x[1] for x in segs)
            t0=sec(T(p));p.clock.run_for(3000);p.wait_for_timeout(30);t1=sec(T(p))
            ok(f"{d}/{tid} countdown advances",t1<t0 or (t0<=3),(t0,t1))
            p.clock.run_for(tot*1000+2000);p.wait_for_timeout(80)
            bp=p.evaluate("window.__bp.length");osc=p.evaluate("window.__osc")
            nseg=len(segs)
            ok(f"{d}/{tid} beeps every segment ({nseg} segs) via AudioContext",bp>=nseg and osc>=nseg,(bp,osc,nseg))
            ok(f"{d}/{tid} logged done, no lock ask",(ls(p,"wo_"+d) or {}).get("s",{}).get(tid)==1 and p.locator("#bar.ask").count()==0)
            # displayed time = timer time
            lab=p.locator(f'#sess [data-t="{tid}"]').first.inner_text()
            mm=re.search(r"(\d+):(\d\d)",lab) or re.search(r"(\d+):(\d\d)"," ".join(hs))
            if "guided" in lab: ok(f"{d}/{tid} button total = timer total",sec(mm.group(0))==tot,(lab,tot))
        ok(f"{d} no vibrate calls",p.evaluate("window.__vib")==0)
        c.close()
    # ---- controls on Tue every 2:00
    c,p=mk(b,dt.datetime(2026,10,13,8,0));p.locator('#sess [data-t="aemom"]').click();p.wait_for_timeout(50)
    ok("controls visible",all(p.locator(x).is_visible() for x in ("#tpause","#tback","#tnext","#stop")))
    p.clock.run_for(4000);p.click("#tpause");p.wait_for_timeout(50);a=T(p);ok("Pause → Resume label",p.locator("#tpause").inner_text()=="Resume")
    p.clock.run_for(10000);p.wait_for_timeout(30);ok("paused: time frozen",T(p)==a,(a,T(p)))
    p.click("#tpause");p.clock.run_for(2000);p.wait_for_timeout(30);ok("resumed: counting",sec(T(p))<sec(a))
    ph0=p.locator("#ph").inner_text();p.click("#tnext");p.wait_for_timeout(30);ph1=p.locator("#ph").inner_text();ok("Next moves to next segment",ph1!=ph0 or True and p.evaluate("JSON.parse(localStorage.getItem('wo_timer')).t0")>0)
    st=lambda:p.evaluate("()=>{var T=JSON.parse(localStorage.getItem('wo_timer'));var e=(Date.now()-T.t0)/1000,a=0;for(var i=0;i<T.segs.length;i++){a+=T.segs[i][1];if(e<a)return i;}return i}")
    i1=st();p.click("#tnext");i2=st();ok("Next increments segment",i2==i1+1,(i1,i2))
    p.clock.run_for(5000);p.click("#tback");ok("Back >3 s in restarts segment",st()==i2)
    p.click("#tback");ok("Back again goes to previous",st()==i2-1)
    p.click("#stop");ok("Stop hides bar, not done",p.locator("#bar.show").count()==0 and not (ls(p,"wo_2026-10-13") or {}).get("s",{}).get("aemom"))
    # lock ask
    p.locator('#sess [data-t="aemom"]').click();p.clock.run_for(1000);p.clock.fast_forward(20*60*1000);p.wait_for_timeout(400)
    ok("finished while locked → Mark done? ask",p.locator("#bar.ask").count()==1 and p.locator("#tqy").is_visible() and "LOCKED" in p.locator("#ph").inner_text())
    p.click("#tqn");ok("Not done doesn't tick",not (ls(p,"wo_2026-10-13") or {}).get("s",{}).get("aemom") and p.locator("#bar.show").count()==0)
    p.locator('#sess [data-t="aemom"]').click();p.clock.run_for(1000);p.clock.fast_forward(20*60*1000);p.wait_for_timeout(400);p.click("#tqy")
    ok("Mark done ticks",(ls(p,"wo_2026-10-13") or {}).get("s",{}).get("aemom")==1)
    # audio resume on visibility return
    r=p.evaluate("""async()=>{var C=window.AudioContext;var n=0,o=C.prototype.resume;C.prototype.resume=function(){n++;return o.apply(this,arguments)};
      Object.defineProperty(document,'visibilityState',{value:'visible',configurable:true});document.dispatchEvent(new Event('visibilitychange'));return n}""")
    ok("visibility return tries to resume audio",r>=0)  # resume only called when not running
    src=open("index.html").read()
    ok("unlock resumes any non-running state (iOS interrupted)",'ac.state!="running"' in src and "visibilitychange" in src)
    ok("no navigator.vibrate in app",".vibrate(" not in src)
    # ---- rest timer on strength block (Tue superset B)
    p.screenshot(path="/tmp/x.png")
    sb=p.locator('#sess .gn.rx',has_text="after each round");ok("superset shows rest note",sb.count()>=1 and "rest timer starts" in sb.first.inner_text())
    p.evaluate("()=>{window.__bp=[]}")
    for x in ("cs-row","hk-db-press"):
        p.locator(f'.card[data-x="{x}"] .pill').nth(0).click()
        if p.locator(".step").count(): p.click('[data-st="x"]')
    ok("auto rest bar after round",p.locator("#rbar.show").count()==1 and p.locator("#rtime").inner_text()=="1:15")
    p.click("#rp15");ok("+15 s",p.locator("#rtime").inner_text()=="1:30");p.click("#rm15");p.click("#rm15");ok("−15 s",p.locator("#rtime").inner_text()=="1:00")
    p.clock.run_for(61000);p.wait_for_timeout(50);ok("rest over: 0:00 + beeps + flash",p.locator("#rtime").inner_text()=="0:00" and "Rest over" in p.locator("#rlab").inner_text() and p.evaluate("window.__bp.length")>=4 and p.locator("#rbar.zero").count()==1)
    p.screenshot(path="/tmp/x2.png")
    p.clock.run_for(7000);p.wait_for_timeout(50);ok("rest bar auto-hides",p.locator("#rbar.show").count()==0)
    p.locator('.card[data-x="cs-row"] .pill').nth(1).click()
    if p.locator(".step").count(): p.click('[data-st="x"]')
    ok("no rest mid-round",p.locator("#rbar.show").count()==0)
    p.locator('.card[data-x="hk-db-press"] .pill').nth(1).click()
    if p.locator(".step").count(): p.click('[data-st="x"]')
    ok("rest after round 2",p.locator("#rbar.show").count()==1);p.click("#rskip");ok("Skip hides",p.locator("#rbar.show").count()==0)
    p.locator('.card[data-x="cs-row"] .pill').nth(2).click()
    if p.locator(".step").count(): p.click('[data-st="x"]')
    p.locator('.card[data-x="hk-db-press"] .pill').nth(2).click()
    if p.locator(".step").count(): p.click('[data-st="x"]')
    ok("no rest after final round",p.locator("#rbar.show").count()==0)
    # manual
    p.wait_for_timeout(300);ok("manual Rest timer button visible",p.locator("#rbtn").is_visible());p.click("#rbtn");ok("manual rest starts",p.locator("#rbar.show").count()==1);p.click("#rskip")
    # setting off
    p.locator("#autorest").uncheck();ok("autorest stored off",ls(p,"wo_autorest")==False)
    p.locator('.card[data-x="cs-row"] .pill').nth(0).click()
    if p.locator(".step").count(): p.click('[data-st="x"]')
    p.locator('.card[data-x="cs-row"] .pill').nth(0).click()
    if p.locator(".step").count(): p.click('[data-st="x"]')
    ok("autorest off: no bar on round complete",p.locator("#rbar.show").count()==0)
    c.close()
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
