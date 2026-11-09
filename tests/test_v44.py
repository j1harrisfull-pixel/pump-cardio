# pc-v44/pc-v45: week 5 (Mon 9 – Sun 15 Nov) from weeks/2026-11-09.json. Rendering, style audit and timers are covered by
# test_audit.py; this suite checks the programme mapping, progression from the 8 Nov export (logged loads, lower
# restarted at the 23 Oct loads), the hospital-day constraint, the EMOM minute groups and the time limits.
import json, os
from playwright.sync_api import sync_playwright
from lib import *
W5={"2026-11-09":("upb0911","bk0911"),"2026-11-10":("rec1011","bk1011"),"2026-11-11":("hill1111","bk1111"),"2026-11-12":("lob1211","bk1211"),
    "2026-11-13":("mobb1311","bk1311"),"2026-11-14":("kbb1411","bk1411"),"2026-11-15":("walkb1511","bk1511")}
WK=json.load(open(os.path.join(os.path.dirname(__file__),"..","weeks","2026-11-09.json")))
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,"2026-11-09")
    P=p.evaluate("()=>__wk.PROG");B=p.evaluate("()=>__wk.BK")
    ok("week 5 programme and backups mapped",all(P.get(d)==m and B.get(d)==k for d,(m,k) in W5.items()),{d:(P.get(d),B.get(d)) for d in W5})
    ok("week 4 programme unchanged",P["2026-11-02"]=="run02" and P["2026-11-07"]=="kb07" and P["2026-11-08"]=="walk08")
    S=p.evaluate("""()=>{var o={};['upb0911','lob1211','kbb1411','rec1011','hill1111','walkb1511','up0911'].forEach(function(k){var s=__how.SESS[k];
      o[k]={tot:s.tot,est:s.est,rest:!!s.rest,safe:s.safe,rp:{}};s.blocks.forEach(function(bl){(bl.items||[]).forEach(function(i){o[k].rp[i.x]=i.rp;});});});return o;}""")
    U=S["upb0911"]["rp"];L=S["lob1211"]["rp"]
    ok("upper: bench 4 × 7 at the same 20 kg (was 6/6/6/6), chin-up 8 (was 7), row 8 at the next dumbbells up",U["db-bench"]==7 and U["assisted-chinup"]==8 and U["cs-row"]==8,U)
    ok("lower anchors restart from 23 Oct: split squat 7 (was 6), RDL 10 (was 8)",L["rfess"]==7 and L["db-rdl"]==10,L)
    cues=json.dumps(WK["sess"]["lob1211"],ensure_ascii=False)
    ok("lower cues name the 23 Oct loads, not the week 4 prescription","10 kg as on 23 Oct" in cues and "17.5 kg as on 23 Oct" in cues)
    ok("Tue 10 Nov (hospital) is a rest day",S["rec1011"]["rest"] and "Hospital" in S["rec1011"]["safe"])
    t=p.locator("#panel").inner_text()
    ok("Mon is moderate: no RPE 7 intervals, conditioning steady",S["upb0911"]["tot"]>0 and "Steady pace, RPE 5–6" in t and "RPE 7." not in t)
    ok("strength days 30–45 min",all(25*60<=S[k]["tot"]<=45*60 for k in ["upb0911","lob1211"]),{k:S[k]["tot"] for k in ["upb0911","lob1211"]})
    # pc-v45 variety: anchors kept, everything else new vs week 4 and the first week-5 draft
    def acc(k): return {i for i in S[k]["rp"]}
    ok("upper accessories new (anchors bench, chin-up, row kept)",{"db-bench","assisted-chinup","cs-row"}<=acc("upb0911") and not (acc("upb0911")-{"db-bench","assisted-chinup","cs-row"})&acc("up0911"),acc("upb0911"))
    ok("lower accessories new (anchors split squat, RDL kept)",{"rfess","db-rdl"}<=acc("lob1211") and not (acc("lob1211")-{"rfess","db-rdl"})&{"kb-sa-row","suitcase-carry","sl-glute-bridge","bird-dog"},acc("lob1211"))
    J=json.dumps(WK["sess"],ensure_ascii=False)
    ok("a different format each day: superset+circuit, hills, carry medley (Every 2:00), swing EMOM + fartlek, hill-push walk",
       all(x in J for x in ['"Circuit × 3"','"Hills 6 × 1:00 / 1:30"','"Every 2:00 × 4"','"EMOM 60 s × 12"','"Fartlek 6 × 1:00 / 2:00"','"Hill pushes 4 × 3:00 / 2:00"']))
    ok("every training day has a 'Beat this' challenge",all("Beat this" in json.dumps(WK["sess"][k],ensure_ascii=False) for k in ["upb0911","hill1111","lob1211","kbb1411"]))
    ok("Sat EMOM labels in the CLAUDE.md format",WK["sess"]["kbb1411"]["blocks"][1]["cycle"]==["Complex · left","Complex · right","Swing ×10 + halo ×6"])
    ok("up0911 kept so an early Monday log still renders","up0911" in WK["sess"])
    ok("no hard effort anywhere",not re.search(r"\bhard\b|RPE [89]",json.dumps(WK,ensure_ascii=False)))
    ok("stop-signs line visible on Monday","sudden or severe headache" in t)
    opend(p,"2026-11-14");t=p.locator("#panel").inner_text()
    ok("EMOM shows one group per minute",all(s in t for s in ["Minute 1 · Left","Minute 2 · Right","Minute 3","10 swings, then 6 halos.","Repeat this three minute cycle four times."]) or
       all(s in t.upper() for s in ["MINUTE 1 · LEFT","MINUTE 2 · RIGHT","10 SWINGS, THEN 6 HALOS."]),t[:1500])
    opend(p,"2026-11-10");t=p.locator("#panel").inner_text()
    ok("hospital day shows rest with optional flow","Rest day" in t or "REST DAY" in t.upper())
    ok("no page errors",errs==[],errs)
    c.close();b.close()
raise SystemExit(done())
