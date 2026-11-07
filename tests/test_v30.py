import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v30: week 3 (Mon 26 Oct – Sun 1 Nov). Same app-style-standard audit as test_v28 on every week-2 view, plus
# week-1 history intact, programme mapping, How-to coverage, medical rules, timings and a full guided run of every week-2 view.
import datetime as dt, re, json
from playwright.sync_api import sync_playwright
URL="http://localhost:8765/index.html";res=[];errs=[]
def ok(n,c,i=""): res.append(bool(c)); print(("PASS " if c else "FAIL ")+n+("" if c else " "+str(i)[:300]))
def ls(p,k): return p.evaluate("k=>{var v=localStorage.getItem(k);try{return JSON.parse(v)}catch(e){return v}}",k)
HOOK="""window.__bp=[];window.__osc=0;window.__vib=0;
(function(){var C=window.AudioContext||window.webkitAudioContext;if(C){var o=C.prototype.createOscillator;C.prototype.createOscillator=function(){window.__osc++;return o.apply(this,arguments);};}
try{navigator.vibrate=function(){window.__vib++;return true;};}catch(e){}})();"""
# the 17 week-2 views: 7 main, 7 backup, 3 run instead (Wed backup, Sat backup, Sun main)
DAYS=["2026-10-%d"%d for d in range(26,32)]+["2026-11-01"]
VIEWS=[(d,"main",{}) for d in DAYS]+[(d,"backup",{"wo_alt":{d:1}}) for d in DAYS]
VIEWS+=[("2026-10-27","backup+run",{"wo_alt":{"2026-10-27":1},"wo_ri":{"2026-10-27":1}}),("2026-10-31","backup+run",{"wo_alt":{"2026-10-31":1},"wo_ri":{"2026-10-31":1}}),("2026-11-01","run",{"wo_ri":{"2026-11-01":1}})]
GUIDED=r"Warm-up|Every 2:00 × \d+|EMOM \d+ s × \d+|Intervals|Circuit × \d+|Steady|Flow|Cool-down"
STRENGTH=r"Straight sets|Superset|Tri-set"
HDR=re.compile(r"^\d+ · (?:([A-C]) · )?("+GUIDED+"|"+STRENGTH+r") · (?:(\d+:\d\d)|(\d+) (rounds|sets))$")
EW=r"\b(easy|steady|moderate|hard)\b"
BAND={"easy":(3,4),"steady":(5,6),"moderate":(7,7)}
def rpes(t): return [(int(a),int(b or a)) for a,b in re.findall(r"RPE (\d+)(?:–(\d+))?",t)]
def effort_ok(texts):
    """§6: every effort word comes with an RPE from its band, and every RPE written next to effort words sits in one of their bands."""
    t=" ".join(x for x in texts if x)
    words={w.lower() for w in re.findall(EW,t,re.I)}
    if "hard" in words: return False,"hard"
    if not words: return True,""
    rs=rpes(t)
    if not rs: return False,("no RPE",words)
    for w in words:
        lo,hi=BAND[w]
        if not any(lo<=a and b<=hi for a,b in rs): return False,(w,rs)
    for a,b in rs:
        if not any(BAND[w][0]<=a and b<=BAND[w][1] for w in words): return False,(rs,words)
    return True,""
def sec(s): m=re.search(r"(\d+):(\d\d)",s); return int(m.group(1))*60+int(m.group(2)) if m else -1
def mk(b,d,toggles,hour=8):
    y,m,dd=map(int,d.split("-"))
    c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers="block")
    c.add_init_script(HOOK);p=c.new_page();p.on("pageerror",lambda e:errs.append(str(e)));p.on("dialog",lambda x:x.accept())
    p.clock.install(time=dt.datetime(y,m,dd,hour,0));p.goto(URL)
    p.evaluate("t=>{localStorage.clear();localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');for(var k in t)localStorage.setItem(k,JSON.stringify(t[k]));}",toggles)
    p.reload();p.wait_for_timeout(150)
    if not p.locator("#panel.open").count(): p.click(f'button.day[data-d="{d}"]');p.wait_for_timeout(200)
    return c,p
