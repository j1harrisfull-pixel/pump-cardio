import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v32: week 4 (Mon 2 – Sun 8 Nov). Same app-style-standard audit as test_v28 on every week-2 view, plus
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
DAYS=["2026-11-0%d"%d for d in range(2,9)]
VIEWS=[(d,"main",{}) for d in DAYS]+[(d,"backup",{"wo_alt":{d:1}}) for d in DAYS]
VIEWS+=[("2026-11-07","backup+run",{"wo_alt":{"2026-11-07":1},"wo_ri":{"2026-11-07":1}}),("2026-11-08","run",{"wo_ri":{"2026-11-08":1}})]
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
    p.evaluate("t=>{localStorage.clear();localStorage.setItem('wo_chg','1');localStorage.setItem('wo_flat','1');localStorage.setItem('wo_startdate','\"2026-10-10\"');localStorage.setItem('wo_ver','12');for(var k in t)localStorage.setItem(k,JSON.stringify(t[k]));}",toggles)
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
    W3P={"2026-10-26":"up26","2026-10-27":"run27","2026-10-28":"mob28","2026-10-29":"lo29","2026-10-30":"mob30","2026-10-31":"kb31","2026-11-01":"walk01"}
    W4P={"2026-11-02":"run02","2026-11-03":"up03","2026-11-04":"mob04","2026-11-05":"lo05","2026-11-06":"mob06","2026-11-07":"kb07","2026-11-08":"walk08"}
    W4B={d:"bk0%d"%int(d[-1]) for d in W4P}
    c,p=mk(b,"2026-11-02",{})
    D=p.evaluate("""()=>{var S=__how.SESS,o={};Object.keys(S).forEach(function(k){o[k]={name:S[k].name,tot:S[k].tot,safe:S[k].safe,blocks:S[k].blocks.map(function(b){return {k:b.k,id:b.id||b.tid||"",
      names:(b.items||[]).map(function(i){return i.x;}),reps:(b.items||[]).map(function(i){return i.x+":"+i.rp;}),list:b.list||[]};})};});return o;}""")
    P=p.evaluate("()=>__wk.PROG");B=p.evaluate("()=>__wk.BK")
    ok("weeks 1-3 programme unchanged",all(P[d]==k for d,k in W3P.items()) and P["2026-10-13"]=="strA" and P["2026-10-20"]=="up20" and B["2026-11-01"]=="bk01")
    ok("week-4 programme + backups mapped",all(P.get(d)==k for d,k in W4P.items()) and all(B.get(d)==k for d,k in W4B.items()),(P,B))
    W4=set(W4P.values())|set(W4B.values());old=[k for k in D if k not in W4]
    ids1={bl["id"] for k in old for bl in D[k]["blocks"] if bl["id"]};ids4=[bl["id"] for k in W4 for bl in D[k]["blocks"] if bl["id"]]
    ok("week-4 block ids unique and new",len(ids4)==len(set(ids4)) and not (set(ids4)&ids1),set(ids4)&ids1)
    ok("week-4 session names new",not ({D[k]["name"] for k in W4}&{D[k]["name"] for k in old}),{D[k]["name"] for k in W4}&{D[k]["name"] for k in old})
    def moves(k): return sorted([n for bl in D[k]["blocks"] for n in bl["reps"]]+[x for bl in D[k]["blocks"] for x in bl["list"]])
    PAIR={"run02":"run27","up03":"up26","mob04":"mob28","lo05":"lo29","mob06":"mob30","kb07":"kb31","walk08":"walk01"}  # same day type in week 3
    for a,b3 in PAIR.items(): ok(f"{a} differs from week 3 ({b3})",moves(a)!=moves(b3))
    for a,b3 in PAIR.items(): ok(f"{a} same length as {b3} (±2 min)",abs(D[a]["tot"]-D[b3]["tot"])<=120,(D[a]["tot"],D[b3]["tot"]))
    rp=lambda k,x:[it.split(":")[1] for bl in D[k]["blocks"] for it in bl["reps"] if it.split(":")[0]==x]
    ok("double progression: bench top of range (8) -> +2 kg at 6",rp("up26","db-bench")==["8"] and rp("up03","db-bench")==["6"] and "add 2 kg" in p.evaluate("()=>JSON.stringify(__how.SESS.up03)"))
    ok("chin-up 6 -> 7, row 12 -> +2 kg x10",rp("up03","assisted-chinup")==["7"] and rp("up03","cs-row")==["10"])
    ok("split squat 8 -> 10, RDL 10 -> 12 same weight",rp("lo05","rfess")==["10"] and rp("lo05","db-rdl")==["12"])
    ok("Thursday has a second pull",rp("lo05","kb-sa-row")==["10"] and rp("up03","cs-row"))
    ok("carry back: Tue farmer's + Thu suitcase",rp("up03","farmers-carry")==["50"] and rp("lo05","suitcase-carry")==["40"])
    ok("Mon 2 Nov = the easy 5 km run, no strength",D["run02"]["name"]=="Easy 5 km Run" and not any(bl["k"]=="ex" for bl in D["run02"]["blocks"]))
    ok("EMOM: 15 windows of 60 s, more reps than week 3",p.evaluate("()=>{var g=__how.SESS.kb07.blocks[1].segs;return g.length==15&&g.every(function(x){return x[1]==60})}") and "×3 each side" in D["kb07"]["blocks"][1]["list"][0])
    lim={"mob04":(13,16),"mob06":(13,16),"run02":(36,40),"bk04":(10,16),"bk06":(10,16),"bk08":(10,16)}
    for k in W4:
        lo,hi=lim.get(k,(20 if k.startswith("bk") else 32,38));m=D[k]["tot"]/60;ok(f"{k} time {m:.1f} min in {lo}–{hi}",lo<=m<=hi)
    miss=p.evaluate("""()=>{var S=__how.SESS,H=__how.HT,o=[];%s.forEach(function(k){S[k].blocks.forEach(function(b){(b.items||[]).forEach(function(i){if(!H[i.x])o.push(i.x);});
      (b.list||[]).forEach(function(x){if(!H[__how.hkey(x)])o.push(x);});});});return o;}"""%json.dumps(sorted(W4)))
    ok("How-to covers every week-4 move",not miss,miss)
    ok("one 16 kg kettlebell only (kettlebell moves cue 16 kg)",all("16 kg" in p.evaluate("k=>JSON.stringify(__how.SESS[k])",k) for k in W4 if any(n.startswith("kb-") or n=="goblet-squat" for bl in D[k]["blocks"] for n in bl["names"])))
    txt=json.dumps({k:D[k] for k in W4})
    ok("medical: no barbell, back squat, conventional deadlift, snatch, inversion",not re.search(r"barbell|back squat|conventional|snatch|handstand|headstand|inverted|valsalva",txt,re.I))
    p.click("#next");p.wait_for_timeout(150)
    ok("9 Nov shows week 5 (built in since pc-v44)",p.locator('button.day[data-d="2026-11-09"] .pl').inner_text()=="Upper",p.locator('button.day[data-d="2026-11-09"] .pl').inner_text())
    c.close()
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
