# pc-v55: cues for a phone on silent with music playing (iOS lets a web app either mix with music or ignore the ring
# switch, not both). Every change washes the whole screen orange once, the end of a block twice, the last three seconds
# pulse the digits; the same for the rest bar. A tick box turns the flashes off. Never more than two flashes a second.
from playwright.sync_api import sync_playwright
from lib import *
with sync_playwright() as pw:
    b=launch(pw)
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block")
    c.add_init_script(HOOK);c.add_init_script("window.__cue=[];");p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.clock.install(time=dt.datetime(2026,11,3,9,0));p.goto(URL)
    p.evaluate("()=>{localStorage.clear();localStorage.setItem('wo_chg','1');localStorage.setItem('wo_flat','1');localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');}");p.reload();p.wait_for_selector("#week button.day");p.click('button.day[data-d="2026-11-03"]');p.wait_for_timeout(200)
    cues=lambda:p.evaluate("()=>window.__cue.slice()")
    ok("setting on by default, worded for the silent phone",p.locator("#cueon").is_checked() and "Flash the screen at every change" in p.locator("label.setr:has(#cueon)").inner_text())
    ok("the cue layer never blocks a tap and is invisible at rest",p.evaluate("()=>{var s=getComputedStyle(document.getElementById('cue'));return s.pointerEvents+'|'+s.opacity+'|'+s.position}")=="none|0|fixed")
    p.locator("#sess [data-t]").first.click();p.wait_for_timeout(60);segs=ls(p,"wo_timer")["segs"]
    p.clock.run_for(6500);p.wait_for_timeout(40);ok("no cue while nothing changes",cues()==[],cues())
    p.clock.run_for(1200);p.wait_for_timeout(40);ok("3 seconds to go: the digits pulse",cues()==["tick"] and "tk3" in p.get_attribute("#time","class"),cues())
    p.clock.run_for(2600);p.wait_for_timeout(60)
    ok("3-2-1 then the change: three digit pulses and one full screen wash",cues()==["tick","tick","tick","change"] and p.get_attribute("#cue","class")=="c1",(cues(),p.get_attribute("#cue","class")))
    ok("the wash is the app orange and fades (animation running on the layer)",p.evaluate("()=>{var s=getComputedStyle(document.getElementById('cue'));return s.animationName+'|'+s.backgroundColor}")=="cue1|rgb(255, 138, 61)")
    ok("a beep still fires with every cue, plus the usual one at the start (ring switch on)",p.evaluate("window.__bp.length")==5,p.evaluate("window.__bp.length"))
    # run to the end: one wash per change, a double wash at the end, never two washes within 500 ms
    p.evaluate("()=>{window.__cue=[];window.__ct=[];var o=window.__cue.push;window.__cue.push=function(k){window.__ct.push([k,Date.now()]);return o.call(this,k)}}")
    left=sum(x[1] for x in segs)-10
    for i in range(left+3): p.clock.run_for(1000)
    p.wait_for_timeout(60);k=cues();ct=p.evaluate("()=>window.__ct")
    ok("each later change washes once; the end of the block washes twice",k.count("change")==len(segs)-2 and k[-1]=="end" and k.count("end")==1,k)
    big=[t for kind,t in ct if kind!="tick"];ok("flashes are at least 500 ms apart",all(b2-a2>=500 for a2,b2 in zip(big,big[1:])),big[:6])
    if p.locator("#bar.show").count(): p.click("#stop")
    # rest bar
    p.evaluate("()=>{window.__cue=[]}");tick(p,"db-bench",0);p.wait_for_timeout(100);rest=sec(p.locator("#rtime").inner_text())
    for i in range(rest+1): p.clock.run_for(1000)
    p.wait_for_timeout(60);k=cues();ok("rest bar: 3-2-1 pulses, then a double wash when the rest is over",k[-1]=="end" and k.count("tick")==3,k)
    if p.locator("#rbar.show").count(): p.click("#rskip")
    # off switch
    p.evaluate("()=>document.getElementById('cueon').click()");p.wait_for_timeout(60);p.evaluate("()=>{window.__cue=[];document.getElementById('cue').className='';document.getElementById('time').classList.remove('tk3')}")
    p.locator("#sess [data-t]").last.click();p.clock.run_for(11500);p.wait_for_timeout(60)
    ok("switched off: no wash and no pulse, the beeps stay",ls(p,"wo_cue")==0 and p.get_attribute("#cue","class")=="" and "tk3" not in (p.get_attribute("#time","class") or "") and p.evaluate("window.__bp.length")>0)
    p.click("#stop");ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
