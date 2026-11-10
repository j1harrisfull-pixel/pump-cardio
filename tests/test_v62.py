# pc-v62: top of the session. One slim bar (Back, title, "n of m"), the big header hidden, date line + Change session on
# one row, the "What did you do?" card collapsed to one quiet row for today's on plan session, the safety note and the
# stop signs line in full inside one card, and the first block near the top of the screen.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";WED="2026-11-11";THU="2026-11-12"
STOP="Stop and get checked if you get a sudden or severe headache, any vision change, dizziness or feel sick."
rect=lambda p,s:p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}",s)
def safety(p,label):
    ok(label+": stop signs line in full and visible",p.locator(".safe .stop").is_visible() and p.locator(".safe .stop").inner_text()==STOP and p.evaluate("()=>{var e=document.querySelector('.safe .stop');return e.scrollHeight<=e.clientHeight+1&&getComputedStyle(e).display!='none'}"))
with sync_playwright() as pw:
    b=launch(pw);c,p=tabs_app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(400)
    ok("the big header is hidden, the slim bar shows the title and progress",p.locator("header").is_hidden() and p.locator("#sbar").is_visible() and p.locator("#sbt").inner_text()=="Lower · Carry Medley" and p.locator("#sbp").inner_text()=="0 of 19",(p.locator("#sbt").inner_text(),p.locator("#sbp").inner_text()))
    bar=rect(p,"#sbar");bk=rect(p,"#close")
    ok("Back sits inside the bar, top left; the title starts to its right",bar[1]==0 and bk[1]>=0 and bk[3]<=bar[3] and bk[0]<20 and p.evaluate("()=>document.getElementById('sbt').getBoundingClientRect().left")>bk[2],(bar,bk))
    ok("date line and Change session share one row",abs((rect(p,"#dnote")[1]+rect(p,"#dnote")[3])/2-(rect(p,"#chg")[1]+rect(p,"#chg")[3])/2)<4 and rect(p,"#chg")[0]>200,(rect(p,"#dnote"),rect(p,"#chg")))
    ok("Change session still opens the options",(p.click("#chg"),p.wait_for_timeout(150),p.locator("#dcm").is_visible())[2]);p.click("#chg");p.wait_for_timeout(100)
    ok("the question is one quiet row, chips hidden",p.locator("#topq .tqq").is_visible() and p.locator("#toc").count()==0 and rect(p,"#topq")[3]-rect(p,"#topq")[1]<=48)
    ok("the first block header is in the top 330 px",p.evaluate("()=>document.querySelector('#sess h2').getBoundingClientRect().top")<=330,p.evaluate("()=>document.querySelector('#sess h2').getBoundingClientRect().top"))
    safety(p,"strength day")
    ok("session note present",len(p.locator("#safe1").inner_text())>20 and p.locator("#safe1").is_visible())
    x=p.evaluate("()=>document.querySelector('.srow').dataset.x");tick(p,x,0);p.wait_for_timeout(200)
    ok("a tick updates the bar",p.locator("#sbp").inner_text()=="1 of 19",p.locator("#sbp").inner_text())
    p.click("#topq .tqq");p.wait_for_timeout(150)
    ok("tapping the row opens the three chips",p.locator("#toc [data-toc]").count()==3 and p.locator("#toc .rc.on").inner_text()=="The plan")
    p.click('[data-toc="else"]');p.wait_for_timeout(200);ok("the chips still work",p.locator("#toc .rc.on").inner_text()=="Something else" and (ls(p,"wo_run_"+THU) or {}).get("sub")==1)
    safety(p,"off plan day");p.click('[data-toc="plan"]');p.wait_for_timeout(150)
    p.click("#close");p.wait_for_timeout(200);p.click('#home [data-hm="open"]');p.wait_for_timeout(300)
    ok("closing and reopening collapses the question again",p.locator("#topq .tqq").count()==1)
    fin(p);p.wait_for_timeout(200)
    ok("once logged the bar says so",p.locator("#sbp").inner_text().startswith("✓"),p.locator("#sbp").inner_text())
    p.click("#o_done");p.wait_for_timeout(300);c.close()
    # past day and run day
    c,p=tabs_app(b,THU);p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(200);p.click(f'#wlist [data-d="{WED}"]');p.wait_for_timeout(300)
    ok("a past day shows the question open (not collapsed)",p.locator("#toc [data-toc]").count()==3 and p.locator("#topq .tqq").count()==0)
    safety(p,"run day")
    ok("the bar title and date row on a past day",p.locator("#sbt").inner_text()=="Hill Hunter Run" and "Wed 11 Nov" in p.locator("#dnote").inner_text())
    c.close()
    # small iPhone
    c,p=tabs_app(b,THU,w=375,h=667);p.click('#home [data-hm="start"]');p.wait_for_timeout(300)
    ok("375 × 667: the first card is partly visible above the dock and tab bar",rect(p,"#sess .card")[1]<667-120,rect(p,"#sess .card"))
    ok("375 × 667: bar title does not run into the progress text",p.evaluate("()=>document.getElementById('sbt').getBoundingClientRect().right<=document.getElementById('sbp').getBoundingClientRect().left+1"))
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
