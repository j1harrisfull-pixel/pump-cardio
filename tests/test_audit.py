import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
# Data-driven audit of every session view in the programme (main, backup, quick option, run instead):
# app-style-standard.md on the rendered DOM, every guided block run to the end (fast clock), the EMOM minute groups,
# and the per-week data rules (How-to coverage, medical wording, timer shape). Reads the weeks from the app's own
# PROG / BK / QK tables, so a new week is covered without a new suite.
#   WEEK=current  only the latest week (the fast tier)   ·   default: every week
from playwright.sync_api import sync_playwright
from lib import *
import re
with sync_playwright() as pw:
    b=launch(pw)
    c,p=view(b,"2026-10-13",open_day=False)
    WK=weeks(p)
    if os.environ.get("WEEK")=="current": WK=WK[-1:]
    allviews=[(w,)+v for w in WK for v in week_views(p,w)]
    c.close()
    ok(f"{len(WK)} week(s), {len(allviews)} views in the data",len(allviews)>=7)
    dev=[];ran={};counts={}
    for w,d,ty,tg in allviews:
        c,p=view(b,d,tg);V=read_view(p);vw=f"{d} {ty} ({V['name']})"
        ok(f"{vw} renders",len(V["blocks"])>0)
        audit_view(vw,V,dev)
        # guided blocks: run each distinct block once (same id + segments across views = same engine run)
        for tid in V["tids"]:
            segs=next((bl["segs"] for bl in V["blocks"] if bl["id"]==tid),None)
            key=tid+"|"+json.dumps(segs)[:300]
            if key in ran: continue
            r=run_block(p,tid,d);ran[key]=1
            good=r["drops"] and r["beeps"]>=len(r["segs"]) and r["osc"]>=len(r["segs"]) and r["done"] and not r["ask"]
            ok(f"{vw}/{tid}: counts down, beeps on every segment ({len(r['segs'])}), logged done",good,(r["first"],r["beeps"],r["osc"],r["done"],r["ask"]))
            if p.locator("#bar.show").count(): p.click("#stop")
        ok(f"{vw}: no vibrate calls",p.evaluate("window.__vib")==0)
        c.close()
    ok(f"standard audit: 0 deviations across {len(allviews)} views",not dev,len(dev))
    for x in dev[:40]: print("   DEVIATION",x)
    # ---- data rules over every session (cheap: reads SESS once)
    c,p=view(b,"2026-10-13",open_day=False)
    D=p.evaluate("""()=>{var S=__how.SESS,H=__how.HT,o={};Object.keys(S).forEach(function(k){var s=S[k];o[k]={name:s.name,rest:!!s.rest,tot:s.tot,txt:JSON.stringify(s),
      blocks:s.blocks.map(function(b){var t=b.timer||b;return {h:b.h||b.k,k:b.k,id:t.id||b.id||"",flow:!!b.flow,segs:t.segs||[],
        nohow:(b.items||[]).map(function(i){return i.x;}).filter(function(x){return !H[x];}).concat((b.list||[]).filter(function(x){return !H[__how.hkey(x)];})),
        plan:(b.k=="timer"&&/^EMOM/.test(b.h||""))?__app.emomPlan(b):null,list:b.list||[]};})};});return o;}""")
    miss=[k+":"+x for k,s in D.items() for bl in s["blocks"] for x in bl["nohow"]]
    ok("How-to covers every move in every session",not miss,miss[:6])
    bad=[k for k,s in D.items() if re.search(r"barbell|back squat|conventional deadlift|snatch|handstand|headstand|inverted|valsalva",s["txt"],re.I)]
    ok("medical: no barbell, back squat, conventional deadlift, snatch or inversion anywhere",not bad,bad)
    for k,s in D.items():
        for bl in s["blocks"]:
            g=bl["segs"]
            if len(g)<2: continue
            ok(f"{k}/{bl['h']}: no trailing rest, no READY prep, no switch labels",g[-1][0] not in ("REST","READY") and not [x for x in g if x[0]=="READY"] and not [x for x in g if re.search(r"per side|switch →",str(x[2]))],[x[:3] for x in g][-2:])
            if bl["plan"]:
                pl=bl["plan"];reps=sorted(set(int(re.search(r"×(\d+)",x).group(1)) for x in bl["list"] if re.search(r"×(\d+)",x)));used=sorted(set(m["reps"] for q in pl["cycle"] for m in q["mv"] if m["reps"] is not None))
                ok(f"{k}/{bl['id']}: EMOM groups follow the rotation ({pl['p']} × {pl['reps']}), reps unchanged, no 'each side'",pl["p"]*pl["reps"]==len(g) and used==reps and not re.search(r"each side|no rest",json.dumps(pl["cycle"])),(pl["p"],pl["reps"],used,reps))
    c.close()
    ok("no page errors",not errs,errs[:3])
    b.close()
sys.exit(done())
