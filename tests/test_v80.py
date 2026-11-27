# pc-v80: ticking a set never moves the screen. Tap every set circle of a session in order on a phone sized screen (touch,
# tabs layout, scroll anchoring OFF like iOS Safari) and check after each tap, and 600 ms later, that the tapped circle did not
# move, the page did not scroll, and the finger is still on the circle. Finished blocks still fold when the day is reopened.
from playwright.sync_api import sync_playwright
from lib import *
import datetime as dt
NOANCHOR="html,body,#sess{overflow-anchor:none!important}"
def run(b,date,label,anchor_off=True):
    y,m,d=map(int,date.split("-"))
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block")
    c.add_init_script(HOOK);p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda x:x.accept())
    p.clock.install(time=dt.datetime(y,m,d,19,0));p.goto(URL)
    p.evaluate("()=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');localStorage.setItem('wo_fix78','1')}")
    p.reload();p.wait_for_selector("#tabbar button",timeout=10000);p.wait_for_timeout(200)
    if anchor_off:p.add_style_tag(content=NOANCHOR)
    p.click('#home [data-hm="start"]');p.wait_for_timeout(400)
    keys=p.evaluate("()=>[].map.call(document.querySelectorAll('[data-tk]'),function(b){return b.dataset.tk})")
    bad=[];rest_seen=False;worst=0
    for k in keys:
        sel=f'[data-tk="{k}"]'
        cy=p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return r.top+r.height/2}",sel)
        if cy<140 or cy>560:
            p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();window.scrollTo(0,window.scrollY+r.top+r.height/2-340)}",sel);p.wait_for_timeout(120)
        r0=p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,window.scrollY]}",sel)
        p.touchscreen.tap(r0[0],r0[1]);p.wait_for_timeout(30)
        for phase,wait in (("now",0),("later",600)):
            if wait:p.clock.run_for(wait);p.wait_for_timeout(120)
            r1=p.evaluate("s=>{var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,window.scrollY]}",sel)
            hit=p.evaluate("([x,y,s])=>{var e=document.elementFromPoint(x,y);return !!(e&&e.closest(s))}",[r0[0],r0[1],sel])
            if r1 is None: bad.append((k,phase,"circle gone"));continue
            dy=abs(r1[1]-r0[1]);worst=max(worst,dy)
            if dy>2 or abs(r1[2]-r0[2])>0 or not hit: bad.append((k,phase,round(r1[1]-r0[1],1),r1[2]-r0[2],hit))
        if p.locator("#rbar.show").count():rest_seen=True
    ticked=p.evaluate("()=>document.querySelectorAll('[data-tk].on').length")
    pb=p.evaluate("()=>parseFloat(getComputedStyle(document.body).paddingBottom)")
    p.click("#close");p.wait_for_timeout(300)
    p.click('#home [data-hm="open"]');p.wait_for_timeout(400)
    folds=p.locator("#sess .fold").count()
    c.close()
    return bad,rest_seen,ticked,len(keys),pb,folds,worst
with sync_playwright() as pw:
    b=launch(pw)
    for date,label,n in (("2026-11-23","Mon Upper · Density Dash",20),("2026-11-27","Fri Lower · Step-Up Staircase",None)):
        for aoff in (True,False):
            bad,rest,ticked,total,pb,folds,worst=run(b,date,label,aoff)
            tag=f"{label} ({'anchoring off' if aoff else 'anchoring on'})"
            ok(f"{tag}: {total} circles"+(" (20 expected)" if n else ""),total>=10 and (n is None or total==n),total)
            ok(f"{tag}: no tap moved the circle, scrolled the page or lost the finger",not bad,bad[:4])
            ok(f"{tag}: every set ended up ticked",ticked==total,(ticked,total))
            ok(f"{tag}: the rest bar started during the session",rest)
            ok(f"{tag}: room under the last row for the rest bar and tabs",pb>=190,pb)
            ok(f"{tag}: finished blocks fold when the day is reopened",folds>=3 or (n is None and folds>=2),folds)
    ok("no page errors",not errs,errs);b.close()
exit(done())
