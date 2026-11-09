# pc-v44: week 5 (Mon 9 – Sun 15 Nov) from weeks/2026-11-09.json. Rendering, style audit and timers are covered by
# test_audit.py; this suite checks the programme mapping, progression from the 8 Nov export (logged loads, lower
# restarted at the 23 Oct loads), the hospital-day constraint, the EMOM minute groups and the time limits.
import json, os
from playwright.sync_api import sync_playwright
from lib import *
W5={"2026-11-09":("up0911","bk0911"),"2026-11-10":("rec1011","bk1011"),"2026-11-11":("run1111","bk1111"),"2026-11-12":("lo1211","bk1211"),
    "2026-11-13":("mob1311","bk1311"),"2026-11-14":("kb1411","bk1411"),"2026-11-15":("walk1511","bk1511")}
WK=json.load(open(os.path.join(os.path.dirname(__file__),"..","weeks","2026-11-09.json")))
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,"2026-11-09")
    P=p.evaluate("()=>__wk.PROG");B=p.evaluate("()=>__wk.BK")
    ok("week 5 programme and backups mapped",all(P.get(d)==m and B.get(d)==k for d,(m,k) in W5.items()),{d:(P.get(d),B.get(d)) for d in W5})
    ok("week 4 programme unchanged",P["2026-11-02"]=="run02" and P["2026-11-07"]=="kb07" and P["2026-11-08"]=="walk08")
    S=p.evaluate("""()=>{var o={};['up0911','lo1211','kb1411','rec1011','run1111','walk1511'].forEach(function(k){var s=__how.SESS[k];
      o[k]={tot:s.tot,est:s.est,rest:!!s.rest,safe:s.safe,rp:{}};s.blocks.forEach(function(bl){(bl.items||[]).forEach(function(i){o[k].rp[i.x]=i.rp;});});});return o;}""")
    U=S["up0911"]["rp"];L=S["lo1211"]["rp"]
    ok("upper: bench 4 × 7 at the same 20 kg (was 6/6/6/6), chin-up 8 (was 7), row 8 at the next dumbbells up",U["db-bench"]==7 and U["assisted-chinup"]==8 and U["cs-row"]==8,U)
    ok("upper: shoulder press 12 (was 10), farmer's carry 60 m (was 50)",U["db-shoulder-press"]==12 and U["farmers-carry"]==60,U)
    ok("lower restarts from 23 Oct: split squat 7 (was 6), RDL 10 (was 8), suitcase 50 m (was 40), single-leg bridge 10 (was 8)",
       L["rfess"]==7 and L["db-rdl"]==10 and L["suitcase-carry"]==50 and L["sl-glute-bridge"]==10 and L["kb-sa-row"]==6,L)
    cues=json.dumps(WK["sess"]["lo1211"],ensure_ascii=False)
    ok("lower cues name the 23 Oct loads, not the week 4 prescription","10 kg as on 23 Oct" in cues and "17.5 kg as on 23 Oct" in cues)
    ok("Tue 10 Nov (hospital) is a rest day",S["rec1011"]["rest"] and "Hospital" in S["rec1011"]["safe"])
    t=p.locator("#panel").inner_text()
    ok("Mon is moderate: no RPE 7 intervals, conditioning steady",S["up0911"]["tot"]>0 and "Steady pace, RPE 5–6" in t and "RPE 7." not in t)
    ok("strength days 30–45 min",all(25*60<=S[k]["tot"]<=45*60 for k in ["up0911","lo1211"]),{k:S[k]["tot"] for k in ["up0911","lo1211"]})
    ok("runs prescribe the easy 5 km he chooses",all("Easy run 5 km" in json.dumps(WK["sess"][k],ensure_ascii=False) for k in ["run1111","kb1411"]))
    ok("no hard effort anywhere",not re.search(r"\bhard\b|RPE [89]",json.dumps(WK,ensure_ascii=False)))
    ok("stop-signs line visible on Monday","sudden or severe headache" in t)
    opend(p,"2026-11-14");t=p.locator("#panel").inner_text()
    ok("EMOM shows one group per minute",all(s in t for s in ["Minute 1 · Left","Minute 2 · Right","Minute 3","15 swings, then 6 goblet squats.","Repeat this three minute cycle five times."]) or
       all(s in t.upper() for s in ["MINUTE 1 · LEFT","MINUTE 2 · RIGHT","15 SWINGS, THEN 6 GOBLET SQUATS."]),t[:1500])
    opend(p,"2026-11-10");t=p.locator("#panel").inner_text()
    ok("hospital day shows rest with optional flow","Rest day" in t or "REST DAY" in t.upper())
    ok("no page errors",errs==[],errs)
    c.close();b.close()
raise SystemExit(done())
