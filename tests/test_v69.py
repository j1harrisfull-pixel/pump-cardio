# pc-v69: the system pass. Contrast, names and overflow on every screen and sheet in light and dark, one SVG icon set (no
# glyphs or emoji as controls), design tokens, focus handling for sheets, reduced motion, 120% text and four screen sizes.
import sys
from playwright.sync_api import sync_playwright
from lib import *
from audit69 import AUD
L=[{"date":"2026-11-09","name":"Upper · Slow Is Strong","type":"main","min":30,"sub":"Easy 5km","plan":"Upper · Slow Is Strong","act":"run","km":"5","time":"30:27","effort":"easy","oc":"modified","sid":"upb0911"},
   {"date":"2026-11-11","name":"Hill Hunter Run","type":"main","min":38,"km":"6.4","time":"38:12","effort":"steady","sid":"hill1111","feel":"6"}]
for x in ["goblet-squat","db-rdl"]:
    for d,kg in (("2026-11-03","16"),("2026-11-10","18")):
        L.append({"date":d,"name":"Lower","type":"main","min":40,"sets":3,"of":3,"sid":"x","wt":{x:kg},"rp":{x:{"v":["7","7","7"],"u":"","k":[kg,kg,kg]}}})
L.sort(key=lambda e:e["date"])
def run(b,scheme):
    out={}
    def A(name,p):
        r=p.evaluate(AUD);out[name]=r
    c,p=tabs_app(b,"2026-11-12",{"wo_log":L},scheme=scheme);A("today",p)
    p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(250);A("week",p)
    p.click("#ed2");p.wait_for_timeout(250);A("week-edit",p);p.click("#ed")
    p.click('#tabbar [data-tab="prog"]');p.wait_for_timeout(250);A("progress",p)
    p.locator("#hist .hmore").first.click();p.wait_for_timeout(250);A("actions-sheet",p);p.click("#acs .acx");p.click("#bknow");p.wait_for_timeout(250);A("export-sheet",p);p.click(".exx")
    p.locator(".xcard").first.click();p.wait_for_timeout(250);A("xhist-sheet",p);p.click(".xhx")
    p.click('#tabbar [data-tab="today"]');p.wait_for_timeout(200);p.click("#cog");p.wait_for_timeout(250);A("settings",p);p.click("#imp");p.wait_for_timeout(250);A("import",p);p.click(".imx")
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);A("session",p)
    p.click("[data-tqx]");p.evaluate("()=>document.querySelector('.more').click()");p.wait_for_timeout(200);A("session-more",p)
    p.locator("#sess .mvn").first.click();p.wait_for_timeout(300);A("howto",p);p.click("#hs_x")
    x=p.evaluate("()=>document.querySelector('.srow').dataset.x");tick(p,x,0);p.wait_for_timeout(200);A("session-ticked",p)
    p.locator("#sess [data-t]").first.click();p.clock.run_for(14000);p.wait_for_timeout(300);A("clock",p)
    p.click("#stop");p.wait_for_timeout(150);A("clock-stop",p);p.click("#stqn");p.click("#tlock");p.wait_for_timeout(150);A("clock-locked",p);p.click("#tlock");p.click("#stop");p.click("#stqy");p.wait_for_timeout(200)
    fin(p);p.wait_for_timeout(300);A("saved-card",p);p.click("#o_done");p.wait_for_timeout(300);c.close()
    c,p=tabs_app(b,"2026-11-11",{"wo_log":L[:1]},scheme=scheme);p.click('#home [data-hm="else"]');p.wait_for_timeout(300);A("else-form",p);c.close()
    c,p=tabs_app(b,"2026-11-10",{"wo_log":L[:1]},scheme=scheme);A("today-rest",p);c.close()
    return out

