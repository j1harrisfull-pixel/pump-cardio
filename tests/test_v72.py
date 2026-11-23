# pc-v72: week 7 (Mon 23 – Sun 29 Nov) from weeks/2026-11-23.json. Checks the programme mapping, the one-step double
# progression from the last logs (8 Nov export, no newer log), that accessories, formats, kettlebell moves and runs differ
# from weeks 5 and 6 (no EMOM this week: density block, carry ladder, bell circuit), the 16 kg bell only, a Beat this on every
# training day and the time limits.
import json, os, re
from playwright.sync_api import sync_playwright
from lib import *
W7={"2026-11-23":("upe2311","bk2311"),"2026-11-24":("fls2411","bk2411"),"2026-11-25":("mob2511","bk2511"),"2026-11-26":("lov2611","bk2611"),
    "2026-11-27":("mob2711","bk2711"),"2026-11-28":("kbh2811","bk2811"),"2026-11-29":("wlk2911","bk2911")}
D=os.path.join(os.path.dirname(__file__),"..","weeks")
WK=json.load(open(os.path.join(D,"2026-11-23.json")));W5=json.load(open(os.path.join(D,"2026-11-09.json")));W6=json.load(open(os.path.join(D,"2026-11-16.json")))
TRAIN=["upe2311","fls2411","lov2611","kbh2811","wlk2911"]
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,"2026-11-23")
    P=p.evaluate("()=>__wk.PROG");B=p.evaluate("()=>__wk.BK")
    ok("week 7 programme and backups mapped",all(P.get(d)==m and B.get(d)==k for d,(m,k) in W7.items()),{d:(P.get(d),B.get(d)) for d in W7})
    ok("week 6 programme unchanged",P["2026-11-16"]=="upd1611" and P["2026-11-19"]=="lot1911" and P["2026-11-21"]=="kbr2111")
    S=p.evaluate("""()=>{var o={};['upe2311','fls2411','mob2511','lov2611','mob2711','kbh2811','wlk2911'].forEach(function(k){var s=__how.SESS[k];
      o[k]={tot:s.tot,rest:!!s.rest,rp:{}};s.blocks.forEach(function(bl){(bl.items||[]).forEach(function(i){o[k].rp[i.x]=i.rp;});});});return o;}""")
    U=S["upe2311"]["rp"];L=S["lov2611"]["rp"]
    ok("upper anchors by one conservative step from the last logs: bench 8 at 20 kg (log 6), chin-up 8 (log 7), row 8 at 20 kg",U["db-bench"]==8 and U["assisted-chinup"]==8 and U["cs-row"]==8,U)
    ok("lower anchors: split squat 8 each side (log 6), RDL 10 (log 8)",L["rfess"]==8 and L["db-rdl"]==10,L)
    J=json.dumps(WK["sess"],ensure_ascii=False)
    ok("anchor cues name the logged loads","20 kg each hand, 8 reps (last log 6/6/6/6" in J and "10 kg as last logged" in J and "17.5 kg as last logged" in J)
    def acc(w,k): return {i["x"] for bl in w["sess"][k]["blocks"] for i in bl.get("items",[])}
    anch={"db-bench","assisted-chinup","cs-row","rfess","db-rdl"}
    old_up=acc(W5,"upb0911")|acc(W5,"up0911")|acc(W6,"upd1611");old_lo=acc(W5,"lob1211")|acc(W6,"lot1911")
    ok("upper accessories new vs weeks 5 and 6",not (acc(WK,"upe2311")-anch)&old_up,acc(WK,"upe2311"))
    ok("lower accessories new vs weeks 5 and 6",not (acc(WK,"lov2611")-anch)&old_lo,acc(WK,"lov2611"))
    J56=json.dumps([W5["sess"],W6["sess"]],ensure_ascii=False)
    ok("formats new: density block, pickups, carry ladder, bell circuit, gentle hills, walk pickups",
       all(x in J for x in ['"Pickups 4 × 1:30 / 2:30"','"Gentle hills 5 × 0:45 / 1:45"','"Walk pickups 5 × 2:00 / 2:00"','"Density block 8:00"','"Carry ladder"','"Press + squat bell circuit"']) and all(x not in J56 for x in ["Pickups 4 ×","Gentle hills","Walk pickups","Density block","Carry ladder","amrap"]))
    ok("no EMOM this week (weeks 5 and 6 each had two)",not any(bl["k"]=="emom" and bl["h"].startswith("EMOM") for s in WK["sess"].values() for bl in s["blocks"]))
    em=lambda w,k:{x.split(" – ")[0] for bl in w["sess"][k]["blocks"] if bl["k"] in("emom","core") for x in bl["list"]}
    ok("Saturday kettlebell moves are new (press, deadlift, front-rack squat)",not (em(WK,"kbh2811")-{"Kettlebell swing"})&(em(W5,"kbb1411")|em(W6,"kbr2111"))-{"Kettlebell swing"},em(WK,"kbh2811"))
    ok("one 16 kg kettlebell only: no other kettlebell weight named",not re.search(r"(2[04]|12|8) kg (kettle)?bell",J) and "24 kg" not in J,re.findall(r"\d+ kg[^\"]{0,20}",J)[:8])
    lad=[bl for bl in WK["sess"]["lov2611"]["blocks"] if bl.get("id")=="l26lad"][0]
    ok("carry ladder climbs 20 → 50 m and 4 → 10 sumo deadlifts over four 2:00 rungs",lad["h"]=="Every 2:00 × 4" and len(lad["cycle"])==4 and lad["cycle"][0].startswith("Farmer's carry 20 m") and lad["cycle"][3].endswith("×10"))
    ok("every training day has a 'Beat this' challenge",all("Beat this" in json.dumps(WK["sess"][k],ensure_ascii=False) for k in TRAIN))
    ok("no hard effort, no paces",not re.search(r"\bhard\b|RPE [89]|min/km|km/h|\bbrisk\b|\bjog\b",json.dumps(WK,ensure_ascii=False).replace('"JOG"','')))
    ok("Wed and Fri are optional recovery days",S["mob2511"]["rest"] and S["mob2711"]["rest"])
    ok("training sessions 35–46 min",all(35*60<=S[k]["tot"]<=46*60 for k in TRAIN),{k:S[k]["tot"] for k in TRAIN})
    t=p.locator("#panel").inner_text()
    ok("Monday: stop-signs line and Beat this visible","sudden or severe headache" in t and "Beat this: more rounds" in t)
    ok("Monday density block shown with its round",all(s in t for s in ["Density block 8:00","hammer curl ×8 each side, incline push-up ×6, wall slide ×8"]),t[:1500])
    ok("Monday density block is an AMRAP (round counter and score)",p.evaluate("()=>{var b=__how.SESS.upe2311.blocks.filter(function(x){return x.id=='u23dn'})[0];return !!b&&b.amrap==1&&b.segs.length==1&&b.segs[0][1]==480;}"))
    c.close()
    c,p=view(b,"2026-11-26");t=p.locator("#panel").inner_text()
    ok("Thursday: carry ladder and hip airplane shown, stop signs","Carry ladder" in t and "hip airplane" in t.lower() and "sudden or severe headache" in t,t[:1500])
    c.close()
    c,p=view(b,"2026-11-28");t=p.locator("#panel").inner_text()
    ok("Saturday: bell circuit then gentle hills","Press + squat bell circuit" in t and "Gentle hills 5 × 0:45 / 1:45" in t,t[:1500])
    c.close()
    c,p=view(b,"2026-11-24");t=p.locator("#panel").inner_text()
    ok("Tuesday run has the Actual card and pickups","Pickups 4 × 1:30 / 2:30" in t and ("Actual" in t or "ACTUAL" in t))
    ok("no page errors",errs==[],errs)
    c.close();b.close()
raise SystemExit(done())
