<script>
(function(){
"use strict";
// ---- exercise library: id -> [name, suggested, placeholder, weighted]
var X={"db-bench":["Dumbbell bench press","16–20 kg each","16–20",1],"cs-row":["Chest-supported dumbbell row","14–18 kg each","14–18",1],"goblet-squat":["Kettlebell goblet squat","16–20 kg","16–20",1],"pullup-dip":["Assisted pull-up (feet on block)","Bodyweight (use block as needed)","BW",1],"db-shoulder-press":["Seated dumbbell shoulder press","10–14 kg each","10–14",1],"farmers-carry":["Farmer's carry","20–24 kg each","20–24",1],
"incline-db-press":["Incline dumbbell press","12–16 kg each","12–16",1],"hk-db-press":["Half-kneeling one-arm dumbbell press","10–14 kg","10–14",1],"assisted-chinup":["Assisted chin-up (feet on block)","Bodyweight","BW",0],"lateral-raise":["Dumbbell lateral raise","4–6 kg each","4–6",1],"hammer-curl":["Hammer curl","8–12 kg each","8–12",1],
"db-rdl":["Dumbbell Romanian deadlift","14–18 kg each","14–18",1],"dead-bug":["Dead bug","Bodyweight","",0],"reverse-lunge":["Dumbbell reverse lunge","8–12 kg each","8–12",1],"side-plank":["Side plank","Bodyweight","",0],"calf-raise":["Single-leg calf raise","Bodyweight or 8–12 kg","8–12",1],
"kb-swing":["Kettlebell swing","16–20 kg","16–20",1],"incline-pushup":["Incline push-up (hands on bench)","Bodyweight","",0],"kb-sumo-dl":["Kettlebell sumo deadlift","20–24 kg","20–24",1],"suitcase-carry":["Suitcase carry (one hand)","16–24 kg","16–24",1],"prone-y-raise":["Incline prone Y-raise","2–4 kg each","2–4",1],"hip-9090":["90/90 hip switch","Bodyweight","",0],"kb-sa-row":["Single-arm kettlebell row","16–20 kg","16–20",1]};
function iv(n,w,r,wl,rl){var s=[];for(var k=1;k<=n;k++){s.push(["WORK",w,"Interval "+k+" of "+n+" · "+wl]);if(k<n)s.push(["REST",r,"Interval "+k+" of "+n+" · "+rl]);}return s;}
function circ(n,st,w,r){var s=[];for(var k=1;k<=n;k++)for(var j=0;j<st.length;j++){s.push(["WORK",w,"Round "+k+" of "+n+" · "+st[j]]);if(!(k==n&&j==st.length-1))s.push(["REST",r,"Next: "+(st[(j+1)%st.length])]);}return s;}
function emom(n,sec,st){var s=[];for(var k=1;k<=n;k++)for(var j=0;j<st.length;j++)s.push(["WORK",sec,"Round "+k+" of "+n+" · "+st[j]]);return s;}
function posOf(n){var l=n.toLowerCase();if(/90\/90|open book|bridge|lying|dead bug|side-lying/.test(l))return "F";if(/cat-cow|bird-dog|quadruped|thread the needle/.test(l))return "Q";if(/lat reach|bench/.test(l))return "K-bench";if(/kneeling|couch|ankle rocks/.test(l))return "K";if(/pass-through|broomstick/.test(l))return "S-stick";if(/rack|doorway/.test(l))return "S-rack";if(/block/.test(l))return "S-block";if(/wall/.test(l))return "S-wall";return "S";}
var PRK={S:3,K:2,Q:1,F:0};
function mergeLR(mv){var o=[];mv.forEach(function(m){var x=/^(.*?) – (left|right)(.*)$/.exec(m[0]);if(x){var base=(x[1]+x[3]).trim(),key=x[1].replace(/\s*\(.*?\)/g,"").trim(),pv=o[o.length-1];if(pv&&pv.key==key&&pv.lr&&x[2]=="right"){pv.sec+=m[1];pv.r=m[1];return;}o.push({name:base.replace(/\s+/g," "),key:key,sec:m[1],l:m[1],side:1,lr:1,p:m[2]});return;}var y=/^(.*?) – each side(.*)$/.exec(m[0]);if(y){o.push({name:(y[1]+y[2]).trim(),sec:m[1],side:1,p:m[2]});return;}o.push({name:m[0],sec:m[1],p:m[2]});});return o;}
function fl(id,h,name,note,mv,ph,dir){ph=ph||"STRETCH";var o=mergeLR(mv);o.forEach(function(m,i){m.pos=m.p||posOf(m.name);m.i=i;});dir=dir||(/warm/i.test(h)?"up":"down");o.sort(function(a,b){var d=(PRK[a.pos[0]]-PRK[b.pos[0]])*(dir=="up"?1:-1);return d||(a.pos<b.pos?-1:a.pos>b.pos?1:0)||a.i-b.i;});
var segs=[],list=[],pp=null;o.forEach(function(m){if(m.pos!=pp)segs.push(["READY",10,m.name+(m.side?" · left side":"")]);pp=m.pos;if(m.side){var a=m.l&&m.r?m.l:Math.ceil(m.sec/2),b=m.sec-a;segs.push([ph,a,m.name+" · left side"]);segs.push([ph,b,m.name+" · switch → right side"]);list.push(m.name+" – "+a+" s each side");}else{segs.push([ph,m.sec,m.name]);list.push(m.name+" – "+m.sec+" s");}});
return{k:"timer",id:id,h:h,name:name,note:FLN,small:note||"",segs:segs,list:list,flow:1};}
function dur(segs){return (segs||[]).reduce(function(a,x){return a+x[1];},0);}
function mmss(t){return Math.floor(t/60)+":"+String(t%60).padStart(2,"0");}
function tps(tp){if(!tp)return 3;return tp.split("").reduce(function(a,c){return a+(c=="X"?1:+c);},0);}
function wsec(it){if(it.ws)return it.ws;var reps=it.rp*(it.side?2:1);if(it.ru=="s")return reps+(it.side?10:5);if(it.ru=="m")return 45;return Math.ceil((reps*tps(it.tp)+5)/5)*5;}
function nmI(it){return (it.lab?it.lab+" ":"")+X[it.x][0];}
// strength / carry blocks are list mode (no countdown); this is only the time estimate for the ≈ day total
function bEst(b){var t=0;for(var r=1;r<=b.n;r++){b.items.forEach(function(it){t+=15+wsec(it);});if(r<b.n)t+=b.rest;}return t;}
// EMOM / Every from strength items: one segment per minute (window); rest is whatever is left, never timed
function emomLab(it){return X[it.x][0]+" × "+it.rp+(it.ru?" "+it.ru:"")+(it.side?" each side":"");}
function bEmom(b){var s=[];for(var r=1;r<=b.n;r++)b.items.forEach(function(it){s.push(["WORK",b.win,emomLab(it),r]);});return s;}
function bEvery(b){var s=[];for(var r=1;r<=b.n;r++)s.push(["WORK",b.win,b.items.map(emomLab).join(" → "),r]);return s;}
// pc-v30 clock mode: every guided block becomes one segment per move / minute / interval. Drops READY prep (one 10 s
// get-ready is added when a block starts), folds set-up into rest, and writes sides as "· left" / "· right".
// Session data keeps its existing format, so weekly additions don't change.
function cln(l){return String(l||"").replace(/^Interval \d+(?: of |\/)\d+ · /,"").replace(/ · (round|set) \d+\/\d+/g,"").replace(/ ?[–·] switch → right side/," · right").replace(/ ?[–·] (left|right) side/," · $1").trim();}
function rnd(l){var m=/(?:round |Interval )(\d+)(?:\/| of )\d+/.exec(String(l||""));return m?+m[1]:0;}
function kindOf(b){var h=b.h||"";return b.amrap?"amrap":b.flow?"flow":/^EMOM/.test(h)?"emom":/^Every/.test(h)?"every":/^Intervals/.test(h)?"iv":/^Circuit/.test(h)?"circ":"one";}
function winOf(h){var m=/(\d+):(\d\d)/.exec(h);if(m)return +m[1]*60+ +m[2];m=/(\d+) s/.exec(h);return m?+m[1]:60;}
function clk(b,segs){var kd=kindOf(b),o=[];segs=segs||[];
 if(kd=="emom"||kd=="every"){var win=winOf(b.h),acc=0,cur=[],r=0;
  var flush=function(){if(!cur.length)return;var nm=[],sd={};cur.forEach(function(g){var l=cln(g[2]),m=/^(.*) · (left|right)$/.exec(l),base=m?m[1]:l;if(nm.indexOf(base)<0)nm.push(base);if(m)(sd[base]=sd[base]||{})[m[2]]=1;});
   o.push(["WORK",win,nm.map(function(x){var q=sd[x];return q?x+(q.left&&q.right?" · each side":q.left?" · left":" · right"):x;}).join(", "),++r]);cur=[];acc=0;};
  segs.forEach(function(g){if(g[0]!="READY"&&g[0]!="REST")cur.push(g);acc+=g[1];if(acc>=win)flush();});flush();return o;}
 var first=segs[0]&&segs[0][0]=="READY"?String(segs[0][2]||""):"",pf="",wk=0;
 if(kd=="iv")pf=(first&&!/^Interval/.test(first)?first.split(" · ")[0]:String(b.name||"").replace(/ intervals.*$| \d+ ×.*$/i,"")).replace(/^Run\/walk$/,"Run");
 segs.forEach(function(g,i){var ph=g[0],l=cln(g[2]),pv=o[o.length-1];
  if(ph=="READY"){if(i==0||kd=="flow")return;if(pv&&pv[0]=="REST"){pv[1]+=g[1];return;}o.push(["REST",g[1],"Rest"]);return;}
  if(ph=="REST"){var rl=l.replace(/^Rest( · )?/,"");if(/next$|^switch hands$|^then |^park the bell$/i.test(rl))rl="";if(pv&&pv[0]=="REST"){pv[1]+=g[1];return;}o.push(["REST",g[1],"Rest"+(rl?" · "+rl:""),rnd(g[2])]);return;}
  if(kd=="iv"){var e=(/\b(easy|steady|moderate)\b/i.exec(l)||[""])[0].toLowerCase();if(pf)l=pf+" · "+mmss(g[1])+(e&&pf.toLowerCase().indexOf(e)<0?" · "+e:"");}
  o.push([ph,g[1],l||b.name||"",rnd(g[2])||(kd=="iv"?++wk:0)]);});
 return o;}
function ivr(n){var s=[];for(var k=1;k<=n;k++){s.push(["READY",5,"Interval "+k+"/"+n+" · moderate pace"]);s.push(["WORK",60,"Interval "+k+"/"+n+" · moderate pace"]);if(k<n)s.push(["REST",55,"Rest · light paddle"]);}return s;}
function tmean(tp){if(!tp)return "";var d=tp.split(""),o=[d[0]+" s down"];if(d[1]!="0")o.push(d[1]+" s pause");o.push(d[2]=="X"?"up with intent":d[2]+" s up");if(d[3]!="0")o.push(d[3]+" s hold");return o.join(" · ");}
var MV={
up:[["Cat-cow, slow",40],["World's greatest stretch – left",40],["World's greatest stretch – right",40],["Thoracic open book – each side",40],["Broomstick pass-throughs",40],["Lunge with overhead reach",40]],
low:[["Leg swings – front to back",40],["Leg swings – side to side",40],["90/90 hip switches",40],["World's greatest stretch – left",40],["World's greatest stretch – right",40],["Bodyweight squat, slow",40]],
full:[["Cat-cow, slow",40],["World's greatest stretch – left",40],["World's greatest stretch – right",40],["90/90 hip switches",40],["Broomstick pass-throughs",40],["Lunge with overhead reach",40]],
run:[["Leg swings – front to back",40],["Leg swings – side to side",40],["Walking lunge with overhead reach",40],["Ankle rocks – each side",40],["90/90 hip switches",40],["Standing hip circles (CARs)",40]],
cd:[["Couch stretch – left (active: squeeze glute)",30],["Couch stretch – right",30],["Half-kneeling hip flexor with reach – each side",40],["Thoracic open book – each side",40],["90/90 hold with lift-offs",30]],
cdu:[["Doorway/rack chest stretch – left",30],["Doorway/rack chest stretch – right",30],["Broomstick pass-throughs, slow",30],["Thoracic open book – each side",40],["Seated lat reach at bench – each side",40]]};
// pc-v28 layout standard: timers carry h (format), name (card title), note (fixed instruction line), small (small print, string or array)
var FLN="Each move: time shown · sides cued.",NOREST="Last round has no rest.";
function tm(id,h,name,note,sec,ph,x){var b={k:"timer",id:id,h:h,name:name,note:note,segs:[[ph,sec]]};for(var q in x||{})b[q]=x[q];return b;}
// timed core circuit: m=[name, work s, set-up s, sided]; rest between rounds only (none after the last)
function core(n,mv,rest){var s=[];for(var r=1;r<=n;r++){var t=" · round "+r+"/"+n;mv.forEach(function(m){if(m[3]){s.push(["READY",m[2],m[0]+" – left side"+t]);s.push(["WORK",m[1],m[0]+" – left side"+t]);s.push(["READY",10,m[0]+" – switch → right side"+t]);s.push(["WORK",m[1],m[0]+" – right side"+t]);}else{s.push(["READY",m[2],m[0]+t]);s.push(["WORK",m[1],m[0]+t]);}});if(r<n)s.push(["REST",rest,"Rest · round "+(r+1)+" next"]);}return s;}
var STOP_RUN="Zone 2 run: conversational, a little breathless. Take a walk break whenever you need one. Steady pace, RPE 5–6.";
var SESS={
pump:{name:"Pump + Cardio",short:"Pump",safe:"Moderate weights, breathe out every rep, no breath-holding or straining, stop 2 reps short of failure (2 RIR).",blocks:[
 tm("wu","Warm-up","Easy row (Concept2)","Easy pace, RPE 3–4.",240,"WARM-UP",{small:"18–20 s/m · damper 4–5."}),
 {k:"ex",h:"Pump circuit",gn:"Aim for RPE 6–7. Can't get 12 smooth reps? Drop a step.",n:3,unit:"Round",rk:"r",rest:60,btn:"Round done – rest 60 s",note:"12–15 reps · ~60 s rest between rounds",items:[{x:"db-bench",rx:"12–15 reps"},{x:"cs-row",rx:"Face down on incline bench · 12–15 reps"},{x:"goblet-squat",rx:"12–15 reps"},{x:"pullup-dip",rx:"Feet on block · 8–10 controlled reps"},{x:"db-shoulder-press",rx:"12–15 reps"},{x:"farmers-carry",rx:"30–40 m or 30 s · heavy but breathing steadily"}]},
 {k:"timer",id:"cardio",h:"Intervals",name:"Run/walk intervals 4 × 1:00",note:"Each round: 1:00 work · 1:00 rest. Moderate pace, RPE 7.",small:["Rest is a recovery walk. Tired legs: row it instead.",NOREST],segs:iv(4,60,60,"moderate run","recovery walk")},
 tm("cd","Cool-down","Cool-down walk + stretch","Easy walk, RPE 3–4.",120,"COOL-DOWN")]},
easyrun:{name:"Easy Run",short:"Run",safe:STOP_RUN,blocks:[
 tm("rwu","Warm-up","Warm-up walk","Easy walk, RPE 3–4.",300,"WARM-UP"),
 tm("rmain","Steady","Zone 2 run","Steady pace, Zone 2, RPE 5–6.",900,"JOG",{counter:1,small:"1:00 walk break whenever needed: tap +1 walk break."}),
 tm("rcd","Cool-down","Cool-down walk + stretch","Easy walk, RPE 3–4.",300,"COOL-DOWN",{small:"Then stretch calves, hamstrings and hips."}),{k:"fields"}]},
easyrun12:{name:"Zone 2 Run",was:["Easy Run"],short:"Run",safe:STOP_RUN,blocks:[
 fl("mwu","Warm-up","Dynamic stretch","",MV.run),
 tm("rwu","Warm-up","Warm-up walk","Easy walk, RPE 3–4.",300,"WARM-UP"),
 tm("rmain","Steady","Zone 2 run","Steady pace, Zone 2, RPE 5–6.",900,"JOG",{counter:1,small:"1:00 walk break whenever needed: tap +1 walk break."}),
 tm("rcd","Cool-down","Cool-down walk","Easy walk, RPE 3–4.",300,"COOL-DOWN"),
 fl("mfin","Flow","Standing → floor flow","Slow and controlled, nasal breathing.",[["Standing hip CARs – each side",40],["Couch stretch (active: squeeze glute) – each side",60],["Cat-cow, slow",40],["90/90 hold with lift-offs – each side",60],["Thoracic open book – each side",60]],"FLOW"),{k:"fields"}]},
strA:{name:"Strength A · Upper",short:"Upper",safe:"Quality first at RPE 6–7. Breathe out on every press and pull, never hold your breath, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("awu","Warm-up","Dynamic stretch – upper","No forcing.",MV.up),
 {k:"ex",h:"A · Superset",mode:"sup",n:4,rr:[60,90],unit:"Set",tid:"aemom",items:[{x:"incline-db-press",lab:"A1",rp:6,tp:"3011",cue:"Bench about 30°, breathe out as you press."},{x:"prone-y-raise",lab:"A2",rp:6,tp:"2011",sw:15,cue:"Chest on incline bench, thumbs up, lift with the shoulder blades."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"asb",fill:"20 s hip flexor reach each side",items:[{x:"cs-row",lab:"B1",rp:8,tp:"2011",cue:"Face down on incline bench, pause at the top."},{x:"hk-db-press",lab:"B2",rp:6,side:1,tp:"2010",sw:20,cue:"Half-kneeling, ribs down, breathe out on the press."}]},
 {k:"ex",h:"C · Tri-set",mode:"sup",n:2,rr:[60,90],unit:"Set",tid:"asc",items:[{x:"assisted-chinup",lab:"C1",rp:5,tp:"3010",cue:"Feet on block for help, slow lowering."},{x:"lateral-raise",lab:"C2",rp:12,tp:"2010",cue:"Lead with elbows, stop at shoulder height."},{x:"hammer-curl",lab:"C3",rp:10,tp:"2010",cue:"Elbows pinned, no swinging."}]},
 {k:"timer",id:"afl",h:"Intervals",name:"Row intervals 3 × 0:50 / 0:30",note:"Each round: 0:50 work · 0:30 rest. Moderate pace, RPE 7.",small:["Work 22–24 s/m · rest light paddle 18–20 s/m · damper 4–5.",NOREST],segs:[["READY",10,"Row · moderate pace"]].concat(iv(3,50,30,"moderate pace","light paddle"))},
 fl("acd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cdu)]},
row:{name:"Rower Intervals",short:"Row",safe:"Intervals never all-out: short phrases only. Go by RPE, damper 4–5, breathe out on the drive. Moderate pace, RPE 7.",blocks:[
 fl("wwu0","Warm-up","Dynamic stretch","",MV.full),
 tm("wwu","Warm-up","Easy row","Easy pace, RPE 3–4.",240,"WARM-UP",{small:"Build gently · 18–22 s/m · damper 4–5."}),
 {k:"timer",id:"wiv",h:"Intervals",name:"Row intervals 6 × 1:00 / 1:00",note:"Each round: 1:00 work · 1:00 rest. Moderate pace, RPE 7.",small:["Work 24–26 s/m · rest light paddle 18–20 s/m · damper 4–5.","5 s get-ready before each interval. "+NOREST],segs:ivr(6)},
 tm("wst","Steady","Steady row","Steady pace, RPE 5–6.",240,"STEADY",{small:"20–22 s/m · damper 4–5."}),
 {k:"timer",id:"wcore",h:"Circuit × 2",name:"Core stability",note:"Each round: 25–45 s per move · 30 s rest.",small:"Side plank with knees down. Exhale slowly, no breath-holding.",segs:core(2,[["Bird-dog @3131, alternate",45,10],["Side plank",25,20,1],["Dead bug @3030",40,20]],30),list:["Bird-dog @3131 – 45 s","Side plank – 25 s each side","Dead bug @3030 – 40 s"]},
 fl("wcd","Cool-down","Active stretch","",MV.cd),{k:"fields",dist:"Distance (m, from PM5)"}]},
mob:{name:"Active Mobility Flow",short:"Mobility",rest:1,safe:"Recovery day. Slow controlled rotations and gentle end-range holds – no head-down positions, no forcing, breathe slowly.",blocks:[
 {k:"rest",name:"Recovery day",note:"Gentle mobility only. Walk, hydrate, sleep well."},
 fl("mob","Flow","Active Mobility Flow","CARs and end-range holds. 10 s set-up only on position changes.",[["Shoulder CARs – left",60],["Shoulder CARs – right",60],["Hip CARs (standing, hold rack) – left",60],["Hip CARs – right",60],["Segmental cat-cow",75],["Thoracic open book – left",60],["Thoracic open book – right",60],["90/90 end-range hold + lift-offs – left",75],["90/90 end-range hold + lift-offs – right",75],["Couch stretch (active) – each side",75],["Supported deep squat hold (hold rack)",70],["Slow breathing lying on back",120]],"MOBILITY")]},
strB:{name:"Strength B · Lower + Core",short:"Lower",safe:"No heavy spinal loading. Quality first at RPE 6–7, breathe out on the effort, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("bwu","Warm-up","Dynamic stretch – lower","No forcing.",MV.low),
 {k:"ex",h:"A · Superset",mode:"sup",n:4,rr:[60,90],unit:"Set",tid:"bemom",items:[{x:"goblet-squat",lab:"A1",rp:6,tp:"3011",cue:"Slow down, breathe out as you stand."},{x:"hip-9090",lab:"A2",rp:6,tp:"2020",sw:20,cue:"Sit tall, rotate knees side to side."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"bsb",fill:"20 s couch stretch each side",items:[{x:"reverse-lunge",lab:"B1",rp:6,side:1,tp:"2011",cue:"Offset: one dumbbell, opposite side. Hold the rack if needed."},{x:"dead-bug",lab:"B2",rp:5,side:1,tp:"2020",sw:20,cue:"Low back flat, slow exhale as you reach."}]},
 {k:"ex",h:"C · Tri-set",mode:"sup",n:2,rr:[45,75],unit:"Set",tid:"bsc",items:[{x:"db-rdl",lab:"C1",rp:8,tp:"3011",cue:"Hips back, eyes a little ahead – don't drop the head."},{x:"side-plank",lab:"C2",rp:20,ru:"s",side:1,sw:20,cue:"Keep breathing the whole time."},{x:"calf-raise",lab:"C3",rp:8,side:1,tp:"2010",cue:"Edge of the block, hand on rack."}]},
 {k:"timer",id:"bfl",h:"Intervals",name:"Assault Runner 2 × 0:40 / 0:50",note:"Each round: 0:40 work · 0:50 rest. Moderate pace, RPE 7.",small:["Rest is a recovery walk.",NOREST],segs:[["READY",10,"Assault Runner · moderate run"]].concat(iv(2,40,50,"moderate run","recovery walk"))},
 fl("bcd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cd)]},
kb:{name:"KB + Carry Flow",short:"KB",safe:"Exhale on every swing and put the bell down whenever form slips. Smooth reps at RPE 6–7, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("kwu","Warm-up","Dynamic stretch – full body","",MV.full),
 {k:"ex",h:"A · Superset",mode:"sup",n:4,rr:[60,90],unit:"Set",tid:"kemom",items:[{x:"kb-sa-row",lab:"A1",rp:5,side:1,tp:"2011",cue:"Hand on bench, flat back, pull to the hip."},{x:"incline-pushup",lab:"A2",rp:8,tp:"2010",sw:15,cue:"Hands on bench, body straight."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Round",tid:"kcirc",items:[{x:"kb-swing",lab:"B1",rp:10,cue:"One bell for B1, B2 and C1. Hinge and snap the hips."},{x:"kb-sumo-dl",lab:"B2",rp:8,tp:"2011",cue:"Same bell as the swings. Wide stance, chest proud."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:3,rr:[60,90],unit:"Round",tid:"kcarry",items:[{x:"suitcase-carry",lab:"C1",rp:30,ru:"m",cue:"Same bell, one hand. Switch hands halfway."},{x:"farmers-carry",lab:"C2",rp:30,ru:"m",sw:20,cue:"Pick up two dumbbells. Shoulders down, short steps."}]},
 fl("kcd","Cool-down","Active stretch","",MV.cd)]},
walk:{name:"Easy Long Walk",short:"Walk",safe:"Zone 1–2 walk with nasal breathing, outside or on the Assault Runner. Easy pace, RPE 3–4.",blocks:[
 fl("swu","Warm-up","Dynamic stretch","",MV.run),tm("swalk","Steady","Long walk (Zone 1–2)","Easy pace, RPE 3–4.",1500,"EASY",{small:"Outside or on the Assault Runner."}),fl("sst","Cool-down","Cool-down stretch","Breathe out into each stretch.",[["Calf stretch on block – left",50],["Calf stretch on block – right",50],["Couch stretch – left",50],["Couch stretch – right",50],["90/90 hold with lift-offs – each side",50],["Thoracic open book – each side",50],["Slow breathing lying on back",50]]),{k:"fields"}]},
// ---- backup sessions (one per day; gi offset 100 so ticks never collide with the main session)
bk12:{name:"Backup · Zone 2 Row + Mobility",was:["Backup · Easy Row + Mobility"],short:"Row",g0:100,safe:"No running. Zone 2 row: conversational, a little breathless. Damper 4–5, breathe steadily. Steady pace, RPE 5–6.",blocks:[
 fl("x12wu","Warm-up","Dynamic stretch","",MV.full),
 {k:"timer",id:"x12row",h:"Steady",name:"Zone 2 row",note:"Steady pace, Zone 2, RPE 5–6.",small:"24:00 at 18–20 s/m · damper 4–5.",segs:[["READY",10,"Zone 2 row"],["STEADY",1440,"Zone 2 row · steady pace"]]},
 fl("x12mob","Flow","Mobility flow","Controlled, keep breathing.",[["Hip CARs – left",40],["Hip CARs – right",40],["90/90 hip switches",50],["Couch stretch – left",40],["Couch stretch – right",40],["Thoracic open book – each side",50]],"MOBILITY"),
 {k:"fields",dist:"Distance (m, from PM5)"}]},
bk13:{name:"Backup · Upper (KB + Bodyweight)",short:"Upper",g0:100,safe:"Less kit: one kettlebell plus the bars. RPE 6–7, breathe out on every press and pull, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("x13wu","Warm-up","Dynamic stretch – upper","No forcing.",MV.up),
 {k:"ex",h:"A · Superset",mode:"sup",n:4,rr:[60,90],unit:"Set",tid:"x13a",items:[{x:"kb-floor-press",lab:"A1",rp:5,side:1,tp:"3010",cue:"Lie on the floor, elbow touches down softly."},{x:"scap-pullup",lab:"A2",rp:6,tp:"2011",sw:20,cue:"Hang, then pull shoulders down without bending elbows."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"x13b",items:[{x:"kb-sa-row",lab:"B1",rp:8,side:1,tp:"2011",cue:"Hand on bench, pull to the hip."},{x:"kb-halo",lab:"B2",rp:5,side:1,tp:"2020",sw:15,cue:"Light bell, slow circles, ribs down."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:2,rr:[45,75],unit:"Set",tid:"x13c",items:[{x:"dip-hold",lab:"C1",rp:20,ru:"s",cue:"Arms straight on the dip bars, feet on block if needed."},{x:"kb-curl",lab:"C2",rp:10,tp:"2010",sw:15,cue:"Hold the bell by the horns, elbows pinned."}]},
 {k:"timer",id:"x13fl",h:"Intervals",name:"Row intervals 4 × 0:40 / 0:20",note:"Each round: 0:40 work · 0:20 rest. Moderate pace, RPE 7.",small:["Work 22–24 s/m · rest light paddle · damper 4–5.",NOREST],segs:[["READY",10,"Row · moderate pace"]].concat(iv(4,40,20,"moderate pace","light paddle"))},
 fl("x13cd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cdu)]},
bk14:{name:"Backup · Runner Walk + Core",short:"Walk+",g0:100,safe:"Lower energy, no rowing: power walk and recovery walk. Breathe out slowly during the core work. Steady pace, RPE 5–6.",blocks:[
 fl("x14wu","Warm-up","Dynamic stretch","",MV.run),
 {k:"timer",id:"x14iv",h:"Intervals",name:"Walk intervals 8 × 1:00 / 1:00",note:"Each round: 1:00 work · 1:00 rest. Steady pace, RPE 5–6.",small:["Power walk, then recovery walk · Assault Runner.",NOREST],segs:[["READY",10,"Power walk"]].concat(iv(8,60,60,"power walk","recovery walk"))},
 {k:"timer",id:"x14core",h:"Circuit × 2",name:"Floor core",note:"Each round: 25–40 s per move · 30 s rest.",small:"Side plank with knees down. Exhale slowly, no breath-holding.",segs:core(2,[["Glute bridge @2011",40,20],["Dead bug @3030",40,10],["Side plank",25,15,1]],30),list:["Glute bridge @2011 – 40 s","Dead bug @3030 – 40 s","Side plank – 25 s each side"]},
 fl("x14cd","Cool-down","Active stretch","",MV.cd),{k:"fields"}]},
bk15:{name:"Backup · Easy Walk + Breathing",short:"Walk",g0:100,safe:"Recovery day. Zone 1 walk with nasal breathing, then slow breathing. Easy pace, RPE 3–4.",blocks:[
 tm("x15walk","Steady","Recovery walk (Zone 1)","Easy pace, RPE 3–4.",600,"EASY",{small:"Nasal breathing."}),
 fl("x15br","Cool-down","Down-regulate","Slow, calm breathing.",[["Calf stretch on block – each side",50],["Seated lat reach at bench – each side",50],["90/90 hold with lift-offs – each side",50],["Slow breathing lying on back",90]],"MOBILITY")]},
bk16:{name:"Backup · Lower (Single-leg + Floor)",short:"Lower",g0:100,safe:"Lower energy, light loads, no spinal loading. RPE 6, breathe out on the effort, hold the rack for balance.",blocks:[
 fl("x16wu","Warm-up","Dynamic stretch – lower","No forcing.",MV.low),
 {k:"ex",h:"A · Superset",mode:"sup",n:4,rr:[60,90],unit:"Set",tid:"x16a",items:[{x:"split-squat",lab:"A1",rp:5,side:1,tp:"3010",cue:"Static split stance, hold the rack, back knee lowers softly."},{x:"glute-bridge",lab:"A2",rp:6,tp:"2011",sw:20,cue:"On the floor, squeeze glutes at the top, ribs down."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"x16b",items:[{x:"single-leg-rdl",lab:"B1",rp:6,side:1,tp:"3011",cue:"Hand on the rack, light bell, hips square, head level."},{x:"side-plank",lab:"B2",rp:20,ru:"s",side:1,sw:20,cue:"Knees down if needed, keep breathing."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:2,rr:[45,75],unit:"Set",tid:"x16c",items:[{x:"wall-sit",lab:"C1",rp:30,ru:"s",cue:"Back flat on the wall, breathe the whole time."},{x:"calf-raise",lab:"C2",rp:10,side:1,tp:"2010",sw:15,cue:"Edge of the block, hand on rack."}]},
 {k:"timer",id:"x16fl",h:"Steady",name:"Easy row 3:00",note:"Easy pace, RPE 3–4.",small:"18–20 s/m · damper 4–5 · flush the legs.",segs:[["READY",10,"Easy row"],["EASY",180,"Easy row · easy pace"]]},
 fl("x16cd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cd)]},
bk17:{name:"Backup · Dumbbell Flow (no KB)",short:"DB",g0:100,safe:"Dumbbells only. Breathe out on every press and put the weights down whenever form slips. Smooth reps at RPE 6.",blocks:[
 fl("x17wu","Warm-up","Dynamic stretch – full body","",MV.full),
 {k:"ex",h:"A · Superset",mode:"sup",n:4,rr:[60,90],unit:"Set",tid:"x17a",items:[{x:"db-shoulder-press",lab:"A1",rp:8,tp:"2011",cue:"Seated, back supported, ribs down."},{x:"cs-row",lab:"A2",rp:8,tp:"2011",sw:15,cue:"Chest on the incline bench, pause at the top."}]},
 {k:"ex",h:"B · Tri-set",mode:"sup",n:3,rr:[60,90],unit:"Round",tid:"x17b",items:[{x:"db-squat-press",lab:"B1",rp:8,tp:"2010",cue:"Light dumbbells; squat, stand, then press – breathe out on the press."},{x:"pullup-dip",lab:"B2",rp:6,cue:"Feet on block; slow lowering. Dips are the alternative (How to)."},{x:"farmers-carry",lab:"B3",rp:30,ru:"m",sw:20,cue:"Two dumbbells, tall posture, short steps."}]},
 {k:"timer",id:"x17fl",h:"Steady",name:"Cool-down walk 5:00",note:"Easy walk, RPE 3–4.",small:"Assault Runner.",segs:[["READY",10,"Cool-down walk"],["EASY",300,"Cool-down walk · easy pace"]]},
 fl("x17cd","Cool-down","Active stretch","",MV.cd)]},
bk18:{name:"Backup · Long Stretch + Breathe",short:"Stretch",rest:0,g0:100,safe:"Lowest energy option. Long, gentle holds – no forcing, no head-down positions, breathe slowly.",blocks:[
 fl("x18fl","Flow","Long-hold stretch","Gentle holds, no forcing.",[["Doorway/rack chest stretch – each side",90],["Seated lat reach at bench – each side",90],["Couch stretch – left",90],["Couch stretch – right",90],["Calf stretch on block – each side",90],["Supported deep squat hold (hold rack)",90],["90/90 hold with lift-offs – each side",90],["Thoracic open book – each side",90],["Slow breathing lying on back",150]],"MOBILITY")]},
rest0:{name:"Rest day",short:"Rest",rest:1,safe:"Rest and recover.",blocks:[{k:"rest",name:"Rest day",note:"Walk, stretch, sleep well."}]},
tbc:{name:"No plan yet",short:"Soon",rest:1,tbc:1,safe:"",blocks:[{k:"rest",name:"Plan coming Sunday",note:"This week's sessions are added each Sunday. If you have a week file, import it from History."}]}};
// ---- how-to library: key -> {u:summary, s:steps(<=12 words), c:tips, m:mistake, z:safety, q:demo search}
var BR="Breathe out on the effort; never hold your breath.";
var HT={
"db-bench":{q:"dumbbell bench press",u:"Chest press lying on a flat bench.",s:["Lie back with dumbbells over your chest, feet flat.","Pull shoulder blades together and down.","Lower slowly to the sides of your chest.","Press up, breathing out."],c:["Elbows about 45° from your body","Wrists over elbows"],m:"Elbows flared straight out.",z:BR},
"cs-row":{q:"chest supported dumbbell row",u:"Back row lying face down on an incline bench.",s:["Lie chest-down on a 30–45° bench, arms hanging.","Pull elbows back towards your hips.","Squeeze shoulder blades and pause.","Lower slowly to a full stretch."],c:["Chest stays on the pad","Neck long"],m:"Shrugging towards your ears.",z:BR},
"goblet-squat":{q:"kettlebell goblet squat",u:"Squat holding a kettlebell at your chest.",s:["Hold the bell by the horns against your chest.","Stand feet shoulder-width, toes slightly out.","Sit down between your heels, chest up.","Drive through the whole foot to stand."],c:["Heels down","Knees follow toes"],m:"Knees caving in.",z:BR},
"pullup-dip":{q:"assisted pull up feet on box",u:"Pull-up with feet on the block for help.",s:["Grip the bar, feet on the block.","Pull your chest up towards the bar.","Use your legs only as much as needed.","Lower slowly every rep."],c:["Shoulders away from ears","No kicking","Alternative: assisted dips, lowering to upper arms level"],m:"Dropping fast from the top.",z:BR},
"db-shoulder-press":{q:"seated dumbbell shoulder press",u:"Overhead press sitting on an upright bench.",s:["Sit back-supported, dumbbells at shoulder height.","Brace lightly, ribs down.","Press up until arms are straight, breathing out.","Lower slowly to the shoulders."],c:["Forearms vertical","Back stays on the pad"],m:"Arching the lower back.",z:BR},
"farmers-carry":{q:"farmers carry",u:"Walk holding a heavy weight in each hand.",s:["Pick up both weights with a flat back.","Stand tall, shoulders down.","Walk with short, steady steps.","Hinge or squat to set them down."],c:["Tall posture","Tight grip"],m:"Rounding the shoulders forward.",z:"Breathe normally the whole time."},
"incline-db-press":{q:"incline dumbbell press",u:"Chest press on a low-incline bench.",s:["Set the bench to about 30°.","Lie back, dumbbells over your upper chest.","Lower slowly to the sides of your chest.","Press up and slightly in, breathing out."],c:["Low incline only","Follow the tempo"],m:"Bench too steep.",z:BR},
"hk-db-press":{q:"half kneeling single arm dumbbell press",u:"One-arm overhead press kneeling on one knee.",s:["Kneel on one knee, weight on the same side.","Squeeze the back glute, ribs down.","Press straight up, breathing out.","Lower slowly, then switch sides."],c:["Don't lean away","Bicep finishes by your ear"],m:"Arching or tilting to lift.",z:BR},
"assisted-chinup":{q:"assisted chin up feet on box",u:"Chin-up with palms facing you, feet on the block.",s:["Grip shoulder-width, palms facing you.","Put your feet on the block for help.","Pull your chest up towards the bar.","Lower slowly for about 4 seconds."],c:["Shoulders down first","Feet help only as needed"],m:"Dropping quickly.",z:BR},
"lateral-raise":{q:"dumbbell lateral raise",u:"Light raise out to the sides for shoulders.",s:["Stand with light dumbbells at your sides.","Raise arms out sideways, leading with elbows.","Stop at shoulder height.","Lower slowly."],c:["Light weight","No shrugging"],m:"Swinging the body.",z:BR},
"hammer-curl":{q:"dumbbell hammer curl",u:"Curl with palms facing in.",s:["Stand with dumbbells at your sides, palms in.","Pin elbows to your sides.","Curl up towards your shoulders.","Lower slowly to straight arms."],c:["Elbows still","Slow lowering"],m:"Swinging the hips.",z:BR},
"db-rdl":{q:"dumbbell romanian deadlift",u:"Hip hinge for hamstrings and glutes.",s:["Hold dumbbells at your thighs, feet hip-width.","Soften knees and push your hips back.","Slide the weights to mid-shin, back flat.","Drive hips forward to stand, breathing out."],c:["Hips back, not down","Weights close to legs","Eyes a little ahead"],m:"Rounding the back.",z:"Breathe out to stand; keep your head above your hips."},
"dead-bug":{q:"dead bug exercise",u:"Lying core move, reaching opposite arm and leg.",s:["Lie on your back, arms up, knees over hips.","Press your lower back gently into the floor.","Reach one arm back and the opposite leg out.","Return and switch sides."],c:["Low back stays down","Move slowly"],m:"Back arching off the floor.",z:"Breathe out slowly as you reach."},
"reverse-lunge":{q:"dumbbell reverse lunge",u:"Step back into a lunge holding dumbbells.",s:["Stand tall holding dumbbells (or one, for offset).","Step one foot back and lower the knee.","Keep your chest tall and front heel down.","Push through the front foot to stand."],c:["Soft knee touch","Front knee over toes"],m:"Front knee caving in.",z:"Breathe out to stand; hold the rack if needed."},
"side-plank":{q:"side plank",u:"Hold your body straight on one elbow.",s:["Lie on your side, elbow under shoulder.","Bend knees for the easier short-lever version.","Lift your hips into a straight line.","Hold, then switch sides."],c:["Hips high","Elbow under shoulder"],m:"Hips sagging.",z:"Keep breathing; no breath-holding."},
"calf-raise":{q:"single leg calf raise",u:"One-leg heel raise on the edge of the block.",s:["Stand on one foot on the block edge.","Hold the rack lightly for balance.","Lower the heel slowly, then rise high.","Finish the reps, then switch."],c:["Full range","Pause top and bottom"],m:"Bouncing at the bottom.",z:BR},
"kb-swing":{q:"kettlebell swing",u:"Hip-powered swing to chest height.",s:["Stand with the bell a foot in front.","Hinge and hike it back between your legs.","Snap your hips forward to float it up.","Let it swing back and repeat."],c:["Hinge, don't squat","Arms stay relaxed"],m:"Lifting with the arms.",z:"Breathe out at the top of every swing."},
"incline-pushup":{q:"incline push up on bench",u:"Push-up with hands on a bench.",s:["Hands on the bench, just wider than shoulders.","Walk feet back into a straight line.","Lower your chest slowly to the bench.","Push away, breathing out."],c:["Body straight","Elbows about 45°"],m:"Hips sagging.",z:BR},
"kb-sumo-dl":{q:"kettlebell sumo deadlift",u:"Wide-stance deadlift with a kettlebell.",s:["Stand wide, toes out, bell between your feet.","Hinge and bend knees to grip, back flat.","Push the floor away to stand tall.","Lower the same way."],c:["Knees push out","Chest proud"],m:"Rounding to reach the bell.",z:BR},
"suitcase-carry":{q:"suitcase carry",u:"Walk holding one weight on one side.",s:["Pick up one weight at your side.","Stand tall, shoulders level.","Walk steadily without leaning.","Switch hands halfway."],c:["Shoulders level","Brace lightly"],m:"Leaning towards the weight.",z:"Breathe normally the whole time."},
"prone-y-raise":{q:"incline prone y raise",u:"Light raise into a Y, chest on the bench.",s:["Lie chest-down on an incline, thumbs up.","Set shoulder blades back and down.","Raise arms forward into a Y.","Lower slowly."],c:["Very light","Thumbs up"],m:"Shrugging with the neck.",z:BR},
"hip-9090":{q:"90 90 hip switch",u:"Seated hip rotation from side to side.",s:["Sit with both knees bent at 90°.","Sit tall, hands behind you if needed.","Rotate both knees to the other side.","Keep switching slowly."],c:["Tall spine","Feet stay put"],m:"Slumping and rushing.",z:"Stay in a pain-free range."},
"kb-sa-row":{q:"single arm kettlebell row",u:"One-arm row with a hand on the bench.",s:["Hand and knee on the bench, back flat.","Let the bell hang under your shoulder.","Row it towards your hip, breathing out.","Lower slowly, then switch."],c:["Elbow to hip","No twisting"],m:"Twisting to yank it up.",z:BR},
"Cat-cow":{q:"cat cow stretch",u:"Gentle spine wave on hands and knees.",s:["Hands under shoulders, knees under hips.","Breathe in and gently arch, chest forward.","Breathe out and round your back up.","Move slowly between the two."],c:["Segment by segment","Head in line"],m:"Rushing or cranking the neck.",z:"Keep your head level with your spine."},
"World's greatest stretch":{q:"worlds greatest stretch",u:"Lunge, elbow drop and rotation.",s:["Step into a long lunge, hands inside front foot.","Drop the front elbow towards the instep.","Rotate and reach that arm to the ceiling.","Return, repeat, then switch sides."],c:["Back leg long","Eyes follow the hand"],m:"Hips collapsing to the floor.",z:"Use the block so your head stays above hips."},
"Thoracic open book":{q:"thoracic open book stretch",u:"Side-lying upper-back rotation.",s:["Lie on your side, knees bent and stacked.","Arms straight out in front.","Open the top arm across, rotating your upper back.","Pause, breathe out, return."],c:["Knees stay together","Eyes follow the hand"],m:"Knees lifting apart.",z:"Breathe out into the rotation."},
"Broomstick pass-throughs":{q:"broomstick shoulder pass through",u:"Shoulder circle with a stick.",s:["Hold a stick wide in front of your hips.","Lift it overhead with straight arms.","Take it behind you as far as comfortable.","Return the same way."],c:["Wide grip","Ribs down"],m:"Grip too narrow.",z:"Widen the grip if it pinches."},
"Lunge with overhead reach":{q:"lunge with overhead reach",u:"Hip flexor stretch with a long reach.",s:["Step back into a lunge, back knee low.","Squeeze the back glute.","Reach the same-side arm overhead.","Hold briefly, then switch."],c:["Ribs down","Tall chest"],m:"Arching the lower back.",z:"Breathe out as you reach."},
"Wall slides":{q:"wall slides exercise",u:"Slide arms up a wall for shoulder control.",s:["Back to the wall, arms in a W.","Keep lower back and arms on the wall.","Slide arms up into a Y.","Slide back down slowly."],c:["Ribs down","Slow"],m:"Back arching off the wall.",z:"Breathe steadily."},
"Leg swings":{q:"leg swings dynamic stretch",u:"Loose swings to open the hips.",s:["Hold the rack for balance.","Swing one leg front to back or across.","Start small, build range gradually.","Switch legs."],c:["Tall posture","Relaxed"],m:"Swinging wildly at once.",z:"Smooth and controlled."},
"Bodyweight squat":{q:"bodyweight squat",u:"Slow squat with no weight.",s:["Stand feet shoulder-width, toes slightly out.","Sit down slowly between your heels.","Pause at a comfortable depth.","Stand, breathing out."],c:["Heels down","Chest up"],m:"Knees caving in.",z:BR},
"Ankle rocks":{q:"knee to wall ankle mobility",u:"Knee-over-toe rocks for ankle range.",s:["Half-kneel, front foot near a wall.","Keep the front heel down.","Rock the knee forward over your toes.","Rock back and repeat."],c:["Heel stays down","Knee over middle toe"],m:"Heel lifting.",z:"Pain-free range only."},
"Hip CARs":{q:"standing hip CARs controlled articular rotations",u:"Slow, full circles of one hip.",s:["Stand tall holding the rack.","Lift one knee up in front.","Open it out, then circle it behind you.","Reverse direction, then switch legs."],c:["Only the hip moves","Slow with tension"],m:"Twisting the pelvis.",z:"Breathe slowly; pain-free range."},
"Couch stretch":{q:"couch stretch",u:"Deep front-hip and thigh stretch.",s:["Kneel with your back shin up the bench.","Step the other foot forward into a lunge.","Squeeze the back glute, chest tall.","Hold and breathe."],c:["Pad under the knee","Ribs down"],m:"Arching the lower back.",z:"Ease in; breathe out into it."},
"Half-kneeling hip flexor with reach":{q:"half kneeling hip flexor stretch with reach",u:"Kneeling hip stretch with an overhead reach.",s:["Kneel on one knee, other foot forward.","Tuck your pelvis, squeeze the back glute.","Shift gently forward.","Reach the kneeling-side arm up and over."],c:["Small shift","Long reach"],m:"Leaning too far forward.",z:"Breathe out into the stretch."},
"90/90 hold":{q:"90 90 hip stretch lift offs",u:"Seated hip hold with small lift-offs.",s:["Sit with both knees bent at 90°.","Sit tall over the front shin.","Lift the back knee slightly off the floor.","Lower, repeat, then switch sides."],c:["Tall spine","Small, controlled lift"],m:"Leaning back to cheat.",z:"Keep breathing."},
"Doorway/rack chest stretch":{q:"doorway chest stretch",u:"Forearm on the rack, gentle chest stretch.",s:["Forearm on the rack at shoulder height.","Step through gently until you feel it.","Hold and breathe.","Switch sides."],c:["Elbow at shoulder height","Gentle"],m:"Pushing into pain.",z:"Breathe out into it."},
"Seated lat reach at bench":{q:"seated lat stretch",u:"Side-of-back stretch with elbows on the bench.",s:["Kneel facing the bench, elbows on it.","Sit hips back, head level.","Feel the stretch down your back.","Lean slightly to each side."],c:["Head in line","Long exhale"],m:"Head dropping below hips.",z:"Keep the head level."},
"Shoulder CARs":{q:"shoulder CARs controlled articular rotations",u:"Slow, full circles of one shoulder.",s:["Stand tall, fist made, brace lightly.","Raise the straight arm forward and up.","Circle it behind you and down.","Reverse, then switch arms."],c:["Only the shoulder moves","Ribs down"],m:"Twisting the torso.",z:"Breathe slowly; pain-free range."},
"Ankle CARs":{q:"ankle CARs",u:"Slow circles of the ankle.",s:["Sit or stand, lift one foot.","Point and flex the foot.","Draw big slow circles both ways.","Switch feet."],c:["Shin stays still","Big circles"],m:"Moving the whole leg.",z:"Pain-free range."},
"Supported deep squat hold":{q:"supported deep squat hold",u:"Rest in a deep squat holding the rack.",s:["Hold the rack upright with both hands.","Sit down into a deep squat.","Hold, chest up, breathing slowly.","Stand using the rack."],c:["Heels down if you can","Chest tall"],m:"Head dropping forward.",z:"Keep the head up; breathe."},
"Wrist CARs":{q:"wrist CARs",u:"Slow wrist circles.",s:["Hold your forearm still with the other hand.","Make a fist.","Draw slow, big circles both ways.","Switch sides."],c:["Forearm still","Full range"],m:"Rushing.",z:""},
"Slow breathing lying on back":{q:"diaphragmatic breathing lying down",u:"Calm belly breathing to finish.",s:["Lie on your back, knees bent.","Breathe in through the nose for 4 seconds.","Breathe out slowly for 6 seconds.","Relax more with each breath."],c:["Belly rises first","Relax the jaw"],m:"Forcing big chest breaths.",z:"Stop if you feel dizzy."},
"Calf stretch on block":{q:"calf stretch on step",u:"Heel drop off the block for the calf.",s:["Ball of one foot on the block.","Hold the rack and lower the heel.","Hold straight, then with knee slightly bent.","Switch sides."],c:["Slow","Hold the rack"],m:"Bouncing.",z:""},
"Bird-dog":{q:"bird dog exercise",u:"Reach opposite arm and leg on hands and knees.",s:["Hands and knees, back flat.","Reach one arm forward, opposite leg back.","Hold one second, hips level.","Return slowly and switch."],c:["Hips level","Reach long, not high"],m:"Twisting or arching.",z:"Breathe out as you reach; head level."}};
var HAL={"Segmental cat-cow":"Cat-cow","Standing hip CARs":"Hip CARs","Standing hip circles":"Hip CARs","Walking lunge with overhead reach":"Lunge with overhead reach","90/90 hold with lift-offs":"90/90 hold","90/90 end-range hold":"90/90 hold","90/90 hip switches":"hip-9090","Side plank":"side-plank","Dead bug":"dead-bug"};
function hkey(n){var k=n.replace(/\s*\(.*?\)/g,"").replace(/ – .*$/,"").replace(/,.*$/,"").replace(/ @.*$/,"").replace(/ \+ lift-offs$/,"").trim();return HAL[k]||k;}
function demoURL(q){return "https://www.youtube.com/results?search_query="+encodeURIComponent(q+" how to").replace(/%20/g,"+");}

// ---- programme: date -> session id (add future weeks here)
Object.assign(X,{"kb-floor-press":["Kettlebell floor press","12–16 kg","12–16",1],"scap-pullup":["Scap pull-up (hang)","Bodyweight","",0],"kb-halo":["Kettlebell halo","8–12 kg","8–12",1],"dip-hold":["Dip bar support hold","Bodyweight","",0],"kb-curl":["Kettlebell horn curl","12–16 kg","12–16",1],"split-squat":["Split squat (hold rack)","Bodyweight or 8–12 kg each","8–12",1],"glute-bridge":["Glute bridge","Bodyweight or 16–20 kg","16–20",1],"single-leg-rdl":["Single-leg kettlebell RDL","12–16 kg","12–16",1],"wall-sit":["Wall sit","Bodyweight","",0],"db-squat-press":["Dumbbell squat to press","6–10 kg each","6–10",1]});
Object.assign(HT,{
"kb-floor-press":{q:"kettlebell floor press",u:"One-arm chest press lying on the floor.",s:["Lie on your back, knees bent, bell at your chest.","Rest your upper arm on the floor.","Press the bell straight up, breathing out.","Lower until the elbow touches down softly."],c:["Wrist straight","Free hand on your belly"],m:"Bouncing the elbow off the floor.",z:BR},
"scap-pullup":{q:"scapular pull up",u:"Shoulder-blade pull while hanging from the bar.",s:["Hang from the bar, feet on the block if needed.","Keep your elbows straight.","Pull your shoulders down away from your ears.","Lower slowly back to a relaxed hang."],c:["Small movement","Straight arms"],m:"Bending the elbows into a pull-up.",z:BR},
"kb-halo":{q:"kettlebell halo",u:"Slow bell circle around your head.",s:["Stand tall holding the bell upside down by the horns.","Circle it slowly around your head.","Keep it close, elbows soft.","Reverse direction each rep."],c:["Ribs down","Light bell"],m:"Arching the lower back.",z:"Breathe steadily; keep your head still and level."},
"dip-hold":{q:"dip bar support hold",u:"Hold yourself up on straight arms on the dip bars.",s:["Hands on the dip bars, feet on the block.","Press up until your arms are straight.","Shoulders down, chest proud.","Hold, breathing steadily, then step down."],c:["Shoulders away from ears","Feet help as needed"],m:"Shrugging the shoulders up.",z:"Breathe steadily; no breath-holding."},
"kb-curl":{q:"kettlebell horn curl",u:"Curl holding the bell by the horns.",s:["Stand holding the bell by the horns.","Pin your elbows to your sides.","Curl the bell up to your chest.","Lower slowly."],c:["Elbows still","No swinging"],m:"Leaning back to lift.",z:BR},
"split-squat":{q:"split squat",u:"Static lunge holding the rack for balance.",s:["Stand in a long split stance, hand on the rack.","Lower the back knee softly towards the floor.","Keep your chest tall.","Push up through the front foot."],c:["Front heel down","Torso upright"],m:"Front knee caving in.",z:BR},
"glute-bridge":{q:"glute bridge",u:"Hip lift lying on your back.",s:["Lie on your back, knees bent, feet flat.","Squeeze your glutes and lift your hips.","Pause at the top, ribs down.","Lower slowly."],c:["Push through heels","No back arch"],m:"Arching the back at the top.",z:BR},
"single-leg-rdl":{q:"single leg romanian deadlift kettlebell",u:"One-leg hip hinge with a hand on the rack.",s:["Hold the rack with one hand, bell in the other.","Stand on the leg opposite the bell.","Hinge forward, back leg reaching behind.","Stand up tall, breathing out."],c:["Hips square","Head level with the spine"],m:"Twisting open at the hips.",z:"Breathe out to stand; keep your head above your hips."},
"wall-sit":{q:"wall sit",u:"Hold a seated position against a wall.",s:["Back flat against the wall.","Slide down until knees are about 90°.","Hold, breathing steadily.","Slide back up to stand."],c:["Knees over ankles","Breathe"],m:"Holding your breath.",z:"Keep breathing the whole time."},
"db-squat-press":{q:"dumbbell squat to press",u:"Light squat then overhead press.",s:["Hold light dumbbells at your shoulders.","Squat down with your chest up.","Stand, then press the dumbbells overhead.","Lower to shoulders and repeat."],c:["Light weights","Ribs down when pressing"],m:"Arching the back on the press.",z:BR},
"Glute bridge":{q:"glute bridge",u:"Hip lift lying on your back.",s:["Lie on your back, knees bent, feet flat.","Squeeze your glutes and lift your hips.","Pause at the top, ribs down.","Lower slowly."],c:["Push through heels","No back arch"],m:"Arching the back at the top.",z:BR}});
// ---- quick option (third choice for a day): date -> session id
Object.assign(HT,{
"Single-arm swing":{q:"single arm kettlebell swing",u:"One-hand hip-powered swing to chest height.",s:["Bell a foot in front, one hand on the handle.","Hinge and hike it back high between your legs.","Snap your hips to float it to chest height.","Free arm stays relaxed by your side.","Do all reps, then park the bell."],c:["Hinge, don't squat","Shoulder packed, arm loose"],m:"Lifting with the arm or rotating the torso.",z:"Breathe out sharply at the top of every swing."},
"Kettlebell clean":{q:"kettlebell clean single arm",u:"Bring the bell to the rack position smoothly.",s:["Hike the bell back like a swing.","Drive the hips and keep the elbow close.","Let the bell roll round your wrist, no bang.","Finish in the rack: fist by chin, elbow down.","Lower back to the hike and repeat."],c:["Zip the bell up close","Soft landing on the forearm"],m:"Swinging wide so the bell crashes onto the wrist.",z:"Breathe out as the bell lands in the rack."},
"Single-arm press":{q:"single arm kettlebell overhead press",u:"Standing one-arm press from the rack.",s:["Start in the rack, glutes and abs lightly on.","Press up and slightly out, biceps by your ear.","Lock out with the wrist straight.","Lower slowly back to the rack."],c:["Ribs down, no lean back","Squeeze the free fist"],m:"Leaning back to finish the press.",z:"Breathe out as you press; never hold your breath."},
"Front-rack squat":{q:"single arm kettlebell front rack squat",u:"Squat holding one bell in the rack.",s:["Bell in the rack, feet shoulder width.","Sit down between your hips, chest tall.","Go as deep as stays smooth.","Stand by driving the floor away."],c:["Elbow stays tucked","Don't lean toward the bell"],m:"Twisting or leaning away from the bell.",z:"Breathe out on the way up."},
"Split-stance row":{q:"split stance single arm kettlebell row",u:"One-arm row from a staggered stance.",s:["Step one foot forward, free hand on that thigh.","Hinge forward, flat back, head level with spine.","Row the bell to your hip.","Lower slowly to a long arm."],c:["Elbow to back pocket","Hips stay square"],m:"Twisting the torso to heave the bell.",z:"Breathe out as you row; keep your head above hip height."},
"Kettlebell hip hinge drill":{q:"kettlebell deadlift hip hinge",u:"Slow two-hand deadlift to groove the hinge.",s:["Bell between your feet, hands on the horns.","Push the hips back, shins near vertical.","Stand tall by squeezing the glutes.","Lower slowly with a flat back."],c:["Hips back, not down","Long spine"],m:"Rounding the back to reach the bell.",z:BR},
"Prying goblet squat":{q:"prying goblet squat",u:"Goblet squat hold that opens the hips.",s:["Hold the bell at your chest.","Sit down into a deep, comfortable squat.","Use your elbows to gently push the knees out.","Shift side to side, then stand up slowly."],c:["Heels down","Chest tall"],m:"Forcing depth until the back rounds.",z:"Breathe slowly; stand up slowly if you feel lightheaded."},
"Single-arm kettlebell deadlift":{q:"single arm kettlebell deadlift",u:"One-hand deadlift that trains anti-lean.",s:["Bell beside one foot.","Hinge and grip it with one hand.","Stand tall without leaning toward the bell.","Lower slowly and repeat."],c:["Shoulders level","Hips back"],m:"Leaning toward the bell.",z:BR},
"Suitcase hold":{q:"kettlebell suitcase hold",u:"Stand tall holding the bell at one side.",s:["Hold the bell by your side, arm long.","Stand tall, shoulders level.","Breathe slowly through the nose.","Switch hands when cued."],c:["Don't lean","Ribs down"],m:"Shrugging or leaning away.",z:"Keep breathing steadily; never hold your breath."},
"Lying figure-4 stretch":{q:"supine figure four stretch",u:"Gentle glute stretch lying on your back.",s:["Lie on your back, knees bent, head down flat.","Cross one ankle over the other knee.","Pull the lower thigh gently towards you.","Breathe slowly with long exhales."],c:["Relax the shoulders","Gentle, no forcing"],m:"Lifting the head and neck to pull harder.",z:"Breathe out slowly; ease off if anything pinches."}});
HAL["Kettlebell halo"]="kb-halo";
function q17(){var s=[],A="Swing ×5, Clean ×3, Press ×3",B="Front-rack squat ×4, Row ×6";for(var r=1;r<=5;r++){var c=r%2?A:B,t=" · round "+r+"/5";s.push(["READY",10,c+" · left side"+t]);s.push(["WORK",45,c+" · left side"+t]);s.push(["WORK",45,c+" · switch → right side"+t]);if(r<5)s.push(["REST",20,"Rest · park the bell"]);}return s;}
SESS.kbq17={name:"15-min KB Flow (16 kg)",short:"KB 15",quick:1,g0:200,safe:"One 16 kg kettlebell, calm pace. Breathe out on every swing, clean and press; never hold your breath. Smooth reps at RPE 6–7, 2 reps short of failure (2 RIR).",blocks:[
 fl("q17wu","Warm-up","Kettlebell warm-up","Slow and smooth with the 16 kg bell.",[["Kettlebell halo, slow, alternate direction",40],["Kettlebell hip hinge drill",40],["Prying goblet squat",50],["Single-arm kettlebell deadlift – each side",40]],"WARM-UP","up"),
 {k:"timer",id:"q17a",h:"Every 2:00 × 5",name:"Single-bell flow",note:"Each round: 45 s left · 45 s right · 20 s rest. RPE 6–7.",small:NOREST,segs:q17(),groups:[["Rounds 1 · 3 · 5",[["Single-arm swing","Swing",5],["Kettlebell clean","Clean",3],["Single-arm press","Press",3]]],["Rounds 2 · 4",[["Front-rack squat","Front-rack squat",4],["Split-stance row","Row",6]]]],list:["Single-arm swing – ×5","Kettlebell clean – ×3","Single-arm press – ×3","Front-rack squat – ×4","Split-stance row – ×6"]},
 fl("q17fin","Cool-down","Hold → down-regulate","Long, slow exhales to wind down for the evening.",[["Suitcase hold – left",30],["Suitcase hold – right",30],["Lying figure-4 stretch, slow nasal breathing – each side",60]],"FINISH","down")]};
var QK={"2026-10-17":"kbq17"};
function qOn(k){var a=LS.get("wo_quick",{})||{};return !!a[k];}
function setQ(k,v){var a=LS.get("wo_quick",{})||{};if(v)a[k]=1;else delete a[k];LS.set("wo_quick",a);}
// ==== WEEK 2 · Mon 19 – Sun 25 Oct 2026 (added by the Health & Fitness bot; rationale in docs/programme-week2.md) ====
Object.assign(X,{"rfess":["Rear-foot-elevated split squat","8–12 kg each","8–12",1],"bird-dog":["Bird-dog","Bodyweight","",0],"sl-glute-bridge":["Single-leg glute bridge","Bodyweight","",0],"wall-slide":["Wall slide","Bodyweight","",0]});
Object.assign(HT,{
"rfess":{q:"dumbbell rear foot elevated split squat",u:"Single-leg squat with the back foot on the bench.",s:["Back foot laces-down on the bench, front foot forward.","Hold the rack or light dumbbells at your sides.","Lower the back knee slowly towards the floor.","Drive through the front heel to stand, breathing out."],c:["Front heel stays down","Torso tall, slight forward lean is fine","Short stance? Step the front foot further out"],m:"Bouncing off the bottom or pushing off the back foot.",z:"Breathe out to stand; hold the rack for balance."},
"bird-dog":HT["Bird-dog"],
"sl-glute-bridge":{q:"single leg glute bridge",u:"Hip lift on one leg, lying on your back.",s:["Lie on your back, knees bent, feet flat.","Lift one foot, knee over hip.","Push through the planted heel to lift your hips.","Pause, lower slowly, then switch legs."],c:["Hips stay level","Ribs down"],m:"Hips dropping on the lifted-leg side.",z:BR},
"wall-slide":HT["Wall slides"],
"Side-lying windmill":{q:"side lying windmill stretch",u:"Lying arm circle that opens the upper back.",s:["Lie on your side, knees bent and stacked, head supported.","Trace a big circle overhead with the top arm.","Let your upper back open as the arm goes behind.","Return slowly, then switch sides."],c:["Knees stay together","Eyes follow the hand"],m:"Rolling the hips to fake the range.",z:"Breathe out as the arm opens."}});
HAL["Kettlebell swing"]="kb-swing";HAL["Wall sit"]="wall-sit";HAL["Incline push-up"]="incline-pushup";
// Sat 24 EMOM: every minute in order – complex left, complex right, two-hand swings – 4 rounds (12 min, no rest after the last)
function k24(){var s=[],C="Complex",n=4;for(var r=1;r<=n;r++){var t=" · round "+r+"/"+n;s.push(["READY",10,C+" · left side"+t]);s.push(["WORK",35,C+" · left side"+t]);s.push(["REST",15,"Rest · switch hands"]);
 s.push(["READY",10,C+" · switch → right side"+t]);s.push(["WORK",35,C+" · right side"+t]);s.push(["REST",15,"Rest · swings next"]);
 s.push(["READY",10,"Two-hand swing ×10"+t]);s.push(["WORK",25,"Two-hand swing ×10"+t]);if(r<n)s.push(["REST",25,"Rest · complex next"]);}return s;}
Object.assign(SESS,{
mob19:{name:"Recovery · Hips + Ankles Flow",short:"Mobility",rest:1,safe:"Recovery day. Slow controlled moves and gentle holds – no head-down positions, no forcing, breathe slowly.",blocks:[
 {k:"rest",name:"Recovery day",note:"Rest, or do the optional 15-min flow. Walk, hydrate, sleep well."},
 fl("m19","Flow","Hips + ankles flow","Gentle hip and ankle range. 10 s set-up only on position changes.",[["Ankle CARs – each side",80],["World's greatest stretch – each side",80],["Bodyweight squat, slow",80],["Calf stretch on block – each side",80],["Half-kneeling hip flexor with reach – each side",80],["Bird-dog, slow",80],["Glute bridge, slow",80],["90/90 hip switches",60],["Lying figure-4 stretch – each side",80],["Slow breathing lying on back",150]],"MOBILITY")]},
up20:{name:"Strength A2 · Upper",short:"Upper",safe:"Quality first at RPE 6–7. Breathe out on every press and pull, never hold your breath, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("u20wu","Warm-up","Shoulder prep – upper","No forcing.",[["Cat-cow, slow",40],["Shoulder CARs – each side",60],["Wall slides",40],["Broomstick pass-throughs",40],["Thoracic open book – each side",60]],"WARM-UP"),
 {k:"ex",h:"A · Straight sets",mode:"sup",n:4,rr:[90,120],unit:"Set",tid:"u20a",items:[{x:"db-bench",lab:"A1",rp:6,tp:"3110",cue:"Flat bench. Start about 2 kg above last week's incline press. 3 s down, 1 s pause, breathe out as you press."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"u20b",items:[{x:"assisted-chinup",lab:"B1",rp:5,tp:"3010",cue:"Feet on block – use a little less leg help than last week."},{x:"cs-row",lab:"B2",rp:10,tp:"2011",sw:15,cue:"Same weight as last week, 2 more reps. Pause at the top."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"u20c",items:[{x:"farmers-carry",lab:"C1",rp:40,ru:"m",cue:"Two dumbbells, tall posture, short steps, breathe steadily."},{x:"wall-slide",lab:"C2",rp:8,tp:"2121",sw:15,cue:"Back and arms on the wall, slide up slowly, ribs down."}]},
 {k:"timer",id:"u20fl",h:"Intervals",name:"Row intervals 5 × 0:30 / 0:30",note:"Each round: 0:30 work · 0:30 rest. Moderate pace, RPE 7.",small:["Work 24–26 s/m · rest light paddle · damper 4–5.",NOREST],segs:[["READY",10,"Row · moderate pace"]].concat(iv(5,30,30,"moderate pace","light paddle"))},
 fl("u20cd","Cool-down","Active stretch – upper","Breathe out into each stretch.",[["Doorway/rack chest stretch – each side",60],["Seated lat reach at bench – each side",60],["Half-kneeling hip flexor with reach – each side",60],["Slow breathing lying on back",60]])]},
run21:{name:"Zone 2 Run · 5–6 km",short:"Run",safe:STOP_RUN,blocks:[
 fl("r21wu","Warm-up","Dynamic stretch – run","",[["Ankle CARs – each side",40],["Leg swings – front to back",40],["Leg swings – side to side",40],["Walking lunge with overhead reach",40],["Standing hip CARs – each side",40]],"WARM-UP"),
 tm("r21w","Warm-up","Warm-up walk","Easy walk, RPE 3–4.",180,"WARM-UP"),
 tm("r21run","Steady","Zone 2 run","Steady pace, Zone 2, RPE 5–6.",1800,"JOG",{counter:1,small:["Aim for 5–6 km; finish early if you reach 6 km.","1:00 walk break whenever needed: tap +1 walk break."]}),
 tm("r21cd","Cool-down","Cool-down walk","Easy walk, RPE 3–4.",180,"COOL-DOWN",{small:"Then stretch calves, hamstrings and hips."}),{k:"fields"}]},
mob22:{name:"Recovery · Shoulders + Spine Flow",short:"Mobility",rest:1,safe:"Recovery day. Slow controlled rotations and gentle holds – no head-down positions, no forcing, breathe slowly.",blocks:[
 {k:"rest",name:"Recovery day",note:"Rest, or do the optional 15-min flow. Walk, hydrate, sleep well."},
 fl("m22","Flow","Shoulders + spine flow","Upper-body range after Tuesday. 10 s set-up only on position changes.",[["Wrist CARs – each side",60],["Shoulder CARs – each side",80],["Broomstick pass-throughs, slow",70],["Doorway/rack chest stretch – each side",90],["Wall slides",70],["Seated lat reach at bench – each side",90],["Cat-cow, slow",60],["Thoracic open book – each side",90],["Side-lying windmill – each side",80],["Slow breathing lying on back",140]],"MOBILITY")]},
lo23:{name:"Strength B2 · Lower + Core",short:"Lower",safe:"No heavy spinal loading. Quality first at RPE 6–7, breathe out on the effort, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("l23wu","Warm-up","Hip prep – lower","No forcing.",[["Ankle rocks – each side",60],["Leg swings – front to back",40],["Bodyweight squat, slow",40],["World's greatest stretch – each side",60],["Glute bridge, slow",40]],"WARM-UP"),
 {k:"ex",h:"A · Straight sets",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"l23a",items:[{x:"rfess",lab:"A1",rp:6,side:1,tp:"3110",cue:"Back foot on the bench. Hold the rack, or light dumbbells once balance is solid."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"l23b",items:[{x:"db-rdl",lab:"B1",rp:8,tp:"3111",cue:"Last week's weight, slower: 3 s down, pause at mid-shin. Head above hips."},{x:"bird-dog",lab:"B2",rp:4,side:1,tp:"2111",sw:15,cue:"Slow reach, hips level, breathe out as you reach."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"l23c",items:[{x:"suitcase-carry",lab:"C1",rp:40,ru:"m",cue:"One heavy dumbbell, switch hands halfway. Stand tall, don't lean."},{x:"sl-glute-bridge",lab:"C2",rp:8,side:1,tp:"2011",sw:15,cue:"On the floor, hips level, squeeze at the top."}]},
 {k:"timer",id:"l23fl",h:"Steady",name:"Easy row 4:00",note:"Easy pace, RPE 3–4.",small:"18–20 s/m · damper 4–5 · flush the legs.",segs:[["READY",10,"Easy row"],["EASY",240,"Easy row · easy pace"]]},
 fl("l23cd","Cool-down","Active stretch – lower","Breathe out into each stretch.",[["Couch stretch – each side",60],["Calf stretch on block – each side",60],["90/90 hold with lift-offs – each side",60],["Lying figure-4 stretch – each side",60]])]},
kb24:{name:"KB EMOM + Zone 2 Run",short:"KB",safe:"One 16 kg kettlebell. Breathe out on every clean, press and swing; never hold your breath. Smooth reps at RPE 6–7, 2 reps short of failure (2 RIR).",blocks:[
 fl("k24wu","Warm-up","Kettlebell warm-up","Slow and smooth with the 16 kg bell.",[["Kettlebell halo, slow, alternate direction",40],["Prying goblet squat",50],["Kettlebell hip hinge drill",40],["World's greatest stretch – each side",60],["Leg swings – side to side",40]],"WARM-UP","up"),
 {k:"timer",id:"k24a",h:"EMOM 60 s × 12",name:"Single-bell EMOM",note:"Each 60 s: complex left · complex right · swings.",small:["Complex = clean, front-rack squat, press (one side).",NOREST],segs:k24(),list:["Kettlebell clean – ×2 each side","Front-rack squat – ×2 each side","Single-arm press – ×2 each side","Kettlebell swing – ×10"]},
 tm("k24run","Steady","Zone 2 run","Steady pace, Zone 2, RPE 5–6.",900,"JOG",{counter:1,small:"Outside or Assault Runner. 1:00 walk break whenever needed."}),
 fl("k24cd","Cool-down","Active stretch","Breathe out into each stretch.",[["Calf stretch on block – each side",60],["Couch stretch – each side",60],["Thoracic open book – each side",60]])]},
walk25:{name:"Long Walk + Stretch",short:"Walk",safe:"Longer walk this week, nasal breathing, outside if you can or on the Assault Runner. Easy pace, RPE 3–4.",blocks:[
 tm("w25walk","Steady","Long walk (Zone 1–2)","Easy pace, RPE 3–4.",1800,"EASY",{small:"Hills are fine at the same effort. Outside or Assault Runner."}),
 fl("w25st","Cool-down","Stretch","Breathe out into each stretch.",[["Calf stretch on block – each side",60],["Half-kneeling hip flexor with reach – each side",60],["Seated lat reach at bench – each side",60],["Lying figure-4 stretch – each side",60],["Slow breathing lying on back",60]]),{k:"fields"}]},
// ---- week-2 backups (g0 100)
bk19:{name:"Backup · Recovery Walk + Breathe",short:"Walk",g0:100,safe:"Recovery day. Zone 1 walk with nasal breathing, then slow breathing. Easy pace, RPE 3–4.",blocks:[
 tm("x19walk","Steady","Recovery walk (Zone 1)","Easy pace, RPE 3–4.",720,"EASY",{small:"Nasal breathing, outside if you can."}),
 fl("x19br","Cool-down","Down-regulate","Slow, calm breathing.",[["Lying figure-4 stretch – each side",60],["Slow breathing lying on back",90]],"MOBILITY")]},
bk20:{name:"Backup · Upper (KB + Bench)",short:"Upper",g0:100,safe:"Less kit: one kettlebell plus the bench and bars. RPE 6–7, breathe out on every press and pull, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("x20wu","Warm-up","Dynamic stretch – upper","No forcing.",MV.up),
 {k:"ex",h:"A · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"x20a",items:[{x:"incline-pushup",lab:"A1",rp:10,tp:"3010",cue:"Hands on the bench, body straight, 3 s down."},{x:"kb-sa-row",lab:"A2",rp:8,side:1,tp:"2011",sw:15,cue:"Hand on bench, flat back, pull to the hip."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:2,rr:[45,75],unit:"Set",tid:"x20b",items:[{x:"kb-halo",lab:"B1",rp:4,side:1,tp:"2020",cue:"Light bell, slow circles, ribs down."},{x:"dip-hold",lab:"B2",rp:20,ru:"s",sw:15,cue:"Arms straight on the dip bars, feet on block if needed."}]},
 {k:"timer",id:"x20fl",h:"Intervals",name:"Row intervals 4 × 0:30 / 0:30",note:"Each round: 0:30 work · 0:30 rest. Moderate pace, RPE 7.",small:["Work 22–24 s/m · rest light paddle · damper 4–5.",NOREST],segs:[["READY",10,"Row · moderate pace"]].concat(iv(4,30,30,"moderate pace","light paddle"))},
 fl("x20cd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cdu)]},
bk21:{name:"Backup · Zone 2 Row + Core",short:"Row",g0:100,safe:"No running. Zone 2 row: conversational, a little breathless. Damper 4–5, breathe steadily. Steady pace, RPE 5–6.",blocks:[
 fl("x21wu","Warm-up","Dynamic stretch","",MV.full),
 {k:"timer",id:"x21row",h:"Steady",name:"Zone 2 row",note:"Steady pace, Zone 2, RPE 5–6.",small:"20:00 at 18–20 s/m · damper 4–5.",segs:[["READY",10,"Zone 2 row"],["STEADY",1200,"Zone 2 row · steady pace"]]},
 {k:"timer",id:"x21core",h:"Circuit × 2",name:"Floor core",note:"Each round: 25–40 s per move · 30 s rest.",small:"Side plank with knees down. Exhale slowly, no breath-holding.",segs:core(2,[["Glute bridge @2011",40,15],["Bird-dog @2121, alternate",40,15],["Side plank",25,15,1]],30),list:["Glute bridge @2011 – 40 s","Bird-dog @2121 – 40 s","Side plank – 25 s each side"]},
 fl("x21cd","Cool-down","Active stretch","",MV.cd),{k:"fields",dist:"Distance (m, from PM5)"}]},
bk22:{name:"Backup · Easy Row + Breathe",short:"Row",g0:100,safe:"Recovery day. Very light rowing with nasal breathing, then slow breathing. Easy pace, RPE 3–4.",blocks:[
 {k:"timer",id:"x22row",h:"Steady",name:"Easy row",note:"Easy pace, RPE 3–4.",small:"12:00 at 18–20 s/m · damper 3–4.",segs:[["READY",10,"Easy row"],["EASY",720,"Easy row · easy pace"]]},
 fl("x22br","Cool-down","Down-regulate","Slow, calm breathing.",[["Seated lat reach at bench – each side",60],["Thoracic open book – each side",60],["Slow breathing lying on back",90]],"MOBILITY")]},
bk23:{name:"Backup · Lower (Bodyweight + Core)",short:"Lower",g0:100,safe:"Lower energy, light loads, no spinal loading. RPE 6, breathe out on the effort, hold the rack for balance.",blocks:[
 fl("x23wu","Warm-up","Dynamic stretch – lower","No forcing.",MV.low),
 {k:"ex",h:"A · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"x23a",items:[{x:"split-squat",lab:"A1",rp:8,side:1,tp:"3010",cue:"Static split stance, hold the rack, back knee lowers softly."},{x:"dead-bug",lab:"A2",rp:5,side:1,tp:"2020",sw:15,cue:"Low back flat, slow exhale as you reach."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"x23b",items:[{x:"glute-bridge",lab:"B1",rp:12,tp:"2011",cue:"On the floor, squeeze glutes at the top, ribs down."},{x:"suitcase-carry",lab:"B2",rp:30,ru:"m",sw:15,cue:"One kettlebell, switch hands halfway. Stand tall."}]},
 fl("x23cd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cd)]},
bk24:{name:"Backup · Zone 2 Row + Bodyweight",short:"Row",g0:100,safe:"No kettlebell. Zone 2 row then light bodyweight work; breathe out on every effort. Steady pace, RPE 5–6.",blocks:[
 fl("x24wu","Warm-up","Dynamic stretch – full body","",MV.full),
 {k:"timer",id:"x24row",h:"Steady",name:"Zone 2 row",note:"Steady pace, Zone 2, RPE 5–6.",small:"15:00 at 18–20 s/m · damper 4–5.",segs:[["READY",10,"Zone 2 row"],["STEADY",900,"Zone 2 row · steady pace"]]},
 {k:"timer",id:"x24c",h:"Circuit × 2",name:"Bodyweight circuit",note:"Each round: 30–40 s per move · 30 s rest.",small:"Smooth reps, breathe out on every effort.",segs:core(2,[["Incline push-up",30,15],["Glute bridge @2011",40,15],["Bird-dog @2121, alternate",40,15]],30),list:["Incline push-up – 30 s","Glute bridge @2011 – 40 s","Bird-dog @2121 – 40 s"]},
 fl("x24cd","Cool-down","Active stretch","",MV.cd),{k:"fields",dist:"Distance (m, from PM5)"}]},
bk25:{name:"Backup · Gentle Stretch + Breathe",short:"Stretch",rest:0,g0:100,safe:"Lowest energy option. Long, gentle holds – no forcing, no head-down positions, breathe slowly.",blocks:[
 fl("x25fl","Flow","Gentle stretch","Gentle holds, no forcing.",[["Wall slides",60],["Half-kneeling hip flexor with reach – each side",90],["Cat-cow, slow",60],["Glute bridge, slow",60],["Side-lying windmill – each side",90],["Lying figure-4 stretch – each side",90],["Doorway/rack chest stretch – each side",90],["Calf stretch on block – each side",90],["Slow breathing lying on back",210]],"MOBILITY")]}});
// ==== WEEK 3 · Mon 26 Oct – Sun 1 Nov 2026 (added by the Health & Fitness bot; rationale in docs/programme-week3.md) ====
// Wed 28 = hospital test day (rest), so the run moves to Tue (steady only) and Lower to Thu.
// Sat 31 EMOM: minute 1 complex left, minute 2 complex right, minute 3 swings – 5 rounds (15 min, no rest after the last)
function k31(){var s=[],C="Complex",n=5;for(var r=1;r<=n;r++){var t=" · round "+r+"/"+n;s.push(["READY",5,C+" · left side"+t]);s.push(["WORK",40,C+" · left side"+t]);s.push(["REST",15,"Rest · switch hands"]);
 s.push(["READY",5,C+" · switch → right side"+t]);s.push(["WORK",40,C+" · right side"+t]);s.push(["REST",15,"Rest · swings next"]);
 s.push(["READY",10,"Two-hand swing ×15"+t]);s.push(["WORK",35,"Two-hand swing ×15"+t]);if(r<n)s.push(["REST",15,"Rest · complex next"]);}return s;}
Object.assign(SESS,{
up26:{name:"Strength A3 · Upper",short:"Upper",safe:"More reps, same weight. Still RPE 6–7: breathe out on every press and pull, never hold your breath, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("u26wu","Warm-up","Shoulder prep – upper","No forcing.",[["Cat-cow, slow",40],["Broomstick pass-throughs",40],["Wall slides",40],["Thoracic open book – each side",60]],"WARM-UP"),
 {k:"ex",h:"A · Straight sets",mode:"sup",n:4,rr:[90,120],unit:"Set",tid:"u26a",items:[{x:"db-bench",lab:"A1",rp:8,tp:"3110",cue:"Same weight as last Tuesday, now 8 reps (was 6). If last week felt RPE 6 or less, add 2 kg and do 6–8."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"u26b",items:[{x:"assisted-chinup",lab:"B1",rp:6,tp:"3010",cue:"6 reps (was 5), feet on block, a touch less leg help."},{x:"cs-row",lab:"B2",rp:12,tp:"2011",sw:15,cue:"Same weight, 12 reps (was 10). Pause at the top."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"u26c",items:[{x:"hk-db-press",lab:"C1",rp:8,side:1,tp:"2010",cue:"Half-kneeling, ribs down, breathe out on the press."},{x:"farmers-carry",lab:"C2",rp:50,ru:"m",sw:15,cue:"50 m (was 40 m), same dumbbells. Tall, short steps, breathe."}]},
 {k:"timer",id:"u26fl",h:"Intervals",name:"Row intervals 6 × 0:30 / 0:30",note:"Each round: 0:30 work · 0:30 rest. Moderate pace, RPE 7.",small:["One more than last week. Work 24–26 s/m · damper 4–5.",NOREST],segs:[["READY",10,"Row · moderate pace"]].concat(iv(6,30,30,"moderate pace","light paddle"))},
 fl("u26cd","Cool-down","Active stretch – upper","Breathe out into each stretch.",[["Doorway/rack chest stretch – each side",60],["Seated lat reach at bench – each side",60],["Slow breathing lying on back",60]])]},
run27:{name:"Zone 2 Run · 31 min",short:"Run",safe:STOP_RUN,blocks:[
 fl("r27wu","Warm-up","Dynamic stretch – run","",MV.run),
 tm("r27w","Warm-up","Warm-up walk","Easy walk, RPE 3–4.",120,"WARM-UP"),
 tm("r27run","Steady","Zone 2 run","Steady pace, Zone 2, RPE 5–6.",1860,"JOG",{counter:1,small:["1 min longer than last week. Keep it conversational.","Hospital test tomorrow: stay steady, never push the pace.","1:00 walk break whenever needed: tap +1 walk break."]}),
 tm("r27cd","Cool-down","Cool-down walk","Easy walk, RPE 3–4.",120,"COOL-DOWN",{small:"Then stretch calves, hamstrings and hips."}),{k:"fields"}]},
mob28:{name:"Hospital Day · Rest",short:"Rest",rest:1,safe:"Test day: rest. Only if you feel fine afterwards: gentle moves, no forcing, no head-down positions, breathe slowly.",blocks:[
 {k:"rest",name:"Hospital test 10:00 – rest",note:"No training before the test. Later, only if you feel fine: the gentle flow or an easy walk."},
 fl("m28","Flow","Gentle full-body flow","Very gentle. 10 s set-up only on position changes.",[["Shoulder CARs – each side",80],["Leg swings – front to back",60],["Calf stretch on block – each side",80],["Hip CARs (standing, hold rack) – each side",80],["Couch stretch – each side",80],["Cat-cow, slow",60],["90/90 hold with lift-offs – each side",80],["Glute bridge, slow",60],["Thoracic open book – each side",80],["Slow breathing lying on back",180]],"MOBILITY")]},
lo29:{name:"Strength B3 · Lower + Core",short:"Lower",safe:"No heavy spinal loading. More reps, same weight, still RPE 6–7. Breathe out on the effort, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("l29wu","Warm-up","Hip prep – lower","No forcing.",[["Ankle rocks – each side",60],["Leg swings – side to side",40],["Bodyweight squat, slow",40],["Lunge with overhead reach – each side",60],["Glute bridge, slow",40]],"WARM-UP"),
 {k:"ex",h:"A · Straight sets",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"l29a",items:[{x:"rfess",lab:"A1",rp:8,side:1,tp:"3110",cue:"Same set-up as last Friday, 8 reps each side (was 6). Hold the rack if balance wobbles."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[45,75],unit:"Set",tid:"l29b",items:[{x:"db-rdl",lab:"B1",rp:10,tp:"3111",cue:"Same dumbbells, 10 reps (was 8). Head above hips, breathe out to stand."},{x:"side-plank",lab:"B2",rp:25,ru:"s",side:1,sw:20,cue:"25 s each side. Knees down if needed, keep breathing."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"l29c",items:[{x:"goblet-squat",lab:"C1",rp:10,tp:"3011",cue:"The 16 kg bell at your chest, 3 s down."},{x:"calf-raise",lab:"C2",rp:10,side:1,tp:"2010",sw:15,cue:"Edge of the block, hand on rack."}]},
 {k:"timer",id:"l29fl",h:"Steady",name:"Easy row 3:00",note:"Easy pace, RPE 3–4.",small:"18–20 s/m · damper 4–5 · flush the legs.",segs:[["READY",10,"Easy row"],["EASY",180,"Easy row · easy pace"]]},
 fl("l29cd","Cool-down","Active stretch – lower","Breathe out into each stretch.",[["Half-kneeling hip flexor with reach – each side",60],["Calf stretch on block – each side",60],["Lying figure-4 stretch – each side",60]])]},
mob30:{name:"Recovery · Hips + T-spine Flow",short:"Mobility",rest:1,safe:"Recovery day. Slow controlled moves and gentle holds – no head-down positions, no forcing, breathe slowly.",blocks:[
 {k:"rest",name:"Recovery day",note:"Rest, or do the optional 15-min flow. Walk, hydrate, sleep well."},
 fl("m30","Flow","Hips + T-spine flow","Fresh legs for Saturday. 10 s set-up only on position changes.",[["World's greatest stretch – each side",80],["Lunge with overhead reach – each side",80],["Supported deep squat hold (hold rack)",70],["Doorway/rack chest stretch – each side",80],["Half-kneeling hip flexor with reach – each side",80],["Seated lat reach at bench – each side",80],["Bird-dog, slow",60],["Side-lying windmill – each side",80],["Lying figure-4 stretch – each side",80],["Slow breathing lying on back",150]],"MOBILITY")]},
kb31:{name:"KB EMOM 15 + Zone 2 Run",short:"KB",safe:"One 16 kg kettlebell. Breathe out on every clean, press and swing; never hold your breath. Smooth reps at RPE 6–7, 2 reps short of failure (2 RIR).",blocks:[
 fl("k31wu","Warm-up","Kettlebell warm-up","Slow and smooth with the 16 kg bell.",[["Kettlebell hip hinge drill",40],["Prying goblet squat",50],["Single-arm kettlebell deadlift – each side",60],["Leg swings – front to back",40],["Shoulder CARs – each side",40]],"WARM-UP","up"),
 {k:"timer",id:"k31a",h:"EMOM 60 s × 15",name:"Single-bell EMOM",note:"Each 60 s: complex left · complex right · swings.",small:["Complex = clean ×2, front-rack squat ×3, press ×3.",NOREST],segs:k31(),list:["Kettlebell clean – ×2 each side","Front-rack squat – ×3 each side","Single-arm press – ×3 each side","Kettlebell swing – ×15"]},
 tm("k31run","Steady","Zone 2 run","Steady pace, Zone 2, RPE 5–6.",720,"JOG",{counter:1,small:"Outside or Assault Runner. 1:00 walk break whenever needed."}),
 fl("k31cd","Cool-down","Active stretch","Breathe out into each stretch.",[["Couch stretch – each side",60],["Calf stretch on block – each side",60],["Thoracic open book – each side",60]])]},
walk01:{name:"Hill Walk + Stretch",short:"Walk",safe:"Faster than last Sunday: hills or incline, still able to talk. Steady pace, RPE 5–6.",blocks:[
 tm("w01walk","Steady","Hill walk (Zone 2)","Steady walk, RPE 5–6.",1800,"STEADY",{small:"Hills outside, or incline on the Assault Runner."}),
 fl("w01st","Cool-down","Stretch","Breathe out into each stretch.",[["Calf stretch on block – each side",60],["Couch stretch – each side",60],["90/90 hold with lift-offs – each side",60],["Thoracic open book – each side",60],["Slow breathing lying on back",60]]),{k:"fields"}]},
// ---- week-3 backups (g0 100)
bk26:{name:"Backup · Upper (16 kg KB + Bench)",short:"Upper",g0:100,safe:"Less kit: the 16 kg kettlebell plus the bench and bars. RPE 6–7, breathe out on every press and pull, stop 2 reps short of failure (2 RIR).",blocks:[
 fl("x26wu","Warm-up","Dynamic stretch – upper","No forcing.",MV.up),
 {k:"ex",h:"A · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"x26a",items:[{x:"incline-pushup",lab:"A1",rp:12,tp:"3010",cue:"Hands on the bench, body straight, 3 s down."},{x:"kb-sa-row",lab:"A2",rp:10,side:1,tp:"2011",sw:15,cue:"16 kg bell, hand on bench, pull to the hip."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:2,rr:[45,75],unit:"Set",tid:"x26b",items:[{x:"kb-curl",lab:"B1",rp:10,tp:"2010",cue:"16 kg bell by the horns, elbows pinned."},{x:"dip-hold",lab:"B2",rp:25,ru:"s",sw:15,cue:"Arms straight on the dip bars, feet on block if needed."}]},
 {k:"timer",id:"x26fl",h:"Intervals",name:"Row intervals 5 × 0:30 / 0:30",note:"Each round: 0:30 work · 0:30 rest. Moderate pace, RPE 7.",small:["Work 22–24 s/m · rest light paddle · damper 4–5.",NOREST],segs:[["READY",10,"Row · moderate pace"]].concat(iv(5,30,30,"moderate pace","light paddle"))},
 fl("x26cd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cdu)]},
bk27:{name:"Backup · Zone 2 Row + Stretch",short:"Row",g0:100,safe:"No running. Zone 2 row: conversational, a little breathless. Damper 4–5, breathe steadily. Steady pace, RPE 5–6.",blocks:[
 fl("x27wu","Warm-up","Dynamic stretch","",MV.full),
 {k:"timer",id:"x27row",h:"Steady",name:"Zone 2 row",note:"Steady pace, Zone 2, RPE 5–6.",small:"24:00 at 18–20 s/m · damper 4–5.",segs:[["READY",10,"Zone 2 row"],["STEADY",1440,"Zone 2 row · steady pace"]]},
 fl("x27cd","Cool-down","Mobility","Controlled, keep breathing.",[["Couch stretch – each side",60],["90/90 hip switches",60],["Thoracic open book – each side",60],["Slow breathing lying on back",60]],"MOBILITY"),{k:"fields",dist:"Distance (m, from PM5)"}]},
bk28:{name:"Backup · Easy Walk",short:"Walk",g0:100,safe:"Only if you feel fine after the test. Zone 1 walk, nasal breathing. Easy pace, RPE 3–4.",blocks:[
 tm("x28walk","Steady","Easy walk (Zone 1)","Easy walk, RPE 3–4.",900,"EASY",{small:"Outside if you can. Stop and rest if you feel unwell."})]},
bk29:{name:"Backup · Lower (Bodyweight + KB)",short:"Lower",g0:100,safe:"Lower energy, light loads, no spinal loading. RPE 6, breathe out on the effort, hold the rack for balance.",blocks:[
 fl("x29wu","Warm-up","Dynamic stretch – lower","No forcing.",MV.low),
 {k:"ex",h:"A · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"x29a",items:[{x:"reverse-lunge",lab:"A1",rp:8,side:1,tp:"2011",cue:"Bodyweight, hold the rack if needed."},{x:"sl-glute-bridge",lab:"A2",rp:10,side:1,tp:"2011",sw:15,cue:"On the floor, hips level."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"x29b",items:[{x:"kb-sumo-dl",lab:"B1",rp:12,tp:"2011",cue:"16 kg bell, wide stance, chest proud."},{x:"side-plank",lab:"B2",rp:20,ru:"s",side:1,sw:20,cue:"Knees down if needed, keep breathing."}]},
 fl("x29cd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cd)]},
bk30:{name:"Backup · Runner Walk + Stretch",short:"Walk",g0:100,safe:"Recovery day. Easy walk on the Assault Runner or outside, then gentle stretches. Easy pace, RPE 3–4.",blocks:[
 tm("x30walk","Steady","Easy walk (Zone 1)","Easy walk, RPE 3–4.",600,"EASY",{small:"Nasal breathing."}),
 fl("x30st","Cool-down","Stretch","Gentle, no forcing.",[["Calf stretch on block – each side",60],["Couch stretch – each side",60],["Slow breathing lying on back",90]],"MOBILITY")]},
bk31:{name:"Backup · Zone 2 Row + Circuit",short:"Row",g0:100,safe:"No kettlebell. Zone 2 row then light bodyweight work; breathe out on every effort. Steady pace, RPE 5–6.",blocks:[
 fl("x31wu","Warm-up","Dynamic stretch – full body","",MV.full),
 {k:"timer",id:"x31row",h:"Steady",name:"Zone 2 row",note:"Steady pace, Zone 2, RPE 5–6.",small:"16:00 at 18–20 s/m · damper 4–5.",segs:[["READY",10,"Zone 2 row"],["STEADY",960,"Zone 2 row · steady pace"]]},
 {k:"timer",id:"x31c",h:"Circuit × 2",name:"Bodyweight circuit",note:"Each round: 30–40 s per move · 30 s rest.",small:"Smooth reps, breathe out on every effort.",segs:core(2,[["Wall sit",30,15],["Incline push-up",30,15],["Dead bug @3030",40,15]],30),list:["Wall sit – 30 s","Incline push-up – 30 s","Dead bug @3030 – 40 s"]},
 fl("x31cd","Cool-down","Active stretch","",MV.cd),{k:"fields",dist:"Distance (m, from PM5)"}]},
bk01:{name:"Backup · Easy Walk + Long Stretch",short:"Stretch",g0:100,safe:"Lowest energy option. Easy walk, then long gentle holds – no forcing, no head-down positions. Easy pace, RPE 3–4.",blocks:[
 tm("x01walk","Steady","Easy walk (Zone 1)","Easy walk, RPE 3–4.",480,"EASY"),
 fl("x01fl","Flow","Long-hold stretch","Gentle holds, no forcing.",[["Doorway/rack chest stretch – each side",80],["Half-kneeling hip flexor with reach – each side",80],["Lying figure-4 stretch – each side",80],["Slow breathing lying on back",120]],"MOBILITY")]}});
// ==== WEEK 4 · Mon 2 – Sun 8 Nov 2026 (added by the Health & Fitness bot; rationale in docs/programme-week4.md) ====
// Mon 2 = the easy 5 km James ran today; Upper moves to Tue, Lower + second pull + carry on Thu.
// Sat 7 EMOM: minute 1 complex left, minute 2 complex right, minute 3 swings + goblet squats – 5 rounds, sides alternate by minute
function k07(){var s=[],C="Complex",n=5;for(var r=1;r<=n;r++){var t=" · round "+r+"/"+n;s.push(["READY",5,C+" · left side"+t]);s.push(["WORK",40,C+" · left side"+t]);s.push(["REST",15,"Rest · switch hands"]);
 s.push(["READY",5,C+" · switch → right side"+t]);s.push(["WORK",40,C+" · right side"+t]);s.push(["REST",15,"Rest · swings next"]);
 s.push(["READY",5,"Swing ×15 + goblet squat ×5"+t]);s.push(["WORK",40,"Swing ×15 + goblet squat ×5"+t]);if(r<n)s.push(["REST",15,"Rest · complex next"]);}return s;}
Object.assign(SESS,{
run02:{name:"Easy 5 km Run",short:"Run",safe:"Done today: easy 5 km. Log it with Finish workout. Conversational, walk whenever needed. Easy pace, RPE 3–4.",blocks:[
 fl("r02wu","Warm-up","Dynamic stretch – run","",[["Leg swings – front to back",40],["Leg swings – side to side",40],["Ankle rocks – each side",60],["Standing hip CARs – each side",60]],"WARM-UP"),
 tm("r02w","Warm-up","Warm-up walk","Easy walk, RPE 3–4.",120,"WARM-UP"),
 tm("r02run","Steady","Easy run 5 km","Easy run, RPE 3–4.",1860,"JOG",{counter:1,small:["5 km at an easy, chatty effort – the time is a guide.","1:00 walk break whenever needed: tap +1 walk break."]}),
 tm("r02cd","Cool-down","Cool-down walk","Easy walk, RPE 3–4.",120,"COOL-DOWN",{small:"Then stretch calves, hamstrings and hips."}),{k:"fields"}]},
up03:{name:"Strength A4 · Upper",short:"Upper",safe:"Top of the range last week, so a little more weight. Still RPE 6–7: breathe out on every rep, no grinding, stop 2 reps short (2 RIR).",blocks:[
 fl("u03wu","Warm-up","Shoulder prep – upper","No forcing.",[["Shoulder CARs – each side",60],["Broomstick pass-throughs",40],["Wall slides",40],["Cat-cow, slow",40]],"WARM-UP"),
 {k:"ex",h:"A · Straight sets",mode:"sup",n:4,rr:[90,120],unit:"Set",tid:"u03a",items:[{x:"db-bench",lab:"A1",rp:6,tp:"3110",cue:"You hit 8 last week: add 2 kg each hand, back to 6. Next week build to 8 again."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"u03b",items:[{x:"assisted-chinup",lab:"B1",rp:7,tp:"3010",cue:"7 reps (was 6), same help from the block."},{x:"cs-row",lab:"B2",rp:10,tp:"2011",sw:15,cue:"You hit 12 last week: add 2 kg each hand, 10 reps."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"u03c",items:[{x:"db-shoulder-press",lab:"C1",rp:10,tp:"2011",cue:"Seated, back supported, ribs down, breathe out as you press."},{x:"farmers-carry",lab:"C2",rp:50,ru:"m",sw:15,cue:"Same 50 m, 2 kg heavier each hand. Tall, short steps, breathe."}]},
 {k:"timer",id:"u03fl",h:"Intervals",name:"Row intervals 6 × 0:40 / 0:30",note:"Each round: 0:40 work · 0:30 rest. Moderate pace, RPE 7.",small:["10 s longer than last week. Work 24–26 s/m · damper 4–5.",NOREST],segs:[["READY",10,"Row · moderate pace"]].concat(iv(6,40,30,"moderate pace","light paddle"))},
 fl("u03cd","Cool-down","Active stretch – upper","Breathe out into each stretch.",[["Doorway/rack chest stretch – each side",60],["Seated lat reach at bench – each side",60]])]},
mob04:{name:"Recovery · Spine + Hips Flow",short:"Mobility",rest:1,safe:"Recovery day. Slow controlled moves and gentle holds – no head-down positions, no forcing, breathe slowly.",blocks:[
 {k:"rest",name:"Recovery day",note:"Rest, or do the optional 15-min flow. Walk, hydrate, sleep well."},
 fl("m04","Flow","Spine + hips flow","After Tuesday's upper day. 10 s set-up only on position changes.",[["Wrist CARs – each side",60],["Shoulder CARs – each side",80],["Hip CARs (standing, hold rack) – each side",80],["Supported deep squat hold (hold rack)",70],["Couch stretch – each side",80],["Seated lat reach at bench – each side",80],["Cat-cow, slow",60],["Thoracic open book – each side",80],["90/90 hip switches",60],["Slow breathing lying on back",180]],"MOBILITY")]},
lo05:{name:"Strength B4 · Lower + Pull",short:"Lower",safe:"No heavy spinal loading. More reps, same weight, RPE 6–7, no grinding. Breathe out on the effort, stop 2 reps short (2 RIR).",blocks:[
 fl("l05wu","Warm-up","Hip prep – lower","No forcing.",[["Ankle rocks – each side",60],["Bodyweight squat, slow",40],["World's greatest stretch – each side",60],["Glute bridge, slow",40]],"WARM-UP"),
 {k:"ex",h:"A · Straight sets",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"l05a",items:[{x:"rfess",lab:"A1",rp:10,side:1,tp:"3110",cue:"Same weight as last Thursday, 10 reps each side (was 8). All left, then all right."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"l05b",items:[{x:"db-rdl",lab:"B1",rp:12,tp:"3111",cue:"Same dumbbells, 12 reps (was 10). Head above hips. At 12 smooth, add 2 kg next week."},{x:"kb-sa-row",lab:"B2",rp:10,side:1,tp:"2011",sw:15,cue:"16 kg bell, hand on bench, pull to the hip. All left, then all right."}]},
 {k:"ex",h:"C · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"l05c",items:[{x:"suitcase-carry",lab:"C1",rp:40,ru:"m",cue:"16 kg bell: 40 m in one hand, then switch hands. Stand tall, don't lean."},{x:"dead-bug",lab:"C2",rp:6,side:1,tp:"2020",sw:15,cue:"Low back flat, slow exhale as you reach."}]},
 {k:"timer",id:"l05fl",h:"Steady",name:"Easy row 3:00",note:"Easy pace, RPE 3–4.",small:"18–20 s/m · damper 4–5 · flush the legs.",segs:[["READY",10,"Easy row"],["EASY",180,"Easy row · easy pace"]]},
 fl("l05cd","Cool-down","Active stretch – lower","Breathe out into each stretch.",[["Couch stretch – each side",60],["Lying figure-4 stretch – each side",60]])]},
mob06:{name:"Recovery · Legs + Breathe Flow",short:"Mobility",rest:1,safe:"Recovery day. Slow controlled moves and gentle holds – no head-down positions, no forcing, breathe slowly.",blocks:[
 {k:"rest",name:"Recovery day",note:"Rest, or do the optional 15-min flow. Fresh legs for Saturday."},
 fl("m06","Flow","Legs + breathe flow","Gentle hips and calves. 10 s set-up only on position changes.",[["Ankle CARs – each side",80],["Leg swings – front to back",60],["Calf stretch on block – each side",80],["Half-kneeling hip flexor with reach – each side",80],["Bird-dog, slow",60],["Glute bridge, slow",60],["Side-lying windmill – each side",80],["Lying figure-4 stretch – each side",80],["90/90 hold with lift-offs – each side",80],["Slow breathing lying on back",150]],"MOBILITY")]},
kb07:{name:"KB EMOM 15 · Round 2 + Run",short:"KB",safe:"One 16 kg kettlebell. Breathe out on every clean, press and swing; never hold your breath. Smooth reps at RPE 6–7, no grinding (2 RIR).",blocks:[
 fl("k07wu","Warm-up","Kettlebell warm-up","Slow and smooth with the 16 kg bell.",[["Kettlebell halo, slow, alternate direction",40],["Kettlebell hip hinge drill",40],["Prying goblet squat",50],["World's greatest stretch – each side",60]],"WARM-UP","up"),
 {k:"timer",id:"k07a",h:"EMOM 60 s × 15",name:"Single-bell EMOM",note:"Each 60 s: complex left · complex right · swings.",small:["Complex = clean ×3, front-rack squat ×3, press ×3.",NOREST],segs:k07(),list:["Kettlebell clean – ×3 each side","Front-rack squat – ×3 each side","Single-arm press – ×3 each side","Kettlebell swing – ×15","Kettlebell goblet squat – ×5"]},
 tm("k07run","Steady","Zone 2 run","Steady pace, Zone 2, RPE 5–6.",720,"JOG",{counter:1,small:"Outside or Assault Runner. 1:00 walk break whenever needed."}),
 fl("k07cd","Cool-down","Active stretch","Breathe out into each stretch.",[["Couch stretch – each side",60],["Calf stretch on block – each side",60],["Thoracic open book – each side",60]])]},
walk08:{name:"Hill Walk 32 + Stretch",short:"Walk",safe:"Two minutes longer than last Sunday: hills or incline, still able to talk. Steady pace, RPE 5–6.",blocks:[
 tm("w08walk","Steady","Hill walk (Zone 2)","Steady walk, RPE 5–6.",1920,"STEADY",{small:"Hills outside, or incline on the Assault Runner."}),
 fl("w08st","Cool-down","Stretch","Breathe out into each stretch.",[["Calf stretch on block – each side",60],["Half-kneeling hip flexor with reach – each side",60],["Lying figure-4 stretch – each side",60],["Slow breathing lying on back",60]]),{k:"fields"}]},
// ---- week-4 backups (g0 100)
bk02:{name:"Backup · Easy Row + Stretch",short:"Row",g0:100,safe:"No running. Easy row with nasal breathing, then gentle stretches. Easy pace, RPE 3–4.",blocks:[
 {k:"timer",id:"x02row",h:"Steady",name:"Easy row",note:"Easy pace, RPE 3–4.",small:"20:00 at 18–20 s/m · damper 4–5.",segs:[["READY",10,"Easy row"],["EASY",1200,"Easy row · easy pace"]]},
 fl("x02st","Cool-down","Stretch","Gentle, no forcing.",[["Couch stretch – each side",60],["Thoracic open book – each side",60],["Slow breathing lying on back",90]],"MOBILITY"),{k:"fields",dist:"Distance (m, from PM5)"}]},
bk03:{name:"Backup · Upper (16 kg KB + Bars)",short:"Upper",g0:100,safe:"Less kit: the 16 kg kettlebell plus the bench and bars. RPE 6–7, breathe out on every press and pull, stop 2 reps short (2 RIR).",blocks:[
 fl("x03wu","Warm-up","Dynamic stretch – upper","No forcing.",MV.up),
 {k:"ex",h:"A · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"x03a",items:[{x:"kb-floor-press",lab:"A1",rp:8,side:1,tp:"3010",cue:"16 kg bell, elbow touches down softly. All left, then all right."},{x:"scap-pullup",lab:"A2",rp:8,tp:"2011",sw:15,cue:"Hang, pull shoulders down, elbows straight."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:2,rr:[45,75],unit:"Set",tid:"x03b",items:[{x:"incline-pushup",lab:"B1",rp:12,tp:"2010",cue:"Hands on the bench, body straight."},{x:"farmers-carry",lab:"B2",rp:40,ru:"m",sw:15,cue:"Two dumbbells, tall, short steps."}]},
 {k:"timer",id:"x03fl",h:"Intervals",name:"Row intervals 5 × 0:30 / 0:30",note:"Each round: 0:30 work · 0:30 rest. Moderate pace, RPE 7.",small:["Work 22–24 s/m · rest light paddle · damper 4–5.",NOREST],segs:[["READY",10,"Row · moderate pace"]].concat(iv(5,30,30,"moderate pace","light paddle"))},
 fl("x03cd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cdu)]},
bk04:{name:"Backup · Recovery Walk",short:"Walk",g0:100,safe:"Recovery day. Zone 1 walk with nasal breathing. Easy pace, RPE 3–4.",blocks:[
 tm("x04walk","Steady","Recovery walk (Zone 1)","Easy walk, RPE 3–4.",900,"EASY",{small:"Outside if you can."})]},
bk05:{name:"Backup · Lower + Pull (Light)",short:"Lower",g0:100,safe:"Lower energy, light loads, no spinal loading. RPE 6, breathe out on the effort, hold the rack for balance.",blocks:[
 fl("x05wu","Warm-up","Dynamic stretch – lower","No forcing.",MV.low),
 {k:"ex",h:"A · Superset",mode:"sup",n:3,rr:[60,90],unit:"Set",tid:"x05a",items:[{x:"goblet-squat",lab:"A1",rp:10,tp:"3011",cue:"16 kg bell at your chest, 3 s down."},{x:"kb-sa-row",lab:"A2",rp:8,side:1,tp:"2011",sw:15,cue:"16 kg bell, hand on bench. All left, then all right."}]},
 {k:"ex",h:"B · Superset",mode:"sup",n:2,rr:[45,75],unit:"Round",tid:"x05b",items:[{x:"glute-bridge",lab:"B1",rp:12,tp:"2011",cue:"On the floor, squeeze at the top."},{x:"suitcase-carry",lab:"B2",rp:30,ru:"m",sw:15,cue:"16 kg bell, switch hands at 30 m."}]},
 fl("x05cd","Cool-down","Active stretch","Breathe out into each stretch.",MV.cd)]},
bk06:{name:"Backup · Easy Row 12",short:"Row",g0:100,safe:"Recovery day. Very light rowing, nasal breathing. Easy pace, RPE 3–4.",blocks:[
 {k:"timer",id:"x06row",h:"Steady",name:"Easy row",note:"Easy pace, RPE 3–4.",small:"12:00 at 18–20 s/m · damper 3–4.",segs:[["READY",10,"Easy row"],["EASY",720,"Easy row · easy pace"]]},
 fl("x06br","Cool-down","Down-regulate","Slow, calm breathing.",[["Calf stretch on block – each side",60],["Slow breathing lying on back",90]],"MOBILITY")]},
bk07:{name:"Backup · Zone 2 Row + Floor Core",short:"Row",g0:100,safe:"No kettlebell. Zone 2 row then light floor core; breathe out on every effort. Steady pace, RPE 5–6.",blocks:[
 fl("x07wu","Warm-up","Dynamic stretch – full body","",MV.full),
 {k:"timer",id:"x07row",h:"Steady",name:"Zone 2 row",note:"Steady pace, Zone 2, RPE 5–6.",small:"16:00 at 18–20 s/m · damper 4–5.",segs:[["READY",10,"Zone 2 row"],["STEADY",960,"Zone 2 row · steady pace"]]},
 {k:"timer",id:"x07c",h:"Circuit × 2",name:"Floor core",note:"Each round: 30–40 s per move · 30 s rest.",small:"Exhale slowly, no breath-holding.",segs:core(2,[["Glute bridge @2011",40,15],["Dead bug @3030",40,15],["Bird-dog @2121, alternate",30,15]],30),list:["Glute bridge @2011 – 40 s","Dead bug @3030 – 40 s","Bird-dog @2121 – 30 s"]},
 fl("x07cd","Cool-down","Active stretch","",MV.cd),{k:"fields",dist:"Distance (m, from PM5)"}]},
bk08:{name:"Backup · Easy Walk + Stretch",short:"Walk",g0:100,safe:"Lowest energy option. Easy walk, then gentle holds – no forcing, no head-down positions. Easy pace, RPE 3–4.",blocks:[
 tm("x08walk","Steady","Easy walk (Zone 1)","Easy walk, RPE 3–4.",600,"EASY"),
 fl("x08fl","Flow","Gentle stretch","Gentle holds, no forcing.",[["Doorway/rack chest stretch – each side",80],["Couch stretch – each side",80],["Slow breathing lying on back",120]],"MOBILITY")]}});
HAL["Kettlebell goblet squat"]="goblet-squat";
// ---- backups: date -> backup session id (one per day)
var BK={"2026-10-12":"bk12","2026-10-13":"bk13","2026-10-14":"bk14","2026-10-15":"bk15","2026-10-16":"bk16","2026-10-17":"bk17","2026-10-18":"bk18",
 "2026-10-19":"bk19","2026-10-20":"bk20","2026-10-21":"bk21","2026-10-22":"bk22","2026-10-23":"bk23","2026-10-24":"bk24","2026-10-25":"bk25",
 "2026-10-26":"bk26","2026-10-27":"bk27","2026-10-28":"bk28","2026-10-29":"bk29","2026-10-30":"bk30","2026-10-31":"bk31","2026-11-01":"bk01",
 "2026-11-02":"bk02","2026-11-03":"bk03","2026-11-04":"bk04","2026-11-05":"bk05","2026-11-06":"bk06","2026-11-07":"bk07","2026-11-08":"bk08"};
// ---- one-day overrides: date -> session id. Replaces only that day's main session (backups unchanged). Example: OVR["2026-10-16"]="bk16";
var OVR={};
var PROG={"2026-10-12":"easyrun12","2026-10-13":"strA","2026-10-14":"row","2026-10-15":"mob","2026-10-16":"strB","2026-10-17":"kb","2026-10-18":"walk",
 // week 2
 "2026-10-19":"mob19","2026-10-20":"up20","2026-10-21":"run21","2026-10-22":"mob22","2026-10-23":"lo23","2026-10-24":"kb24","2026-10-25":"walk25",
 // week 3
 "2026-10-26":"up26","2026-10-27":"run27","2026-10-28":"mob28","2026-10-29":"lo29","2026-10-30":"mob30","2026-10-31":"kb31","2026-11-01":"walk01",
 // week 4
 "2026-11-02":"run02","2026-11-03":"up03","2026-11-04":"mob04","2026-11-05":"lo05","2026-11-06":"mob06","2026-11-07":"kb07","2026-11-08":"walk08"};
var LEGACY_END="2026-10-11",PAT=["Run","Rest","Pump","Run","Rest","Pump","Run"],DEFP={"2026-10-10":"Pump"},LEG={Pump:"pump",Run:"easyrun",Rest:"rest0"};
var ENC=["Strong work, James. That counts.","Showing up on a flat day is the win.","Nicely done – recover well.","Good session. Hydrate and rest up."];
// prepare item global indices
// ---- "Run instead" outdoor run versions (same timings and effort words)
var RI={
 row:{wwu:{name:"Warm-up walk",note:"Easy walk, RPE 3–4.",small:"",segs:[["WARM-UP",240,"Warm-up walk"]]},
  wiv:{name:"Run/walk intervals 6 × 1:00",note:"Each round: 1:00 work · 1:00 rest. Moderate pace, RPE 7.",small:["Rest is a recovery walk, with 5 s get-ready.",NOREST],segs:ivr(6).map(function(g){return g[0]=="REST"?["REST",g[1],"Rest · recovery walk"]:[g[0],g[1],g[2].replace(/ · .*$/," · run, moderate pace")];})},
  wst:{name:"Zone 2 run",note:"Steady pace, Zone 2, RPE 5–6.",small:"Walk break whenever needed.",segs:[["STEADY",240,"Zone 2 run"]]}},
 bk14:{x14iv:{name:"Run/walk intervals 8 × 1:00",note:"Each round: 1:00 work · 1:00 rest. Steady pace, RPE 5–6.",small:["Steady run, then recovery walk.",NOREST],segs:[["READY",10,"Steady run"]].concat(iv(8,60,60,"steady run","recovery walk"))}},
 bk17:{x17fl:{name:"Zone 2 run 5:00",note:"Steady pace, Zone 2, RPE 5–6.",small:"",segs:[["READY",10,"Zone 2 run"],["STEADY",300,"Zone 2 run"]]}},
 walk:{swalk:{name:"Zone 2 run with walk breaks",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["STEADY",1500,"Zone 2 run"]],counter:1}}};
// week-2 run-instead versions (must match block times)
Object.assign(RI,{
 bk21:{x21row:{name:"Zone 2 run",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["READY",10,"Zone 2 run"],["STEADY",1200,"Zone 2 run"]],counter:1}},
 bk24:{x24row:{name:"Zone 2 run",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["READY",10,"Zone 2 run"],["STEADY",900,"Zone 2 run"]],counter:1}},
 walk25:{w25walk:{name:"Zone 2 run with walk breaks",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["STEADY",1800,"Zone 2 run"]],counter:1}}});
// week-3 run-instead versions
Object.assign(RI,{
 bk27:{x27row:{name:"Zone 2 run",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["READY",10,"Zone 2 run"],["STEADY",1440,"Zone 2 run"]],counter:1}},
 bk31:{x31row:{name:"Zone 2 run",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["READY",10,"Zone 2 run"],["STEADY",960,"Zone 2 run"]],counter:1}},
 walk01:{w01walk:{name:"Zone 2 run with walk breaks",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["STEADY",1800,"Zone 2 run"]],counter:1}}});
// week-4 run-instead versions
Object.assign(RI,{
 bk07:{x07row:{name:"Zone 2 run",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["READY",10,"Zone 2 run"],["STEADY",960,"Zone 2 run"]],counter:1}},
 walk08:{w08walk:{name:"Zone 2 run with walk breaks",note:"Steady pace, Zone 2, RPE 5–6.",small:"1:00 walk break whenever needed: tap +1 walk break.",segs:[["STEADY",1920,"Zone 2 run"]],counter:1}}});
var LS={get:function(k,d){try{var v=localStorage.getItem(k);if(v==null)return d;try{return JSON.parse(v);}catch(e){return v;}}catch(e){return d;}},set:function(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}},del:function(k){try{localStorage.removeItem(k);}catch(e){}}};

// ---- weeks as data (pc-v39). A week is one JSON object (docs/week-format.md): sessions, days, How-to entries and
// run-instead versions. Built-in weeks come from weeks/*.json (scripts/build.sh inlines them as WEEKS_BUILTIN);
// imported weeks live in localStorage wo_weeks {monday: week} and are applied after the built-in ones. A week never
// replaces a session id that already exists in the code, so saved logs keep rendering.
var WEEKS={};
var SPEC=["moves","phase","dir","sec","n","work","wl","rl","rounds","cycle","win"];
function strip(b,keys){keys.forEach(function(q){delete b[q];});return b;}
function mkBlock(sp){var b={},q;for(q in sp)b[q]=sp[q];var k=b.k,o;
 if(k=="flow"){o=fl(b.id,b.h,b.name,b.note||"",b.moves||[],b.phase,b.dir);for(q in b)if(SPEC.indexOf(q)<0&&q!="k"&&q!="note")o[q]=b[q];return o;}
 if(k=="tm"){o=tm(b.id,b.h,b.name,b.note||"",+b.sec||0,b.phase||"STEADY");for(q in b)if(SPEC.indexOf(q)<0&&q!="k")o[q]=b[q];return o;}
 if(k=="iv"){b.k="timer";b.segs=iv(+b.n||1,+b.work||0,+b.rest||0,b.wl||"",b.rl||"rest");delete b.rest;return strip(b,SPEC);}
 if(k=="core"){b.k="timer";b.segs=core(+b.rounds||1,b.moves||[],+b.rest||30);delete b.rest;return strip(b,SPEC);}
 if(k=="emom"){b.k="timer";var s=[];for(var r=0;r<(+b.rounds||1);r++)(b.cycle||[]).forEach(function(l){s.push(["WORK",+b.win||60,l]);});b.segs=s;return strip(b,SPEC);}
 return b;}
function mkRI(sp){if(!sp||!sp.k)return sp;var o=mkBlock(sp);delete o.k;delete o.id;return o;}
function buildWeek(w){var o={sess:{},ri:{}};Object.keys(w.sess||{}).forEach(function(k){var S=w.sess[k],T={},q;for(q in S)T[q]=S[q];T.blocks=(S.blocks||[]).map(mkBlock);o.sess[k]=T;});
 Object.keys(w.ri||{}).forEach(function(k){o.ri[k]={};Object.keys(w.ri[k]).forEach(function(id){o.ri[k][id]=mkRI(w.ri[k][id]);});});return o;}
var EFFORT=/\b(easy|steady|moderate)\b/i;
// banned terms (paces, combined effort words, unsafe moves); spelt in pieces so the app source itself never contains them
var BANNED=new RegExp(["\\bhard\\b","min\\/"+"km","km\\/"+"h","\\/500 ?"+"m","drag "+"factor","moderate-"+"hard","steady-"+"hard","easy-"+"steady","barbell","back squat","conventional deadlift","snatch","handstand","headstand","inverted","valsalva"].join("|"),"i");
var BANNED2=new RegExp(["\\b[Bb]ri"+"sk\\b","\\bj"+"og\\b"].join("|"));  // effort words we never use (case sensitive: JOG is a clock phase)
var PHASES=["READY","WORK","REST","WARM-UP","EASY","STEADY","JOG","FLOW","STRETCH","MOBILITY","FINISH","COOL-DOWN","WALK"];
function validateWeek(w){var E=[],W=[],info={sess:0,days:0,how:0};var err=function(m){E.push(m);},warn=function(m){W.push(m);};
 if(!w||typeof w!="object")return {errors:["Not a week object."],warnings:[],info:info};
 if(w.v!=1)err("v must be 1.");
 if(!/^\d{4}-\d\d-\d\d$/.test(w.week||""))err("week must be the Monday as YYYY-MM-DD.");else if(pd(w.week).getDay()!=1)err("week "+w.week+" is not a Monday.");
 var mon=w.week||"",sun=mon?addDays(mon,6):"";var B;try{B=buildWeek(w);}catch(e){return {errors:["Could not build the sessions: "+(e&&e.message||e)],warnings:W,info:info};}
 var XX={},q;for(q in X)XX[q]=X[q];for(q in w.x||{})XX[q]=w.x[q];var HH={},AA={};for(q in HT)HH[q]=HT[q];for(q in w.ht||{})HH[q]=w.ht[q];for(q in HAL)AA[q]=HAL[q];for(q in w.hal||{})AA[q]=w.hal[q];
 var hk=function(n){var k=String(n).replace(/\s*\(.*?\)/g,"").replace(/ – .*$/,"").replace(/,.*$/,"").replace(/ @.*$/,"").replace(/ \+ lift-offs$/,"").trim();return AA[k]||k;};
 Object.keys(w.x||{}).forEach(function(k){var x=w.x[k];if(!Array.isArray(x)||x.length<4||typeof x[0]!="string")err("x."+k+" must be [name, suggested, range, weighted 0/1].");else if(!HH[k])err("x."+k+" ("+x[0]+") has no How-to (ht."+k+").");});
 Object.keys(w.ht||{}).forEach(function(k){var h=w.ht[k];if(!h||!h.u||!Array.isArray(h.s)||!h.s.length)err("ht."+k+" needs u (summary) and s (steps).");else{h.s.forEach(function(t){if(String(t).split(/\s+/).length>12)warn("ht."+k+": step over 12 words: "+t);});info.how++;}});
 var ids=Object.keys(B.sess);info.sess=ids.length;if(!ids.length)err("No sessions (sess).");
 ids.forEach(function(k){var S=B.sess[k],txt=JSON.stringify(w.sess[k]);if(SESS[k]&&!(WEEKS[mon]&&WEEKS[mon].ids.indexOf(k)>=0))err("Session id "+k+" already exists in the app; use a new id.");
  if(!S.name)err(k+": name missing.");if(!S.short)err(k+": short (week strip label) missing.");if(!S.rest&&!S.safe)err(k+": safe (safety line) missing.");if(S.safe&&S.safe.length>160)err(k+": safe is over 160 characters.");
  if(S.safe&&!/breathe out|breath/i.test(S.safe)&&S.blocks.some(function(b){return b.k=="ex";}))warn(k+": strength session, safety line does not mention breathing out.");
  if(BANNED.test(txt))err(k+": contains a banned term ("+BANNED.exec(txt)[0]+").");else if(BANNED2.test(txt))err(k+": contains a banned effort word ("+BANNED2.exec(txt)[0]+"); use easy, steady or moderate.");
  if(/\bRPE 8|RPE 9|RPE 10\b/.test(txt))err(k+": RPE 8+ is not used.");
  var seen={};S.blocks.forEach(function(b,i){var id=b.id||b.tid;if(b.k=="timer"||b.k=="ex"){if(!id)err(k+" block "+(i+1)+": id missing.");else if(seen[id])err(k+": duplicate block id "+id);seen[id]=1;}
   if(b.k=="timer"){if(!b.h)err(k+"/"+id+": h (header) missing.");if(!Array.isArray(b.segs)||!b.segs.length)err(k+"/"+id+": no segments.");else b.segs.forEach(function(g){if(!Array.isArray(g)||PHASES.indexOf(g[0])<0||!(+g[1]>0))err(k+"/"+id+": bad segment "+JSON.stringify(g));});
    (b.list||[]).forEach(function(m){if(!HH[hk(m)])err(k+"/"+id+": no How-to for \""+m+"\".");});
    if(/^EMOM/.test(b.h||"")&&!(b.list&&b.list.length))warn(k+"/"+id+": EMOM without a list of moves.");}
   else if(b.k=="ex"){if(!b.h)err(k+"/"+id+": h missing (e.g. \"A · Superset\").");if(!(+b.n>0))err(k+"/"+id+": n (sets or rounds) missing.");if(!Array.isArray(b.rr)||b.rr.length!=2)err(k+"/"+id+": rr [lo, hi] rest range missing.");
    (b.items||[]).forEach(function(it){if(!XX[it.x])err(k+"/"+id+": unknown exercise id "+it.x+" (add it to x).");else if(!HH[it.x]&&!HH[hk(XX[it.x][0])])err(k+"/"+id+": no How-to for "+it.x+".");if(it.rp==null)err(k+"/"+id+"/"+it.x+": rp (reps) missing.");});
    if(!b.items||!b.items.length)err(k+"/"+id+": no items.");}
   else if(b.k!="fields"&&b.k!="rest")err(k+" block "+(i+1)+": unknown kind "+b.k+".");});
  S.blocks.forEach(function(b){if(/^Circuit/.test(b.h||"")&&(b.list||[]).length<3)warn(k+"/"+b.id+": a circuit lists fewer than 3 moves (the standard expands 3 or more).");});
  if(S.blocks.some(function(b){return b.k=="timer"&&/^(Steady|Intervals)/.test(b.h||"")&&!EFFORT.test(b.note||"")&&!EFFORT.test(b.small||"")&&!EFFORT.test(b.h||"");}))warn(k+": a timed block has no effort word in its note (easy RPE 3–4, steady RPE 5–6 or moderate RPE 7).");});
 var days=Object.keys(w.days||{});info.days=days.length;if(!days.length)err("No days.");
 days.forEach(function(d){if(d<mon||d>sun)err("days."+d+" is outside the week "+mon+" to "+sun+".");var dd=w.days[d]||{};["main","backup","quick"].forEach(function(t){var id=dd[t];if(id&&!B.sess[id]&&!SESS[id])err("days."+d+"."+t+": unknown session "+id+".");});if(!dd.main)err("days."+d+": main missing (use a rest session).");});
 Object.keys(B.ri).forEach(function(k){var S=B.sess[k]||SESS[k];if(!S){err("ri."+k+": unknown session.");return;}Object.keys(B.ri[k]).forEach(function(id){var b=null;S.blocks.forEach(function(x){if(x.id==id)b=x;});if(!b){err("ri."+k+"."+id+": no such block.");return;}var v=B.ri[k][id];if(!v.segs)err("ri."+k+"."+id+": segs missing.");else if(dur(v.segs)!=dur(b.segs))err("ri."+k+"."+id+": run-instead time "+dur(v.segs)+" s differs from "+dur(b.segs)+" s.");});if(!(w.rin||{})[k])warn("ri."+k+": no rin [name, short] for the run version.");});
 return {errors:E,warnings:W,info:info};}
function applyWeek(w,src){var v=validateWeek(w);if(v.errors.length){WEEKS[w&&w.week||"?"]={src:src,errors:v.errors,ids:[]};return false;}
 var B=buildWeek(w),q;for(q in w.x||{})X[q]=w.x[q];for(q in w.ht||{})HT[q]=w.ht[q];for(q in w.hal||{})HAL[q]=w.hal[q];
 for(q in B.sess)SESS[q]=B.sess[q];for(q in B.ri)RI[q]=B.ri[q];for(q in w.rin||{})RIN[q]=w.rin[q];for(q in w.ris||{})RIS[q]=w.ris[q];
 Object.keys(w.days).forEach(function(d){var dd=w.days[d];PROG[d]=dd.main;if(dd.backup)BK[d]=dd.backup;else delete BK[d];if(dd.quick)QK[d]=dd.quick;else delete QK[d];});
 WEEKS[w.week]={src:src,title:w.title||"",ids:Object.keys(B.sess),days:Object.keys(w.days).length,errors:[],warnings:v.warnings};return true;}
var RIN={row:["Run Intervals","Run"],walk:["Zone 2 Run","Run"],bk14:["Backup · Run/Walk + Core","Run"],bk17:["Backup · Dumbbell Flow + Zone 2 Run","DB"]};
var RIS={bk14:"Lower energy, no rowing. Breathe out slowly during the core work. Steady pace, RPE 5–6.",row:"Run intervals never all-out: short phrases only. Walk whenever you need to and breathe rhythmically. Moderate pace, RPE 7.",walk:STOP_RUN};
// renamed sessions (pc-v28): logs saved under the old name still count as that day's log
Object.assign(RIN,{bk21:["Backup · Zone 2 Run + Core","Run"],bk24:["Backup · Zone 2 Run + Bodyweight","Run"],walk25:["Zone 2 Run + Stretch","Run"]});
Object.assign(RIS,{bk21:"No rowing. Zone 2 run: conversational, a little breathless, walk whenever needed. Steady pace, RPE 5–6.",bk24:STOP_RUN,walk25:STOP_RUN});
Object.assign(RIN,{bk27:["Backup · Zone 2 Run + Stretch","Run"],bk31:["Backup · Zone 2 Run + Circuit","Run"],walk01:["Zone 2 Run + Stretch (Sun)","Run"]});
Object.assign(RIS,{bk27:STOP_RUN,bk31:STOP_RUN,walk01:STOP_RUN});
Object.assign(RIN,{bk07:["Backup · Zone 2 Run + Floor Core","Run"],walk08:["Zone 2 Run 32 + Stretch","Run"]});
Object.assign(RIS,{bk07:STOP_RUN,walk08:STOP_RUN});
// weeks as data load here, after every table they extend exists; then run-instead versions attach to their blocks
(typeof WEEKS_BUILTIN!="undefined"&&Array.isArray(WEEKS_BUILTIN)?WEEKS_BUILTIN:[]).forEach(function(w){applyWeek(w,"file");});
(function(){var m=LS.get("wo_weeks",{});if(m&&typeof m=="object")Object.keys(m).sort().forEach(function(k){applyWeek(m[k],"import");});})();
Object.keys(RI).forEach(function(k){SESS[k].blocks.forEach(function(b){var v=RI[k][b.id];if(!v)return;var a=0,c=0;b.segs.forEach(function(g){a+=g[1];});v.segs.forEach(function(g){c+=g[1];});if(a!=c)throw new Error("run-instead time mismatch "+b.id);b.ri=v;});});
var ALIAS={"Zone 2 Run":["Easy Run"],"Backup · Zone 2 Row + Mobility":["Backup · Easy Row + Mobility"],"Backup · Dumbbell Flow + Zone 2 Run":["Backup · Dumbbell Flow + Easy Run"]};
function isName(n,name){return n==name||(ALIAS[name]||[]).indexOf(n)>=0;}
function hasRI(S){S=S&&(S.base||S);return !!(S&&S.blocks.some(function(b){return b.ri;}));}
function riOn(k){var a=LS.get("wo_ri",{})||{};return !!a[k];}
function setRI(k,v){var a=LS.get("wo_ri",{})||{};if(v)a[k]=1;else delete a[k];LS.set("wo_ri",a);}
function VB(b){return b.ri&&riOn(sel)?Object.assign({},b,b.ri,{ri:null}):b;}
Object.keys(SESS).forEach(function(k){var S=SESS[k],g=S.g0||0;S.nt=0;S.tot=0;S.blocks.forEach(function(b,bi){b.bi=bi;if(b.rr)b.rest=(b.rr[0]+b.rr[1])/2;if(b.k=="timer"&&!b.clk){b.segs=clk(b,b.segs);if(b.ri)b.ri.segs=clk(Object.assign({},b,b.ri),b.ri.segs);b.clk=1;}if(b.mode=="sup"){b.est=bEst(b);S.tot+=b.est;S.est=1;}else{if(b.mode){b.timer={id:b.tid,segs:b.mode=="every"?bEvery(b):bEmom(b)};}var tt=b.timer||b;S.tot+=dur(tt.segs);}if(b.k=="ex"){b.items.forEach(function(it){it.gi=g++;S.nt+=b.n;});if(!b.rk)b.rk="r"+bi;}if(b.k=="timer"||b.timer)S.nt++;});});
function $(id){return document.getElementById(id);}
function esc(v){return String(v).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;");}
function ymd(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");}
function pd(k){var a=k.split("-");return new Date(+a[0],+a[1]-1,+a[2],12);}
function addDays(k,n){var d=pd(k);d.setDate(d.getDate()+n);return ymd(d);}
function fmt(s){return Math.floor(s/60)+":"+String(s%60).padStart(2,"0");}
var today=ymd(new Date()),SD,sel=today,isOpen=false,weekOff=0,editing=false;
var PUMPIDS=SESS.pump.blocks[1].items.map(function(i){return i.x;});
function migrate(){var v=+LS.get("wo_ver",0)||0;if(v<9){var lg=LS.get("wo_log",[]);if(!Array.isArray(lg))lg=[];var m={},o=[];lg.forEach(function(e){if(!e||!e.date)return;e.name=e.name||"Pump + Cardio";m[e.name+"|"+e.date]=e;});Object.keys(m).forEach(function(k){o.push(m[k]);});o.sort(function(a,b){return a.date<b.date?-1:a.date>b.date?1:0;});LS.set("wo_log",o);}
if(v<10){try{for(var j=0;j<localStorage.length;j++){var key=localStorage.key(j);if(/^wo_\d{4}-\d\d-\d\d$/.test(key)){var ds=key.slice(3),st=LS.get(key,{})||{};Object.keys(st.w||{}).forEach(function(i){if(PUMPIDS[i]&&st.w[i]!==""&&st.w[i]!=null&&dayW(PUMPIDS[i],ds)==null)setW(PUMPIDS[i],ds,st.w[i]);});}}}catch(e){}}
if(v<12)LS.set("wo_ver",12);
(function(){var D="2026-10-14",lg=LS.get("wo_log",[]);if(!Array.isArray(lg))return;var ch=false,ri=LS.get("wo_ri",{})||{};lg.forEach(function(e){if(!e||e.date!=D||e.type=="run")return;var isRow=(e.name=="Rower Intervals")||e.sid=="row";if(!isRow)return;/* flag set, or flag not stored: relabel either way */e.name="Easy run 5 km";e.type="run";e.sid="row";e.ri=1;e.custom=1;e.mig="v24";ch=true;});if(ch){LS.set("wo_log",lg);ri[D]=1;LS.set("wo_ri",ri);}})();
var sd=LS.get("wo_startdate",null);if(typeof sd!="string"||!/^\d{4}-\d\d-\d\d$/.test(sd))sd=today<"2026-10-10"?today:"2026-10-10";if(sd>"2026-10-10")sd="2026-10-10";LS.set("wo_startdate",sd);SD=sd;}
function P(d){var s=LS.get("wo_"+d,null);if(!s||typeof s!="object")s={};s.t=s.t||{};s.w=s.w||{};s.r=s.r||1;s.s=s.s||{};return s;}
function R(d){var s=LS.get("wo_run_"+d,null);if(!s||typeof s!="object")s={};s.b=s.b||0;s.s=s.s||{};return s;}
function WT(){var o=LS.get("wo_wt",{});return o&&typeof o=="object"?o:{};}
function dayW(id,d){var o=WT()[id];return o&&o[d]!=null&&o[d]!==""?String(o[d]):null;}
function setW(id,d,v){var o=WT();o[id]=o[id]||{};if(v===""||v==null)delete o[id][d];else o[id][d]=String(v);LS.set("wo_wt",o);}
function lastW(id,d){var o=WT()[id]||{},b=null;Object.keys(o).forEach(function(k){if(k<d&&o[k]!==""&&o[k]!=null&&(!b||k>b))b=k;});return b?{d:b,v:String(o[b])}:null;}
function sdl(k){var d=pd(k);return d.toLocaleDateString("en-GB",{weekday:"short"})+" "+d.getDate()+" "+d.toLocaleDateString("en-GB",{month:"short"});}
function items(S){var a=[];S.blocks.forEach(function(b){if(b.k=="ex")b.items.forEach(function(it){a.push(it);});});return a;}
function altOn(k){var a=LS.get("wo_alt",{})||{};return !!a[k];}
function setAlt(k,v){var a=LS.get("wo_alt",{})||{};if(v)a[k]=1;else delete a[k];LS.set("wo_alt",a);}
// swap days (pc-v34): wo_daymap {calendar date: source date}. A date shows the source day's main session; its backup,
// quick option and run-instead versions travel with it. Toggles (wo_alt / wo_ri / wo_quick / wo_plan Rest) and logs stay on the calendar date.
function srcOf(k){var m=LS.get("wo_daymap",{});return m&&typeof m=="object"&&typeof m[k]=="string"&&/^\d{4}-\d\d-\d\d$/.test(m[k])?m[k]:k;}
function bkOf(k){return BK[srcOf(k)];}
function qkOf(k){return QK[srcOf(k)];}
function baseSid(k){var s=srcOf(k);return OVR[s]||PROG[s];}
function sid(k){if(k<SD)return null;var o=LS.get("wo_plan",{})||{};if(k<=LEGACY_END)return LEG[o[k]||DEFP[k]||PAT[pd(k).getDay()]]||"rest0";var b=baseSid(k);if(!b)return "tbc";if(o[k]=="Rest")return "rest0";if(qOn(k)&&qkOf(k)&&SESS[qkOf(k)])return qkOf(k);return altOn(k)&&bkOf(k)&&SESS[bkOf(k)]?bkOf(k):b;}
function S_(k){var i=sid(k);if(!i)return null;var S=SESS[i];if(!(hasRI(S)&&riOn(k)))return S;var V=Object.create(S);V.base=S;V.isRun=1;V.name=(RIN[i]||[S.name+" (run)"])[0];V.short=(RIN[i]||[0,S.short])[1];V.safe=RIS[i]||S.safe;V.blocks=S.blocks.map(function(b){if(b.k=="fields")return Object.assign({},b,{dist:"Distance (km)"});return b.ri?Object.assign({},b,b.ri,{ri:null}):b;});return V;}
function curType(k){var S=S_(k);if(!S)return null;if(S.quick)return "quick";return S.isRun?"run":(altOn(k)&&bkOf(k)&&sid(k)==bkOf(k)?"backup":"main");}
function plan(k){var S=S_(k);return S?S.short:null;}
function mode(k){return k<SD?"pre":k>today?"future":k<today?"past":"today";}
function logs(){var l=LS.get("wo_log",[]);return Array.isArray(l)?l:[];}
function sameE(e,k,name){return e.date==k&&(!name||isName(e.name||"Pump + Cardio",name)||(e.custom&&e.type&&e.type==curType(k)));}
function logFor(k,name){var l=logs();for(var i=0;i<l.length;i++)if(sameE(l[i],k,name))return l[i];return null;}
function sdone(d,id){return !!(P(d).s[id]||R(d).s[id]);}
// audio
var ac=null;function unlock(){audioMode();try{if(!ac){var C=window.AudioContext||window.webkitAudioContext;if(!C)return;ac=new C();var b=ac.createBuffer(1,1,22050),s=ac.createBufferSource();s.buffer=b;s.connect(ac.destination);s.start(0);}if(ac.state!="running")ac.resume();}catch(e){}sndUI();}
document.addEventListener("pointerdown",unlock,{passive:true});document.addEventListener("touchend",unlock,{passive:true});
function beep(f,d){try{if(ac){var o=ac.createOscillator(),g=ac.createGain();o.frequency.value=f||880;g.gain.value=.3;o.connect(g);g.connect(ac.destination);o.start();o.stop(ac.currentTime+(d||.25));}}catch(e){}window.__bp&&window.__bp.push(f);}
var wl=null;function wake(){try{if("wakeLock" in navigator&&!wl&&document.visibilityState=="visible")navigator.wakeLock.request("screen").then(function(l){wl=l;l.addEventListener("release",function(){wl=null;});}).catch(function(){});}catch(e){}}
function unwake(){try{if(wl)wl.release();}catch(e){}wl=null;}
function wantWake(){return isOpen&&sel==today;}
function relWake(){if(!(T||RT||wantWake()))unwake();if(!T&&!RT)keepAudio(false);}
// iPhone mutes Web Audio beeps when the ring switch is on silent unless an audio element is playing: loop a silent clip while a timer runs
// pc-v54: music first. The silent clip makes iOS treat the app as a music player, which pauses whatever is playing, so it
// only runs when "Beep even on silent" is switched on (wo_loud). By default the app asks for the ambient audio session:
// beeps mix with the user's music and follow the ring switch.
function loud(){return !!LS.get("wo_loud",0);}
function audioMode(){try{if(navigator.audioSession)navigator.audioSession.type=loud()?"playback":"ambient";}catch(e){}}
function keepAudio(on){var a=$("snda");if(!a)return;if(!loud())on=false;try{if(on){if(a.paused){var pr=a.play();if(pr&&pr.catch)pr.catch(function(){});}}else if(!a.paused)a.pause();}catch(e){}}
// timer
var T=LS.get("wo_timer",null),lastI=-2,lastL=-1,hideAt=0;
function tnow(){return T&&T.pa?T.pa:Date.now();}
function tstate(){var e=(tnow()-T.t0)/1000,acc=0;for(var i=0;i<T.segs.length;i++){var L=T.segs[i][1];if(e<acc+L)return{i:i,left:Math.max(1,Math.ceil(acc+L-e))};acc+=L;}return{i:T.segs.length,left:0};}
// pc-v35 EMOM overview: per-minute groups derived from the block's minute labels (segs) and its move list.
// Sided minutes ("Complex · left") take the "each side" moves; other minutes take the moves named in their label.
var NUMW=["zero","one","two","three","four","five","six","seven","eight","nine","ten"];
function numw(n){return NUMW[n]||String(n);}
function shortMv(n){var x=String(n).replace(/^(Kettlebell|Dumbbell|Single-arm|Two-hand|Double|Barbell) /i,"").replace(/\s*\(.*?\)/g,"").replace(/-/g," ").trim().toLowerCase();return x;}
function plural(x){return /(s|sh|ch|x|z)$/.test(x)?x+"es":x+"s";}
function emomPlan(b){var segs=b.segs||[],n=segs.length;if(!n)return null;var labs=segs.map(function(g){return String(g[2]||"");}),p=n;
 for(var q=1;q<n;q++){if(n%q)continue;var okk=true;for(var i=0;i<n&&okk;i++)if(labs[i]!=labs[i%q])okk=false;if(okk){p=q;break;}}
 var items=(b.list||[]).map(function(x){var m=/^(.*?) – ×(\d+)( each side)?$/.exec(x);return m?{name:m[1],reps:+m[2],side:!!m[3]}:{name:x,reps:null,side:false};});
 var cyc=[];for(var j=0;j<p;j++){var L=labs[j],m=/^(.*?) · (left|right)$/i.exec(L),side=m?m[2].toLowerCase():"",base=m?m[1]:L,mv;
  if(side){mv=items.filter(function(it){return it.side;});if(!mv.length)mv=items;}
  else{var un=items.filter(function(it){return !it.side;}),lo=base.toLowerCase();mv=un.filter(function(it){return lo.indexOf(shortMv(it.name).split(" ").pop())>=0;});if(!mv.length)mv=un;
   if(!mv.length)mv=base.split(/ \+ |, /).map(function(t){var k=/^(.*?) ×(\d+)$/.exec(t.trim());return k?{name:k[1],reps:+k[2],side:false}:{name:t.trim(),reps:null,side:false};});}
  var seq=/ \+ /.test(base),parts=mv.map(function(it){return {name:it.name,reps:it.reps,word:it.reps==null?shortMv(it.name):(it.reps==1?shortMv(it.name):plural(shortMv(it.name)))};});
  var text=parts.map(function(x,i){return (i&&seq?"then ":"")+(x.reps==null?"":x.reps+" ")+x.word;}).join(", ")+".";
  cyc.push({i:j,side:side,title:"Minute "+(j+1)+(side?" · "+side.charAt(0).toUpperCase()+side.slice(1):""),mv:parts,text:text});}
 return {cycle:cyc,p:p,n:n,reps:n/p,win:segs[0][1]||60};}
function emomLines(pl){var a=[];if(!pl)return a;pl.cycle.forEach(function(g){a.push(g.title+": "+g.text);});if(pl.reps>1)a.push("Repeat this "+numw(pl.p)+" minute cycle "+numw(pl.reps)+" times.");a.push("Start each group on the minute. Rest for whatever remains of that minute.");return a;}
function emomHTML(pl){var h='<div class="emp">';pl.cycle.forEach(function(g){h+='<div class="emg"><div class="emh">'+esc(g.title)+'</div><div class="emm">'+g.mv.map(function(x,i){var hk=hkey(x.name),w=esc(x.word),inner=HT[hk]?'<button class="mv" data-h="'+esc(hk)+'">'+w+'</button>':w;return (i&&/ then /.test(" "+g.text+" ")?"then ":"")+(x.reps==null?"":x.reps+" ")+inner;}).join(", ")+'.</div></div>';});
 if(pl.reps>1)h+='<div class="emr">Repeat this '+numw(pl.p)+' minute cycle '+numw(pl.reps)+' times.</div>';h+='<div class="emr">Start each group on the minute. Rest for whatever remains of that minute.</div></div>';return h;}
function moveList(b){if(b.list)return b.list;if(b.groups)return b.groups.map(function(g){return g[0]+": "+g[1].map(function(m){return m[1]+" ×"+m[2];}).join(", ");});return null;}
function findT(S,id){var r=null;S.blocks.forEach(function(b){b=VB(b);if(b.k=="timer"&&b.id==id){r={label:b.name||b.h,kind:kindOf(b),segs:b.segs,list:moveList(b),amrap:b.amrap?1:0,score:kindOf(b)=="every"?1:0};if(r.kind=="emom"){var pl=emomPlan(b);if(pl){r.plan=pl;r.list=emomLines(pl);}}}if(b.timer&&b.timer.id==id)r={label:b.h,kind:b.mode=="every"?"every":"emom",segs:b.timer.segs,list:b.items.map(emomLab)};if(b.k=="ex"&&"rest:"+b.rk==id)r={label:b.unit+" "+Math.min(P(sel)[b.rk]||1,b.n)+" of "+b.n,segs:[["REST",b.rest]],max:b.n,nopre:1};});return r;}
function startT(id){var m=mode(sel);if(m=="future"||m=="pre")return;var S=S_(sel),def=S&&findT(S,id);if(!def)return;unlock();var d=sel,s=P(d);
if(!s.start&&!LS.get("wo_runstart_"+d,null)){s.start=Date.now();LS.set("wo_"+d,s);}
keepAudio(true);T={id:id,label:def.label,kind:def.kind||"one",segs:def.nopre?def.segs:[["READY",10,"Get ready"]].concat(def.segs),pre:def.nopre?0:1,list:def.list||null,amrap:def.amrap||0,score:def.score||0,plan:def.plan||null,rounds:0,max:def.max,t0:Date.now(),date:d};$("bar").classList.remove("locked");lockLab(false);$("peek").hidden=true;LS.set("wo_timer",T);lastI=-1;lastL=-1;lastTick=Date.now();if(RT)stopRest();wake();loop();}
function segStart(i){var a=0;for(var j=0;j<i;j++)a+=T.segs[j][1];return a;}
function tJump(i){if(!T)return;i=Math.max(0,Math.min(i,T.segs.length-1));T.t0=tnow()-segStart(i)*1000;LS.set("wo_timer",T);lastI=-1;lastL=-1;loop();}
function tPause(){if(!T)return;if(T.pa){T.t0+=Date.now()-T.pa;delete T.pa;unlock();}else T.pa=Date.now();LS.set("wo_timer",T);lastL=-1;loop();}
function tBack(){if(!T)return;var st=tstate(),el=(tnow()-T.t0)/1000-segStart(st.i);tJump(el>3?st.i:st.i-1);}
function tNext(){if(!T)return;var st=tstate();if(st.i>=T.segs.length-1){T.t0=tnow()-dur(T.segs)*1000;LS.set("wo_timer",T);loop();}else tJump(st.i+1);}
var LOCKC='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg> ',LOCKO=LOCKC.replace('<path d="M8 11V8a4 4 0 0 1 8 0v3"/>','<path d="M8 11V8a4 4 0 0 1 7.5-2"/>');
function lockLab(on){var b=$("tlock");if(!b)return;if(TABS)b.innerHTML=(on?LOCKC:LOCKO)+(on?"Locked · tap to unlock":"Lock");else b.textContent=on?"🔒 Locked":"🔓 Lock";}
function sd(s){return String(s).replace(/each hand/g,"each side");}  // pc-v64: sides always read "each side" on the clock
function sct(){var el=$("sct");if(!el)return;if(!T||!TABS){el.hidden=true;return;}var d=T.date,s=P(d),st=+LS.get("wo_runstart_"+d,0)||s.start||0;el.hidden=!st;if(!st)return;var en=s.end&&s.end>=st?s.end:0;el.textContent=(en?"Paused · ":"")+hms((en||Date.now())-st)+(LAP&&LAP.d==d&&!en?" · lap "+hms(Date.now()-LAP.t):"");}
function stopT(){T=null;LS.del("wo_timer");relWake();$("stq").hidden=true;$("bar").classList.remove("show","ask","locked");lockLab(false);}
function doneT(noTick){var t=T;T=null;LS.del("wo_timer");relWake();$("bar").classList.remove("ask");var p=P(t.date);if(noTick){$("bar").classList.remove("show");if(isOpen)renderPanel();return;}
if(t.id.indexOf("rest:")==0){var rk=t.id.slice(5),c=+p[rk]||1;if(c<(t.max||3))p[rk]=c+1;else p[rk]=c;}else if(t.amrap||t.score){scSheet(t);}else p.s[t.id]=1;LS.set("wo_"+t.date,p);
$("ph").textContent="DONE";$("ph").className="rest";$("now").textContent="Done";$("time").textContent="0:00";$("sub").textContent=t.label;$("bar").className="show p-rest";beep(988,.3);setTimeout(function(){beep(988,.6);},380);flash("bar");cue("end");hideAt=Date.now()+4000;if(isOpen)renderPanel();prog();}
// AMRAP: score entered once at the end (rounds, kg, effort word), then the block is ticked
var SCT=null;
function scSheet(t){SCT={id:t.id,date:t.date,e:""};$("sc_d").textContent=t.label;$("sc_r").value=t.rounds||(t.score?t.segs.filter(function(g){return g[0]=="WORK";}).length:0);$("sc_k").value="";[].forEach.call($("sc_e").children,function(x){x.classList.remove("on");});$("scs").classList.add("show");}
$("sc_e").addEventListener("click",function(ev){var x=ev.target.closest("[data-e]");if(!x||!SCT)return;SCT.e=x.dataset.e;[].forEach.call(this.children,function(y){y.classList.toggle("on",y==x);});});
$("sc_ok").onclick=function(){if(!SCT)return;var p=P(SCT.date);p.sc=p.sc||{};p.sc[SCT.id]={r:+$("sc_r").value||0,kg:$("sc_k").value,e:SCT.e};p.s[SCT.id]=1;LS.set("wo_"+SCT.date,p);SCT=null;$("scs").classList.remove("show");if(isOpen)renderPanel();prog();};
function short(l){return String(l||"").split(" · ")[0];}
function segLab(g){return g[0]=="READY"?"Get ready":g[2]||(g[0]=="REST"?"Rest":T.label);}
function nextLab(i){var g=T.segs[i+1];if(!g)return "";if(T.plan&&isWork(g)){var q=emomGroup(i+1);return q?(q.side?q.side.charAt(0).toUpperCase()+q.side.slice(1)+" · ":"")+q.text:segLab(g);}var l=segLab(g);if(g[0]=="REST"&&T.segs[i+2])l+=", then "+segLab(T.segs[i+2]);return l;}
// EMOM minute group for segment index i (work segments only)
function emomGroup(i){if(!T.plan||!isWork(T.segs[i]||[]))return null;var w=0;for(var j=0;j<i;j++)if(isWork(T.segs[j]))w++;return T.plan.cycle[w%T.plan.p]||null;}
function isWork(g){return g[0]!="READY"&&g[0]!="REST";}
// top line: counts work rounds only
function ctr(i){var k=T.kind,N=0,done=0,pre=T.pre?T.segs[0][1]:0;T.segs.forEach(function(g,j){if(isWork(g)){N++;if(j<=i)done++;}});
 if(k=="emom")return "Minute "+Math.max(1,done)+" of "+N;
 if(k=="every")return "Round "+Math.max(1,done)+" of "+N;
 if(k=="iv"||k=="circ"){var n=0,r=0;T.segs.forEach(function(g){n=Math.max(n,g[3]||0);});for(var j=Math.min(i,T.segs.length-1);j>=0&&!r;j--)r=T.segs[j][3]||0;return "Round "+Math.max(1,r)+" of "+(n||N);}
 var tot=dur(T.segs)-pre,el=Math.max(0,Math.floor((tnow()-T.t0)/1000-pre));return fmt(Math.min(tot,el))+" of "+fmt(tot);}
var lastTick=0;
// pc-v55: cues you can see (and, where iOS allows, feel) for a phone on silent with music playing. cue("change") washes
// the whole screen orange once, cue("end") twice, cue("tick") pulses the digits on 3-2-1. Never faster than two a second.
function cueOn(){return LS.get("wo_cue",1)!=0;}
function hap(){try{var l=$("hxl");if(l)l.click();}catch(e){}}  // best effort: Safari gives a light tap when a switch input toggles
function cue(kind){window.__cue&&window.__cue.push(kind);if(!cueOn())return;
 if(kind=="tick"){["time","rtime"].forEach(function(i){var e=$(i);if(!e)return;e.classList.remove("tk3");void e.offsetWidth;e.classList.add("tk3");});return;}
 var c=$("cue");if(!c)return;c.className="";void c.offsetWidth;c.className=kind=="end"?"c2":"c1";hap();if(kind=="end")setTimeout(hap,600);}
function flash(id){var e=$(id);if(!e)return;e.classList.remove("flash");void e.offsetWidth;e.classList.add("flash");setTimeout(function(){e.classList.remove("flash");},900);}
function sndUI(){var e=$("snd");if(e)e.hidden=!((T||RT)&&(!ac||ac.state!="running"));}
// pc-v56: session clock. Starts with the session (first tick, first guided timer, or a tap on "Start session"), stops
// at Finish (s.end). Tap it while running for a lap you can use on timed exercises; tap again to clear the lap.
var LAP=null;
function hms(ms){var t=Math.max(0,Math.floor(ms/1000)),h=Math.floor(t/3600),m=Math.floor(t%3600/60),x=t%60;return (h?h+":"+String(m).padStart(2,"0"):m)+":"+String(x).padStart(2,"0");}
function ic(p,s){return '<svg class="ic" viewBox="0 0 24 24" width="'+(s||18)+'" height="'+(s||18)+'" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+p+'</svg>';}
var IP={back:'<path d="M15 5l-7 7 7 7"/>',fwd:'<path d="M9 5l7 7-7 7"/>',tick:'<path d="M5 12.5l4.5 4.5L19 7.5"/>',timer:'<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2M9.5 3h5"/>',play:'<path d="M8 5.5v13l11-6.5z" fill="currentColor"/>',pause:'<path d="M9 5v14M15 5v14"/>',stop:'<rect x="6" y="6" width="12" height="12" rx="2" fill="currentColor"/>',snd:'<path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M17 9l4 6M21 9l-4 6"/>'};
function SI(k){return TABS?ic(IP[k],k=="tick"?18:16):{play:"▶",timer:"⏱",pause:"⏸",tick:"✓",stop:"■"}[k];}
var SCMAX=3*3600000;  // pc-v57: a session clock left running stops itself after 3 hours
function sclkState(){var S=isOpen?S_(sel):null;if(!S)return null;var s=P(sel),st=+LS.get("wo_runstart_"+sel,0)||s.start||0,en=s.end&&s.end>=st?s.end:0;
 if(st&&!en&&Date.now()-st>SCMAX){en=st+SCMAX;s.end=en;LS.set("wo_"+sel,s);}
 var anyLog=logs().some(function(e){return e&&e.date==sel&&e.type!="extra";});if(st&&!en&&anyLog){en=Date.now();s.end=en;LS.set("wo_"+sel,s);}return {S:S,s:s,st:st,en:en,lg:anyLog};}
function sclk(){var el=$("sclk");if(!el)return;var q=sclkState(),r=isOpen?R(sel):null;
 var show=!!(q&&!q.S.rest&&!q.S.tbc&&mode(sel)=="today"&&!(r.sub||q.s.oc=="skipped"));if(!show){if(!el.hidden){el.hidden=true;LAP=null;}return;}
 var h,cls;
 if(!q.st){h=q.lg?"":'<button type="button" class="sc_go" data-sc="go"><span class="si">'+SI("play")+'</span> Start session</button>';cls="sclk idle";}
 else if(q.en){LAP=null;h=q.lg?'<span class="sc_t"><span class="si">'+SI("tick")+'</span> '+hms(q.en-q.st)+'</span>':'<button type="button" class="sc_t" data-sc="resume" aria-label="Resume the session clock"><span class="si">'+SI("pause")+'</span> '+hms(q.en-q.st)+' <small>resume</small></button>';cls="sclk "+(q.lg?"done":"paused");}
 else{h='<button type="button" class="sc_t" data-sc="lap" aria-label="Lap"><span class="si">'+SI("timer")+'</span> <b>'+hms(Date.now()-q.st)+'</b>'+(LAP&&LAP.d==sel?'<span class="lap">lap '+hms(Date.now()-LAP.t)+'</span>':'')+'</button><button type="button" class="sc_x" data-sc="stop" aria-label="Stop the session clock">'+SI("stop")+'</button>';cls="sclk run";}
 el.hidden=!h;if(el.className!=cls)el.className=cls;if(el.__h!==h){el.innerHTML=h;el.__h=h;}}
function loop(){var now=Date.now(),gap=now-lastTick;lastTick=now;restTick(gap);sndUI();sclk();sct();
if(!T){if(!$("stq").hidden)$("stq").hidden=true;if(hideAt&&now>hideAt){hideAt=0;$("bar").classList.remove("show");}return;}
$("bar").classList.add("show");hideAt=0;$("tpause").textContent=T.pa?"Resume":"Pause";$("bar").classList.toggle("paused",!!T.pa);var s=tstate();$("cname").textContent=T.label;$("tround").hidden=!T.amrap;$("trn").textContent=T.rounds||0;
if(s.i>=T.segs.length){if(gap>2500||T.ask||document.hidden){T.ask=1;LS.set("wo_timer",T);$("bar").classList.add("ask");$("ph").textContent="FINISHED WHILE LOCKED";$("ph").className="";$("now").textContent="Mark done?";$("time").textContent="0:00";$("sub").textContent=T.label;return;}doneT();return;}
$("cctr").textContent=ctr(s.i);var cpi=$("cpi");if(cpi)cpi.style.width=Math.min(100,Math.max(0,(tnow()-T.t0)/10/dur(T.segs)))+"%";
var g=T.segs[s.i];if(s.i!=lastI){if(lastI!=-2){beep(988,.6);flash("bar");if(lastI>=0)cue("change");}lastI=s.i;var rd=g[0]=="READY",rs=g[0]=="REST";$("ph").textContent=rd?"GET READY":rs?"REST":"WORK";$("ph").className=rd?"ready":rs?"rest":"work";
 ["p-work","p-rest","p-ready"].forEach(function(c){$("bar").classList.remove(c);});$("bar").classList.add(rd?"p-ready":rs?"p-rest":"p-work");
 var eg=rd||rs?null:emomGroup(s.i);$("nowd").textContent=eg&&eg.side?eg.text:"";$("nowd").hidden=!(eg&&eg.side);
 $("now").textContent=rd?"Get ready":eg?(eg.side?eg.side.charAt(0).toUpperCase()+eg.side.slice(1):eg.text):T.amrap&&!rs&&T.list?T.list.slice(0,4).join("\n"):segLab(g);var nx=nextLab(s.i);if(TABS){var cl=s.i>0?nextLab(s.i-1):"";if(nx&&cl&&sd(nx)===sd(cl))nx="same again";$("now").textContent=sd($("now").textContent);nx=sd(nx);}$("sub").textContent=nx?"Next: "+nx:(T.plan?"Last minute":"Last one");}
if(s.left!=lastL){$("time").textContent=fmt(s.left);if(!T.pa&&s.left<=3&&lastL>s.left){beep(440,.1);cue("tick");}lastL=s.left;}}
// rest timer (strength blocks)
var RT=LS.get("wo_rest",null);
function autoRest(){return LS.get("wo_autorest",true)!==false;}
function startRest(sec,label){keepAudio(true);RT={end:Date.now()+sec*1000,dur:sec,label:label||"Rest"};LS.set("wo_rest",RT);unlock();wake();restTick(0);}
function rbtnVis(){var S=isOpen?S_(sel):null,off=isOpen&&(R(sel).sub||P(sel).oc=="skipped");$("rbtn").hidden=!!T||!isOpen||!S||!!S.rest||!!S.tbc||!!off;}
function stopRest(){RT=null;LS.del("wo_rest");$("rbar").classList.remove("show","zero");rbtnVis();relWake();}
function restAdj(d){if(!RT)return;RT.end=Math.max(Date.now()+1000,RT.end+d*1000);LS.set("wo_rest",RT);restTick(0);}
function restTick(gap){var rb=$("rbar");if(!RT){rb.classList.remove("show");rbtnVis();return;}$("rbtn").hidden=true;rb.classList.add("show");var left=Math.ceil((RT.end-Date.now())/1000);
if(left<=0){if(!RT.z){RT.z=Date.now();LS.set("wo_rest",RT);rb.classList.add("zero");$("rtime").textContent="0:00";$("rlab").textContent="Rest over · next set";beep(1175,.8);flash("rbar");cue("end");}else if(Date.now()-RT.z>6000)stopRest();return;}
$("rtime").textContent=fmt(left);$("rlab").textContent=RT.label;if(left<=3&&RT.ll>left){beep(440,.08);cue("tick");}RT.ll=left;}
setInterval(loop,250);
// rendering
function ticks(s){return Object.keys(s.t).filter(function(k){return s.t[k];}).length;}
function score(k){var S=S_(k);if(!S||S.rest)return null;var s=P(k),d=0,t=0;S.blocks.forEach(function(b){if(b.k=="ex")b.items.forEach(function(it){if(skp(s,it.gi))return;for(var r=0;r<bn(b,s);r++){t++;if(s.t[it.gi+"_"+r])d++;}});var tid=b.k=="timer"?b.id:b.timer?b.timer.id:null;if(tid){t++;if(sdone(k,tid))d++;}});return{d:d,t:t||S.nt};}
function bn(b,s){return b.n+((s&&s.xs&&+s.xs[b.tid||b.id])||0);}
function skp(s,gi){return !!(s&&s.sk&&s.sk[gi]);}
function setsTotal(S,s){var n=0;s=s||P(sel);S.blocks.forEach(function(b){if(b.k=="ex")b.items.forEach(function(it){if(!skp(s,it.gi))n+=bn(b,s);});});return n;}
function prog(){if(TABS&&!isOpen){var wk=weekRows(1)[0],pl=wk.plw,fw=pl?Math.min(1,wk.dn/pl):0;$("rg").style.strokeDashoffset=194.8*(1-fw);$("pct").textContent=pl?wk.dn+"/"+pl:"–";var pb0=$("sbp");if(pb0)pb0.textContent="";return;}var k=isOpen?sel:today,sc=score(k),f=sc?Math.min(1,sc.d/sc.t):0;var S=S_(k),lgp=S&&!S.rest?logFor(k,S.name):null;if(lgp&&(lgp.km||lgp.time||lgp.oc=="planned"||lgp.oc=="modified"))f=1;$("rg").style.strokeDashoffset=194.8*(1-f);$("pct").textContent=sc?Math.round(f*100)+"%":"–";var pb=$("sbp");if(pb)pb.textContent=!sc?"":lgp&&!lgp.sub?"✓ Logged":lgp?"✓ "+(lgp.min||0)+" min":sc.d+" of "+sc.t;}
var EDK=null,MO={},SM={};
function unitOf(it){return it.ru=="s"?"s":it.ru=="m"?"m":"";}
function rxOf(b,it){return b.n+" × "+it.rp+(it.ru=="s"?" s":it.ru=="m"?" m":"")+(it.side?" each side":"");}
function repV(s,k,it){return s.rp&&s.rp[k]!=null?s.rp[k]:it.rp;}
function stepOf(it){return it.ru?5:1;}
// run fields (pc-v35): actual distance, elapsed time, effort word, feel, notes. Never prefilled from the plan.
var RUNOPEN={};
var ACT={run:"Run",walk:"Walk",row:"Row",gym:"Gym session",mob:"Mobility",other:"Other"},ACTD={run:1,walk:1,row:1};
function actRow(r){var at=r.at||"run";return '<div class="l">What<div class="rcs" id="r_at">'+Object.keys(ACT).map(function(k){return '<button type="button" class="rc'+(at==k?" on":"")+'" data-at="'+k+'">'+ACT[k]+'</button>';}).join("")+'</div></div>';}
function actLabel(r){var at=r.at||"run",o=ACT[at];if((r.sl||"").trim())return r.sl.trim();if(ACTD[at]&&r.d)o+=" "+r.d+" km";if(r.t&&tnorm(r.t))o+=" "+tnorm(r.t);return o;}
var DET={};
// the one log form. Plan / extra: every field. A day that became something else (pc-v53, r.sub): What · Distance · Time ·
// Save, with name, effort, feel and notes behind "Add details" so the common case is three taps and a Save.
function runCard(dl,r,extra){var at=r.at||"run",quick=!!r.sub&&!extra,typed=extra||quick,dist=!typed||ACTD[at],open=!quick||!!DET[sel];
 var eff='<div class="l">Effort<div class="rcs" id="r_e">'+["easy","steady","moderate"].map(function(w){return '<button type="button" class="rc'+(r.e==w?" on":"")+'" data-e="'+w+'">'+w+'</button>';}).join("")+'</div></div>';
 var det=(quick?'<label class="l">Name it (optional)<input class="f" id="r_sl" type="text" placeholder="e.g. 5K easy run"></label>':'')+eff+'<label class="l">How it felt (1–10)<input class="f" id="r_f" type="number" inputmode="numeric" min="1" max="10"></label><label class="l">Notes<textarea class="f" id="r_n" rows="2"></textarea></label>';
 var have=[(r.sl||"").trim(),r.e,r.f?"felt "+r.f:"",(r.n||"").trim()?"note":""].filter(Boolean);
 return '<div class="card lock runc'+(quick?" quick":"")+'"'+(extra?' id="runx"':'')+'>'+(typed?actRow(r):'')+'<label class="l"'+(dist?'':' hidden')+'>'+dl+'<input class="f" id="r_d" type="number" inputmode="decimal" step="0.01" placeholder="e.g. 6.87"></label><label class="l">'+(quick?"Time":"Elapsed time")+'<input class="f" id="r_t" type="text" inputmode="decimal" placeholder="29:40 · 29.40 · 2940"></label>'+(open?det:'')+(quick?'<button type="button" class="link moredet" id="moredet">'+(open?"Hide details":have.length?"Details: "+esc(have.join(" · ")):"Add details")+'</button><button type="button" class="btn" id="fin2">Save</button>':'')+(extra?'<button class="btn" id="runsave">Save activity</button><button class="sm" id="runclose">Close</button>':'')+'</div>';}
// run day only: did he run the plan, or something else? (the prescription stays on the card; the log records the swap)
function subRow(r){return '<div class="l">Plan<div class="rcs" id="r_sub"><button type="button" class="rc'+(r.sub?"":" on")+'" data-sub="0">As prescribed</button><button type="button" class="rc'+(r.sub?" on":"")+'" data-sub="1">Did a different run</button></div></div>'+(r.sub?'<label class="l">What you ran instead<input class="f" id="r_sl" type="text" placeholder="e.g. 5K easy run"></label>':'');}
function planOf(S){var b=null;(S.blocks||[]).forEach(function(x){x=VB(x);if(b||x.k!="timer"||/warm|cool/i.test(x.h||""))return;if(x.counter||/^(Steady|Intervals)/.test(x.h||""))b=x;});return b?b.name+" "+mmss(dur(b.segs)):S.name;}
function ocLine(e){var o=[];if(e.sub)o.push("did "+esc(e.sub)+" instead of "+esc(e.plan||"the plan"));if(e.oc&&e.oc!="planned"&&!(e.sub&&e.oc=="modified"))o.push(esc(e.oc));return o.join(" · ");}
function tnorm(t){t=String(t||"").trim();if(!t)return "";var m=/^(\d+):(\d\d)(?::(\d\d))?$/.exec(t);if(m)return m[3]?m[1]+":"+m[2]+":"+m[3]:(+m[1])+":"+m[2];
 if(/^\d{4}$/.test(t)&&+t.slice(2)<60)return (+t.slice(0,2))+":"+t.slice(2);  // 3005 → 30:05 (the iPhone number pad has no colon key)
 var ds=/^(\d+)\.(\d\d)$/.exec(t);if(ds&&+ds[2]<60)return (+ds[1])+":"+ds[2];  // 29.40 → 29:40 (what a watch shows); 29.5 stays 29:30
 if(/^\d+(\.\d+)?$/.test(t)){var x=Math.round(+t*60);return Math.floor(x/60)+":"+String(x%60).padStart(2,"0");}return t;}
function tmin(t){var m=/^(\d+):(\d\d)(?::(\d\d))?$/.exec(tnorm(t));if(!m)return 0;return m[3]?+m[1]*60+ +m[2]+Math.round(+m[3]/60):+m[1]+Math.round(+m[2]/60);}
function extraFor(d){var l=logs();for(var i=0;i<l.length;i++)if(l[i]&&l[i].date==d&&l[i].type=="extra")return i;return -1;}
function runLine(e){var x=[];if(e.km)x.push(esc(e.km)+(e.sid=="row"&&!e.ri?" m":" km"));if(e.time)x.push(esc(tnorm(e.time)));if(e.effort)x.push(esc(e.effort));return x.join(" · ");}
function hasRun(S){return !!(S&&S.blocks&&(S.blocks.some(function(b){return b.k=="fields";})||S.blocks.some(function(b){return VB(b).counter;})));}
// pc-v41: a block is done when its timer flag is set or every set is ticked; done blocks fold to one line (tap to show)
var UNF={},LASTB=null;
function blockOfGi(S,gi){var r=null;S.blocks.forEach(function(b){if(b.k=="ex"&&b.items.some(function(it){return it.gi==gi;}))r=b;});return r;}
function blockDone(b,s){if(b.k=="timer")return sdone(sel,b.id);if(b.k=="ex"){if(b.timer)return sdone(sel,b.timer.id);var any=false;for(var q=0;q<bn(b,s);q++)for(var i=0;i<b.items.length;i++){if(skp(s,b.items[i].gi))continue;any=true;if(!s.t[b.items[i].gi+"_"+q])return false;}return any;}return false;}
function foldLine(fold,id,label){return fold?'<button type="button" class="fold" data-unf="'+esc(id)+'">✓ Done · '+esc(label)+' · show</button>':'';}
function foldCards(){var kids=[].slice.call($("sess").children),on=false;kids.forEach(function(el){if(el.tagName=="H2"||el.classList.contains("bh")){on=false;return;}if(el.classList.contains("fold")){on=true;return;}if(on)el.classList.add("folded");});}
var SHOWP={},ACTS={run:"Run",walk:"Walk",row:"Row",gym:"Gym",mob:"Mobility",other:"Other"};
// pc-v49: the question sits at the top of the day. "Something else" / "Skipped it" put the day in off-plan mode: the log
// card leads, the planned blocks fold behind "Show the planned session", and a Save button sits right under the form.
function topQ(S,s,r){var tq=$("topq");if(!tq)return;var m=mode(sel);if(!S||S.rest||S.tbc||m=="future"||m=="pre"){tq.hidden=true;tq.innerHTML="";return;}tq.hidden=false;
 var cur=r.sub?"else":s.oc=="skipped"?"skip":"plan",coll=TABS&&m=="today"&&cur=="plan"&&!logFor(sel,S.name)&&extraFor(sel)<0&&!TQO[sel],h='<div class="tql">What did you do?</div><div class="rcs" id="toc">'+[["plan","The plan"],["else","Something else"],["skip","Skipped"]].map(function(c){return '<button type="button" class="rc'+(cur==c[0]?" on":"")+'" data-toc="'+c[0]+'">'+c[1]+'</button>';}).join("")+'</div>';
 var xi=extraFor(sel),lgm=logFor(sel,S.name);if(xi>=0&&!r.sub&&(!lgm||lgm.oc=="skipped")){var x=logs()[xi],rl=runLine(x).replace(/<[^>]*>/g,"");h+='<div class="conv">You logged <b>'+esc(x.name||"an activity")+(rl?" · "+esc(rl):"")+'</b> on this day.<button type="button" class="btn" id="xconv">It replaced '+esc(S.name)+'</button></div>';}
 tq.classList.toggle("q",coll);if(coll)h='<button type="button" class="tqq" data-tqx="1">Doing something else or skipping?<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>';tq.innerHTML=h;}
var TQO={};
function renderSess(){var S=S_(sel),s=P(sel),r=R(sel),h="",hA="",hX="",hO="",n=0,hasF=false,nDone=0,firstOpen=-1;
NXB=null;if(TABS&&mode(sel)=="today"){var apb=LASTB&&LASTB.indexOf(sel+"|")==0?LASTB.slice(sel.length+1):null,fob=null,abb=null;S.blocks.forEach(function(b0){if(b0.k=="rest"||b0.k=="fields")return;var b1=VB(b0);if(b1.k!="ex")return;var id1=b1.tid||b1.id;if(!blockDone(b1,s)){if(fob==null)fob=id1;if(apb&&id1==apb)abb=id1;}});NXB=abb||fob;}
var offp0=!S.rest&&!S.tbc&&!!(r.sub||s.oc=="skipped"),fc=TABS&&!offp0&&!S.rest&&!S.tbc,hXL="";
S.blocks.forEach(function(b){
 if(b.k=="rest"){var nmx=b.name,ntx=b.note;if(S.tbc){nmx="No plan yet";ntx="Nothing planned for w/c "+sdl(monOf(sel))+". Ask Health & Fitness for the week file, then "+(TABS?"Settings on the Today screen → Import week.":"History → Weeks → Import week.")+(sel<=today?(TABS?" Until then, rest or log any activity below.":" Until then, pick a backup from another day or rest."):"");}h+='<div class="card"><div class="name">'+nmx+'</div><div class="note">'+ntx+'</div></div>';return;}
 if(b.k=="fields"){hA+='<h2>Actual</h2>'+runCard(b.dist||"Distance (km)",r,false);hasF=true;return;}
 n++;b=VB(b);var tt=b.timer||b,D=dur(tt.segs);var bdn=blockDone(b,s),fold=bdn&&!UNF[sel+"|"+(b.id||b.tid)]&&!(b.k=="ex"&&LASTB==sel+"|"+(b.tid||b.id));if(bdn)nDone++;else if(firstOpen<0)firstOpen=n;
 if(b.k=="timer"){h+='<h2>'+n+' · '+b.h+' · '+mmss(D)+'</h2>'+foldLine(fold,b.id,b.name)+'<div class="card tcard'+(sdone(sel,b.id)?" done":"")+'" id="c_'+b.id+'"><div class="name">'+b.name+'</div>'+(b.note?'<div class="note">'+b.note+'</div>':'')+lastScore(b.id);
  var mvl=function(a){return '<ul class="lst">'+a.map(function(x){var hk=hkey(x);return "<li>"+(HT[hk]?'<button class="mv" data-h="'+esc(hk)+'">'+x+'</button>':x)+"</li>";}).join("")+'</ul>';};
  if(b.groups)h+=b.groups.map(function(g){return '<div class="rg"><div class="rgh">'+g[0]+' <span>each side</span></div><ul class="lst rgl">'+g[1].map(function(m){var hk=hkey(m[0]);return '<li>'+(HT[hk]?'<button class="mv" data-h="'+esc(hk)+'">'+m[1]+'</button>':m[1])+' <b>×'+m[2]+'</b></li>';}).join("")+'</ul></div>';}).join("");
  else if(kindOf(b)=="emom"&&emomPlan(b))h+=emomHTML(emomPlan(b));
  else if(b.list&&!b.flow)h+=mvl(b.list);
  else if(b.list){var op=SM[b.id];h+='<button class="sm" data-sm="'+b.id+'">'+(op?"Hide moves":"Show "+b.list.length+" moves")+'</button>';if(op)h+=mvl(b.list);}
  if(kindOf(b)!="emom")h+=sps(b.small);  // EMOM: the per-minute groups say it all; every minute is a full 60 s
  var dn=sdone(sel,b.id);h+='<button class="btn lock'+(dn?" gt dn":"")+'" data-t="'+b.id+'">'+(dn?"✓ Done · run guided timer again":b.flow?"Start guided flow":"Start guided timer")+' · '+mmss(D)+'</button>'+(b.counter?'<button class="btn ghost lock" id="brkb">+1 walk break · <span id="brk">'+r.b+'</span></button>':'')+'</div>';return;}
 // exercise group
 if(b.rr){var one=b.items.length==1;h+='<div class="bh"><h2>'+n+' · '+b.h+' · '+b.n+(one?' sets':' rounds')+'</h2></div>'+foldLine(fold,b.tid||b.id,b.items.map(function(it){return nm(it.x);}).join(" + "));
  h+='<div class="gn rx">Each '+(one?'set':'round')+': '+b.items.map(function(it){return it.lab;}).join(" → ")+'. Rest '+b.rr[0]+'–'+b.rr[1]+' s.</div>'+sps([autoRest()?(one?"Tick a set to start the rest timer.":"Tick the last move of a round to start the rest timer."):"",b.fill?"Optional in the rest: "+b.fill+".":""]);}
 else h+='<div class="bh"><h2>'+n+' · '+b.h+(D?' · '+mmss(D):'')+'</h2></div>'+foldLine(fold,b.tid||b.id,b.items.map(function(it){return nm(it.x);}).join(" + "));
 if(b.gn)h+='<div class="gn">'+b.gn+'</div>';
 if(b.rr&&!b.timer){h+=listBlock(b,s);return;}
 if(b.rest&&!b.mode)h+='<div class="round">'+b.unit+' <span id="rd_'+b.rk+'">'+Math.min(+s[b.rk]||1,b.n)+'</span> of '+b.n+' · '+b.note+'</div>';
 b.items.forEach(function(it){var e=X[it.x],i=it.gi,cur=dayW(it.x,sel),last=lastW(it.x,sel),pf=cur==null&&last?last.v:null,val=cur!=null?cur:pf,mo=MO[i];
  h+='<div class="card ex'+(mo?" mo":"")+'" data-x="'+it.x+'"><div class="hd"><div class="name">'+(it.lab?'<span class="lab">'+it.lab+'</span>':'')+e[0]+'</div><button class="more" data-mo="'+i+'">'+(mo?"Less":"More")+'</button></div>';
  h+='<div class="note">'+(it.rp?rxOf(b,it):it.rx)+(it.tp?' <span class="chip">'+it.tp+'</span><span class="tm">'+tmean(it.tp)+'</span>':'')+'</div>';
  h+='<div class="row">';
  for(var q=0;q<b.n;q++){var k=i+"_"+q;if(it.rp){var v=repV(s,k,it);h+='<button class="pill lock'+(s.t[k]?" on":"")+(EDK==k?" ed":"")+'" data-k="'+k+'" aria-label="'+b.unit+' '+(q+1)+'">'+(s.t[k]?"✓ ":"")+v+unitOf(it)+'</button>';}
   else h+='<button class="tick lock'+(b.n>3?" sm":"")+(s.t[k]?" on":"")+'" data-k="'+k+'" aria-label="'+b.unit+' '+(q+1)+'">'+(s.t[k]?"✓":(q+1))+'</button>';}
  if(e[3])h+=val!=null?'<input class="w lock'+(pf!=null?' pf':'')+'" type="number" inputmode="decimal" placeholder="'+e[2]+'" data-w="'+i+'" value="'+esc(val)+'">':'<button class="addw lock" data-a="'+i+'">+ kg</button>';
  h+='</div>';
  if(EDK&&+EDK.split("_")[0]==i&&it.rp){var qq=+EDK.split("_")[1];h+='<div class="step lock"><span>Set '+(qq+1)+'</span><button data-st="-1" aria-label="fewer">−</button><b id="stv">'+repV(s,EDK,it)+(it.ru?" "+it.ru:" reps")+'</b><button data-st="1" aria-label="more">+</button><button data-st="u" class="su">Undo</button><button data-st="x" class="su">OK</button></div>';}
  h+='<div class="mx"'+(mo?'':' hidden')+'>'+(it.cue?'<div class="cue">'+it.cue+'</div>':'')+'<div class="note">'+(e[3]?(last?'Last: '+esc(last.v)+' kg ('+sdl(last.d)+')'+(cur!=null&&+cur>+last.v?' <span class="up">↑</span>':''):'Suggested: '+e[1]):e[1])+'</div><button class="how" data-h="'+it.x+'">How to</button></div>'+sugHTML(it.x,it)+'</div>';});
 if(b.rest&&!b.mode)h+='<button class="btn lock" data-t="rest:'+b.rk+'">'+b.btn+'</button>';
 if(b.timer)h+='<button class="btn lock gt'+(sdone(sel,b.timer.id)?" dn":"")+'" data-t="'+b.timer.id+'" id="c_'+b.timer.id+'">'+(sdone(sel,b.timer.id)?"✓ Done · run guided timer again":"Start guided timer")+' · '+mmss(D)+'</button>';});
if(!hasF&&hasRun(S)){hA+='<h2>Actual</h2>'+runCard("Distance (km)",r,false);hasF=true;}  // a run inside a mixed session (pc-v38) gets the same card as a run day
var subF=false;if(!hasF&&r.sub&&!S.rest&&!S.tbc){hA+='<h2>Actual</h2>'+runCard("Distance (km)",r,false);subF=true;}  // a day that became something else gets the same card
if(!hasF&&!(r.sub&&!S.rest&&!S.tbc)){var xi=extraFor(sel),open=RUNOPEN[sel]||xi>=0;hX+=(fc&&!open?'<h2 class="vh">Extra</h2>':'<h2>Extra</h2>')+(open?runCard("Distance (km)",r,true):(fc?(hXL='<button class="link addrun" id="addrun">+ Add an activity</button>',''):'<button class="link addrun" id="addrun">+ Add an activity</button>'));}
// B. outcome of the session, for the log and for the coach: as planned / modified / cut short / skipped (+ a note on days without the run card)
if(!S.rest&&!S.tbc){var chips=hasF?["planned","different run","modified","cut short","skipped"]:["planned","something else","modified","cut short","skipped"],cur=r.sub?(hasF?"different run":"something else"):(s.oc||""),off=!!(r.sub||s.oc=="skipped");
 hO+=(fc?'<h2 class="vh">How did it go?</h2>':'<h2>How did it go?</h2>')+'<div class="card lock ocard'+(fc?' fcard':'')+'" id="logsec">'+(fc?'<div class="ftit">Finish</div><div class="fl">How did it go?</div>':'')+'<div class="rcs" id="oc">'+chips.map(function(w){return '<button type="button" class="rc'+(cur==w?" on":"")+'" data-oc="'+w+'">'+(w=="planned"?"as planned":w)+'</button>';}).join("")+'</div>'+(hasF||subF?'':'<label class="l">Notes<textarea class="f" id="s_nt" rows="2" placeholder="anything Grokbot should know"></textarea></label>')+(off&&!r.sub?'<button type="button" class="btn" id="fin2">Save</button>':'')+(fc?'<button type="button" class="btn" id="fin_c">'+esc($("fin").textContent)+'</button>':'')+'</div>';}
var offp=!S.rest&&!S.tbc&&!!(r.sub||s.oc=="skipped");$("panel").classList.toggle("offp",offp&&!SHOWP[sel]);$("panel").classList.toggle("fc",!!fc);topQ(S,s,r);$("safe1").hidden=offp;var bare=offp&&!SHOWP[sel];$("acts").hidden=!!S.rest||bare;$("rstw").hidden=!!S.rest||bare;[].forEach.call(document.querySelectorAll(".setr"),function(sr){sr.hidden=bare;});
h=offp?(r.sub?hA:hO)+'<button type="button" class="link showp" id="showp">'+(SHOWP[sel]?"Hide":"Show")+' the planned session</button>'+(SHOWP[sel]?h:"")+hX:h+hA+hX+hO+(fc?'<div class="frow">'+hXL+'<button type="button" class="link lock" id="rst_c">Reset this day…</button></div>':"");
$("sess").innerHTML=h;foldCards();if(firstOpen>0&&nDone>0){var hx=null;[].forEach.call($("sess").querySelectorAll("h2"),function(x){if(!hx&&x.textContent.indexOf(firstOpen+" · ")==0)hx=x;});if(hx){var up=document.createElement("div");up.className="upnext";up.textContent="Up next";var ref=hx.parentNode.classList.contains("bh")?hx.parentNode:hx;ref.parentNode.insertBefore(up,ref);}}["d","t","f","n","sl"].forEach(function(k){var el=$("r_"+k);if(el)el.value=r[k]||"";});var nt=$("s_nt");if(nt)nt.value=s.nt||"";}
// save or update the one "Extra run" entry for this date (never a second strength log)
function saveExtra(d){var r=R(d),l=logs(),i=extraFor(d),e=i>=0?l[i]:{date:d,name:"Extra run",type:"extra",extra:1};var at=r.at||"run";e.act=at;e.name=at=="run"?"Extra run":ACT[at];e.km=ACTD[at]?(r.d||""):"";e.time=tnorm(r.t||"");e.effort=r.e||"";e.feel=r.f||"";e.notes=r.n||"";e.min=tmin(e.time)||e.min||0;if(i>=0)l[i]=e;else l.push(e);LS.set("wo_log",l);}
// list mode (pc-v30): one card per block; rows = set | kg | reps | tick, supersets alternate B1, B2; no block timer
function kgOf(s,k,it){if(!X[it.x][3])return null;if(s.kg&&s.kg[k]!=null&&s.kg[k]!=="")return {v:String(s.kg[k])};var c=dayW(it.x,sel);if(c!=null)return {v:c};var l=lastW(it.x,sel);return l?{v:l.v,pf:1}:{v:""};}
function lastSets(x){var l=logs(),best=null;l.forEach(function(e){if(e.date<sel&&e.rp&&e.rp[x]&&(!best||e.date>best.date))best=e;});if(!best)return null;var r=best.rp[x];return {v:r.v||[],u:r.u||"",k:r.k||null,w:best.wt&&best.wt[x],n:r.n||"",sub:r.sub||"",d:best.date};}
function restLab(b){return fmt(b.rest);}
// ---- progression (pc-v40): a suggestion from the last logged sets of the same exercise, never from the plan.
// Rule: every set hit the target reps last time → add one step (2 kg dumbbells, 4 kg kettlebells); a missed set →
// same weight; the suggestion always says it holds only if last time felt RPE 6–7 (2 RIR).
function kstep(x){var n=(X[x]&&X[x][0]||"").toLowerCase();return /kettlebell|^kb-/.test(n)||/^kb-/.test(x)?4:2;}
function suggest(x,it){if(!X[x]||!X[x][3]||it.ru)return null;var ls=lastSets(x);if(!ls||!ls.v||!ls.v.length||ls.sub)return null;var tgt=+it.rp;if(!(tgt>0))return null;
 var kgs=(ls.k||[]).filter(function(v){return v&&v!="–"&&!isNaN(+v);}).map(Number),kg=kgs.length?Math.max.apply(null,kgs):(ls.w&&!isNaN(+ls.w)?+ls.w:null);if(kg==null)return null;
 var done=ls.v.filter(function(v){return v!="–"&&v!=null&&v!=="";}),hit=done.length>0&&done.every(function(v){return +v>=tgt;});
 return hit?{kg:kg+kstep(x),why:"all "+done.length+" sets hit "+tgt+" at "+kg+" kg last time",up:1}:{kg:kg,why:"last time "+ls.v.join("/")+" at "+kg+" kg, target "+tgt,up:0};}
function sugHTML(x,it){var g=suggest(x,it);if(!g)return "";var cur=dayW(x,sel);if(cur!=null&&+cur==g.kg)return "";
 if(!g.up)return cur!=null?"":'<div class="sug same">Stay at '+g.kg+' kg · '+esc(g.why)+'</div>';
 return '<div class="sug"><button type="button" class="btn sm sfill lock" data-sf="'+x+'|'+g.kg+'">Use '+g.kg+' kg</button><span>'+esc(g.why)+' · only if it felt RPE 6–7</span></div>';}
function fillKg(x,kg){var S=S_(sel),s=P(sel);s.kg=s.kg||{};S.blocks.forEach(function(b){if(b.k!="ex")return;b.items.forEach(function(it){if(it.x!=x)return;for(var q=0;q<bn(b,s);q++){var k=it.gi+"_"+q;if(!s.t[k])s.kg[k]=String(kg);}});});LS.set("wo_"+sel,s);setW(x,sel,kg);renderSess();}
// ---- Progress screen (pc-v40): the last weeks, strength by exercise, recent runs; all from wo_log and the programme
function weekRows(n){var rows=[],m=monOf(today),l=logs();for(var i=0;i<n;i++){var mon=addDays(m,-7*i),sun=addDays(mon,6),pl=0,plw=0,dn={},runs=0,km=0,min=0;
  Object.keys(PROG).forEach(function(d){if(d<mon||d>sun||d<=LEGACY_END)return;var S=SESS[baseSid(d)];if(S&&!S.rest){plw++;if(d<=today)pl++;}});
  l.forEach(function(e){if(!e||!e.date||e.date<mon||e.date>sun)return;if(e.type!="extra"&&!(e.oc=="skipped"))dn[e.date]=1;if(e.km||e.time){runs++;km+=parseFloat(e.km)||0;min+=tmin(e.time||"");}});
  rows.push({mon:mon,pl:pl,plw:plw,dn:Object.keys(dn).length,runs:runs,km:Math.round(km*10)/10,min:min});}return rows;}
function exRows(){var by={};logs().forEach(function(e){if(!e||!e.rp)return;Object.keys(e.rp).forEach(function(x){(by[x]=by[x]||[]).push({d:e.date,w:e.wt&&e.wt[x],r:e.rp[x]});});});
 return Object.keys(by).map(function(x){var a=by[x].sort(function(p,q){return p.d<q.d?-1:1;}),last=a.slice(-3),prev=a.length>1?a[a.length-2]:null,now=a[a.length-1],kn=kgOfLog(now),kp=prev?kgOfLog(prev):null;
  return {x:x,name:nm(x),rows:last,trend:(now.r.sub||(prev&&prev.r.sub))?"":kn!=null&&kp!=null?(kn>kp&&!(now.r.v||[]).some(function(v){return v=="–"||v===""||v==null;})?"up":kn<kp?"down":"same"):""};}).sort(function(p,q){return p.rows[p.rows.length-1].d<q.rows[q.rows.length-1].d?1:-1;});}
function kgOfLog(e){var k=(e.r&&e.r.k||[]).filter(function(v){return v&&v!="–"&&!isNaN(+v);}).map(Number);if(k.length)return Math.max.apply(null,k);return e.w&&!isNaN(+e.w)?+e.w:null;}
var XALL=false;
function progressT(el){if(!logs().length){el.innerHTML='<div class="pempty"><b>Nothing logged yet.</b>Once you finish a session, this page shows your week against last week, your last four weeks, your lifts with their trend and your recent runs.</div>';return;}
 var wr=weekRows(4),tw=wr[0],lw=wr[1],h="",tile=function(l,n,u,c){return '<div><span class="tl">'+l+'</span><b>'+n+(u?'<small>'+u+'</small>':'')+'</b><span class="tc">'+c+'</span></div>';};
 h+='<div class="wkbig t4">'+tile("Sessions",tw.dn," / "+tw.plw,lw?"last week "+lw.dn+" of "+lw.plw:"this week")+tile("Runs",tw.runs,"",lw?"last week "+lw.runs:"this week")+tile("Distance",tw.km," km",lw?"last week "+lw.km+" km":"this week")+tile("Running",tw.min," min",lw?"last week "+lw.min+" min":"this week")+'</div>';
 h+='<div class="hs_h">Last 4 weeks</div>'+wr.map(function(r,ri){var pl=ri==0?r.plw:r.pl,pc=pl?Math.min(100,Math.round(r.dn/pl*100)):0;return '<div class="prow wk4"><b>w/c '+esc(sdl(r.mon).replace(/^\w+ /,""))+'</b> · '+(pl||r.dn?r.dn+' of '+pl+' sessions':'nothing planned')+(r.runs?' · '+r.runs+' run'+(r.runs==1?'':'s')+' · '+r.km+' km'+(r.min?' · '+r.min+' min':''):'')+'<div class="bar" aria-hidden="true"><i style="width:'+pc+'%"></i></div></div>';}).join("");
 var ex=exRows();if(ex.length){var shown=XALL?ex:ex.slice(0,5);h+='<div class="hs_h">Strength · last 3 per exercise</div>'+shown.map(function(e){return '<button type="button" class="xcard" data-xh="'+esc(e.x)+'"><span class="xn">'+esc(e.name)+(e.trend=="up"?' <span class="up">↑</span>':e.trend=="down"?' <span class="dn">↓</span>':'')+'</span><small>'+e.rows.map(function(r){return esc(sdl(r.d).replace(/^\w+ /,""))+': '+esc((r.r.v||[]).join("/")+(r.r.u?" "+r.r.u:""))+(kgOfLog(r)!=null?' @ '+kgOfLog(r)+' kg':'')+(r.r.sub?' (as '+esc(r.r.sub)+')':'')+(r.r.n?' · '+esc(r.r.n):'');}).join(" · ")+'</small></button>';}).join("")+(ex.length>5?'<button type="button" class="link xall" data-xall="1">'+(XALL?"Show fewer":"Show all "+ex.length)+'</button>':"");}
 var runs=logs().filter(function(e){return e&&(e.km||e.time);}).slice(-5).reverse();if(runs.length)h+='<div class="hs_h">Recent runs</div><div class="rtab">'+runs.map(function(e){return '<div class="rrow"><b>'+esc(sdl(e.date).replace(/^\w+ /,""))+'</b><span>'+(e.km?esc(e.km)+' km':'–')+'</span><span>'+(e.time?esc(e.time):'–')+'</span><span>'+(e.effort?esc(e.effort):'–')+'</span></div>'+(e.sub||e.type=="extra"?'<div class="rnote">'+(e.sub?'instead of '+esc(e.plan||"the plan"):'')+(e.type=="extra"?(e.sub?' · ':'')+'extra':'')+'</div>':'');}).join("")+'</div>';
 el.innerHTML=h;}
$("prog_b").addEventListener("click",function(e){var x=e.target.closest("[data-xh]");if(x){xhist(x.dataset.xh);return;}if(e.target.closest("[data-xall]")){XALL=!XALL;progress();}});
function progress(){var el=$("prog_b");if(!el)return;if(TABS){progressT(el);return;}var h="",wr=weekRows(4),tw=wr[0],lw=wr[1];
 h+='<div class="wkbig"><div><b>'+tw.dn+'<small>/'+(TABS?tw.plw:tw.pl)+'</small></b><span>sessions</span></div><div><b>'+tw.runs+'</b><span>run'+(tw.runs==1?'':'s')+'</span></div><div><b>'+tw.km+'<small> km</small></b><span>'+(lw?'last week '+lw.km+(TABS?'':' km'):'this week')+'</span></div><div><b>'+tw.min+'<small> min</small></b><span>'+(lw&&!TABS?'last week '+lw.min+' min':'running')+'</span></div></div>';
 h+='<div class="hs_h">Last 4 weeks</div>'+wr.map(function(r,ri){var pl=TABS&&ri==0?r.plw:r.pl;return '<div class="prow"><b>w/c '+esc(sdl(r.mon).replace(/^\w+ /,""))+'</b> · '+(pl||r.dn?r.dn+' of '+pl+' sessions':'nothing planned')+(r.runs?' · '+r.runs+' run'+(r.runs==1?'':'s')+' · '+r.km+' km'+(r.min?' · '+r.min+' min':''):'')+'</div>';}).join("");
 var ex=exRows();if(ex.length)h+='<div class="hs_h">Strength · last 3 per exercise</div>'+ex.map(function(e){return '<div class="prow"><b>'+esc(e.name)+'</b>'+(e.trend=="up"?' <span class="up">↑</span>':e.trend=="down"?' <span class="dn">↓</span>':'')+'<br><small>'+e.rows.map(function(r){return esc(sdl(r.d).replace(/^\w+ /,""))+': '+esc((r.r.v||[]).join("/")+(r.r.u?" "+r.r.u:""))+(kgOfLog(r)!=null?' @ '+kgOfLog(r)+' kg':'')+(r.r.sub?' (as '+esc(r.r.sub)+')':'')+(r.r.n?' · '+esc(r.r.n):'');}).join(" · ")+'</small></div>';}).join("");
 var runs=logs().filter(function(e){return e&&(e.km||e.time);}).slice(-5).reverse();if(runs.length)h+='<div class="hs_h">Recent runs</div>'+runs.map(function(e){return '<div class="prow"><b>'+esc(sdl(e.date).replace(/^\w+ /,""))+'</b> · '+esc(runLine(e).replace(/<[^>]*>/g,""))+(e.sub?' · instead of '+esc(e.plan||"the plan"):'')+(e.type=="extra"?' · extra':'')+'</div>';}).join("");
 el.innerHTML=h||"<div class=\"prow\">Nothing logged yet.</div>";}
var DOTS='<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>',NXB=null;
function listBlock(b,s){var multi=b.items.length>1,h='<div class="card ex blk" data-b="'+b.bi+'">';
 b.items.forEach(function(it){var e=X[it.x],i=it.gi,cur=dayW(it.x,sel),last=lastW(it.x,sel),mo=MO[i];
  var rx=s.rx&&s.rx[i],sk=skp(s,i),xn=s.xn&&s.xn[i]||"";
  h+='<div class="mvh'+(sk?" skp":"")+'" data-x="'+it.x+'"><div class="hd"><div class="name">'+(it.lab?'<span class="lab">'+it.lab+'</span>':'')+(rx?'<span class="rxn">'+esc(rx)+'</span> <small class="rxs">instead of</small> ':'')+'<button class="mvn" data-h="'+it.x+'">'+e[0]+'</button>'+(sk?' <small class="rxs">· skipped</small>':'')+'</div><button class="more" data-mo="'+i+'"'+(TABS?' aria-label="'+(mo?"Less":"More")+'">'+DOTS:'>'+(mo?"Less":"More"))+'</button></div>';
  if(ls0(it.x))h+='<div class="note lnote">Last time: '+esc(ls0(it.x))+'</div>';
  h+='<div class="note">'+rxOf(b,it)+(it.tp?' <span class="chip">'+it.tp+'</span><span class="tm">'+tmean(it.tp)+'</span>':'')+'</div>';
  h+='<div class="mx"'+(mo?'':' hidden')+'>'+(it.cue?'<div class="cue">'+it.cue+'</div>':'')+'<div class="note">'+(e[3]?(last?'Last: '+esc(last.v)+' kg ('+sdl(last.d)+')'+(cur!=null&&+cur>+last.v?' <span class="up">↑</span>':''):'Suggested: '+e[1]):e[1])+'</div><button class="how" data-h="'+it.x+'">How to</button><label class="l xl">Note for next time<input class="f lock" type="text" data-xn="'+i+'" value="'+esc(xn)+'" placeholder="e.g. left knee twinge on rep 6"></label><label class="l xl">Did a different exercise<input class="f lock" type="text" data-rx="'+i+'" value="'+esc(rx||"")+'" placeholder="e.g. Goblet squat (rack was busy)"></label><button type="button" class="link lock" data-sk="'+i+'">'+(sk?"Un-skip this exercise":"Skip this exercise")+'</button> <button type="button" class="link" data-xh="'+it.x+'">History</button></div>'+(sk?'':sugHTML(it.x,it))+'</div>';});
 h+='<div class="rs">rest '+restLab(b)+(multi?' after '+b.items[b.items.length-1].lab:' after each set')+'</div>';
 var nxd=false,actb=TABS&&NXB&&(b.tid||b.id)==NXB&&mode(sel)=="today";for(var q=0;q<bn(b,s);q++){if(TABS)h+='<div class="rnd"><div class="rn">'+(q+1)+'</div><div class="rrows">';b.items.forEach(function(it){if(skp(s,it.gi))return;var k=it.gi+"_"+q,on=!!s.t[k],kg=kgOf(s,k,it),ls=lastSets(it.x),lv=ls&&ls.v[q]!=null&&ls.v[q]!=="–"?ls.v[q]:null,lk=ls?(ls.k&&ls.k[q]?ls.k[q]:ls.w):null;
  h+='<div class="srow'+(on?" on":"")+(actb&&!on&&!nxd?(nxd=true," nx"):"")+'" data-x="'+it.x+'" data-row="'+k+'"><span class="sn">'+(TABS?'':(q+1))+(multi?(TABS?'':' · ')+it.lab:'')+(lv!=null?'<small class="lchip" data-xh="'+it.x+'">last '+(lk?esc(lk)+' kg × ':'')+esc(lv)+(ls.u?" "+ls.u:"")+'</small>':'')+'</span>';
  h+=kg?'<input class="w lock'+(kg.pf?' pf':'')+'" type="number" inputmode="decimal" placeholder="'+(TABS&&lk&&!isNaN(+lk)&&+lk>0?esc(lk):"kg")+'" aria-label="kg set '+(q+1)+'" data-kw="'+k+'" value="'+esc(kg.v)+'">':'<span class="bw">BW</span>';
  h+='<button class="rpb lock'+(EDK==k?" ed":"")+'" data-rp="'+k+'" aria-label="reps set '+(q+1)+'">'+repV(s,k,it)+(it.ru?" "+it.ru:"")+'</button>';
  h+='<button class="tk lock'+(on?" on":"")+'" data-tk="'+k+'" aria-label="'+b.unit+' '+(q+1)+(multi?' '+it.lab:'')+' done">'+(on?(TABS?ic(IP.tick,20):"✓"):"")+'</button></div>';
  if(EDK==k)h+='<div class="step lock"><span>Set '+(q+1)+'</span><button data-st="-1" aria-label="fewer">−</button><b id="stv">'+repV(s,k,it)+(it.ru?" "+it.ru:" reps")+'</b><button data-st="1" aria-label="more">+</button><button data-st="u" class="su">Undo</button><button data-st="x" class="su">OK</button></div>';});if(TABS)h+='</div></div>';}
 var xs=(s.xs&&+s.xs[b.tid||b.id])||0;h+='<div class="setctl"><button type="button" class="link lock" data-xs="1" data-b="'+esc(b.tid||b.id)+'">+ '+(multi?"round":"set")+'</button>'+(xs>0?'<button type="button" class="link lock" data-xs="-1" data-b="'+esc(b.tid||b.id)+'">− '+(multi?"round":"set")+'</button>':'')+'</div>';
 return h+'</div>';}
function lastScore(id){var best=null;logs().forEach(function(e){if(e&&e.date<sel&&e.sc&&e.sc[id]&&(!best||e.date>best.date))best=e;});if(!best)return "";var q=best.sc[id];return '<div class="note lnote">Last time: '+(q.r||0)+' rounds'+(q.kg?' · '+esc(q.kg)+' kg':'')+(q.e?' · '+esc(q.e):'')+' ('+esc(sdl(best.date))+')</div>';}
function ls0(x){var l=lastSets(x);return l&&l.n?l.n:"";}
// rest bar line: the next unticked set in this block
function nextSet(b,s){for(var q=0;q<bn(b,s);q++)for(var j=0;j<b.items.length;j++){var it=b.items[j],k=it.gi+"_"+q;if(skp(s,it.gi))continue;if(!s.t[k]){var kg=kgOf(s,k,it);return "Next: set "+(q+1)+" · "+repV(s,k,it)+(it.ru?" "+it.ru:"")+(kg&&kg.v?" @ "+kg.v+" kg":"")+(b.items.length>1?" · "+(it.lab||X[it.x][0]):"");}}return "Rest";}
function sps(a){return [].concat(a||[]).filter(Boolean).map(function(x){return '<div class="sp">'+x+'</div>';}).join("");}
function maybeRest(S,s,k){if(!autoRest()||mode(sel)!="today"||(T&&T.date==sel))return;var gi=+k.split("_")[0],q=+k.split("_")[1];S.blocks.forEach(function(b){if(b.mode!="sup"||!b.items.some(function(it){return it.gi==gi;}))return;if(!b.items.every(function(it){return skp(s,it.gi)||s.t[it.gi+"_"+q];}))return;if(q>=bn(b,s)-1){if(RT)stopRest();return;}startRest(b.rest,nextSet(b,s));});}
function itemByGi(S,gi){var a=items(S);for(var i=0;i<a.length;i++)if(a[i].gi==gi)return a[i];return null;}
function renderPanel(){var S=S_(sel),m=mode(sel);if(!S)return;$("acts").hidden=!!S.rest;$("rstw").hidden=!!S.rest;
$("safe1").textContent=S.safe;document.querySelector(".safe .stop").hidden=!!S.tbc;$("panel").classList.toggle("ro",m=="future");
var lg=!S.rest?logFor(sel,S.name):null,lab=sdl(sel);
$("dnote").textContent=(m=="future"?"Planned · "+lab:m=="past"?(S.rest?"":lg?"Logged · ":extraFor(sel)>=0?"Extra logged · ":"Not logged · ")+lab:(lg?"Logged today":"Today"))+(lg&&lg.min?" · "+lg.min+" min":S.tot>0&&!S.tbc?" · "+(S.est?"≈ ":"")+Math.round(S.tot/60)+" min":"")+(srcOf(sel)!=sel?" · moved from "+sdl(srcOf(sel)).split(" ")[0]:"");
$("fin").textContent=lg?"Update log":"Finish workout";
var o=LS.get("wo_plan",{})||{},hasBk=!!(bkOf(sel)&&SESS[bkOf(sel)]&&o[sel]!="Rest"&&sel>LEGACY_END),on=altOn(sel);$("dctl").hidden=!(hasBk||m=="today"||m=="future")||!!S.tbc;
var hasQ=!!(qkOf(sel)&&SESS[qkOf(sel)]&&o[sel]!="Rest"),qo=qOn(sel);$("qk").hidden=!hasQ;if(hasQ){$("qk").textContent=qo?"↩ Back to main: "+SESS[baseSid(sel)].name:"Quick option: "+SESS[qkOf(sel)].name;$("qk").classList.toggle("on",qo);$("dctl").hidden=false;}
$("alt").hidden=!hasBk;if(hasBk){on=on&&!qo;$("alt").textContent=on?"↩ Back to main: "+SESS[baseSid(sel)].name:"Use backup session: "+SESS[bkOf(sel)].name.replace("Backup · ","");$("alt").classList.toggle("on",on);}
if(m=="today")wake();$("swap").hidden=!(m=="today"||m=="future")||!!S.tbc;$("swap").textContent=m=="today"?"Swap today's session":"Swap this session";var hr=hasRI(S);$("ri").hidden=!hr;if(hr){var ro=riOn(sel);$("ri").textContent=ro?"↩ Back to "+(sid(sel)=="row"?"row":"Assault Runner / walk"):"Run instead (outdoor run)";$("ri").classList.toggle("on",ro);if(hr)$("dctl").hidden=false;}
// pc-v50: the rare options (backup, quick option, run instead, swap) sit behind one "Change session" button; the menu
// stays open while one of them is active so "↩ Back to main" is always in reach (wo_chg=1 keeps it open, used by the tests)
var anyOpt=["alt","qk","ri","swap"].some(function(i){return !$(i).hidden;}),act=altOn(sel)||qOn(sel)||(hr&&riOn(sel)),openM=!!(DCO[sel]||act||LS.get("wo_chg",0));
$("chg").hidden=!anyOpt||!!act||!!LS.get("wo_chg",0);$("chg").textContent=DCO[sel]?"Hide session options":"Change session";$("chg").setAttribute("aria-expanded",openM?"true":"false");$("dcm").hidden=!openM;if(!anyOpt)$("dctl").hidden=true;
renderSess();hist();}
var DCO={};
function subLog(k){var S=S_(k),lg=S&&!S.rest?logFor(k,S.name):null;return lg&&lg.sub?lg:null;}
function stripLab(k){var lg=subLog(k);return lg&&lg.act&&ACTS[lg.act]?ACTS[lg.act]:plan(k);}
function title(){var k=isOpen?sel:today,S=S_(k),sl=subLog(k);$("ttl").textContent=sl?sl.sub:S?S.name:"Pump + Cardio";var sb=$("sbt");if(sb)sb.textContent=$("ttl").textContent;$("date").textContent=pd(k).toLocaleDateString("en-GB",{weekday:"long",day:"numeric",month:"long"})+(sl?" · instead of "+(sl.plan||S.name):"")+(TABS&&!isOpen&&TAB=="today"?" · "+dayStatus(k):"");}
function monday(){var d=pd(today),off=(d.getDay()+6)%7;return addDays(today,-off+weekOff*7);}
function editable(k){return k>=today&&k>=SD&&(k<=LEGACY_END||!!baseSid(k));}
function week(){var m=monday(),h="",done={};logs().forEach(function(e){if(e&&e.date&&!(e.oc=="skipped"&&!e.sub&&!e.km&&!e.time))done[e.date]=1;});
for(var i=0;i<7;i++){var k=addDays(m,i),d=pd(k),md=mode(k),dn=d.toLocaleDateString("en-GB",{weekday:"short"});
if(md=="pre"){h+='<div class="day pre"><div class="dn">'+dn+'</div><div class="dd">'+d.getDate()+'</div><div class="pl">–</div></div>';continue;}
h+='<button class="day '+md+(k==today?" today":"")+(isOpen&&k==sel?" sel":"")+(editable(k)?" ed":"")+(srcOf(k)!=k?" moved":"")+(swA==k?" pick":"")+'" data-d="'+k+'"><div class="dn">'+dn+'</div><div class="dd">'+d.getDate()+'</div><div class="pl">'+stripLab(k)+'</div>'+(done[k]?'<span class="ok">✓</span>':"")+"</button>";}
$("week").innerHTML=h;wlist(m);$("week").classList.toggle("editing",editing);$("prev").disabled=m<=SD;swUI();$("wlab").textContent=weekOff==0?"This week":weekOff==1?"Next week":weekOff==-1?"Last week":pd(m).toLocaleDateString("en-GB",{day:"numeric",month:"short"});
var none=weekOff>=0&&[0,1,2,3,4,5,6].every(function(i){var k=addDays(m,i);return sid(k)=="tbc";});$("hint").classList.toggle("np",!!none);if(TABS){$("wlab").textContent=wrange(m);var eh=$("ehint");if(eh)eh.hidden=!editing;}$("hint").textContent=none?"Nothing planned for this week yet. Health & Fitness adds the week file; you can still log any activity on a day.":"Tap a day to see its workout";}
function wrange(m){var A0=pd(m),B0=pd(addDays(m,6)),mo=function(d){return d.toLocaleDateString("en-GB",{month:"short"});};return A0.getDate()+(mo(A0)!=mo(B0)?" "+mo(A0):"")+" to "+B0.getDate()+" "+mo(B0);}
function wlist(m){var el=$("wlist");if(!el||!TABS)return;var h="",dots="",none=weekOff>=0&&[0,1,2,3,4,5,6].every(function(i){return sid(addDays(m,i))=="tbc";});
 for(var i=0;i<7;i++){var k=addDays(m,i),md=mode(k),d=pd(k),dl=d.toLocaleDateString("en-GB",{weekday:"short"});
  if(md=="pre"){dots+='<span class="wd1 rest"><i></i><b>'+dl.charAt(0)+'</b></span>';continue;}
  var S=S_(k),lg=S&&!S.rest?logFor(k,S.name):null,sl=lg&&lg.sub?lg:null,sk=lg&&lg.oc=="skipped"&&!lg.sub,xi=extraFor(k),planned=!!(S&&!S.rest&&!S.tbc);
  var st=lg?(sk?"Skipped":"✓ Done"):xi>=0?"✓ Extra":k==today?"Today":md=="past"&&planned?"Not logged":"",cl=lg&&!sk||xi>=0?"ok":sk?"sk":st=="Today"?"td":st?"nl":"";
  var mv=srcOf(k)!=k?" · ⇄ moved from "+sdl(srcOf(k)).split(" ")[0]:"",sm="";
  if(sl)sm='<small>'+(sl.min?sl.min+' min · ':'')+'instead of '+esc(sl.plan||S.name)+'</small>';else if(lg&&!sk)sm='<small>'+(lg.min?lg.min+' min':'logged')+mv+'</small>';else if(planned&&S.tot>0)sm='<small>'+(S.est?"≈ ":"")+Math.round(S.tot/60)+' min'+mv+'</small>';else if(mv)sm='<small>'+mv.slice(3)+'</small>';
  var dc=lg&&!sk||xi>=0?"done":sk?"skip":!S||S.rest||S.tbc?"rest":k==today?"today":md=="past"?"miss":"fut";
  dots+='<span class="wd1 '+dc+'"><i></i><b>'+dl.charAt(0)+'</b></span>';
  h+='<button type="button" class="wrow'+(k==today?" today":"")+(S&&S.rest?" rest":"")+'" data-d="'+k+'"><span class="wd">'+dl+'<b>'+d.getDate()+'</b></span><span class="wn">'+esc(sl?sl.sub:S?S.name:"–")+sm+'</span>'+(st?'<span class="ws '+cl+'">'+st+'</span>':'')+'</button>';}
 h='<div class="wdots" aria-hidden="true">'+dots+'</div>'+(none?'<div class="wnp"><b>Nothing planned for this week yet.</b> Ask Health &amp; Fitness for the week file, then Settings on the Today screen, Import week. You can still log any activity: tap a day.</div>':'')+h+'<button type="button" class="wedit" id="ed2">Edit this week\'s plan</button>';
 if(el.__h!==h){el.innerHTML=h;el.__h=h;}
 if(TAB=="week"&&!isOpen){var sun=addDays(m,6),w=weekOff==0?weekRows(1)[0]:null;$("ttl").textContent=weekOff==0?"This week":weekOff==1?"Next week":weekOff==-1?"Last week":"Week of "+sdl(m).replace(/^\w+ /,"");
  $("date").textContent=w?(w.plw||w.dn?w.dn+" of "+w.plw+" sessions":"Nothing planned")+(w.runs?" · "+w.runs+" run"+(w.runs==1?"":"s")+" · "+w.km+" km":""):sdl(m)+" to "+sdl(sun);}}
function nm(id){return X[id]?X[id][0]:id;}
function repParts(kg,r){var k=r.k||[],mix=k.filter(function(x,i,a){return x!="–"&&a.indexOf(x)==i;}).length>1,kk=!kg&&!mix?k.filter(function(x){return x!="–";})[0]:null;return {kg:(kg||kk)&&!mix?(kg||kk)+" kg":"",reps:(mix?r.v.map(function(v,i){return v+(k[i]&&k[i]!="–"?"@"+k[i]:"");}):r.v).join("/")+(r.u?" "+r.u:"")+(mix?" (kg)":""),note:r.n?"note: "+r.n:""};}
function repBody(kg,r){var p=repParts(kg,r);return [p.kg,p.reps,p.note].filter(Boolean).join(" · ");}
function repLine(id,kg,r){if(!(r.v||[]).length)return nm(id)+(r.n?" · note: "+r.n:"");var p=repParts(kg,r);return (r.sub?r.sub+" (instead of "+nm(id)+")":nm(id))+(p.kg?" "+p.kg:"")+" · "+p.reps+(p.note?" · "+p.note:"");}
function hist(){var NL=logs().length,h=logs().slice().reverse().map(function(e,ri){var w;if(e.wt&&Object.keys(e.wt).length)w=Object.keys(e.wt).filter(function(i){return e.wt[i];}).map(function(i){return nm(i)+": "+esc(e.wt[i])+" kg";}).join(", ");else w=Object.keys(e.w||{}).filter(function(i){return e.w[i]&&PUMPIDS[i];}).map(function(i){return nm(PUMPIDS[i])+": "+esc(e.w[i])+" kg";}).join(", ");if(e.rp&&Object.keys(e.rp).length)w=Object.keys(e.rp).map(function(i){return esc(repLine(i,e.wt&&e.wt[i],e.rp[i]));}).join("<br>");var x=[];if(e.sets!=null&&!(e.sub&&!e.sets))x.push(e.sets+"/"+(e.of||18)+" sets");var rl=runLine(e);if(rl)x.push(rl);var ol=ocLine(e);if(ol)x.push(ol);if(e.feel)x.push("felt "+esc(e.feel)+"/10");if(e.breaks)x.push(e.breaks+" walk breaks");if(e.notes)x.push(esc(e.notes));if(x.length)w=(w?w+", ":"")+x.join(" · ");var op=e.type=="extra"?[]:typeOpts(e.date),ed=op.length>1?'<label class="hed">Edit: <select data-hd="'+e.date+'" data-hn="'+esc(e.name||"")+'">'+op.map(function(o){return '<option value="'+o[0]+'"'+((e.type||"main")==o[0]?" selected":"")+">"+o[1]+"</option>";}).join("")+"</select></label>":"";var canRun=e.type=="extra"||e.km||e.time||e.effort||(e.sid?hasRun(SESS[e.sid]):false);if(canRun)ed+='<button class="link erun" data-er="'+esc(e.date)+'|'+esc(e.name||"")+'|'+esc(e.type||"")+'">Edit run</button>';ed+='<button type="button" class="link hdel" data-del="'+(NL-1-ri)+'">Delete</button>';var dl0=esc(sdl(e.date))+(e.date.slice(0,4)!=today.slice(0,4)?" "+e.date.slice(0,4):"");
if(TABS)return '<li class="hcard"><div class="hh"><b data-d="'+esc(e.date)+'">'+dl0+'</b><span class="hnm">'+esc(e.name||"Pump + Cardio")+'</span><span class="hmn">'+e.min+' min</span><button type="button" class="hmore" data-hmo="'+(NL-1-ri)+'" aria-label="Actions for '+esc(e.name||"this entry")+'">'+DOTS+'</button></div>'+(w?'<small>'+w+'</small>':'')+'</li>';
return '<li><b data-d="'+esc(e.date)+'">'+dl0+"</b> · "+esc(e.name||"Pump + Cardio")+" – "+e.min+" min"+(w?"<br><small>"+w+"</small>":"")+ed+"</li>";}).join("");$("hist").innerHTML=h||"<li>No workouts yet</li>";if(TABS){var hsd=$("hsd");if(hsd)hsd.hidden=!NL;}weeksList();progress();backupLine();}
function acOpen(e,i){var op=e.type=="extra"?[]:typeOpts(e.date),h="",canRun=e.type=="extra"||e.km||e.time||e.effort||(e.sid?hasRun(SESS[e.sid]):false);$("ac_t").textContent=e.name||"Entry";$("ac_d").textContent=sdl(e.date)+" · "+e.min+" min";
 if(op.length>1)h+='<div class="hs_h">Change type</div><div class="rcs">'+op.map(function(o){return '<button type="button" class="rc'+((e.type||"main")==o[0]?" on":"")+'" data-ty="'+o[0]+'" data-td="'+esc(e.date)+'" data-tn="'+esc(e.name||"")+'">'+esc(o[1])+'</button>';}).join("")+'</div>';
 if(canRun)h+='<button type="button" class="btn ghost" data-er="'+esc(e.date)+'|'+esc(e.name||"")+'|'+esc(e.type||"")+'">Edit run</button>';
 h+='<button type="button" class="btn ghost acdel" data-del="'+i+'">Delete this entry</button>';$("ac_b").innerHTML=h;$("acs").classList.add("show");}
$("hist").addEventListener("click",function(ev){var b=ev.target.closest("[data-hmo]");if(!b)return;var l=logs(),i=+b.dataset.hmo;if(l[i])acOpen(l[i],i);});
$("acs").addEventListener("click",function(e){if(e.target===this||e.target.closest(".acx")){$("acs").classList.remove("show");return;}var ty=e.target.closest("[data-ty]");if(ty){$("acs").classList.remove("show");setType(ty.dataset.td,ty.dataset.ty,ty.dataset.tn);return;}var er=e.target.closest("[data-er]");if(er){$("acs").classList.remove("show");var q=er.dataset.er.split("|");openRunEdit(q[0],q[1],q[2]);}});
// edit a saved run from history (session run entries and extra runs)
var ER=null;
function findLog(d,name,type){var l=logs();for(var i=0;i<l.length;i++){var e=l[i];if(e&&e.date==d&&(e.name||"")==name&&(e.type||"")==type)return i;}return -1;}
function openRunEdit(d,name,type){var i=findLog(d,name,type);if(i<0)return;var e=logs()[i];ER={d:d,name:name,type:type,e:""+(e.effort||""),sub:e.sub?1:0};$("er_subw").hidden=type=="extra";$("er_sl").value=e.sub||"";[].forEach.call($("er_sub").children,function(y){y.classList.toggle("on",(+y.dataset.sub?1:0)==ER.sub);});$("er_slw").hidden=!ER.sub;$("er_d").textContent=sdl(d)+" · "+name;$("er_km").value=e.km||"";$("er_t").value=tnorm(e.time||"");$("er_f").value=e.feel||"";$("er_n").value=e.notes||"";[].forEach.call($("er_e").children,function(y){y.classList.toggle("on",y.dataset.e==ER.e);});$("ers").classList.add("show");}
$("er_t").addEventListener("change",function(){this.value=tnorm(this.value);});
$("er_sub").addEventListener("click",function(ev){var x=ev.target.closest("[data-sub]");if(!x||!ER)return;ER.sub=+x.dataset.sub?1:0;[].forEach.call(this.children,function(y){y.classList.toggle("on",(+y.dataset.sub?1:0)==ER.sub);});$("er_slw").hidden=!ER.sub;});
$("er_e").addEventListener("click",function(ev){var x=ev.target.closest("[data-e]");if(!x||!ER)return;ER.e=ER.e==x.dataset.e?"":x.dataset.e;[].forEach.call(this.children,function(y){y.classList.toggle("on",y.dataset.e==ER.e);});});
$("er_ok").onclick=function(){if(!ER)return;var l=logs(),i=findLog(ER.d,ER.name,ER.type);if(i<0){ER=null;$("ers").classList.remove("show");return;}var e=l[i];e.km=$("er_km").value;e.time=tnorm($("er_t").value);e.effort=ER.e;e.feel=$("er_f").value;e.notes=$("er_n").value;if(e.type!="extra"){if(ER.sub){e.sub=($("er_sl").value||"").trim()||"a different run";if(!e.plan){var S9=S_(ER.d);e.plan=S9?planOf(S9):"";}}else{if(e.sub&&e.oc=="modified"){e.oc="planned";var s9=P(ER.d);s9.oc="planned";LS.set("wo_"+ER.d,s9);}delete e.sub;delete e.plan;}}if(e.type=="extra")e.min=tmin(e.time)||e.min||0;l[i]=e;LS.set("wo_log",l);
 var r=R(ER.d);r.d=e.km;r.t=e.time;r.e=e.effort;r.f=e.feel;r.n=e.notes;if(e.type!="extra"){r.sub=e.sub?1:0;r.sl=e.sub||"";}LS.set("wo_run_"+ER.d,r);ER=null;$("ers").classList.remove("show");all();hist();};
$("ers").addEventListener("click",function(e){if(e.target===this||e.target.closest(".erx")){ER=null;$("ers").classList.remove("show");}});
$("hist").addEventListener("click",function(ev){var x=ev.target.closest("[data-er]");if(!x)return;var a=x.dataset.er.split("|");openRunEdit(a[0],a[1],a[2]);});
// export: readable history + the raw log, shared from the phone only when James taps Export
function monOf(d){var x=pd(d),off=(x.getDay()+6)%7;return addDays(d,-off);}
function exportSummary(l){var out=["SUMMARY"],last={},wk={},subs=[],ocs={modified:[],"cut short":[],skipped:[]};
 l.forEach(function(e){if(!e||!e.date)return;Object.keys(e.rp||{}).forEach(function(x){last[x]={d:e.date,w:e.wt&&e.wt[x],r:e.rp[x]};});
  if(e.km||e.time){var m=monOf(e.date);wk[m]=wk[m]||{n:0,km:0,min:0};wk[m].n++;wk[m].km+=parseFloat(e.km)||0;wk[m].min+=tmin(e.time||"");}
  if(e.sub)subs.push(e.date+": "+e.sub+" instead of "+(e.plan||"the plan"));if(e.oc&&ocs[e.oc]&&!(e.sub&&e.oc=="modified"))ocs[e.oc].push(e.date);});
 var lk=Object.keys(last);if(lk.length){out.push("Last weights and reps:");lk.sort().forEach(function(x){out.push("  "+repLine(x,last[x].w,last[x].r)+" ("+last[x].d+")");});}
 var wks=Object.keys(wk).sort();if(wks.length){out.push("Runs by week:");wks.forEach(function(m){var q=wk[m];out.push("  w/c "+m+": "+q.n+" run"+(q.n==1?"":"s")+" · "+(Math.round(q.km*100)/100)+" km"+(q.min?" · "+q.min+" min":""));});}
 var dm=LS.get("wo_daymap",{})||{},sw=Object.keys(dm).filter(function(k){return typeof dm[k]=="string"&&dm[k]!=k;}).sort();if(sw.length)out.push("Swapped days: "+sw.map(function(k){var S=SESS[baseSid(k)];return sdl(k)+" ran "+sdl(dm[k])+"'s session"+(S?" ("+S.name+")":"");}).join("; "));
 if(subs.length)out.push("Different runs: "+subs.join("; "));
 var oo=Object.keys(ocs).filter(function(k){return ocs[k].length;});if(oo.length)out.push("Outcomes: "+oo.map(function(k){return k+" "+ocs[k].join(", ");}).join(" · "));
 var fl=l.filter(function(e){return e&&+e.feel>0&&e.date>=addDays(today,-28);});if(fl.length)out.push("Feel (last 4 weeks): average "+(Math.round(fl.reduce(function(t,e){return t+ +e.feel;},0)/fl.length*10)/10)+"/10 over "+fl.length+" session"+(fl.length==1?"":"s"));
 var logged={};l.forEach(function(e){if(e&&e.date)logged[e.date]=1;});var from=addDays(monOf(today),-14),miss=Object.keys(PROG).filter(function(d){var S=SESS[baseSid(d)];return d<today&&d>=from&&d>LEGACY_END&&S&&!S.rest&&!logged[d];}).sort();
 if(miss.length)out.push("Planned but not logged (last 3 weeks): "+miss.map(function(d){return sdl(d)+" ("+SESS[baseSid(d)].name+")";}).join("; "));
 var nxt=addDays(monOf(today),7),hasNext=Object.keys(PROG).some(function(d){return d>=nxt&&d<addDays(nxt,7);});out.push("Next week (w/c "+sdl(nxt)+"): "+(hasNext?"planned":"not planned yet"));
 out.push("");return out;}
function rxOfLog(e,x){var S=e.sid&&SESS[e.sid];if(!S)return "";var r="";S.blocks.forEach(function(b){if(b.k=="ex")b.items.forEach(function(it){if(it.x==x&&!r)r=b.n+" × "+it.rp+(it.ru?" "+it.ru:"")+(it.side?" each side":"");});});return r;}
function exportText(){var l=logs(),out=["Pump + Cardio training history · exported "+sdl(today)+" "+pd(today).getFullYear(),""].concat(exportSummary(l));l.slice().reverse().forEach(function(e){var bits=[e.date+" · "+(e.name||"Pump + Cardio")+(e.type?" ("+e.type+")":"")];if(e.min)bits.push(e.min+" min");if(e.sets!=null&&!(e.sub&&!e.sets))bits.push(e.sets+"/"+(e.of||18)+" sets");var rl=runLine(e).replace(/<[^>]*>/g,"");if(rl)bits.push(rl);var ol=ocLine(e).replace(/<[^>]*>/g,"");if(ol)bits.push(ol);if(e.feel)bits.push("felt "+e.feel+"/10");if(e.breaks)bits.push(e.breaks+" walk breaks");if(e.ri)bits.push("run instead");out.push(bits.join(" · "));
 if(e.bk&&e.bk.n)out.push("  blocks: "+(e.bk.d.length==e.bk.n?"all "+e.bk.n+" done":e.bk.d.length?e.bk.d.join(", ")+" ("+e.bk.d.length+" of "+e.bk.n+")":"none of "+e.bk.n+" done"));
 if(e.rp)Object.keys(e.rp).forEach(function(i){var pl=rxOfLog(e,i);var rr=e.rp[i];out.push("  "+(pl&&(rr.v||[]).length?nm(i)+": planned "+pl+" → "+(rr.sub?"did "+rr.sub+" · ":"")+repBody(e.wt&&e.wt[i],rr):repLine(i,e.wt&&e.wt[i],rr)));});else if(e.wt)Object.keys(e.wt).forEach(function(i){if(e.wt[i])out.push("  "+nm(i)+" "+e.wt[i]+" kg");});
 if(e.skx&&e.skx.length)out.push("  skipped: "+e.skx.map(nm).join(", "));
 if(e.sc)Object.keys(e.sc).forEach(function(i){var q=e.sc[i];out.push("  "+i+": "+(q.r||0)+" rounds"+(q.kg?" · "+q.kg+" kg":"")+(q.e?" · "+q.e:""));});if(e.notes)out.push("  notes: "+e.notes);});
 out.push("","--- JSON (wo_log) ---",JSON.stringify(l));return out.join("\n");}
function backupLine(){var el=$("bkn");if(!el)return;var n=logs().length,last=LS.get("wo_lastexport",null),days=last?Math.round((pd(today)-pd(last))/86400000):null,due=n>=5&&(last==null||days>30);el.hidden=!n;el.classList.toggle("due",!!due);el.innerHTML=(last?"Last backup "+esc(sdl(last))+(days>1?" · "+days+" days ago":""):"No backup yet")+(due?" · your history only lives on this phone":"")+' <button type="button" class="link" id="bknow">'+(TABS?"Export history":"Back up now")+'</button>';}
function doExport(){LS.set("wo_lastexport",today);backupLine();var t=exportText(),done=function(){};if(navigator.share){navigator.share({title:"Pump + Cardio history",text:t}).catch(function(){showExport(t);});}else showExport(t);}
function showExport(t){$("ex_t").value=t;$("exs").classList.add("show");}
$("exp").onclick=doExport;$("ex_copy").onclick=function(){var t=$("ex_t").value;if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(function(){$("ex_copy").textContent="Copied";});else{$("ex_t").select();try{document.execCommand("copy");$("ex_copy").textContent="Copied";}catch(e){}}};
$("exs").addEventListener("click",function(e){if(e.target===this||e.target.closest(".exx"))$("exs").classList.remove("show");});
function typeOpts(d){if(d<=LEGACY_END)return [];var b=baseSid(d);if(!b||!SESS[b])return [];var o=[["main","Main"]];if(bkOf(d)&&SESS[bkOf(d)])o.push(["backup","Backup"]);if(hasRI(SESS[b]))o.push(["run","Run instead"]);if(qkOf(d)&&SESS[qkOf(d)])o.push(["quick",SESS[qkOf(d)].name]);return o;}
function setType(d,t,oldName){setAlt(d,t=="backup");setRI(d,t=="run");setQ(d,t=="quick");var l=logs(),S=S_(d);for(var i=0;i<l.length;i++){var e=l[i];if(e.date==d&&(e.name||"")==oldName){e.type=t;e.sid=sid(d);e.name=S.name;delete e.custom;if(t=="run")e.ri=1;else delete e.ri;}}LS.set("wo_log",l);all();hist();}
function review(){var el=$("wrev");if(!el)return;var now=new Date(),mon=monOf(today),show=now.getDay()==0&&now.getHours()>=15&&LS.get("wo_rev","")!=mon&&weekOff==0&&!isOpen;el.hidden=!show;if(!show){el.innerHTML="";return;}
 var w=weekRows(1)[0],l=logs(),logged={},miss=[],sk=[];l.forEach(function(e){if(e&&e.date>=mon&&e.date<=today){if(e.oc=="skipped"&&!e.sub)sk.push(e.date);else logged[e.date]=1;}});
 for(var i=0;i<7;i++){var k=addDays(mon,i),S=k<=today&&mode(k)!="pre"?SESS[baseSid(k)]:null;if(S&&!S.rest&&!logged[k]&&sk.indexOf(k)<0)miss.push(sdl(k).split(" ")[0]+" "+S.name);}
 var nxt=addDays(mon,7),hasNext=Object.keys(PROG).some(function(d){return d>=nxt&&d<addDays(nxt,7);});
 el.innerHTML='<div class="tql">Your week</div><div class="wkbig"><div><b>'+w.dn+'<small>/'+w.pl+'</small></b><span>sessions</span></div><div><b>'+w.runs+'</b><span>run'+(w.runs==1?'':'s')+'</span></div><div><b>'+w.km+'<small> km</small></b><span>distance</span></div><div><b>'+w.min+'<small> min</small></b><span>running</span></div></div>'+(miss.length?'<div class="prow">Not logged: '+esc(miss.join(" · "))+'</div>':'')+(sk.length?'<div class="prow">Skipped: '+esc(sk.map(function(d){return sdl(d).split(" ")[0];}).join(", "))+'</div>':'')+'<div class="prow">Next week: '+(hasNext?"planned":"not planned yet")+'</div><div class="nagb"><button type="button" class="btn" id="rev_go">Send this week to Grok</button><button type="button" class="swb" id="rev_x">Done</button></div>';}
// pc-v58: three screens. Visibility is pure CSS on body classes (tabs, t-today / t-week / t-prog, open), so the DOM the
// audit reads is unchanged. wo_flat=1 keeps the old one page layout (every older test suite seeds it).
var TABS=!LS.get("wo_flat",0),TAB="today";
function layout(){var c=document.body.classList;c.toggle("tabs",TABS);if(!TABS)return;["today","week","prog"].forEach(function(t){c.toggle("t-"+t,TAB==t);});c.toggle("open",isOpen);c.toggle("ed",!!editing);
 [].forEach.call(document.querySelectorAll("#tabbar [data-tab]"),function(b){var on=b.dataset.tab==TAB;b.classList.toggle("on",on);b.setAttribute("aria-current",on?"page":"false");});
 var cb=$("close");if(cb.textContent!="Back")cb.innerHTML=ic(IP.back,18)+"Back";}
function setTab(t){if(isOpen)closeP();TAB=t;if(t!="week"&&weekOff){weekOff=0;}if(t=="prog"){var d=$("prg");if(d)d.open=true;var d2=$("hsd");if(d2)d2.open=true;}all();window.scrollTo(0,0);}
function tagOf(b){var h=String(b.h||""),n=String(b.name||"");if(b.k=="ex")return h.replace(/^[A-Z] · /,"").replace(/\s*·.*$/,"")||"Strength";if(/warm/i.test(h))return "Warm-up";if(/cool/i.test(h))return "Cool-down";if(/every|carry/i.test(h+" "+n))return /carry/i.test(n)?"Carry":"Every";if(/emom/i.test(h))return "EMOM";if(/flow|mobility|stretch|reset/i.test(h+" "+n))return "Flow";if(/interval/i.test(h))return "Intervals";if(/steady|zone|easy|run|walk/i.test(h))return "Run";return h.split(" ")[0]||"Block";}
function hprev(S,s){var rows=[],up=false;S.blocks.forEach(function(b){b=VB(b);if(b.k!="timer"&&b.k!="ex")return;var dn=blockDone(b,s),nmb,meta;
  if(b.k=="timer"){nmb=b.name||b.h;var tt=0;(b.segs||[]).forEach(function(g){tt+=g[1];});meta=tt?fmt(tt):"";}else{nmb=b.items.map(function(it){return nm(it.x);}).join(" + ");meta=bn(b,s)+" rounds";}
  var first=!dn&&!up;if(first)up=true;
  rows.push('<div class="pr'+(dn?' dn':'')+(first?' up':'')+'"><span class="pl"><span class="tg">'+esc(tagOf(b))+'</span>'+(first&&s.start?'<em class="un">Up next</em>':'')+'<span class="pn">'+esc(nmb)+'</span></span><small>'+(dn?'✓':esc(meta))+'</small></div>');});
 return rows.length?'<button type="button" class="hprev" data-hm="peek" aria-label="Look at the session">'+rows.join("")+'</button>':"";}
function nextPlanned(){for(var i=1;i<=14;i++){var k=addDays(today,i),S=mode(k)=="pre"?null:S_(k);if(S&&!S.rest&&!S.tbc)return {k:k,S:S,i:i};}return null;}
function nextLine(){var n=nextPlanned();if(!n)return "";return (n.i==1?"Tomorrow":pd(n.k).toLocaleDateString("en-GB",{weekday:"long"}))+" · "+n.S.name+(n.S.tot>0?" · "+(n.S.est?"≈ ":"")+Math.round(n.S.tot/60)+" min":"");}
function tomorrowLine(){var k=addDays(today,1),S=mode(k)=="pre"?null:S_(k);if(!S||S.tbc)return "Tomorrow: nothing planned yet";if(S.rest)return "Tomorrow: rest";return "Tomorrow: "+S.name+(S.tot>0?" · "+(S.est?"≈ ":"")+Math.round(S.tot/60)+" min":"");}
function hsum(lg){var d=[];if(lg.sets!=null&&!(lg.sub&&!lg.sets))d.push(lg.sets+" of "+(lg.of||lg.sets)+" sets");if(lg.km)d.push(esc(lg.km)+" km");if(lg.time)d.push(esc(lg.time));if(lg.effort)d.push(esc(lg.effort));if(+lg.feel>0)d.push("felt "+esc(lg.feel)+"/10");
 return '<div class="hsum"><div class="hs1">'+esc(lg.sub||lg.name||"Session")+'</div>'+(lg.sub&&lg.plan?'<div class="hs0">instead of '+esc(lg.plan)+'</div>':'')+(d.length?'<div class="hs2">'+d.join(" · ")+'</div>':'')+'<div class="hs3">'+esc(tomorrowLine())+'</div></div>';}
function dayStatus(k){var S=S_(k);if(!S)return "";if(S.tbc)return "No plan yet";if(S.rest)return "Rest day";var s=P(k),r=R(k),lg=logFor(k,S.name),st=+LS.get("wo_runstart_"+k,0)||s.start||0,en=s.end&&s.end>=st?s.end:0;
 if(lg)return lg.oc=="skipped"&&!lg.sub?"Skipped":"Logged";if(r.sub||s.oc=="skipped")return "Not saved yet";if(st)return en?"Paused":"In progress";return "Not started";}
function home(){var el=$("home");if(!el||!TABS)return;var S=mode(today)=="pre"?null:S_(today),h="";
 if(S){var s=P(today),r=R(today),lg=!S.rest?logFor(today,S.name):null,st=+LS.get("wo_runstart_"+today,0)||s.start||0,en=s.end&&s.end>=st?s.end:0,xi=extraFor(today),sc=S.rest?null:score(today);
  var lk=function(k,txt){return '<button type="button" class="link hlink" data-hm="'+k+'">'+txt+'</button>';},lks=[],nl=nextLine();
  if(S.tbc)h+='<div class="hline">Nothing planned for this week yet.</div><div class="hnote">Ask Health &amp; Fitness for the week file, then Settings, Import week. You can still log anything you do.</div><button type="button" class="btn ghost" data-hm="open">Log an activity</button>';
  else if(S.rest)h+='<div class="hline">Rest day'+(S.blocks.some(function(b){return b.k=="timer";})?" · optional mobility inside":"")+(xi>=0?" · activity logged ✓":"")+'</div><div class="hnote">Nothing to log today. Rest is part of the plan.</div>'+(nl?'<div class="hnext"><span>Next</span>'+esc(nl)+'</div>':'')+'<button type="button" class="btn ghost" data-hm="open">Open today</button>';
  else if(lg&&lg.oc=="skipped"&&!lg.sub)h+='<div class="hline">Skipped today</div><div class="hnext"><span>Next</span>'+esc(tomorrowLine().replace(/^Tomorrow: /,"Tomorrow · "))+'</div><button type="button" class="btn ghost" data-hm="open">View today</button>';
  else if(lg)h+='<div class="hline good">✓ Logged'+(lg.min?" · "+lg.min+" min":"")+'</div>'+hsum(lg)+'<button type="button" class="btn ghost" data-hm="open">View today</button>';
  else if(r.sub||s.oc=="skipped"){h+='<div class="hline">Marked as '+(r.sub?"something else":"skipped")+' · not saved yet</div><button type="button" class="btn" data-hm="open">Finish logging</button>';lks.push(lk("plan","Back to the plan"));}
  else if(st){h+='<div class="hline">'+(en?"Paused at "+hms(en-st):"In progress · started "+esc(new Date(st).toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit"})))+' · '+sc.d+' of '+sc.t+' parts done</div>'+hprev(S,s)+'<button type="button" class="btn" data-hm="'+(en?"resume":"open")+'">Continue</button>';lks.push(lk("else","I did something else"));}
  else{h+='<div class="hline">'+(S.tot>0?(S.est?"≈ ":"")+Math.round(S.tot/60)+" min · ":"")+S.blocks.filter(function(b){return b.k=="timer"||b.k=="ex";}).length+' blocks'+(xi>=0?" · "+esc(logs()[xi].name||"activity")+" logged ✓":"")+'</div>'+hprev(S,s)+'<button type="button" class="btn" data-hm="start">Start session</button>';
   if(hasRun(S))lks.push(lk("run","Log my run"));lks.push(lk("else","I did something else"));if(xi>=0)lks.push(lk("conv","It replaced this session"));}
  if(lks.length)h+='<div class="hlinks">'+lks.join("")+'</div>';}
 var w=weekRows(1)[0];h+='<button type="button" class="hweek" data-hm="week">This week · '+(w.plw||w.dn?w.dn+' of '+w.plw+' sessions':'nothing planned')+(w.runs?' · '+w.km+' km':'')+' ›</button>';
 if(el.__h!==h){el.innerHTML=h;el.__h=h;}}
function all(){layout();title();week();if(isOpen)renderPanel();sclk();prog();hist();if(!RT)rbtnVis();nag();review();home();}
var WSY=0;
function openDay(k){EDK=null;if(mode(k)=="pre")return;if(isOpen&&k==sel){closeP();return;}if(TABS&&TAB=="week"&&!isOpen)WSY=window.scrollY;sel=k;isOpen=true;renderPanel();$("panel").classList.add("open");$("hint").classList.add("hid");all();if(TABS)place(k);}
var SCY={};
function place(k,to){var y=SCY[k],el=null;if(to=="actual")[].forEach.call(document.querySelectorAll("#sess h2"),function(x){if(!el&&x.textContent=="Actual")el=x;});else if(to)el=document.querySelector(to);if(el){el.scrollIntoView({block:"start"});window.scrollBy(0,-70);return;}if(y>0){window.scrollTo(0,y);return;}
 var u=k==today?document.querySelector("#sess .upnext"):null;if(u){u.scrollIntoView({block:"start"});window.scrollBy(0,-64);}else window.scrollTo(0,0);}
function closeP(){if(TABS&&isOpen){SCY[sel]=window.scrollY;delete TQO[sel];var r0=R(sel),s0=P(sel);
  if(r0.sub&&!subLog(sel)&&!(r0.d||r0.t||r0.n||r0.sl||r0.e||r0.f)){r0.sub=0;if(s0.oc=="modified")s0.oc="";LS.set("wo_run_"+sel,r0);LS.set("wo_"+sel,s0);}}
 isOpen=false;setTimeout(relWake,0);$("panel").classList.remove("open");$("hint").classList.remove("hid");all();if(TABS)window.scrollTo(0,TAB=="week"?WSY:0);}
// ---- swap two day slots in the current week (Edit plan → Swap days → tap day A, then day B)
var swapping=false,swA=null;
function curWeekDays(){var d=pd(today),m=addDays(today,-((d.getDay()+6)%7)),a=[];for(var i=0;i<7;i++)a.push(addDays(m,i));return a;}
function started(k){var s=LS.get("wo_"+k,null);return !!(s&&typeof s=="object"&&((s.t&&Object.keys(s.t).some(function(x){return s.t[x];}))||(s.s&&Object.keys(s.s).some(function(x){return s.s[x];}))));}
function swapBlock(k){if(curWeekDays().indexOf(k)<0)return "Only days in this week can be swapped.";if(k<SD||k<=LEGACY_END||!baseSid(k))return "That day has no session to move.";if(logs().some(function(e){return e&&e.date==k;}))return sdl(k).split(" ")[0]+" is already logged, so it stays put.";if(started(k))return sdl(k).split(" ")[0]+" already has sets ticked, so it stays put.";return "";}
function swapDays(a,b){var m=LS.get("wo_daymap",{});if(!m||typeof m!="object")m={};var sa=srcOf(a),sb=srcOf(b);m[a]=sb;m[b]=sa;[a,b].forEach(function(k){if(m[k]==k)delete m[k];});LS.set("wo_daymap",m);}
function weekSwapped(){return curWeekDays().some(function(k){return srcOf(k)!=k;});}
function resetWeek(){var m=LS.get("wo_daymap",{});if(!m||typeof m!="object")m={};curWeekDays().forEach(function(k){delete m[k];});LS.set("wo_daymap",m);}
function swUI(){var on=editing&&weekOff==0;$("swr").hidden=!on;if(!on){swapping=false;swA=null;}$("swd").textContent=swapping?"Cancel swap":"Swap days";$("swd").classList.toggle("on",swapping);$("swreset").hidden=!(on&&weekSwapped());$("swh").textContent=swapping?(swA?"Now tap the day to swap with "+sdl(swA).split(" ")[0]+".":"Tap the first day."):"";}
function pickSwap(k){var why=swapBlock(k);if(why){$("swh").textContent=why;return;}if(!swA){swA=k;week();return;}if(k==swA){swA=null;week();return;}var a=swA;swapDays(a,k);swA=null;swapping=false;all();$("swh").textContent="Swapped "+sdl(a).split(" ")[0]+" and "+sdl(k).split(" ")[0]+". Swap them again to undo.";}
function cyc(k){if(!editable(k))return;var o=LS.get("wo_plan",{})||{};if(k<=LEGACY_END){var n={Pump:"Run",Run:"Rest",Rest:"Pump"};o[k]=n[plan(k)];}else if(o[k]=="Rest")delete o[k];else o[k]="Rest";LS.set("wo_plan",o);all();}
// events
var lpT=null,lp=false,sx=0,sy=0,moved=false;
$("week").addEventListener("pointerdown",function(e){var b=e.target.closest("button.day");sx=e.clientX;sy=e.clientY;moved=false;lp=false;clearTimeout(lpT);if(!b)return;var k=b.dataset.d;if(editable(k))lpT=setTimeout(function(){lp=true;cyc(k);},550);});
$("week").addEventListener("pointermove",function(e){if(Math.abs(e.clientX-sx)>10||Math.abs(e.clientY-sy)>10){moved=true;clearTimeout(lpT);}});
$("week").addEventListener("pointerup",function(e){clearTimeout(lpT);var dx=e.clientX-sx;if(moved&&Math.abs(dx)>50&&Math.abs(dx)>Math.abs(e.clientY-sy)){if(dx<0)weekOff++;else if(!$("prev").disabled)weekOff--;week();}});
var WSW=false,wsx=0,wsy=0;
$("wlist").addEventListener("pointerdown",function(e){wsx=e.clientX;wsy=e.clientY;WSW=false;});
$("wlist").addEventListener("pointerup",function(e){var dx=e.clientX-wsx;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(e.clientY-wsy)*1.5){WSW=true;setTimeout(function(){WSW=false;},400);if(dx<0)weekOff++;else if(!$("prev").disabled)weekOff--;week();}});
$("week").addEventListener("pointercancel",function(){clearTimeout(lpT);});
$("week").addEventListener("contextmenu",function(e){e.preventDefault();});
$("week").addEventListener("click",function(e){var b=e.target.closest("button.day");if(!b||lp||moved){lp=false;return;}var k=b.dataset.d;if(editing){if(swapping){pickSwap(k);return;}cyc(k);return;}openDay(k);});
$("prev").onclick=function(){if(!this.disabled){weekOff--;week();}};$("next").onclick=function(){weekOff++;week();};
$("ed").onclick=function(){editing=!editing;this.textContent=editing?"Done":"Edit plan";week();layout();};
$("swd").onclick=function(){swapping=!swapping;swA=null;week();};
$("swreset").onclick=function(){resetWeek();swapping=false;swA=null;all();$("swh").textContent="Week order reset.";};
$("close").onclick=closeP;$("stop").onclick=function(){if(TABS)$("stq").hidden=false;else stopT();};$("stqy").onclick=stopT;$("stqn").onclick=function(){$("stq").hidden=true;};$("sct").onclick=function(){if(!T)return;var d=T.date,s=P(d);if(s.end)return;LAP=LAP&&LAP.d==d?null:{d:d,t:Date.now()};sct();};$("tpause").onclick=tPause;$("tback").onclick=tBack;$("tnext").onclick=tNext;
$("tqy").onclick=function(){doneT();};
$("tlock").onclick=function(){var on=$("bar").classList.toggle("locked");lockLab(on);};
$("ctop").onclick=function(){if(!T)return;var pk=$("peek");if(pk.hidden){var a=T.list||T.segs.filter(isWork).map(segLab).filter(function(x,i,arr){return arr.indexOf(x)==i;});pk.innerHTML=a.slice(0,8).map(esc).join("<br>");}pk.hidden=!pk.hidden;};
$("tround").onclick=function(){if(!T)return;T.rounds=(T.rounds||0)+1;LS.set("wo_timer",T);$("trn").textContent=T.rounds;};$("tqn").onclick=function(){doneT(true);};
$("rskip").onclick=stopRest;$("rm15").onclick=function(){restAdj(-15);};$("rp15").onclick=function(){restAdj(15);};
$("rbtn").onclick=function(){startRest(+LS.get("wo_restlast",90)||90,"Rest");};
$("snd").onclick=function(){unlock();};
(function(){var c=$("cueon");c.checked=cueOn();c.onchange=function(){LS.set("wo_cue",c.checked?1:0);if(c.checked)cue("change");};})();
(function(){var c=$("loud");c.checked=loud();c.onchange=function(){LS.set("wo_loud",c.checked?1:0);audioMode();keepAudio(!!(T||RT));};audioMode();})();
(function(){var c=$("autorest");c.checked=autoRest();c.onchange=function(){LS.set("wo_autorest",c.checked);if(isOpen)renderSess();};})();
var SX=$("sess");
SX.addEventListener("click",function(e){var xh=e.target.closest("[data-xh]");if(xh){xhist(xh.dataset.xh);return;}var hb=e.target.closest("[data-h]");if(hb){howto(hb.dataset.h);return;}
var mo=e.target.closest("[data-mo]");if(mo){MO[mo.dataset.mo]=!MO[mo.dataset.mo];renderSess();return;}
var smb=e.target.closest("[data-sm]");if(smb){SM[smb.dataset.sm]=!SM[smb.dataset.sm];renderSess();return;}if(mode(sel)=="future")return;var t=e.target.closest("[data-t]");if(t){startT(t.dataset.t);return;}
if(e.target.closest("#brkb")){var r=R(sel);r.b++;LS.set("wo_run_"+sel,r);$("brk").textContent=r.b;return;}
var skb=e.target.closest("[data-sk]");if(skb){var s8=P(sel);s8.sk=s8.sk||{};if(s8.sk[skb.dataset.sk])delete s8.sk[skb.dataset.sk];else s8.sk[skb.dataset.sk]=1;LS.set("wo_"+sel,s8);renderSess();prog();return;}
var xsb=e.target.closest("[data-xs]");if(xsb){var s0=P(sel);s0.xs=s0.xs||{};var cur0=(+s0.xs[xsb.dataset.b])||0,nx=Math.max(0,cur0+ +xsb.dataset.xs);if(nx)s0.xs[xsb.dataset.b]=nx;else delete s0.xs[xsb.dataset.b];LS.set("wo_"+sel,s0);renderSess();prog();return;}
var uf=e.target.closest("[data-unf]");if(uf){UNF[sel+"|"+uf.dataset.unf]=1;renderSess();return;}
var sf=e.target.closest("[data-sf]");if(sf){var pr=sf.dataset.sf.split("|");fillKg(pr[0],+pr[1]);return;}
var atb=e.target.closest("#r_at [data-at]");if(atb){var r8=R(sel);r8.at=atb.dataset.at;LS.set("wo_run_"+sel,r8);renderSess();return;}
var sb=e.target.closest("#r_sub [data-sub]");if(sb){var r3=R(sel);r3.sub=+sb.dataset.sub?1:0;LS.set("wo_run_"+sel,r3);renderSess();var sl=$("r_sl");if(sl&&r3.sub)sl.focus();return;}
if(e.target.closest("#moredet")){DET[sel]=!DET[sel];renderSess();return;}
if(e.target.closest("#showp")){SHOWP[sel]=!SHOWP[sel];renderSess();return;}
if(e.target.closest("#fin2")){$("fin").click();return;}
var oc=e.target.closest("#oc [data-oc]");if(oc){var s4=P(sel),r4=R(sel),w4=oc.dataset.oc,was=(r4.sub?(hasRun(S_(sel))?"different run":"something else"):(s4.oc||""));
 if(w4=="different run"||w4=="something else"){r4.sub=was==w4?0:1;s4.oc=r4.sub?"modified":"";}else{r4.sub=0;s4.oc=was==w4?"":w4;}LS.set("wo_"+sel,s4);LS.set("wo_run_"+sel,r4);renderSess();return;}
var ec=e.target.closest("#r_e [data-e]");if(ec){var r2=R(sel);r2.e=r2.e==ec.dataset.e?"":ec.dataset.e;LS.set("wo_run_"+sel,r2);[].forEach.call(ec.parentNode.children,function(y){y.classList.toggle("on",y.dataset.e==r2.e);});return;}
if(e.target.closest("#addrun")){RUNOPEN[sel]=true;renderSess();var f=$("r_d");if(f)f.focus();return;}
if(e.target.closest("#runsave")){saveExtra(sel);RUNOPEN[sel]=true;all();hist();$("swh")&&0;var xr=$("runx");if(xr)flash("runx");return;}
if(e.target.closest("#runclose")){RUNOPEN[sel]=false;renderSess();return;}
var st=e.target.closest("[data-st]");if(st&&EDK){var S0=S_(sel),s0=P(sel),it0=itemByGi(S0,+EDK.split("_")[0]),c=st.dataset.st;s0.rp=s0.rp||{};
 if(c=="u"){s0.t[EDK]=false;delete s0.rp[EDK];EDK=null;}else if(c=="x"){EDK=null;}else{var v=repV(s0,EDK,it0)+(+c)*stepOf(it0);s0.rp[EDK]=Math.max(0,Math.min(99*stepOf(it0),v));}
 LS.set("wo_"+sel,s0);renderSess();prog();return;}
var tk=e.target.closest("[data-tk]");if(tk){var S2=S_(sel),s2=P(sel),k2=tk.dataset.tk,it3=itemByGi(S2,+k2.split("_")[0]);var lb=blockOfGi(S2,+k2.split("_")[0]);LASTB=lb?sel+"|"+(lb.tid||lb.id):null;s2.rp=s2.rp||{};s2.kg=s2.kg||{};if(!s2.start)s2.start=Date.now();
 if(!s2.t[k2]){s2.t[k2]=true;if(s2.rp[k2]==null)s2.rp[k2]=it3.rp;var kg2=kgOf(s2,k2,it3);if(kg2&&kg2.v!==""){s2.kg[k2]=kg2.v;if(dayW(it3.x,sel)==null&&!(s2.rx&&s2.rx[it3.gi]))setW(it3.x,sel,kg2.v);}LS.set("wo_"+sel,s2);maybeRest(S2,s2,k2);}else{delete s2.t[k2];if(EDK==k2)EDK=null;LS.set("wo_"+sel,s2);}
 renderSess();prog();return;}
var rpb=e.target.closest("[data-rp]");if(rpb){EDK=EDK==rpb.dataset.rp?null:rpb.dataset.rp;renderSess();return;}
var pl=e.target.closest(".pill");if(pl){var S1=S_(sel),s1=P(sel),k1=pl.dataset.k,it1=itemByGi(S1,+k1.split("_")[0]);s1.rp=s1.rp||{};if(!s1.start)s1.start=Date.now();
 if(!s1.t[k1]){s1.t[k1]=true;if(s1.rp[k1]==null)s1.rp[k1]=it1.rp;EDK=k1;maybeRest(S1,s1,k1);if(X[it1.x][3]&&dayW(it1.x,sel)==null){var lw1=lastW(it1.x,sel);if(lw1)setW(it1.x,sel,lw1.v);}}else EDK=EDK==k1?null:k1;
 LS.set("wo_"+sel,s1);renderSess();prog();return;}
var b=e.target.closest("[data-k]"),a=e.target.closest("[data-a]"),S=S_(sel),s;
if(b){s=P(sel);var k=b.dataset.k;s.t[k]=!s.t[k];if(!s.start)s.start=Date.now();LS.set("wo_"+sel,s);if(s.t[k]){maybeRest(S,s,k);var gi=+k.split("_")[0],it=itemByGi(S,gi);if(it&&X[it.x][3]&&dayW(it.x,sel)==null){var lw=lastW(it.x,sel);if(lw){setW(it.x,sel,lw.v);var ip=SX.querySelector('input[data-w="'+gi+'"]');if(ip)ip.classList.remove("pf");}}}b.classList.toggle("on",s.t[k]);b.textContent=s.t[k]?"✓":(+k.split("_")[1]+1);prog();}
if(a){var it2=itemByGi(S,+a.dataset.a),inp=document.createElement("input");inp.className="w lock";inp.type="number";inp.inputMode="decimal";inp.placeholder=X[it2.x][2];inp.dataset.w=a.dataset.a;a.replaceWith(inp);inp.focus();}});
SX.addEventListener("input",function(e){if(mode(sel)=="future")return;var el=e.target;
if(el.dataset.kw!=null){var s3=P(sel),it4=itemByGi(S_(sel),+el.dataset.kw.split("_")[0]);s3.kg=s3.kg||{};s3.kg[el.dataset.kw]=el.value;LS.set("wo_"+sel,s3);if(it4&&el.value!==""&&!(s3.rx&&s3.rx[it4.gi]))setW(it4.x,sel,el.value);el.classList.remove("pf");return;}if(el.dataset.w!=null){var it=itemByGi(S_(sel),+el.dataset.w);if(it){setW(it.x,sel,el.value);el.classList.remove("pf");}return;}
var m=/^r_([dtfn]|sl)$/.exec(el.id||"");if(m){var r=R(sel);r[m[1]]=el.value;LS.set("wo_run_"+sel,r);}
if(el.id=="s_nt"){var s5=P(sel);s5.nt=el.value;LS.set("wo_"+sel,s5);}
if(el.dataset.xn!=null){var s6=P(sel);s6.xn=s6.xn||{};if(el.value.trim())s6.xn[el.dataset.xn]=el.value;else delete s6.xn[el.dataset.xn];LS.set("wo_"+sel,s6);return;}
if(el.dataset.rx!=null){var s7=P(sel);s7.rx=s7.rx||{};if(el.value.trim())s7.rx[el.dataset.rx]=el.value.trim();else delete s7.rx[el.dataset.rx];LS.set("wo_"+sel,s7);var hd=el.closest(".mvh");if(hd){var nm0=hd.querySelector(".rxn");if(nm0)nm0.textContent=el.value.trim();}return;}});

SX.addEventListener("change",function(e){var el=e.target;if(el.dataset.rx!=null){renderSess();return;}if(el.id=="r_t"){var tn=tnorm(el.value);el.value=tn;var r7=R(sel);r7.t=tn;LS.set("wo_run_"+sel,r7);return;}if(el.dataset.kw!=null){renderSess();return;}if(el.dataset.w==null)return;var it=itemByGi(S_(sel),+el.dataset.w),last=it&&lastW(it.x,sel),c=el.closest(".card");if(!last||!c)return;var up=c.querySelector(".up"),hi=el.value!==""&&+el.value>+last.v;if(hi&&!up){var sp=document.createElement("span");sp.className="up";sp.textContent="↑";var nt=c.querySelectorAll(".note");nt[nt.length-1].append(" ",sp);}else if(!hi&&up)up.remove();});
function xhist(x){var rows=[];logs().forEach(function(e){if(!e||!e.rp||!e.rp[x])return;var r=e.rp[x];if(!(r.v||[]).length&&!r.n)return;rows.push({d:e.date,r:r,w:e.wt&&e.wt[x]});});rows.sort(function(p,q){return p.d<q.d?1:-1;});
 var best=null;rows.forEach(function(o){if(o.r.sub)return;var kg=kgOfLog({r:o.r,w:o.w}),rv=(o.r.v||[]).filter(function(v){return v!="–"&&!isNaN(+v);}).map(Number),mr=rv.length?Math.max.apply(null,rv):0;if(kg!=null&&mr&&(!best||kg>best.kg||(kg==best.kg&&mr>best.r)))best={kg:kg,r:mr,d:o.d};});
 $("xh_t").textContent=nm(x);$("xh_u").textContent=best?"Best: "+best.kg+" kg × "+best.r+" ("+sdl(best.d)+")":(rows.length?"":"Nothing logged yet.");
 $("xh_b").innerHTML=rows.map(function(o){return '<div class="prow"><b>'+esc(sdl(o.d))+'</b> · '+esc(repBody(o.w,o.r))+(o.r.sub?' <small>(as '+esc(o.r.sub)+')</small>':'')+'</div>';}).join("")||'<div class="prow">No sets logged for this exercise yet.</div>';$("xhs").classList.add("show");}
function howto(k){var h=HT[k];if(!h)return;var nm0=X[k]?X[k][0]:k;$("hs_t").textContent=nm0;$("hs_u").textContent=h.u||"";
$("hs_b").innerHTML='<ol class="hs_s">'+h.s.map(function(x,i){return '<li><span class="hn">'+(i+1)+'</span><span>'+esc(x)+'</span></li>';}).join("")+'</ol><div class="hs_h">Form tips</div><ul class="hs_c">'+h.c.map(function(x){return "<li>"+esc(x)+"</li>";}).join("")+'</ul><p class="hs_m"><b>Avoid:</b> '+esc(h.m)+'</p>'+(h.z?'<p class="hs_m hs_z"><b>Safety:</b> '+esc(h.z)+'</p>':'');
$("hs_b").scrollTop=0;$("hs_l").href=demoURL(h.q||nm0);$("hs").classList.add("show");}
var hy=null;document.addEventListener("pointerdown",function(e){if(e.target.closest(".hs_g,.hs_top"))hy=e.clientY;});document.addEventListener("pointerup",function(e){if(hy!=null&&e.clientY-hy>60)hclose();hy=null;});
function hclose(){$("hs").classList.remove("show");}
$("hs").addEventListener("click",function(e){if(e.target===this||e.target.closest("#hs_x"))hclose();});
document.addEventListener("keydown",function(e){if(e.key=="Escape")hclose();});
window.__how={HT:HT,hkey:hkey,X:X,SESS:SESS,demoURL:demoURL,dur:dur,posOf:posOf,BK:BK};
$("hist").addEventListener("change",function(ev){var x=ev.target.closest("select[data-hd]");if(!x)return;setType(x.dataset.hd,x.value,x.dataset.hn);});
$("ri").onclick=function(){if(T&&T.date==sel)stopT();setRI(sel,!riOn(sel));all();};
$("alt").onclick=function(){if(T&&T.date==sel)stopT();EDK=null;var q=qOn(sel);setQ(sel,false);setAlt(sel,q?true:!altOn(sel));all();};
$("qk").onclick=function(){if(T&&T.date==sel)stopT();EDK=null;var v=!qOn(sel);setQ(sel,v);if(v){setAlt(sel,false);setRI(sel,false);}all();};
var RS=["Shorter","Feeling rough","No running","Different kit","Something else"],swR={};
function swapBody(d){var S=S_(d),l=logs().slice(-5).reverse().map(function(e){return "- "+e.date+" "+(e.name||"Pump + Cardio")+", "+e.min+" min"+(e.feel?", felt "+e.feel+"/10":"");});
return ["Date: "+d,"Current session: "+(S?S.name:"-"),"Reasons: "+(RS.filter(function(r){return swR[r];}).join(", ")||"-"),"Note: "+($("sw_n").value.trim()||"-"),"","Recent log:"].concat(l.length?l:["- none"]).join("\n");}
function swapHref(d){return "mailto:jamesharris+workout@mail.grokbot.com?subject="+encodeURIComponent("Workout swap request "+d)+"&body="+encodeURIComponent(swapBody(d));}
function swapUpd(){$("sw_go").href=swapHref(sel);}
$("swap").onclick=function(){swR={};$("sw_n").value="";$("sw_ok").hidden=true;$("sw_form").hidden=false;$("sw_c").innerHTML=RS.map(function(r){return '<button class="rc" data-r="'+r+'">'+r+'</button>';}).join("");$("sw_d").textContent=sdl(sel)+" · "+S_(sel).name;swapUpd();$("swp").classList.add("show");};
$("sw_c").addEventListener("click",function(e){var b=e.target.closest("[data-r]");if(!b)return;var r=b.dataset.r;swR[r]=!swR[r];b.classList.toggle("on",swR[r]);swapUpd();});
$("sw_n").addEventListener("input",swapUpd);
$("sw_go").addEventListener("click",function(){swapUpd();var q=LS.get("wo_swaps",[]);if(!Array.isArray(q))q=[];q.push({date:sel,at:Date.now(),reasons:RS.filter(function(r){return swR[r];}),note:$("sw_n").value.trim()});LS.set("wo_swaps",q);setTimeout(function(){$("sw_form").hidden=true;$("sw_ok").hidden=false;},50);});
$("swp").addEventListener("click",function(e){if(e.target===this||e.target.closest(".swx"))$("swp").classList.remove("show");});
// ---- week import (pc-v39): paste → Check → Save; the page reloads so the new week builds like a built-in one
function weeksList(){var ks=Object.keys(WEEKS).sort(),h=ks.map(function(k){var w=WEEKS[k],bad=w.errors&&w.errors.length;return "<li><span>w/c "+esc(sdl(k))+(w.title?" · "+esc(w.title):"")+" · "+(w.src=="file"?"built in":"imported")+(bad?" · <b class=\"bad\">not loaded</b>":" · "+w.days+" days")+"</span>"+(w.src=="import"?'<button class="link" data-rmw="'+esc(k)+'">Remove</button>':"")+"</li>";}).join("");
 var codeWeeks={};Object.keys(PROG).forEach(function(d){var m=monOf(d);if(!WEEKS[m]&&d>LEGACY_END)codeWeeks[m]=1;});h=Object.keys(codeWeeks).sort().map(function(k){return "<li><span>w/c "+esc(sdl(k))+" · built in</span></li>";}).join("")+h;$("wks").innerHTML=h||"<li>No weeks loaded</li>";}
var IMW=null;
document.addEventListener("click",function(e){if(e.target.closest("#bknow"))doExport();});
$("topq").addEventListener("click",function(e){if(e.target.closest("[data-tqx]")){TQO[sel]=true;renderSess();return;}var c=e.target.closest("[data-toc]"),S=S_(sel);if(c&&S){var s=P(sel),r=R(sel),w=c.dataset.toc,was=r.sub?"else":s.oc=="skipped"?"skip":"plan";if(w==was)return;
  if(w=="else"){r.sub=1;s.oc="modified";}else if(w=="skip"){r.sub=0;s.oc="skipped";}else{r.sub=0;s.oc="";}LS.set("wo_"+sel,s);LS.set("wo_run_"+sel,r);renderSess();prog();if(!RT)rbtnVis();return;}
 if(e.target.closest("#xconv")&&S){var l=logs(),i=extraFor(sel);if(i<0)return;var x=l[i],r2=R(sel),s2=P(sel);UNDOPRE={log:JSON.stringify(l),d:sel,s:JSON.stringify(s2),r:JSON.stringify(r2)};r2.sub=1;r2.at=x.act||"run";r2.d=x.km||"";r2.t=x.time||"";r2.e=x.effort||"";r2.f=x.feel||"";r2.sl="";r2.n=x.notes||r2.n||"";s2.oc="modified";
  l.splice(i,1);LS.set("wo_log",l);LS.set("wo_"+sel,s2);LS.set("wo_run_"+sel,r2);RUNOPEN[sel]=false;finBusy=false;$("fin").click();}});
$("sess").addEventListener("click",function(e){if(e.target.closest("#fin_c")){$("fin").click();return;}if(e.target.closest("#rst_c"))$("rst").click();});
$("wrev").addEventListener("click",function(e){if(e.target.closest("#rev_go")){doExport();return;}if(e.target.closest("#rev_x")){LS.set("wo_rev",monOf(today));review();}});
$("sclk").addEventListener("click",function(e){var b=e.target.closest("[data-sc]");if(!b)return;var w=b.dataset.sc,s=P(sel),now=Date.now();
 if(w=="go"){s.start=now;delete s.end;LS.set("wo_"+sel,s);LS.del("wo_runstart_"+sel);unlock();wake();}
 else if(w=="lap"){LAP=LAP&&LAP.d==sel?null:{d:sel,t:now};}
 else if(w=="stop"){s.end=now;LS.set("wo_"+sel,s);LAP=null;}
 else if(w=="resume"){var st=+LS.get("wo_runstart_"+sel,0)||s.start||now,gap=now-(s.end||now);if(LS.get("wo_runstart_"+sel,0))LS.set("wo_runstart_"+sel,st+gap);else s.start=st+gap;delete s.end;LS.set("wo_"+sel,s);}
 el_sclk_refresh();});
function el_sclk_refresh(){var el=$("sclk");if(el)el.__h=null;sclk();}
$("chg").onclick=function(){DCO[sel]=!DCO[sel];renderPanel();};
// yesterday's session not logged: one line under the week strip (pc-v50)
function nag(){var el=$("ynag");if(!el)return;var y=addDays(today,-1),S=mode(y)=="pre"?null:S_(y),show=!!(S&&!S.rest&&!S.tbc&&!logFor(y,S.name)&&LS.get("wo_nag","")!=y&&!(isOpen&&sel==y)&&weekOff==0);el.hidden=!show;if(!show){el.innerHTML="";return;}
 el.innerHTML='<span>Yesterday\'s <b>'+esc(S.name)+'</b> is not logged.</span><div class="nagb"><button type="button" class="btn" data-ng="log">Log it</button><button type="button" class="swb" data-ng="skip">Skipped</button><button type="button" class="swb" data-ng="x" aria-label="Dismiss">Not now</button></div>';}
$("ynag").addEventListener("click",function(e){var b=e.target.closest("[data-ng]");if(!b)return;var y=addDays(today,-1),w=b.dataset.ng;if(w=="x"){LS.set("wo_nag",y);nag();return;}
 if(w=="skip"){var s=P(y),r=R(y);UNDOPRE={log:JSON.stringify(logs()),d:y,s:JSON.stringify(s),r:JSON.stringify(r)};s.oc="skipped";r.sub=0;LS.set("wo_"+y,s);LS.set("wo_run_"+y,r);}
 if(w=="skip"&&TABS){QUIET=true;if(!(isOpen&&sel==y))openDay(y);finBusy=false;$("fin").click();QUIET=false;if(isOpen)closeP();toast("Yesterday's "+(S_(y)?S_(y).name:"session")+" logged as skipped.",{label:"Undo",fn:undoLast});return;}
 if(!(isOpen&&sel==y))openDay(y);if(w=="skip"){finBusy=false;$("fin").click();}else{var t=$("topq");if(t&&t.scrollIntoView)t.scrollIntoView({block:"center"});}});
$("imp").onclick=function(){IMW=null;$("im_t").value="";$("im_r").innerHTML="";$("im_ok").hidden=true;$("ims").classList.add("show");setTimeout(function(){$("im_t").focus();},50);};
function histDel(ev){var b=ev.target.closest("[data-del]");if(!b)return;var l=logs(),i=+b.dataset.del,e=l[i];if(!e)return;if(!confirm("Delete this entry?\n"+e.date+" · "+(e.name||"Pump + Cardio")))return;
 l.splice(i,1);LS.set("wo_log",l);if(e.sub||e.oc=="skipped"){var r=R(e.date),s=P(e.date);r.sub=0;if(s.oc)s.oc="";LS.set("wo_run_"+e.date,r);LS.set("wo_"+e.date,s);}$("acs").classList.remove("show");all();}
$("hist").addEventListener("click",histDel);$("acs").addEventListener("click",histDel);
$("xhs").addEventListener("click",function(e){if(e.target===this||e.target.closest(".xhx"))$("xhs").classList.remove("show");});
$("ims").addEventListener("click",function(e){if(e.target===this||e.target.closest(".imx"))$("ims").classList.remove("show");});
$("im_chk").onclick=function(){var w;IMW=null;$("im_ok").hidden=true;try{w=JSON.parse($("im_t").value);}catch(e){$("im_r").innerHTML='<div class="bad">Not valid JSON: '+esc(e.message||e)+'</div>';return;}
 var v=validateWeek(w),h="";if(v.errors.length)h+=v.errors.map(function(m){return '<div class="bad">✕ '+esc(m)+'</div>';}).join("");else{h+='<div class="good">✓ Week of '+esc(sdl(w.week))+(w.title?" · "+esc(w.title):"")+': '+v.info.sess+' sessions, '+v.info.days+' days'+(v.info.how?', '+v.info.how+' How-to '+(v.info.how==1?'entry':'entries'):'')+'.</div><div class="imd">'+esc(weekDays(w))+'</div>';IMW=w;$("im_ok").hidden=false;}
 h+=v.warnings.map(function(m){return '<div class="warn">! '+esc(m)+'</div>';}).join("");$("im_r").innerHTML=h;};
function weekDays(w){var B=null;try{B=buildWeek(w);}catch(e){}return Object.keys(w.days||{}).sort().map(function(d){var dd=w.days[d]||{},S=(B&&B.sess[dd.main])||SESS[dd.main];return sdl(d).split(" ")[0]+" "+(S?S.short||S.name:dd.main||"?")+(dd.backup?" (+ backup)":"");}).join(" · ");}
$("im_ok").onclick=function(){if(!IMW)return;var m=LS.get("wo_weeks",{});if(!m||typeof m!="object")m={};m[IMW.week]=IMW;LS.set("wo_weeks",m);LS.set("wo_flash",{week:IMW.week,msg:"Week of "+sdl(IMW.week)+" saved · "+weekDays(IMW)});location.reload();};
function toast(msg,act){var t=$("toast");if(!t)return;t.textContent=msg;t.classList.toggle("act",!!act);if(act){var b=document.createElement("button");b.type="button";b.className="tact";b.textContent=act.label;b.onclick=function(){t.classList.remove("show");act.fn();};t.appendChild(b);}t.classList.add("show");clearTimeout(toast.t);toast.t=setTimeout(function(){t.classList.remove("show");},6000);}
$("wks").addEventListener("click",function(e){var b=e.target.closest("[data-rmw]");if(!b)return;if(!confirm("Remove the imported week of "+sdl(b.dataset.rmw)+"? Logged workouts are kept."))return;var m=LS.get("wo_weeks",{})||{};delete m[b.dataset.rmw];LS.set("wo_weeks",m);location.reload();});
window.__wk={BK:BK,OVR:OVR,PROG:PROG,QK:QK,swapHref:swapHref};
var finBusy=false,ovAt=0,UNDO=null,UNDOPRE=null,QUIET=false;
$("fin").onclick=function(){var d=sel,S=S_(d),m=mode(d);if(finBusy||m=="future"||m=="pre"||!S||S.rest)return;finBusy=true;setTimeout(function(){finBusy=false;},1500);
var name=S.name,l=logs(),old=null,idx=-1;for(var i=0;i<l.length;i++)if(sameE(l[i],d,name)){old=l[i];idx=i;}
var s=P(d),r=R(d),st0=+LS.get("wo_runstart_"+d,0)||s.start||0,e={name:name,date:d},x=[],tot=setsTotal(S);
if(TABS&&!old&&!r.sub&&!s.oc&&d==today&&!(r.d||r.t)){var sc0=score(d);if(sc0&&sc0.t>2&&sc0.d*3<sc0.t&&!confirm("Finish with only "+sc0.d+" of "+sc0.t+" parts done?")){finBusy=false;return;}}
if(TABS&&r.sub&&s.oc!="skipped"&&!(r.d||tnorm(r.t||"")||(r.sl||"").trim()||(r.n||"").trim())){finBusy=false;toast("Add a time or a distance first.");var ft=$("r_t");if(ft)ft.focus();return;}
if(tot){var w={},wt={};items(S).forEach(function(it){var v=dayW(it.x,d);if(v!=null&&X[it.x][3]&&!(s.rx&&s.rx[it.gi])){wt[it.x]=v;if(sid(d)=="pump")w[it.gi]=v;}});e.w=w;e.wt=wt;e.sets=ticks(s);e.of=setsTotal(S,s);x.push(e.sets+" of "+tot+" sets ticked");
 var rp={},ln=[],skx=[];S.blocks.forEach(function(b){if(b.k=="ex")b.items.forEach(function(it){if(skp(s,it.gi)){skx.push(it.x);return;}if(!it.rp)return;var a=[],kk=[],hk=false,any=false;for(var q=0;q<bn(b,s);q++){var k=it.gi+"_"+q;if(s.t[k]){any=true;a.push(repV(s,k,it));var kv=s.kg&&s.kg[k]!=null&&s.kg[k]!==""?String(s.kg[k]):null;kk.push(kv||"–");if(kv)hk=true;}else{a.push("–");kk.push("–");}}if(any){rp[it.x]={v:a,u:it.ru||""};if(hk)rp[it.x].k=kk;if(s.rx&&s.rx[it.gi])rp[it.x].sub=s.rx[it.gi];if(s.xn&&s.xn[it.gi])rp[it.x].n=s.xn[it.gi];ln.push(repLine(it.x,wt[it.x],rp[it.x]));}else if(s.xn&&s.xn[it.gi]){rp[it.x]={v:[],u:it.ru||"",n:s.xn[it.gi]};}});});if(Object.keys(rp).length){e.rp=rp;x=x.concat(ln);}else delete e.rp;if(skx.length){e.skx=skx;x.push("skipped: "+skx.map(nm).join(", "));}else delete e.skx;}
if(hasRun(S)){e.km=r.d||"";e.time=tnorm(r.t||"");e.effort=r.e||"";e.feel=r.f||"";e.notes=r.n||"";if(e.km)x.push(e.km+" "+(sid(d)=="row"&&!S.isRun?"m":"km"));if(e.time)x.push(e.time);if(e.effort)x.push(e.effort+" effort");if(e.feel)x.push("felt "+e.feel+"/10");}
if(!hasRun(S)&&r.sub){var at9=r.at||"run";e.sub=actLabel(r);e.plan=S.name;e.act=at9;if(ACTD[at9]&&r.d)e.km=r.d;if(r.t&&tnorm(r.t))e.time=tnorm(r.t);if(r.e)e.effort=r.e;if(r.f)e.feel=r.f;if(r.n)e.notes=r.n;x.push("did "+e.sub+" instead of "+e.plan);}
if(hasRun(S)&&r.sub){e.act=r.at||"run";e.sub=(r.sl||"").trim()||(e.act!="run"?actLabel(r):"a different run");var others=S.blocks.some(function(b){b=VB(b);if(b.k=="timer"&&!b.counter&&!/warm|cool/i.test(b.h||""))return sdone(d,b.id);if(b.k=="ex")return b.items.some(function(it){for(var q=0;q<b.n;q++)if(s.t[it.gi+"_"+q])return true;return false;});return false;});e.plan=others||S.blocks.some(function(b){return b.k=="fields";})?planOf(S):S.name;x.push("did "+e.sub+" instead of "+e.plan);}
if(s.oc){e.oc=s.oc;if(!(e.sub&&s.oc=="modified"))x.push(s.oc=="planned"?"as planned":s.oc);}
var bkd=[],bkn=0;S.blocks.forEach(function(b){b=VB(b);if(b.k!="timer"&&b.k!="ex")return;bkn++;if(blockDone(b,s))bkd.push(b.k=="timer"?b.name:(b.h||"").replace(/^[A-C] · /,"")+": "+b.items.map(function(it){return nm(it.x);}).join(" + "));});if(bkn){e.bk={d:bkd,n:bkn};if(bkd.length<bkn&&bkn>1)x.push(bkd.length+" of "+bkn+" blocks done");}if(!e.notes&&s.nt){e.notes=s.nt;}
if(S.blocks.some(function(b){return VB(b).counter;})){e.breaks=r.b;if(r.b)x.push(r.b+" walk break"+(r.b==1?"":"s"));}if(s.sc&&Object.keys(s.sc).length)e.sc=s.sc;e.type=curType(d);e.sid=sid(d);if(S.isRun){e.ri=1;x.push("run instead");}else delete e.ri;if(old&&old.custom&&old.type==e.type){e.name=old.name;e.custom=1;}else if(old&&old.name&&old.name!=name&&isName(old.name,name))e.name=old.name;
if(e.sub&&e.bk&&!e.bk.d.length)x=x.filter(function(l){return !/sets ticked$|blocks done$/.test(l);});  // the session was replaced: no "0 of 20 sets" noise
if(!x.length)x.push(score(d).d+" of "+score(d).t+" parts done");
var stopped=s.end&&s.end>=st0?s.end:0;if(st0&&d==today&&!stopped){s.end=Date.now();LS.set("wo_"+d,s);}
var mins=st0?Math.round(((stopped||Date.now())-st0)/60000):0;if(d!=today||mins>180||!st0)mins=old?old.min:(d==today?Math.min(mins,180):30);if(e.time&&tmin(e.time))mins=tmin(e.time);if(e.oc=="skipped"&&!e.time&&!e.sub)mins=0;e.min=mins;  // a run logged by its actual elapsed time
UNDO=UNDOPRE||{log:JSON.stringify(logs()),d:d,s:JSON.stringify((function(){var q=JSON.parse(JSON.stringify(s));delete q.end;return q;})())};UNDOPRE=null;$("o_undo").hidden=false;
if(e.sub){var l2=[],ni=-1;l.forEach(function(q,qi){if(q&&q.date==d&&q.type=="extra"&&(q.act||"run")==(e.act||"run"))return;if(qi==idx)ni=l2.length;l2.push(q);});l=l2;idx=ni;RUNOPEN[d]=false;}
if(idx>=0)l[idx]=e;else l.push(e);LS.set("wo_log",l);
$("o_n").textContent=name+(d!=today?" · "+(TABS?sdl(d):d):"");document.querySelector("#ov .kicker").textContent=TABS&&e.oc=="skipped"&&!e.sub?"Logged as skipped":"Workout saved";$("o_t").textContent=e.min+" min";$("o_d").innerHTML=x.map(esc).join("<br>");$("o_e").textContent=(old?"Log updated. ":"")+(e.oc=="skipped"?"Logged. Rest up, back at it next time.":e.oc=="cut short"?"Stopping early was the right call. Recover well.":(+e.feel>0&&+e.feel<=4)?ENC[1]:[ENC[0],ENC[2],ENC[3]][Math.floor(Math.random()*3)]);if(!QUIET)$("ov").classList.add("show");ovAt=Date.now();all();};
function undoLast(){if(!UNDO)return;try{LS.set("wo_log",JSON.parse(UNDO.log));}catch(e){}if(UNDO.s)LS.set("wo_"+UNDO.d,JSON.parse(UNDO.s));if(UNDO.r)LS.set("wo_run_"+UNDO.d,JSON.parse(UNDO.r));UNDO=null;$("ov").classList.remove("show");all();toast("Undone. Nothing was saved.");}
$("o_undo").onclick=function(){if(!UNDO||Date.now()-ovAt<700)return;undoLast();};
function ovClose(){$("ov").classList.remove("show");if(TABS&&isOpen){if(RT)stopRest();closeP();delete SCY[sel];window.scrollTo(0,0);}}
$("o_done").onclick=function(){if(Date.now()-ovAt<700)return;ovClose();};$("ov").onclick=function(e){if(e.target===this&&Date.now()-ovAt>700)ovClose();};
$("rst").onclick=function(){var d=sel,S=S_(d);if(mode(d)=="future"||!S)return;if(!confirm("Reset "+(d==today?"today":d)+"'s ticks, timers and weights?"))return;LS.del("wo_"+d);LS.del("wo_run_"+d);LS.del("wo_runstart_"+d);items(S).forEach(function(it){setW(it.x,d,"");});if(T&&T.date==d)stopT();all();};
document.addEventListener("visibilitychange",function(){if(document.visibilityState=="visible"){unlock();if(T||RT||wantWake())wake();checkDay();loop();}});
function checkDay(){var n=ymd(new Date());if(n!=today){today=n;weekOff=0;all();}}
setInterval(checkDay,30000);
migrate();if(T&&(!T.segs||!T.t0))stopT();if(T){lastI=-2;wake();}
(function(){var f=LS.get("wo_flash",null);if(f&&f.week){LS.del("wo_flash");if(TABS)TAB="week";weekOff=Math.round((pd(f.week)-pd(monOf(today)))/604800000);toast(f.msg||"Saved");}})();
all();loop();
// installed on the Home Screen: open straight on today's session (a browser tab keeps the week view)
if(TABS){lockLab(false);$("prev").innerHTML=ic(IP.back,22);$("next").innerHTML=ic(IP.fwd,22);$("tback").innerHTML=ic(IP.back,18)+" Back";$("tnext").innerHTML="Next "+ic(IP.fwd,18);$("snd").innerHTML=ic(IP.snd,18)+" Sound off: tap to turn on";document.addEventListener("click",function(e){var tb=e.target.closest("#tabbar [data-tab]");if(tb){setTab(tb.dataset.tab);return;}
  var hm=e.target.closest("#home [data-hm]");if(hm){var w=hm.dataset.hm;if(w=="week"){setTab("week");return;}
   if(w=="start"){var s=P(today);if(!s.start&&!LS.get("wo_runstart_"+today,0)){s.start=Date.now();delete s.end;LS.set("wo_"+today,s);unlock();}}
   if(w=="else"){var s2=P(today),r2=R(today);r2.sub=1;s2.oc="modified";LS.set("wo_"+today,s2);LS.set("wo_run_"+today,r2);delete SCY[today];}
   if(w=="plan"){var s3=P(today),r3=R(today);r3.sub=0;s3.oc="";LS.set("wo_"+today,s3);LS.set("wo_run_"+today,r3);all();return;}
   if(w=="resume"){var s4=P(today),now4=Date.now(),rs=+LS.get("wo_runstart_"+today,0),gap=now4-(s4.end||now4);if(rs)LS.set("wo_runstart_"+today,rs+gap);else s4.start=(s4.start||now4)+gap;delete s4.end;LS.set("wo_"+today,s4);unlock();}
   if(w=="run"||w=="conv"||w=="else")delete SCY[today];
   if(!(isOpen&&sel==today))openDay(today);if(w=="run")place(today,"actual");else if(w=="conv")place(today,"#xconv");else if(w=="else"||w=="start"||w=="peek")window.scrollTo(0,0);return;}
  if(e.target.closest("#cog")){$("sets").classList.add("show");return;}
  if(e.target.closest("#ed2")){$("ed").click();return;}
  var wr=e.target.closest("#wlist [data-d]");if(wr){if(WSW){WSW=false;return;}openDay(wr.dataset.d);return;}});
 $("sets").addEventListener("click",function(e){if(e.target===this||e.target.closest(".swx"))this.classList.remove("show");});
 // settings and the weeks list live in the settings sheet
 (function(){var b=$("sets_b");b.innerHTML='<div class="sgt">Timers</div><div id="sg_t"></div><div class="sgt">Cues</div><div id="sg_c"></div><div class="sgt">Plan</div><div id="sg_p"></div><div class="sgt">About</div><div class="abt" id="sg_a"></div>';
 var two=function(id,to){var i=$(id);if(!i)return;var lab=i.closest("label"),txt=lab.textContent.replace(/\s+/g," ").trim(),m=txt.match(/^(.*?)\s*\((.*)\)$/),s=document.createElement("span");s.className="st";var t1=m?m[1]:txt,t2=m?m[2].charAt(0).toUpperCase()+m[2].slice(1)+".":"";s.innerHTML='<span class="t1">'+esc(t1)+'</span>'+(t2?'<span class="t2">'+esc(t2)+'</span>':'');lab.textContent="";lab.appendChild(i);lab.appendChild(s);$(to).appendChild(lab);};
 two("autorest","sg_t");two("cueon","sg_c");two("loud","sg_c");
 var wk=document.querySelector(".wkl");if(wk)$("sg_p").appendChild(wk);
 var mv=document.querySelector('meta[name="app-version"]');$("sg_a").innerHTML='<div class="t1">Pump + Cardio <span id="sg_v">'+esc(mv?mv.content:"")+'</span></div><div class="t2">Your logs and settings stay on this phone. Nothing leaves it unless you export.</div>';})();
 $("imp").addEventListener("click",function(){$("sets").classList.remove("show");});all();}
(function(){if(TABS)return;var sa=false;try{sa=navigator.standalone===true||(window.matchMedia&&matchMedia("(display-mode: standalone)").matches);}catch(e){}if(sa&&weekOff==0&&!isOpen&&mode(today)!="pre"&&S_(today))openDay(today);})();
if("serviceWorker" in navigator&&/^https?:/.test(location.protocol)){var reload=false;navigator.serviceWorker.addEventListener("controllerchange",function(){if(reload)return;reload=true;location.reload();});
navigator.serviceWorker.register("sw.js").then(function(reg){function show(){var u=$("upd");u.style.display="block";u.onclick=function(){if(reg.waiting)reg.waiting.postMessage("skip");else location.reload();};}
if(reg.waiting&&navigator.serviceWorker.controller)show();reg.addEventListener("updatefound",function(){var w=reg.installing;if(w)w.addEventListener("statechange",function(){if(w.state=="installed"&&navigator.serviceWorker.controller)show();});});
setInterval(function(){reg.update().catch(function(){});},3600000);document.addEventListener("visibilitychange",function(){if(document.visibilityState=="visible")reg.update().catch(function(){});});}).catch(function(){});}
// pc-v69: sheets and the saved card take focus when they open, keep Tab inside, close on Escape and give focus back
(function(){var FOC='button:not([disabled]):not([hidden]),input:not([disabled]),select,textarea,a[href]',cur=null,last=null;
 var vis=function(e){return e.offsetWidth>0||e.offsetHeight>0;},open=function(){var l=document.querySelectorAll("#hs.show,.swp.show,#ov.show");return l.length?l[l.length-1]:null;};
 function sync(){var o=open();if(o&&o!==cur){cur=o;last=document.activeElement;var f=[].filter.call(o.querySelectorAll(FOC),vis)[0];setTimeout(function(){if(f&&cur===o)f.focus({preventScroll:true});},30);}
  else if(!o&&cur){cur=null;var l2=last;last=null;if(l2&&document.contains(l2)&&l2.focus){try{l2.focus({preventScroll:true});}catch(e){}}}}
 new MutationObserver(sync).observe(document.body,{attributes:true,subtree:true,attributeFilter:["class"]});
 document.addEventListener("keydown",function(e){if(!cur)return;if(e.key=="Escape"){var x=cur.querySelector(".hs_top .swx,#hs_x");if(x)x.click();return;}if(e.key!="Tab")return;
  var f=[].filter.call(cur.querySelectorAll(FOC),vis);if(!f.length)return;var a0=f[0],z=f[f.length-1],ae=document.activeElement;
  if(e.shiftKey&&(ae===a0||!cur.contains(ae))){e.preventDefault();z.focus();}else if(!e.shiftKey&&(ae===z||!cur.contains(ae))){e.preventDefault();a0.focus();}});})();
window.__app={get today(){return today;},get sel(){return sel;},checkDay:checkDay,sid:sid,view:function(){return S_(sel);},posOf:posOf,emomPlan:emomPlan,exportText:exportText,suggest:suggest,weekRows:weekRows,validateWeek:validateWeek,buildWeek:buildWeek,get WEEKS(){return WEEKS;}};
})();
</script></body></html>
