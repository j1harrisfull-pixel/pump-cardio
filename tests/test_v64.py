# pc-v64: the full screen clock (tabs layout). Controls in the thumb zone with one big Pause, Stop apart and confirmed,
# Lock with an icon and a clear locked state, a block progress bar, session time as plain text top left (tap = lap),
# NEXT never repeats NOW, sides read "each side".
from playwright.sync_api import sync_playwright
from lib import *
THU="2026-11-12";SAT="2026-11-14"
rect=lambda p,s:p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}",s)
def start_first(p):
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);p.locator("#sess [data-t]").first.click();p.clock.run_for(14000);p.wait_for_timeout(300)
with sync_playwright() as pw:
    b=launch(pw)
    c,p=tabs_app(b,THU);start_first(p)
    ok("the clock hides the tab bar and the dock",p.locator("#tabbar").is_hidden() and p.locator("#dock").is_hidden() and p.locator("#bar.show").count()==1)
    ok("every control still has its id",all(p.locator(i).count()==1 for i in ("#tback","#tpause","#tnext","#stop","#tlock")))
    pa,ba,ne,lo,st=[rect(p,i) for i in ("#tpause","#tback","#tnext","#tlock","#stop")]
    ok("Pause is the big button: at least 64 px high and the widest",pa[3]-pa[1]>=64 and (pa[2]-pa[0])>(ba[2]-ba[0])*1.5 and (pa[2]-pa[0])>(ne[2]-ne[0])*1.5,(pa,ba,ne))
    ok("controls sit in the bottom of the screen, above the home indicator",pa[1]>844*0.6 and lo[3]<=844,(pa,lo))
    ok("Back and Next flank Pause at the same height",abs(ba[1]-pa[1])<10 and abs(ne[1]-pa[1])<10 and ba[2]<pa[0] and ne[0]>pa[2])
    ok("Stop is apart from the controls: top right, 44 px",st[1]<70 and st[2]>350 and st[3]-st[1]>=44 and st[3]<pa[1],st)
    ok("session time is plain text top left, no pill",p.locator("#sct").is_visible() and rect(p,"#sct")[0]<30 and rect(p,"#sct")[1]<60 and p.locator("#sclk").is_hidden() and p.locator("#sct").inner_text().startswith("Session 0:1"),p.locator("#sct").inner_text())
    p.click("#sct");p.clock.run_for(2000);p.wait_for_timeout(250);ok("tapping the session time starts a lap","lap" in p.locator("#sct").inner_text(),p.locator("#sct").inner_text());p.click("#sct");p.wait_for_timeout(150)
    w1=p.evaluate("()=>parseFloat(document.getElementById('cpi').style.width)||0");p.clock.run_for(10000);p.wait_for_timeout(250);w2=p.evaluate("()=>parseFloat(document.getElementById('cpi').style.width)||0")
    ok("a progress bar shows the block and grows",w1>0 and w2>w1 and w2<100,(w1,w2))
    # stop asks first
    p.click("#stop");p.wait_for_timeout(150)
    ok("Stop asks: Stop this timer? Your place is not saved.",p.locator("#stq").is_visible() and "Stop this timer?" in p.locator("#stq").inner_text() and "Your place is not saved." in p.locator("#stq").inner_text() and p.locator("#stqy").is_visible() and p.locator("#stqn").inner_text()=="Keep going")
    p.click("#stqn");p.wait_for_timeout(150);ok("Keep going leaves the timer running",p.locator("#stq").is_hidden() and p.locator("#bar.show").count()==1 and ls(p,"wo_timer") is not None)
    # lock
    p.click("#tlock");p.wait_for_timeout(100)
    ok("Lock: icon and 'Locked · tap to unlock', frame shows",p.locator("#tlock svg").count()==1 and p.locator("#tlock").inner_text().strip()=="Locked · tap to unlock" and p.evaluate("()=>document.getElementById('bar').classList.contains('locked')"))
    ok("while locked only Unlock responds",p.evaluate("()=>['tpause','tback','tnext','stop'].every(function(i){var s=getComputedStyle(document.getElementById(i));return s.pointerEvents=='none'&&+s.opacity<.5})"))
    p.click("#tlock");p.wait_for_timeout(100);ok("Unlock restores it",p.locator("#tlock").inner_text().strip()=="Lock" and not p.evaluate("()=>document.getElementById('bar').classList.contains('locked')"))
    p.click("#tpause");p.wait_for_timeout(100);ok("Pause works and reads Resume",p.locator("#tpause").inner_text()=="Resume");p.click("#tpause")
    p.click("#stop");p.click("#stqy");p.wait_for_timeout(200)
    ok("Stop in the dialog stops it",p.locator("#bar.show").count()==0 and ls(p,"wo_timer") is None and p.locator("#stq").is_hidden())
    c.close()
    # NEXT never repeats NOW, sides read each side, on every guided block of two sessions
    for date,label in ((THU,"Thursday"),(SAT,"Saturday")):
        c,p=tabs_app(b,date);p.click('#home [data-hm="start"]');p.wait_for_timeout(300)
        nb=p.locator("#sess [data-t]").count();rep=[];hand=[]
        for i in range(nb):
            p.locator("#sess [data-t]").nth(i).click();p.clock.run_for(500);p.wait_for_timeout(120)
            for _ in range(90):
                if p.locator("#bar.show").count()==0 or p.locator("#scs.show").count(): break
                now=p.locator("#now").inner_text().replace("\n"," ").strip();sub=p.locator("#sub").inner_text().strip()
                if sub=="Next: "+now: rep.append((i,now))
                if "each hand" in now or "each hand" in sub: hand.append((i,now,sub))
                if p.locator("#bar.ask").count(): break
                try: p.locator("#tnext").click(timeout=1500)
                except Exception: break
                p.clock.run_for(400);p.wait_for_timeout(40)
            if p.locator("#scs.show").count(): p.click("#sc_ok");p.wait_for_timeout(60)
            try:
                if p.locator("#bar.show").count() and p.locator("#stop").is_visible(): p.locator("#stop").click(timeout=1500);p.locator("#stqy").click(timeout=1500)
            except Exception: pass
            p.clock.run_for(5000);p.wait_for_timeout(60)
            if p.locator("#scs.show").count(): p.click("#sc_ok");p.wait_for_timeout(60)
        ok(label+": NEXT never repeats NOW word for word",not rep,rep[:3]);ok(label+": the clock never says each hand",not hand,hand[:3]);c.close()
    ok("no page errors",not errs,errs);b.close()
exit(done())
