# pc-v68: Settings in sections with switches, one style for every sheet, forms with visible inputs, the saved card,
# toasts with an action (the one tap Skipped on yesterday's prompt is Undoable).
from playwright.sync_api import sync_playwright
from lib import *
THU="2026-11-12";WED="2026-11-11"
rect=lambda p,s:p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}",s)
def opaque(p,x,y): return p.evaluate("([x,y])=>{var e=document.elementFromPoint(x,y);return e?(e.closest('.swp,#hs')?'sheet':e.id||e.tagName):null}",[x,y])
with sync_playwright() as pw:
    b=launch(pw);c,p=tabs_app(b,THU);p.click("#cog");p.wait_for_timeout(300)
    heads=p.evaluate("()=>[].map.call(document.querySelectorAll('#sets .sgt'),function(e){return e.textContent})")
    ok("Settings has sections: Timers, Cues, Plan, About",[h.lower() for h in heads]==["timers","cues","plan","about"],heads)
    ok("each setting is in its section",p.evaluate("()=>{var q=function(i){return document.getElementById(i).closest('#sg_t,#sg_c,#sg_p')};return q('autorest').id=='sg_t'&&q('cueon').id=='sg_c'&&q('loud').id=='sg_c'&&q('imp').id=='sg_p'}"))
    ok("the beep on silent row has the music warning as a second line",p.evaluate("()=>document.querySelector('#sets label:has(#loud) .t1').textContent")=="Beep even when the phone is on silent" and p.evaluate("()=>document.querySelector('#sets label:has(#loud) .t2').textContent")=="This pauses your music.")
    sw=p.evaluate("()=>[].map.call(document.querySelectorAll('#sets .setr'),function(l){var i=l.querySelector('input'),r=i.getBoundingClientRect(),s=getComputedStyle(i);return [Math.round(r.width),Math.round(r.height),l.getBoundingClientRect().height,s.backgroundColor,i.checked,l.querySelector('input').type]})")
    ok("switches: 51 x 31, rows at least 56 px, orange when on, grey when off",all(x[0]==51 and x[1]==31 and x[2]>=56 and x[5]=="checkbox" for x in sw) and [x[3] for x in sw if x[4]]==["rgb(255, 138, 61)"]*2 and [x[3] for x in sw if not x[4]]==["rgb(142, 142, 147)"],sw)
    ok("ids unchanged and a row toggles from its text",(p.locator("#sets label:has(#autorest) .t1").click(),ls(p,"wo_autorest")==False)[1])
    ok("About: version from the meta tag, data stays on the phone",p.evaluate("document.querySelector('meta[name=app-version]').content") in p.locator("#sg_a").inner_text() and "stay on this phone" in p.locator("#sg_a").inner_text() and "Reset" not in p.locator("#sets").inner_text())
    ok("no 'Weeks' sub heading, the list and Import week are there","w/c Mon 9 Nov" in p.locator("#sets #wks").inner_text() and p.locator("#imp").is_visible() and p.locator("#sets .wkl .hs_h").is_hidden())
    # the sheet style
    sh=lambda sel:p.evaluate("s=>{var e=document.querySelector(s+' .sh'),c=getComputedStyle(e),g=e.querySelector('.hs_g'),x=e.querySelector('.hs_top .swx,#hs_x');return [c.borderTopLeftRadius,c.borderTopRightRadius,g?Math.round(g.getBoundingClientRect().width):0,x?Math.round(x.getBoundingClientRect().width)+'x'+Math.round(x.getBoundingClientRect().height):null]}",sel)
    base=sh("#sets")
    ok("settings sheet: 24 px top corners, grab handle, 44 px close",base[0]=="24px" and base[1]=="24px" and base[2]==40 and base[3]=="44x44",base)
    ok("the tab bar is not tappable under a sheet",opaque(p,195,820)=="sheet" and opaque(p,60,820)=="sheet")
    p.click("#sets .swx");p.wait_for_timeout(200)
    p.click("#imp") if p.locator("#imp").is_visible() else None
    p.click("#cog");p.wait_for_timeout(200);p.click("#imp");p.wait_for_timeout(300)
    ok("Import week sheet has the same shape",sh("#ims")==base,sh("#ims"));ok("and its field is a visible input",p.evaluate("()=>{var s=getComputedStyle(document.getElementById('im_t'));return parseFloat(s.borderTopWidth)>=1&&s.borderTopColor=='rgb(199, 199, 204)'&&s.fontSize=='17px'&&parseFloat(s.minHeight)>=44}"))
    p.click(".imx");p.wait_for_timeout(200)
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300);p.locator("#sess .mvn").first.click() if p.locator("#sess .mvn").count() else None
    p.wait_for_timeout(300)
    if p.locator("#hs.show").count():
        hs=sh("#hs");ok("How-to sheet has the same shape",hs[0]=="24px" and hs[2]==40 and hs[3]=="44x44",hs);ok("the tab bar is not tappable under it",opaque(p,195,820)=="sheet")
        p.click("#hs_x");p.wait_for_timeout(200)
    else: ok("How-to sheet opens",False)
    p.click("#close");p.wait_for_timeout(200);c.close()
    # saved card
    c,p=tabs_app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(300);x=p.evaluate("()=>document.querySelector('.srow').dataset.x");tick(p,x,0);fin(p);p.wait_for_timeout(300)
    cd=p.evaluate("()=>{var d=document.getElementById('o_d'),c=getComputedStyle(document.getElementById('o_e')),b=document.getElementById('o_done');return [getComputedStyle(d).textAlign,c.color,getComputedStyle(b).backgroundColor,getComputedStyle(document.getElementById('o_t')).fontSize,getComputedStyle(document.getElementById('o_undo')).backgroundColor]}")
    ok("saved card: details left aligned, minutes large, praise in the accent ink, Done is the orange button, Undo a plain link",cd[0]=="left" and cd[1]=="rgb(179, 79, 0)" and cd[2]=="rgb(255, 138, 61)" and cd[3]=="44px" and cd[4]=="rgba(0, 0, 0, 0)",cd)
    c.close()
    # toast with an action, one tap Skipped
    c,p=tabs_app(b,THU);p.click('#ynag [data-ng="skip"]');p.wait_for_timeout(400)
    tr=rect(p,"#toast");sb=rect(p,'#home [data-hm="start"]')
    ok("one tap Skipped: logged, toast with Undo, back on Today",p.locator("#toast .tact").inner_text()=="Undo" and [e["date"] for e in ls(p,"wo_log") if e.get("oc")=="skipped"]==[WED] and p.locator("#home").is_visible())
    ok("the toast sits above the tab bar and does not cover the primary button",tr[3]<=rect(p,"#tabbar")[1] and (tr[1]>=sb[3] or tr[3]<=sb[1]),(tr,sb))
    ok("the toast has a 44 px Undo and is tappable",rect(p,"#toast .tact")[3]-rect(p,"#toast .tact")[1]>=44 and p.evaluate("()=>getComputedStyle(document.getElementById('toast')).pointerEvents")=="auto")
    p.click("#toast .tact");p.wait_for_timeout(300);ok("Undo restores the prompt and says so",not ls(p,"wo_log") and p.locator("#ynag").is_visible() and "Undone" in p.locator("#toast").inner_text() and p.locator("#toast .tact").count()==0)
    c.close()
    # dark
    c,p=tabs_app(b,THU,scheme="dark");p.click("#cog");p.wait_for_timeout(300)
    col=p.evaluate("()=>[getComputedStyle(document.querySelector('#sets .sh')).backgroundColor,getComputedStyle(document.querySelector('#sets .setr input:not(:checked)')||document.querySelector('#sets .setr input')).backgroundColor]")
    ok("dark: the sheet is a dark surface and an off switch is visible",sum(map(int,__import__("re").findall(r"\d+",col[0])[:3]))<200 and col[1]!=col[0],col)
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
