# pc-v63: strength cards, inputs and the finish area. One header pattern for every move, sets grouped by round with the
# next set marked, visible inputs, one Finish card with the two small links under it, and one type scale in a session.
from playwright.sync_api import sync_playwright
from lib import *
THU="2026-11-12";WED="2026-11-11"
rect=lambda p,s:p.evaluate("s=>{var r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}",s)
SIZES="""()=>{var out={};document.querySelectorAll('#sbar *,.panel *,#sess *').forEach(function(e){var r=e.getBoundingClientRect();if(!r.width||!r.height)return;var cs=getComputedStyle(e);
 if(cs.visibility=='hidden'||cs.display=='none')return;var own=[].some.call(e.childNodes,function(n){return n.nodeType==3&&n.textContent.trim()})||e.tagName=='INPUT'||e.tagName=='TEXTAREA';if(!own)return;
 out[cs.fontSize]=(out[cs.fontSize]||'')+' '+(e.id||e.className||e.tagName)});return out}"""
def sizes_ok(p,label):
    r=p.evaluate(SIZES);bad={k:v for k,v in r.items() if k not in ("13px","14px","16px","17px","20px")}
    ok(label+": type sizes limited to 13 14 16 17 20 px",not bad,bad)
with sync_playwright() as pw:
    b=launch(pw)
    seed={"wo_log":[]}
    c,p=tabs_app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(400)
    x=p.evaluate("()=>document.querySelector('.srow').dataset.x")
    hd=p.evaluate("()=>[].map.call(document.querySelectorAll('.mvh'),function(m){var l=m.querySelector('.lab'),n=m.querySelector('.mvn'),r1=l.getBoundingClientRect(),r2=n.getBoundingClientRect();return [Math.abs((r1.top+r1.bottom)/2-(r2.top+r2.bottom)/2),m.querySelector('.more').getBoundingClientRect().width,m.querySelector('.more').getBoundingClientRect().height,!!m.querySelector('.more svg'),m.querySelector('.more').getAttribute('aria-label')]})")
    ok("every move: label chip and name start on one line",all(h[0]<8 for h in hd),hd)
    ok("every More is a 44 px icon button with a name",all(h[1]>=44 and h[2]>=44 and h[3] and h[4]=="More" for h in hd),hd)
    p.locator(".more").first.click();p.wait_for_timeout(150)
    ok("More still opens the move's extras and reads Less",p.locator(".mvh .mx").first.is_visible() and p.locator(".more").first.get_attribute("aria-label")=="Less");p.locator(".more").first.click();p.wait_for_timeout(100)
    rn=p.evaluate("()=>[].map.call(document.querySelectorAll('.blk')[0].querySelectorAll('.rnd'),function(r){return [r.querySelector('.rn').textContent,r.querySelectorAll('.srow').length]})")
    ok("sets are grouped by round: 3 groups of 2 rows",rn==[["1",2],["2",2],["3",2]],rn)
    ok("rows say the move label only (A1, A2)",p.evaluate("()=>[].map.call(document.querySelectorAll('.blk')[0].querySelectorAll('.srow .sn'),function(e){return e.textContent.trim()}).slice(0,4)")==["A1","A2","A1","A2"])
    nx=p.evaluate("()=>[].map.call(document.querySelectorAll('.srow.nx'),function(r){return r.dataset.row})")
    ok("exactly one next set marked, the first row of the block you are in",len(nx)==1 and nx[0].endswith("_0") and p.evaluate("()=>document.querySelector('.srow.nx')===document.querySelector('.srow')"),nx)
    tick(p,x,0);p.wait_for_timeout(200)
    nx2=p.evaluate("()=>[].map.call(document.querySelectorAll('.srow.nx'),function(r){return r.dataset.row})")
    ok("a tick moves the marker to the next row",len(nx2)==1 and nx2[0]!=nx[0],(nx,nx2))
    ok("ticked rows are quieter (muted text, light borders) but still readable",p.evaluate("()=>{var a=getComputedStyle(document.querySelector('.srow.on .rpb')),b=getComputedStyle(document.querySelector('.srow.nx .rpb'));return a.color!=b.color&&a.borderTopColor!=b.borderTopColor&&getComputedStyle(document.querySelector('.srow.on')).opacity=='1'}"))
    ok("the marker is orange",p.evaluate("()=>getComputedStyle(document.querySelector('.srow.nx'),'::before').backgroundColor")=="rgb(255, 138, 61)")
    inp=p.evaluate("()=>{var w=document.querySelector('.srow:not(.on) .w'),r=document.querySelector('.srow:not(.on) .rpb');var a=getComputedStyle(w),c=getComputedStyle(r);return [w.getBoundingClientRect().height,r.getBoundingClientRect().height,a.borderTopWidth,c.borderTopWidth,a.fontSize,a.borderTopColor]}")
    ok("inputs: 44 px high, 1.5 px border, 17 px numbers",inp[0]>=44 and inp[1]>=44 and float(inp[2][:-2])>=1 and float(inp[3][:-2])>=1 and inp[4]=="17px" and inp[5]!="rgb(232, 232, 237)",inp)
    ok("+ round is a 44 px button",rect(p,".setctl .link")[3]-rect(p,".setctl .link")[1]>=44)
    ok("guided card: room above Start",p.evaluate("()=>{var b=document.querySelector('.tcard .btn'),p=b.previousElementSibling;return b.getBoundingClientRect().top-p.getBoundingClientRect().bottom>=14}"))
    # finish card
    p.evaluate("scrollTo(0,document.body.scrollHeight)");p.wait_for_timeout(150)
    ok("one Finish card: title, chips, notes and the Finish button inside it",p.evaluate("()=>{var c=document.querySelector('.fcard');return !!c&&c.querySelector('.ftit').textContent=='Finish'&&c.querySelectorAll('#oc [data-oc]').length==5&&!!c.querySelector('#s_nt')&&!!c.querySelector('#fin_c')}"))
    ok("the old Finish button and Reset line are not shown twice",p.locator("#fin").is_hidden() and p.locator("#rst").is_hidden())
    fr=p.evaluate("()=>{var f=document.querySelector('.frow'),c=document.querySelector('.fcard').getBoundingClientRect();return [f.getBoundingClientRect().top>=c.bottom-1,[].map.call(f.querySelectorAll('button'),function(b){return b.textContent.trim()})]}")
    ok("under the card: + Add an activity and Reset this day… on one line",fr[0] and fr[1]==["+ Add an activity","Reset this day…"],fr)
    ok("the Extra and How did it go? headings are still in the page",p.evaluate("()=>[].map.call(document.querySelectorAll('#sess h2'),function(h){return h.textContent}).filter(function(t){return t=='Extra'||t=='How did it go?'}).length")==2)
    p.click("#addrun");p.wait_for_timeout(200);ok("+ Add an activity opens the form",p.locator("#r_d").is_visible() or p.locator("#r_t").is_visible())
    p.click("#rst_c");p.wait_for_timeout(300);ok("Reset this day… works from its new place (confirm accepted)",p.locator(".srow.on").count()==0)
    p.evaluate("scrollTo(0,0)");p.click("[data-tqx]");p.evaluate("()=>document.querySelector('.more').click()");p.wait_for_timeout(200)
    sizes_ok(p,"strength day")
    # finish through the card
    p.evaluate("()=>document.querySelector('.more').click()");tick(p,x,0);p.wait_for_timeout(100)
    for _ in range(3):
        p.click("#fin_c")
        try: p.wait_for_selector("#ov.show",timeout=1500);break
        except Exception: p.clock.run_for(2000)
    ok("Finish workout in the card saves the log",len(ls(p,"wo_log") or [])==1)
    p.wait_for_timeout(800);p.click("#o_done");p.wait_for_timeout(300)
    c.close()
    # run day and something else
    c,p=tabs_app(b,WED);p.click('#home [data-hm="run"]');p.wait_for_timeout(300);sizes_ok(p,"run day");c.close()
    c,p=tabs_app(b,THU);p.click('#home [data-hm="else"]');p.wait_for_timeout(300);sizes_ok(p,"something else")
    ok("something else: no Finish card, one Save",p.locator(".fcard").count()==0 and p.locator("#fin2").is_visible());c.close()
    # last weight as placeholder or value
    c,p=tabs_app(b,THU);p.click('#home [data-hm="start"]');p.wait_for_timeout(300);x=p.evaluate("()=>document.querySelector('.srow').dataset.x");c.close()
    c,p=tabs_app(b,THU,{"wo_log":[{"date":"2026-11-05","name":"Lower · Old","type":"main","min":30,"sets":3,"of":3,"wt":{x:"20"},"rp":{x:{"v":["7","7","7"],"u":"","k":["20","20","20"]}}}]})
    p.click('#home [data-hm="start"]');p.wait_for_timeout(300)
    w=p.evaluate("()=>{var e=document.querySelector('.srow .w');return [e.placeholder,e.value]}")
    ok("kg shows the last logged weight (as hint or value), nothing saved",("20" in w) and not (ls(p,"wo_wt") or {}).get(x,{}).get(THU),w)
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