with sync_playwright() as pw:
    b=launch(pw)
    for sch in ("light","dark"):
        res=run(b,sch)
        bad={k:v["bad"][:3] for k,v in res.items() if v["bad"]};nm={k:v["names"][:3] for k,v in res.items() if v["names"]};hs=[k for k,v in res.items() if v["hscroll"]]
        ok(sch+": every text on every screen and sheet reaches 4.5:1 (3:1 for large text)",not bad,bad)
        ok(sch+": every button has a name",not nm,nm)
        ok(sch+": no horizontal scroll on any screen",not hs,hs)
        ok(sch+": %d screens and sheets were swept"%len(res),len(res)>=19)
    # icons and tokens
    c,p=tabs_app(b,"2026-11-12",{"wo_log":L})
    ok("design tokens are defined",p.evaluate("()=>{var s=getComputedStyle(document.documentElement);return ['--fs-1','--fs-2','--fs-3','--fs-4','--fs-5','--fs-6'].map(function(k){return s.getPropertyValue(k).trim()}).join(',')}")=="13px,14px,16px,17px,20px,28px" and p.evaluate("()=>getComputedStyle(document.documentElement).getPropertyValue('--r-2').trim()")=="16px")
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);x=p.evaluate("()=>document.querySelector('.srow').dataset.x");tick(p,x,0);p.wait_for_timeout(200)
    GL="⏱▶⏸■◀🔒🔓🔇✕‹›⚙"
    def glyphs():
        return p.evaluate("g=>[].filter.call(document.querySelectorAll('button'),function(b){var r=b.getBoundingClientRect();return r.width>0&&r.height>0&&!b.closest('[hidden]')&&[].some.call(b.textContent,function(ch){return g.indexOf(ch)>=0})}).map(function(b){return (b.id||b.className)+':'+b.textContent.trim().slice(0,12)})",GL)
    ok("session: no glyph or emoji is used as a control",not glyphs(),glyphs())
    ok("tick, Back, timer and dots are one SVG family (stroke 2 or 3, round caps)",p.evaluate("()=>{var s=[].slice.call(document.querySelectorAll('svg.ic'));return s.length>=6&&s.every(function(v){var c=getComputedStyle(v);return ['2px','3px'].indexOf(c.strokeWidth)>=0&&c.strokeLinecap=='round'||v.querySelector('[fill=currentColor]')||v.getAttribute('fill')=='currentColor'})}"))
    p.locator("#sess [data-t]").first.click();p.clock.run_for(14000);p.wait_for_timeout(300)
    ok("clock: no glyph or emoji is used as a control",not glyphs(),glyphs())
    p.click("#stop");p.click("#stqy");p.wait_for_timeout(200);p.click("#close");p.wait_for_timeout(200)
    for tab in ("week","prog"):
        p.click('#tabbar [data-tab="%s"]'%tab);p.wait_for_timeout(250);ok(tab+": no glyph or emoji is used as a control",not glyphs(),glyphs())
    c.close()
    # focus handling
    c,p=tabs_app(b,"2026-11-12");p.click("#cog");p.wait_for_timeout(250)
    ok("a sheet takes focus when it opens",p.evaluate("()=>document.getElementById('sets').contains(document.activeElement)"))
    inside=True
    for _ in range(14):
        p.keyboard.press("Tab")
        if not p.evaluate("()=>document.getElementById('sets').contains(document.activeElement)"): inside=False
    ok("Tab stays inside the sheet",inside)
    p.keyboard.press("Shift+Tab");ok("Shift+Tab stays inside too",p.evaluate("()=>document.getElementById('sets').contains(document.activeElement)"))
    p.keyboard.press("Escape");p.wait_for_timeout(250)
    ok("Escape closes it and focus returns to the cog",p.locator("#sets.show").count()==0 and p.evaluate("()=>document.activeElement&&document.activeElement.id")=="cog")
    c.close()
    # reduced motion
    c=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,service_workers="block",reduced_motion="reduce");c.add_init_script(HOOK);c.add_init_script("window.__cue=[];");p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)))
    import datetime as dt
    p.clock.install(time=dt.datetime(2026,11,12,9,0));p.goto(URL);p.evaluate("()=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12')}");p.reload();p.wait_for_selector("#tabbar button");p.wait_for_timeout(200)
    ok("reduced motion: transitions and animations are off, the screen wash is not drawn",p.evaluate("()=>{var d=function(e,k){return parseFloat(getComputedStyle(e)[k])};return d(document.querySelector('.tabbar button'),'transitionDuration')<0.01&&getComputedStyle(document.getElementById('cue')).display=='none'}"))
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);p.locator("#sess [data-t]").first.click();p.clock.run_for(12000);p.wait_for_timeout(250)
    ok("reduced motion: cues are still recorded (the setting, not the phone, decides)",any(k in (p.evaluate("()=>window.__cue||[]")) for k in ("tick","change")),p.evaluate("()=>window.__cue||[]"))
    c.close()
    # 120% text
    c,p=tabs_app(b,"2026-11-12",{"wo_log":L})
    def zoomed(label):
        p.evaluate("()=>{document.body.style.zoom=1.2}");p.wait_for_timeout(150)
        r=p.evaluate("()=>({h:document.documentElement.scrollWidth>innerWidth+1,w:Math.max.apply(null,[].map.call(document.querySelectorAll('button,.card,input,textarea'),function(e){var r=e.getBoundingClientRect();return r.width>0&&r.height>0?r.right:0}))})")
        ok(label+" at 120% text: no horizontal scroll, nothing wider than the screen",not r["h"] and r["w"]<=391,r)
        p.evaluate("()=>{document.body.style.zoom=1}")
    zoomed("Today")
    p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(250);zoomed("Week")
    p.click('#tabbar [data-tab="prog"]');p.wait_for_timeout(250);zoomed("Progress")
    p.click('#tabbar [data-tab="today"]');p.wait_for_timeout(200);p.click('#home [data-hm="start"]');p.wait_for_timeout(300);zoomed("Session")
    c.close()
    # four screen sizes
    for (w,h) in ((375,667),(390,844),(430,932),(844,390)):
        c,p=tabs_app(b,"2026-11-12",{"wo_log":L},w=w,h=h);bad=[]
        def chk(name):
            r=p.evaluate("()=>({h:document.documentElement.scrollWidth>innerWidth+1,tb:document.getElementById('tabbar').getBoundingClientRect().bottom<=innerHeight+1,mx:Math.max.apply(null,[].map.call(document.querySelectorAll('button,.card,.hprev,.wrow,.xcard,.hcard'),function(e){var r=e.getBoundingClientRect();return r.width>0&&r.height>0?r.right:0}))})")
            if r["h"] or r["mx"]>w+1: bad.append((name,r))
        chk("today");p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(200);chk("week");p.click('#tabbar [data-tab="prog"]');p.wait_for_timeout(200);chk("progress")
        p.click('#tabbar [data-tab="today"]');p.wait_for_timeout(200);p.click('#home [data-hm="start"]');p.wait_for_timeout(300);chk("session")
        bk=p.evaluate("()=>document.getElementById('close').getBoundingClientRect().top")
        ok("%d x %d: no horizontal scroll, nothing clipped at the sides, Back reachable"%(w,h),not bad and bk>=0,bad)
        c.close()
    ok("no page errors",not errs,errs);b.close()
exit(done())