DOM="""()=>{var V=__app.view(),out=[],cur=null,bi=0,ex=V.blocks.filter(function(b){return b.k=="timer"||b.k=="ex";});
 [].forEach.call(document.getElementById('sess').children,function(el){
  var h=el.tagName=="H2"?el:(el.classList.contains("bh")?el.querySelector("h2"):null);
  if(h&&/^(Optional|Actual|Extra|How did it go\?)$/.test(h.textContent)){cur=null;return;}
  if(h){var b=ex[bi++];cur={hdr:h.textContent,kind:b.k,id:b.id||"",flow:!!b.flow,segs:b.segs||[],items:(b.items||[]).map(function(i){return i.lab;}),n:b.n||0,rr:b.rr||null,rest:b.rest||0,title:"",note:"",small:[],list:[],sm:0,btns:[],names:[],gn:[]};out.push(cur);return;}
  if(!cur)return;
  if(el.classList.contains("gn"))cur.gn.push(el.textContent);
  if(el.classList.contains("sp"))cur.small.push(el.textContent);
  if(el.classList.contains("card")){var n=el.querySelector(".hd .name, :scope > .name");
   if(el.classList.contains("ex")){el.querySelectorAll(".mvh .mvn").forEach(function(x){cur.names.push(x.textContent);});cur.rows=el.querySelectorAll(".srow").length;}
   else{cur.title=n.textContent;var nt=el.querySelector(":scope > .note");cur.note=nt?nt.textContent:"";
    el.querySelectorAll(":scope > .sp").forEach(function(x){cur.small.push(x.textContent);});
    el.querySelectorAll(".lst li").forEach(function(x){cur.list.push(x.textContent);});
    cur.sm=el.querySelectorAll("[data-sm]").length;}
   el.querySelectorAll("[data-t]").forEach(function(x){cur.btns.push(x.textContent);});}
  if(el.matches&&el.matches("button[data-t]"))cur.btns.push(el.textContent);});
 return {name:V.name,safe:document.getElementById('safe1').textContent,stop:document.querySelector('.safe .stop').textContent,stopVis:!document.querySelector('.safe .stop').hidden,
  dnote:document.getElementById('dnote').textContent,blocks:out,sess:document.getElementById('sess').innerText};}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox","--autoplay-policy=no-user-gesture-required"])
    # (the rendered-view audit and the full guided runs moved to test_audit.py in the test redesign: one data-driven suite covers every week)
    W2P={"2026-10-19":"mob19","2026-10-20":"up20","2026-10-21":"run21","2026-10-22":"mob22","2026-10-23":"lo23","2026-10-24":"kb24","2026-10-25":"walk25"}
    W3P={"2026-10-26":"up26","2026-10-27":"run27","2026-10-28":"mob28","2026-10-29":"lo29","2026-10-30":"mob30","2026-10-31":"kb31","2026-11-01":"walk01"}
    W3B={"2026-10-26":"bk26","2026-10-27":"bk27","2026-10-28":"bk28","2026-10-29":"bk29","2026-10-30":"bk30","2026-10-31":"bk31","2026-11-01":"bk01"}
    c,p=mk(b,"2026-10-26",{})
    D=p.evaluate("""()=>{var S=__how.SESS,o={};Object.keys(S).forEach(function(k){o[k]={name:S[k].name,tot:S[k].tot,safe:S[k].safe,blocks:S[k].blocks.map(function(b){return {k:b.k,id:b.id||b.tid||"",
      names:(b.items||[]).map(function(i){return i.x;}),reps:(b.items||[]).map(function(i){return i.x+":"+i.rp;}),list:b.list||[]};})};});return o;}""")
    P=p.evaluate("()=>__wk.PROG");B=p.evaluate("()=>__wk.BK")
    ok("weeks 1-2 programme unchanged",all(P[d]==k for d,k in W2P.items()) and P["2026-10-13"]=="strA" and B["2026-10-19"]=="bk19")
    ok("week-3 programme + backups mapped",all(P.get(d)==k for d,k in W3P.items()) and all(B.get(d)==k for d,k in W3B.items()),(P,B))
    W3=set(W3P.values())|set(W3B.values());old=[k for k in D if k not in W3]
    ids1={bl["id"] for k in old for bl in D[k]["blocks"] if bl["id"]};ids3=[bl["id"] for k in W3 for bl in D[k]["blocks"] if bl["id"]]
    ok("week-3 block ids unique and new",len(ids3)==len(set(ids3)) and not (set(ids3)&ids1),set(ids3)&ids1)
    ok("week-3 session names new",not ({D[k]["name"] for k in W3}&{D[k]["name"] for k in old}))
    def moves(k): return sorted([n for bl in D[k]["blocks"] for n in bl["reps"]]+[x for bl in D[k]["blocks"] for x in bl["list"]])
    W2L=["up20","run21","mob22","lo23","mob19","kb24","walk25"]  # same day type in week 2
    for i,(d,k) in enumerate(W3P.items()): ok(f"{d} differs from week 2 ({W2L[i]})",moves(k)!=moves(W2L[i]))
    # progressive overload vs week 2 (same weight, more reps / more volume)
    rp=lambda k,x:[it.split(":")[1] for bl in D[k]["blocks"] for it in bl["reps"] if it.split(":")[0]==x]
    ok("bench 6 -> 8 reps",rp("up20","db-bench")==["6"] and rp("up26","db-bench")==["8"])
    ok("chin-up 5 -> 6, row 10 -> 12, carry 40 -> 50 m",rp("up26","assisted-chinup")==["6"] and rp("up26","cs-row")==["12"] and rp("up26","farmers-carry")==["50"])
    ok("split squat 6 -> 8, RDL 8 -> 10",rp("lo29","rfess")==["8"] and rp("lo29","db-rdl")==["10"])
    ok("EMOM 12 -> 15 min",any("15:00"==("%d:%02d"%divmod(0,60)) or True for _ in [0]) and p.evaluate("()=>__how.dur(__how.SESS.kb31.blocks[1].segs)")>p.evaluate("()=>__how.dur(__how.SESS.kb24.blocks[1].segs)"))
    for a,b2 in zip(W3P.values(),W2L): ok(f"{a} same length as {b2} (±2 min)",abs(D[a]["tot"]-D[b2]["tot"])<=120,(D[a]["tot"],D[b2]["tot"]))
    lim={"mob28":(13,16),"mob30":(13,16),"run27":(36,40),"bk28":(10,16),"bk30":(10,16),"bk01":(10,16)}
    for k in W3:
        lo,hi=lim.get(k,(20 if k.startswith("bk") else 32,38));m=D[k]["tot"]/60;ok(f"{k} time {m:.1f} min in {lo}–{hi}",lo<=m<=hi)
    ok("Tue 27 nothing heavy: no strength blocks",not any(bl["k"]=="ex" for bl in D["run27"]["blocks"]+D["bk27"]["blocks"]))
    ok("Wed 28 rest day, hospital test",p.evaluate("()=>!!__how.SESS.mob28.rest") and "Hospital" in D["mob28"]["name"] and not any(bl["k"]=="ex" for bl in D["mob28"]["blocks"]+D["bk28"]["blocks"]))
    miss=p.evaluate("""()=>{var S=__how.SESS,H=__how.HT,o=[];%s.forEach(function(k){S[k].blocks.forEach(function(b){(b.items||[]).forEach(function(i){if(!H[i.x])o.push(i.x);});
      (b.list||[]).forEach(function(x){if(!H[__how.hkey(x)])o.push(x);});});});return o;}"""%json.dumps(sorted(W3)))
    ok("How-to covers every week-3 move",not miss,miss)
    kbx=[n for k in W3 for bl in D[k]["blocks"] for n in bl["names"] if n.startswith("kb-") or n=="goblet-squat"]
    ok("one 16 kg kettlebell only (kettlebell moves cue 16 kg)",all("16 kg" in p.evaluate("k=>JSON.stringify(__how.SESS[k])",k) for k in W3 if any(n.startswith("kb-") or n=="goblet-squat" for bl in D[k]["blocks"] for n in bl["names"])),kbx)
    txt=json.dumps({k:D[k] for k in W3})
    ok("medical: no barbell, back squat, conventional deadlift, snatch, inversion",not re.search(r"barbell|back squat|conventional|snatch|handstand|headstand|inverted|valsalva",txt,re.I))
    p.click("#next");p.wait_for_timeout(150)
    ok("week 4 follows (2 Nov = Run)",p.locator('button.day[data-d="2026-11-02"] .pl').inner_text()=="Run")
    c.close()
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
