import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
# pc-v29: week 2 (Mon 19 – Sun 25 Oct). Same app-style-standard audit as test_v28 on every week-2 view, plus
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
DAYS=["2026-10-%d"%d for d in range(19,26)]
VIEWS=[(d,"main",{}) for d in DAYS]+[(d,"backup",{"wo_alt":{d:1}}) for d in DAYS]
VIEWS+=[("2026-10-21","backup+run",{"wo_alt":{"2026-10-21":1},"wo_ri":{"2026-10-21":1}}),("2026-10-24","backup+run",{"wo_alt":{"2026-10-24":1},"wo_ri":{"2026-10-24":1}}),("2026-10-25","run",{"wo_ri":{"2026-10-25":1}})]
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
    W1P={"2026-10-12":"easyrun12","2026-10-13":"strA","2026-10-14":"row","2026-10-15":"mob","2026-10-16":"strB","2026-10-17":"kb","2026-10-18":"walk"}
    W2P={"2026-10-19":"mob19","2026-10-20":"up20","2026-10-21":"run21","2026-10-22":"mob22","2026-10-23":"lo23","2026-10-24":"kb24","2026-10-25":"walk25"}
    c,p=mk(b,"2026-10-19",{})
    D=p.evaluate("""()=>{var S=__how.SESS,o={};Object.keys(S).forEach(function(k){o[k]={name:S[k].name,tot:S[k].tot,rest:!!S[k].rest,blocks:S[k].blocks.map(function(b){return {k:b.k,id:b.id||b.tid||"",flow:!!b.flow,
      names:(b.items||[]).map(function(i){return i.x;}),list:b.list||[],segs:(b.segs||[]).map(function(g){return String(g[2]||"");})};})};});return o;}""")
    P=p.evaluate("()=>__wk.PROG");B=p.evaluate("()=>__wk.BK")
    ok("week-1 programme unchanged",all(P[d]==k for d,k in W1P.items()),P)
    ok("week-1 backups unchanged",all(B["2026-10-%d"%d]=="bk%d"%d for d in range(12,19)),B)
    ok("week-2 programme mapped",all(P.get(d)==k for d,k in W2P.items()),P)
    ok("week-2 backups mapped",all(B.get("2026-10-%d"%d)=="bk%d"%d for d in range(19,26)),B)
    W1=set(W1P.values())|{"bk%d"%d for d in range(12,19)}|{"kbq17"};W2=set(W2P.values())|{"bk%d"%d for d in range(19,26)}
    ids1={bl["id"] for k in W1 for bl in D[k]["blocks"] if bl["id"]};ids2=[bl["id"] for k in W2 for bl in D[k]["blocks"] if bl["id"]]
    ok("week-2 block ids unique and new",len(ids2)==len(set(ids2)) and not (set(ids2)&ids1),set(ids2)&ids1)
    ok("week-2 session names new",not ({D[k]["name"] for k in W2}&{D[k]["name"] for k in W1}))
    def moves(k): return sorted([n for bl in D[k]["blocks"] for n in bl["names"]]+[x.split(" – ")[0] for bl in D[k]["blocks"] for x in bl["list"]])
    for d,k in W2P.items():
        d1="2026-10-%d"%(int(d[-2:])-7);ok(f"{d} differs from week 1 ({W1P[d1]})",moves(k)!=moves(W1P[d1]))
    lim={"mob19":(13,16),"mob22":(13,16),"run21":(36,40),"bk19":(10,16),"bk22":(10,16),"bk25":(10,16)}
    for k in W2:
        lo,hi=lim.get(k,(20 if k.startswith("bk") else 32,38));m=D[k]["tot"]/60;ok(f"{k} time {m:.1f} min in {lo}–{hi}",lo<=m<=hi)
    # How-to for every new move: exercise cards, timer lists, flow moves
    miss=p.evaluate("""()=>{var S=__how.SESS,H=__how.HT,o=[];%s.forEach(function(k){S[k].blocks.forEach(function(b){(b.items||[]).forEach(function(i){if(!H[i.x])o.push(i.x);});
      (b.list||[]).forEach(function(x){if(!H[__how.hkey(x)])o.push(x);});});});return o;}"""%json.dumps(sorted(W2)))
    ok("How-to covers every week-2 move",not miss,miss)
    carry=lambda k:[n for bl in D[k]["blocks"] for n in bl["names"] if "carry" in n]
    ok("carries: Tue farmer's only, Fri suitcase only, none Sat",carry("up20")==["farmers-carry"] and carry("lo23")==["suitcase-carry"] and not carry("kb24") and not carry("bk24"))
    ok("Sat: single 16 kg bell","16 kg" in p.evaluate("()=>__how.SESS.kb24.safe"))
    txt=json.dumps({k:D[k] for k in W2})
    ok("medical: no barbell, back squat, conventional deadlift, snatch, inversion",not re.search(r"barbell|back squat|conventional|snatch|handstand|headstand|inverted|valsalva",txt,re.I))
    p.click("#next");p.wait_for_timeout(150)
    ok("week 3 follows (26 Oct = Upper)",p.locator('button.day[data-d="2026-10-26"] .pl').inner_text()=="Upper")
    c.close()
    ok("no page errors",not errs,errs[:3])
    b.close()
print(f"{sum(res)}/{len(res)} passed")
