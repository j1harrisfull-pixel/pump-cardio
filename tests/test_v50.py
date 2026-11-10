# pc-v50: less at the top of the day. One "Change session" button holds the rare options (backup, quick option, run
# instead, swap) and stays open while one is active; Log ↓ is gone. Installed on the Home Screen the app opens straight
# on today's session. A line under the week strip offers to log yesterday when its session has no log.
from playwright.sync_api import sync_playwright
from lib import *
MON="2026-11-09";TUE="2026-11-10";WED="2026-11-11";THU="2026-11-12"
NOCHG="()=>{localStorage.removeItem('wo_chg')}"
def fresh(b,d,seed=None,open_day=True,standalone=False):
    """Like lib.view but as the phone has it: no wo_chg preference; optionally as an installed Home Screen app."""
    y,m,dd=map(int,d.split("-"))
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block")
    c.add_init_script(HOOK)
    if standalone: c.add_init_script("Object.defineProperty(navigator,'standalone',{get:function(){return true}})")
    p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda x:x.accept());p.clock.install(time=dt.datetime(y,m,dd,9,0));p.goto(URL)
    p.evaluate("t=>{localStorage.clear();localStorage.setItem('wo_flat','1');localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');for(var k in t)localStorage.setItem(k,JSON.stringify(t[k]));}",seed or {})
    p.reload();p.wait_for_selector("#week button.day",timeout=10000);p.wait_for_timeout(120)
    if open_day and not p.locator("#panel.open").count(): p.click(f'button.day[data-d="{d}"]');p.wait_for_selector("#panel.open",timeout=5000);p.wait_for_timeout(100)
    return c,p
with sync_playwright() as pw:
    b=launch(pw)
    # ---- Change session ----
    c,p=fresh(b,THU)
    ok("one 'Change session' button; backup and swap are tucked away; no Log button",p.locator("#chg").inner_text()=="Change session" and p.locator("#alt").is_hidden() and p.locator("#swap").is_hidden() and p.locator("#tolog").count()==0)
    first=p.evaluate("()=>{var h=document.querySelector('#sess h2');return h.getBoundingClientRect().top+window.scrollY}")
    ok("the first block header starts within about one and a half screens",first<1300,first)
    p.click("#chg");p.wait_for_timeout(80)
    ok("tap: the options appear",p.locator("#alt").is_visible() and p.locator("#swap").is_visible() and p.locator("#chg").inner_text()=="Hide session options" and p.get_attribute("#chg","aria-expanded")=="true")
    p.click("#alt");p.wait_for_timeout(120)
    ok("backup chosen: the menu stays open with the way back, the Change button steps aside",p.locator("#alt").is_visible() and p.locator("#alt").inner_text().startswith("↩ Back to main") and p.locator("#chg").is_hidden() and "Backup" in p.locator("#ttl").inner_text())
    p.click("#alt");p.wait_for_timeout(120);p.click("#chg");p.wait_for_timeout(80)
    ok("back on main and collapsed again after Hide",p.locator("#alt").is_hidden() and p.locator("#chg").inner_text()=="Change session")
    opend(p,WED);ok("each day starts collapsed",p.locator("#chg").is_visible() and p.locator("#alt").is_hidden())
    opend(p,TUE);ok("a rest day with a backup still offers Change session",p.locator("#chg").is_visible() or p.locator("#dctl").is_hidden())
    c.close()
    c,p=fresh(b,THU,seed={"wo_alt":{THU:1}});ok("a day already on its backup opens with the way back showing",p.locator("#alt").is_visible() and p.locator("#chg").is_hidden());c.close()
    c,p=view(b,THU);ok("wo_chg=1 keeps the options open (what the older suites rely on)",p.locator("#alt").is_visible() and p.locator("#chg").is_hidden());c.close()
    # ---- opens on today when installed ----
    c,p=fresh(b,THU,open_day=False,standalone=True)
    ok("installed app: opens straight on today's session",p.locator("#panel.open").count()==1 and p.locator("#ttl").inner_text()=="Lower · Carry Medley" and p.evaluate("()=>__app.sel")==THU)
    c.close();c,p=fresh(b,THU,open_day=False)
    ok("browser tab: stays on the week view",p.locator("#panel.open").count()==0);c.close()
    # ---- yesterday not logged ----
    c,p=fresh(b,TUE,open_day=False)
    ok("yesterday's session is not logged: one line under the strip",p.locator("#ynag").is_visible() and p.locator("#ynag span").inner_text()=="Yesterday's Upper · Slow Is Strong is not logged." and p.locator("#ynag button").all_inner_texts()==["Log it","Skipped","Not now"],p.locator("#ynag").inner_text())
    p.click('#ynag [data-ng="log"]');p.wait_for_timeout(150)
    ok("Log it opens yesterday with the top question; the line steps aside",p.evaluate("()=>__app.sel")==MON and p.locator("#panel.open").count()==1 and p.locator("#topq").is_visible() and p.locator("#ynag").is_hidden())
    p.click("#close");p.wait_for_timeout(100);ok("still offered after closing",p.locator("#ynag").is_visible())
    p.click('#ynag [data-ng="x"]');p.wait_for_timeout(80);ok("Not now hides it for that day",p.locator("#ynag").is_hidden() and ls(p,"wo_nag")==MON)
    c.close();c,p=fresh(b,TUE,open_day=False);p.click('#ynag [data-ng="skip"]');p.wait_for_selector("#ov.show",timeout=3000);p.clock.fast_forward(1000);p.click("#o_done");p.wait_for_timeout(120)
    e=ls(p,"wo_log")[0];ok("Skipped logs yesterday as skipped in one tap",e["date"]==MON and e["oc"]=="skipped" and e["min"]==0 and p.locator("#ynag").is_hidden(),e)
    c.close();c,p=fresh(b,WED,open_day=False);ok("no line when yesterday was a rest day",p.locator("#ynag").is_hidden())
    c.close();c,p=fresh(b,TUE,seed={"wo_log":[{"date":MON,"name":"Upper · Slow Is Strong","type":"main","min":40,"sid":"upb0911"}]},open_day=False);ok("no line when yesterday is logged",p.locator("#ynag").is_hidden())
    ok("no page errors",not errs,errs);c.close();b.close()
exit(done())
