# pc-v54: music first. Starting a guided timer or the rest bar never starts the silent <audio> clip (that clip turns
# the app into a "music player" for iOS and pauses whatever is playing); the app asks for the ambient audio session so
# beeps mix with the user's music. "Beep even when the phone is on silent (this pauses your music)" is an opt in.
from playwright.sync_api import sync_playwright
from lib import *
AS="""(function(){var v="auto";window.__as=[];try{Object.defineProperty(navigator,"audioSession",{value:{get type(){return v},set type(x){v=x;window.__as.push(x)}},configurable:true});}catch(e){}})();"""
with sync_playwright() as pw:
    b=launch(pw)
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block")
    c.add_init_script(HOOK);c.add_init_script(AS);p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.clock.install(time=dt.datetime(2026,11,3,9,0));p.goto(URL)
    p.evaluate("()=>{localStorage.clear();localStorage.setItem('wo_chg','1');localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');}");p.reload();p.wait_for_selector("#week button.day");p.click('button.day[data-d="2026-11-03"]');p.wait_for_timeout(200)
    paused=lambda:p.evaluate("()=>document.getElementById('snda').paused")
    ok("the app asks for the ambient audio session (mixes with music)",p.evaluate("()=>navigator.audioSession.type")=="ambient",p.evaluate("()=>window.__as"))
    ok("the setting exists, off by default, and says what it costs",p.locator("#loud").is_checked()==False and p.locator("label.setr:has(#loud)").inner_text().strip()=="Beep even when the phone is on silent (this pauses your music)")
    p.locator("#sess [data-t]").first.click();p.clock.run_for(12000);p.wait_for_timeout(100)
    ok("guided timer running: the silent clip is NOT playing, beeps still fire",paused() and p.evaluate("window.__bp.length")>=1 and p.evaluate("()=>navigator.audioSession.type")=="ambient")
    p.click("#stop");tick(p,"db-bench",0);p.wait_for_timeout(120)
    ok("rest bar running: the silent clip is NOT playing",p.locator("#rbar.show").count()==1 and paused());p.click("#rskip")
    p.evaluate("()=>document.getElementById('loud').click()");p.wait_for_timeout(80)
    ok("opt in: stored, and the session switches to playback",p.evaluate("()=>localStorage.getItem('wo_loud')")=="1" and p.evaluate("()=>navigator.audioSession.type")=="playback")
    p.locator("#sess [data-t]").first.click();p.clock.run_for(3000);p.wait_for_timeout(100);ok("with the opt in, the clip plays while a timer runs",not paused())
    p.evaluate("()=>document.getElementById('loud').click()");p.wait_for_timeout(80);ok("switching it off mid timer stops the clip at once and returns to ambient",paused() and p.evaluate("()=>navigator.audioSession.type")=="ambient")
    p.click("#stop");ok("no page errors",not errs,errs);c.close()
    c,p=view(b,"2026-11-03");ok("no audioSession API (older iOS, other browsers): nothing breaks",p.locator("#sess h2").count()>3 and not errs)
    c.close();b.close()
exit(done())
