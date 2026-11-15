# pc-v71: week 6 (Mon 16 – Sun 22 Nov) from weeks/2026-11-16.json. Rendering, style audit and timers are covered by
# test_audit.py; this suite checks the programme mapping, double progression from the last logs (8 Nov export, no newer
# log), that accessories, formats, kettlebell moves and runs differ from week 5, the 16 kg bell only, the EMOM minute
# groups, a Beat this on every training day and the time limits.
import json, os, re
from playwright.sync_api import sync_playwright
from lib import *
W6={"2026-11-16":("upd1611","bk1611"),"2026-11-17":("str1711","bk1711"),"2026-11-18":("mob1811","bk1811"),"2026-11-19":("lot1911","bk1911"),
    "2026-11-20":("mob2011","bk2011"),"2026-11-21":("kbr2111","bk2111"),"2026-11-22":("wlk2211","bk2211")}
D=os.path.join(os.path.dirname(__file__),"..","weeks")
WK=json.load(open(os.path.join(D,"2026-11-16.json")));W5=json.load(open(os.path.join(D,"2026-11-09.json")))
TRAIN=["upd1611","str1711","lot1911","kbr2111","wlk2211"]
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,"2026-11-16")
    P=p.evaluate("()=>__wk.PROG");B=p.evaluate("()=>__wk.BK")
    ok("week 6 programme and backups mapped",all(P.get(d)==m and B.get(d)==k for d,(m,k) in W6.items()),{d:(P.get(d),B.get(d)) for d in W6})
    ok("week 5 programme unchanged",P["2026-11-09"]=="upb0911" and P["2026-11-12"]=="lob1211" and P["2026-11-14"]=="kbb1411")
    S=p.evaluate("""()=>{var o={};['upd1611','str1711','mob1811','lot1911','mob2011','kbr2111','wlk2211'].forEach(function(k){var s=__how.SESS[k];
      o[k]={tot:s.tot,rest:!!s.rest,rp:{}};s.blocks.forEach(function(bl){(bl.items||[]).forEach(function(i){o[k].rp[i.x]=i.rp;});});});return o;}""")
    U=S["upd1611"]["rp"];L=S["lot1911"]["rp"]
    ok("upper anchors by double progression from the last logs: bench 7 at 20 kg (log 6), chin-up 8 (log 7), row 8 at 20 kg",U["db-bench"]==7 and U["assisted-chinup"]==8 and U["cs-row"]==8,U)
    ok("lower anchors: split squat 7 each side (log 6), RDL 10 (log 8)",L["rfess"]==7 and L["db-rdl"]==10,L)
    J=json.dumps(WK["sess"],ensure_ascii=False)
    ok("anchor cues name the logged loads","20 kg each hand, 7 reps (last log 6/6/6/6" in J and "10 kg as last logged" in J and "17.5 kg as last logged" in J)
    def acc(w,k): return {i["x"] for bl in w["sess"][k]["blocks"] for i in bl.get("items",[])}
    up5=acc(W5,"upb0911")|acc(W5,"up0911");lo5=acc(W5,"lob1211")
    ok("upper accessories new vs week 5",not (acc(WK,"upd1611")-{"db-bench","assisted-chinup","cs-row"})&up5,acc(WK,"upd1611"))
    ok("lower accessories new vs week 5",not (acc(WK,"lot1911")-{"rfess","db-rdl"})&lo5,acc(WK,"lot1911"))
    J5=json.dumps(W5["sess"],ensure_ascii=False)
    ok("formats new: push-pull EMOM, strides, tri-set + circuit, clean + lunge EMOM, progression run, long walk",
       all(x in J for x in ['"EMOM 60 s × 8"','"Strides 6 × 0:20 / 1:00"','"B · Tri-set"','"Circuit × 3"','"EMOM 60 s × 9"','"Build to steady"']) and "Strides" not in J5 and "Tri-set" not in J5)
    em5=set(W5["sess"]["kbb1411"]["blocks"][1]["list"]);em6=set(WK["sess"]["kbr2111"]["blocks"][1]["list"])
    ok("Saturday kettlebell complex is new (clean + front-rack reverse lunge)",not {x.split(" – ")[0] for x in em6 if "each side" in x}&{x.split(" – ")[0] for x in em5},em6)
    ok("one 16 kg kettlebell only: no other kettlebell weight named",not re.search(r"(2[04]|12|8) kg (kettle)?bell",J) and "24 kg" not in J,re.findall(r"\d+ kg[^\"]{0,20}",J)[:8])
    ok("EMOM labels in the CLAUDE.md format",WK["sess"]["kbr2111"]["blocks"][1]["cycle"]==["Complex · left","Complex · right","Swing ×12 + push-up ×6"])
    ok("every training day has a 'Beat this' challenge",all("Beat this" in json.dumps(WK["sess"][k],ensure_ascii=False) for k in TRAIN))
    ok("no hard effort, no paces",not re.search(r"\bhard\b|RPE [89]|min/km|km/h",json.dumps(WK,ensure_ascii=False)))
    ok("Wed and Fri are optional recovery days",S["mob1811"]["rest"] and S["mob2011"]["rest"])
    ok("training sessions 35–46 min",all(35*60<=S[k]["tot"]<=46*60 for k in TRAIN),{k:S[k]["tot"] for k in TRAIN})
    t=p.locator("#panel").inner_text()
    ok("Monday: stop-signs line and Beat this visible","sudden or severe headache" in t and "Beat this: 20 s spare" in t)
    ok("Monday EMOM shows one group per minute",all(s in t.upper() for s in ["MINUTE 1","8 PULLOVERS, THEN 8 INCLINE PUSH UPS.","REPEAT THIS ONE MINUTE CYCLE EIGHT TIMES."]),t[:800])
    c.close()
    c,p=view(b,"2026-11-21");t=p.locator("#panel").inner_text()
    ok("Saturday EMOM: left, right, swings + push-ups by minute",all(s in t.upper() for s in ["MINUTE 1 · LEFT","MINUTE 2 · RIGHT","MINUTE 3","12 SWINGS, THEN 6 INCLINE PUSH UPS."]),t[:1500])
    c.close()
    c,p=view(b,"2026-11-17");t=p.locator("#panel").inner_text()
    ok("Tuesday run has the Actual card and strides","Strides 6 × 0:20 / 1:00" in t and ("Actual" in t or "ACTUAL" in t))
    ok("no page errors",errs==[],errs)
    c.close();b.close()
raise SystemExit(done())
