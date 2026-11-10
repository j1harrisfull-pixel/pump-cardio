# pc-v66: Week. Rows with clear state chips, a header card (arrows either side of the dates, seven dots), swipe to change
# week, a labelled Edit this week's plan button, an edit mode with the strip, Swap days and a one line explanation, and an
# unplanned week card.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12";SUN="2026-11-15"
L=[{"date":MON,"name":"Upper · Slow Is Strong","type":"main","min":30,"sub":"Easy 5km","plan":"Upper · Slow Is Strong","act":"run","km":"5","time":"30:27","effort":"easy","oc":"modified","sid":"upb0911"},
   {"date":WED,"name":"Hill Hunter Run","type":"main","min":0,"oc":"skipped","sid":"hill1111"}]
rect=lambda p,s:p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}",s)
with sync_playwright() as pw:
    b=launch(pw);c,p=tabs_app(b,THU,{"wo_log":L});p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300)
    ok("header card: arrows either side of the dates",p.locator("#wlab").inner_text()=="9 to 15 Nov" and rect(p,"#prev")[2]<=rect(p,"#wlab")[0]+2 and rect(p,"#next")[0]>=rect(p,"#wlab")[2]-2,p.locator("#wlab").inner_text())
    dots=p.evaluate("()=>[].map.call(document.querySelectorAll('.wdots .wd1'),function(e){return e.className.replace('wd1 ','')+':'+e.textContent})")
    ok("seven dots: done, rest dash, skipped, today, rest, miss/future",dots==["done:M","rest:T","skip:W","today:T","rest:F","fut:S","fut:S"],dots)
    chips=p.evaluate("()=>[].map.call(document.querySelectorAll('#wlist .wrow'),function(r){var c=r.querySelector('.ws');return c?c.textContent+'|'+c.className.replace('ws ',''):'-'})")
    ok("chips: Done (green), none for rest, Skipped (grey), Today (orange), none for future",chips==["✓ Done|ok","-","Skipped|sk","Today|td","-","-","-"],chips)
    col=p.evaluate("()=>{var g=function(s){var e=document.querySelector(s);return getComputedStyle(e).color+'/'+getComputedStyle(e).backgroundColor};return [g('.wrow .ws.ok'),g('.wrow .ws.td')]}")
    ok("Done is green text, Today is an orange chip",col[0].startswith("rgb(27, 127, 59)") and col[1].endswith("rgb(255, 138, 61)") and col[1].startswith("rgb(17, 17, 17)"),col)
    ok("rest rows are quieter",p.evaluate("()=>+getComputedStyle(document.querySelector('.wrow.rest')).opacity")<0.9)
    ok("a replaced day says what was done with instead of",p.locator(f'#wlist [data-d="{MON}"] small').inner_text()=="30 min · instead of Upper · Slow Is Strong")
    ok("Edit plan is a labelled button under the list, the small Edit plan is gone",p.locator("#ed2").inner_text()=="Edit this week's plan" and rect(p,"#ed2")[1]>rect(p,'#wlist [data-d="%s"]'%SUN)[3] and p.locator("#ed").is_hidden())
    # swipe
    p.mouse.move(300,400);p.mouse.down();p.mouse.move(120,410,steps=6);p.mouse.up();p.wait_for_timeout(300)
    ok("swiping the list left shows next week (and does not open a day)",p.locator("#ttl").inner_text()=="Next week" and p.locator("#panel.open").count()==0 and p.locator("#wlab").inner_text()=="16 to 22 Nov",p.locator("#wlab").inner_text())
    p.mouse.move(120,400);p.mouse.down();p.mouse.move(300,410,steps=6);p.mouse.up();p.wait_for_timeout(300)
    ok("swiping right comes back",p.locator("#ttl").inner_text()=="This week")
    # edit mode
    p.click("#ed2");p.wait_for_timeout(250)
    ok("edit mode: strip, Swap days and the one line; the list is hidden; Done shows",p.locator("#week").is_visible() and p.locator("#swd").is_visible() and p.locator("#ehint").inner_text()=="Tap a day to cycle it. Swap days moves two sessions." and p.locator("#wlist").is_hidden() and p.locator("#ed").inner_text()=="Done" and p.locator("#ed").is_visible())
    p.click("#ed");p.wait_for_timeout(250)
    ok("Done returns to the list",p.locator("#wlist").is_visible() and p.locator("#week").is_hidden() and p.locator("#ehint").is_hidden())
    p.click(f'#wlist [data-d="{THU}"]');p.wait_for_timeout(250);ok("a row still opens the day",p.locator("#panel.open").count()==1);c.close()
    # month boundary label
    c,p=tabs_app(b,"2026-11-30");p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(250);ok("the date range crosses a month",p.locator("#wlab").inner_text() in ("30 Nov to 6 Dec",),p.locator("#wlab").inner_text());c.close()
    # unplanned
    c,p=tabs_app(b,"2026-11-16");p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300)
    ok("unplanned week: one card with what to do and that any activity can be logged",p.locator(".wnp").is_visible() and "Settings on the Today screen, Import week" in p.locator(".wnp").inner_text() and "log any activity" in p.locator(".wnp").inner_text() and p.locator("#wlist .wrow").count()==7)
    p.click('#wlist [data-d="2026-11-17"]');p.wait_for_timeout(250);ok("a day of an unplanned week can still be opened to log an activity",p.locator("#panel.open").count()==1);c.close()
    # dark
    c,p=tabs_app(b,THU,{"wo_log":L},scheme="dark");p.click('#tabbar [data-tab="week"]');p.wait_for_timeout(300)
    col=p.evaluate("()=>[getComputedStyle(document.querySelector('.wrow .ws.ok')).color,getComputedStyle(document.querySelector('.wdots')).backgroundColor]")
    ok("dark: the Done chip is light green and the card is a dark surface",col[0].startswith("rgb(95, 208, 138)") and sum(map(int,__import__("re").findall(r"\d+",col[1])[:3]))<200,col)
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
