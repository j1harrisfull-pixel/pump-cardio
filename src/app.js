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
function bEvery(b){var s=[];for(var r=1;r<=b.n;r++){var used=0;b.items.forEach(function(it,i){var sw=i?(it.sw||15):10;s.push(["READY",sw,nmI(it)]);pushW(s,wsec(it),nmI(it),it.side,"set "+r+"/"+b.n);used+=sw+wsec(it);});if(used>b.win-15)throw new Error("every too tight "+b.h+" "+used);if(r<b.n)s.push(["REST",b.win-used,"Rest"]);}return s;}
function bSup(b){var s=[];for(var r=1;r<=b.n;r++){b.items.forEach(function(it,i){s.push(["READY",i?(it.sw||15):15,nmI(it)]);s.push(["WORK",wsec(it),nmI(it)+" · set "+r+"/"+b.n]);});if(r<b.n)s.push(["REST",b.rest,"Rest"+(b.fill?" · optional "+b.fill:"")]);}return s;}
function pushW(s,w,nm,side,tag){if(side){var a=Math.ceil(w/2);s.push(["WORK",a,nm+" · left side · "+tag]);s.push(["WORK",w-a,nm+" · switch → right side · "+tag]);}else s.push(["WORK",w,nm+" · "+tag]);}
function bEmom(b){var s=[];for(var r=1;r<=b.n;r++)b.items.forEach(function(it,j){var sw=it.sw||15,w=Math.min(wsec(it),b.win-sw),rs=b.win-sw-w;s.push(["READY",sw,nmI(it)]);pushW(s,w,nmI(it),it.side,"round "+r+"/"+b.n);var last=r==b.n&&j==b.items.length-1;if(rs>0&&!last)s.push(["REST",rs,"Rest · then "+nmI(b.items[(j+1)%b.items.length])]);});return s;}
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
tbc:{name:"Plan coming Sunday",short:"Soon",rest:1,tbc:1,safe:"",blocks:[{k:"rest",name:"Plan coming Sunday",note:"This week's sessions are added each Sunday."}]}};
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
// ---- backups: date -> backup session id (one per day)
var BK={"2026-10-12":"bk12","2026-10-13":"bk13","2026-10-14":"bk14","2026-10-15":"bk15","2026-10-16":"bk16","2026-10-17":"bk17","2026-10-18":"bk18",
 "2026-10-19":"bk19","2026-10-20":"bk20","2026-10-21":"bk21","2026-10-22":"bk22","2026-10-23":"bk23","2026-10-24":"bk24","2026-10-25":"bk25",
 "2026-10-26":"bk26","2026-10-27":"bk27","2026-10-28":"bk28","2026-10-29":"bk29","2026-10-30":"bk30","2026-10-31":"bk31","2026-11-01":"bk01"};
// ---- one-day overrides: date -> session id. Replaces only that day's main session (backups unchanged). Example: OVR["2026-10-16"]="bk16";
var OVR={};
var PROG={"2026-10-12":"easyrun12","2026-10-13":"strA","2026-10-14":"row","2026-10-15":"mob","2026-10-16":"strB","2026-10-17":"kb","2026-10-18":"walk",
 // week 2
 "2026-10-19":"mob19","2026-10-20":"up20","2026-10-21":"run21","2026-10-22":"mob22","2026-10-23":"lo23","2026-10-24":"kb24","2026-10-25":"walk25",
 // week 3
 "2026-10-26":"up26","2026-10-27":"run27","2026-10-28":"mob28","2026-10-29":"lo29","2026-10-30":"mob30","2026-10-31":"kb31","2026-11-01":"walk01"};
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
Object.keys(RI).forEach(function(k){SESS[k].blocks.forEach(function(b){var v=RI[k][b.id];if(!v)return;var a=0,c=0;b.segs.forEach(function(g){a+=g[1];});v.segs.forEach(function(g){c+=g[1];});if(a!=c)throw new Error("run-instead time mismatch "+b.id);b.ri=v;});});
var RIN={row:["Run Intervals","Run"],walk:["Zone 2 Run","Run"],bk14:["Backup · Run/Walk + Core","Run"],bk17:["Backup · Dumbbell Flow + Zone 2 Run","DB"]};
var RIS={bk14:"Lower energy, no rowing. Breathe out slowly during the core work. Steady pace, RPE 5–6.",row:"Run intervals never all-out: short phrases only. Walk whenever you need to and breathe rhythmically. Moderate pace, RPE 7.",walk:STOP_RUN};
// renamed sessions (pc-v28): logs saved under the old name still count as that day's log
Object.assign(RIN,{bk21:["Backup · Zone 2 Run + Core","Run"],bk24:["Backup · Zone 2 Run + Bodyweight","Run"],walk25:["Zone 2 Run + Stretch","Run"]});
Object.assign(RIS,{bk21:"No rowing. Zone 2 run: conversational, a little breathless, walk whenever needed. Steady pace, RPE 5–6.",bk24:STOP_RUN,walk25:STOP_RUN});
Object.assign(RIN,{bk27:["Backup · Zone 2 Run + Stretch","Run"],bk31:["Backup · Zone 2 Run + Circuit","Run"],walk01:["Zone 2 Run + Stretch (Sun)","Run"]});
Object.assign(RIS,{bk27:STOP_RUN,bk31:STOP_RUN,walk01:STOP_RUN});
var ALIAS={"Zone 2 Run":["Easy Run"],"Backup · Zone 2 Row + Mobility":["Backup · Easy Row + Mobility"],"Backup · Dumbbell Flow + Zone 2 Run":["Backup · Dumbbell Flow + Easy Run"]};
function isName(n,name){return n==name||(ALIAS[name]||[]).indexOf(n)>=0;}
function hasRI(S){S=S&&(S.base||S);return !!(S&&S.blocks.some(function(b){return b.ri;}));}
function riOn(k){var a=LS.get("wo_ri",{})||{};return !!a[k];}
function setRI(k,v){var a=LS.get("wo_ri",{})||{};if(v)a[k]=1;else delete a[k];LS.set("wo_ri",a);}
function VB(b){return b.ri&&riOn(sel)?Object.assign({},b,b.ri,{ri:null}):b;}
Object.keys(SESS).forEach(function(k){var S=SESS[k],g=S.g0||0;S.nt=0;S.tot=0;S.blocks.forEach(function(b,bi){b.bi=bi;if(b.rr)b.rest=(b.rr[0]+b.rr[1])/2;if(b.mode=="sup"){b.est=dur(bSup(b));S.tot+=b.est;S.est=1;}else{if(b.mode){b.timer={id:b.tid,segs:b.mode=="every"?bEvery(b):bEmom(b)};}var tt=b.timer||b;S.tot+=dur(tt.segs);}if(b.k=="ex"){b.items.forEach(function(it){it.gi=g++;S.nt+=b.n;});if(!b.rk)b.rk="r"+bi;}if(b.k=="timer"||b.timer)S.nt++;});});
var LS={get:function(k,d){try{var v=localStorage.getItem(k);if(v==null)return d;try{return JSON.parse(v);}catch(e){return v;}}catch(e){return d;}},set:function(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}},del:function(k){try{localStorage.removeItem(k);}catch(e){}}};
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
function baseSid(k){return OVR[k]||PROG[k];}
function sid(k){if(k<SD)return null;var o=LS.get("wo_plan",{})||{};if(k<=LEGACY_END)return LEG[o[k]||DEFP[k]||PAT[pd(k).getDay()]]||"rest0";var b=baseSid(k);if(!b)return "tbc";if(o[k]=="Rest")return "rest0";if(qOn(k)&&QK[k]&&SESS[QK[k]])return QK[k];return altOn(k)&&BK[k]&&SESS[BK[k]]?BK[k]:b;}
function S_(k){var i=sid(k);if(!i)return null;var S=SESS[i];if(!(hasRI(S)&&riOn(k)))return S;var V=Object.create(S);V.base=S;V.isRun=1;V.name=(RIN[i]||[S.name+" (run)"])[0];V.short=(RIN[i]||[0,S.short])[1];V.safe=RIS[i]||S.safe;V.blocks=S.blocks.map(function(b){if(b.k=="fields")return Object.assign({},b,{dist:"Distance (km)"});return b.ri?Object.assign({},b,b.ri,{ri:null}):b;});return V;}
function curType(k){var S=S_(k);if(!S)return null;if(S.quick)return "quick";return S.isRun?"run":(altOn(k)&&BK[k]&&sid(k)==BK[k]?"backup":"main");}
function plan(k){var S=S_(k);return S?S.short:null;}
function mode(k){return k<SD?"pre":k>today?"future":k<today?"past":"today";}
function logs(){var l=LS.get("wo_log",[]);return Array.isArray(l)?l:[];}
function sameE(e,k,name){return e.date==k&&(!name||isName(e.name||"Pump + Cardio",name)||(e.custom&&e.type&&e.type==curType(k)));}
function logFor(k,name){var l=logs();for(var i=0;i<l.length;i++)if(sameE(l[i],k,name))return l[i];return null;}
function sdone(d,id){return !!(P(d).s[id]||R(d).s[id]);}
// audio
var ac=null;function unlock(){try{if(!ac){var C=window.AudioContext||window.webkitAudioContext;if(!C)return;ac=new C();var b=ac.createBuffer(1,1,22050),s=ac.createBufferSource();s.buffer=b;s.connect(ac.destination);s.start(0);}if(ac.state!="running")ac.resume();}catch(e){}sndUI();}
document.addEventListener("pointerdown",unlock,{passive:true});document.addEventListener("touchend",unlock,{passive:true});
function beep(f,d){try{if(ac){var o=ac.createOscillator(),g=ac.createGain();o.frequency.value=f||880;g.gain.value=.3;o.connect(g);g.connect(ac.destination);o.start();o.stop(ac.currentTime+(d||.25));}}catch(e){}window.__bp&&window.__bp.push(f);}
var wl=null;function wake(){try{if("wakeLock" in navigator&&!wl&&document.visibilityState=="visible")navigator.wakeLock.request("screen").then(function(l){wl=l;l.addEventListener("release",function(){wl=null;});}).catch(function(){});}catch(e){}}
function unwake(){try{if(wl)wl.release();}catch(e){}wl=null;}
function wantWake(){return isOpen&&sel==today;}
function relWake(){if(!(T||RT||wantWake()))unwake();}
// timer
var T=LS.get("wo_timer",null),lastI=-2,lastL=-1,hideAt=0;
function tnow(){return T&&T.pa?T.pa:Date.now();}
function tstate(){var e=(tnow()-T.t0)/1000,acc=0;for(var i=0;i<T.segs.length;i++){var L=T.segs[i][1];if(e<acc+L)return{i:i,left:Math.max(1,Math.ceil(acc+L-e))};acc+=L;}return{i:T.segs.length,left:0};}
function findT(S,id){var r=null;S.blocks.forEach(function(b){b=VB(b);if(b.k=="timer"&&b.id==id)r={label:b.h,segs:b.segs};if(b.timer&&b.timer.id==id)r={label:b.h,segs:b.timer.segs};if(b.k=="ex"&&"rest:"+b.rk==id)r={label:b.unit+" "+Math.min(P(sel)[b.rk]||1,b.n)+" of "+b.n,segs:[["REST",b.rest]],max:b.n};});return r;}
function startT(id){var m=mode(sel);if(m=="future"||m=="pre")return;var S=S_(sel),def=S&&findT(S,id);if(!def)return;unlock();var d=sel,s=P(d);
if(!s.start&&!LS.get("wo_runstart_"+d,null)){s.start=Date.now();LS.set("wo_"+d,s);}
T={id:id,label:def.label,segs:def.segs,max:def.max,t0:Date.now(),date:d};LS.set("wo_timer",T);lastI=-1;lastL=-1;lastTick=Date.now();if(RT)stopRest();wake();loop();}
function segStart(i){var a=0;for(var j=0;j<i;j++)a+=T.segs[j][1];return a;}
function tJump(i){if(!T)return;i=Math.max(0,Math.min(i,T.segs.length-1));T.t0=tnow()-segStart(i)*1000;LS.set("wo_timer",T);lastI=-1;lastL=-1;loop();}
function tPause(){if(!T)return;if(T.pa){T.t0+=Date.now()-T.pa;delete T.pa;unlock();}else T.pa=Date.now();LS.set("wo_timer",T);lastL=-1;loop();}
function tBack(){if(!T)return;var st=tstate(),el=(tnow()-T.t0)/1000-segStart(st.i);tJump(el>3?st.i:st.i-1);}
function tNext(){if(!T)return;var st=tstate();if(st.i>=T.segs.length-1){T.t0=tnow()-dur(T.segs)*1000;LS.set("wo_timer",T);loop();}else tJump(st.i+1);}
function stopT(){T=null;LS.del("wo_timer");relWake();$("bar").classList.remove("show","ask");}
function doneT(noTick){var t=T;T=null;LS.del("wo_timer");relWake();$("bar").classList.remove("ask");var p=P(t.date);if(noTick){$("bar").classList.remove("show");if(isOpen)renderPanel();return;}
if(t.id.indexOf("rest:")==0){var rk=t.id.slice(5),c=+p[rk]||1;if(c<(t.max||3))p[rk]=c+1;else p[rk]=c;}else p.s[t.id]=1;LS.set("wo_"+t.date,p);
$("ph").textContent="DONE";$("ph").className="rest";$("time").textContent="0:00";$("sub").textContent=t.label;beep(988,.8);flash("bar");hideAt=Date.now()+4000;if(isOpen)renderPanel();prog();}
function short(l){return String(l||"").split(" · ")[0];}
function nextLab(i){for(var j=i+1;j<T.segs.length;j++){var g=T.segs[j];if(g[0]!="READY")return g[0]=="REST"?"Rest":short(g[2]||T.label);}return "";}
var lastTick=0;
function flash(id){var e=$(id);if(!e)return;e.classList.remove("flash");void e.offsetWidth;e.classList.add("flash");setTimeout(function(){e.classList.remove("flash");},900);}
function sndUI(){var e=$("snd");if(e)e.hidden=!((T||RT)&&(!ac||ac.state!="running"));}
function loop(){var now=Date.now(),gap=now-lastTick;lastTick=now;restTick(gap);sndUI();
if(!T){if(hideAt&&now>hideAt){hideAt=0;$("bar").classList.remove("show");}return;}
$("bar").classList.add("show");hideAt=0;$("tpause").textContent=T.pa?"Resume":"Pause";$("bar").classList.toggle("paused",!!T.pa);var s=tstate();
if(s.i>=T.segs.length){if(gap>2500||T.ask||document.hidden){T.ask=1;LS.set("wo_timer",T);$("bar").classList.add("ask");$("ph").textContent="FINISHED WHILE LOCKED";$("ph").className="";$("time").textContent="0:00";$("sub").textContent=T.label;return;}doneT();return;}
var g=T.segs[s.i];if(s.i!=lastI){var sw=/switch → right side/.test(g[2]||"");if(lastI!=-2){if(sw){beep(880,.15);setTimeout(function(){beep(880,.15);},220);}else beep(g[0]=="REST"?523:g[0]=="READY"?660:988,.4);flash("bar");}lastI=s.i;var rd=g[0]=="READY";$("ph").textContent=rd?"GET READY":sw?"SWITCH SIDES":g[0];$("ph").className=g[0]=="WORK"?"work":g[0]=="REST"?"rest":rd?"ready":"";
var nx=nextLab(s.i);$("sub").textContent=rd?"Next: "+(g[2]||""):(g[2]||T.label)+(nx?"  ·  Next: "+nx:"");$("now").textContent=rd?"":"Now";}
if(s.left!=lastL){$("time").textContent=fmt(s.left);if(!T.pa&&s.left<=3&&lastL>s.left)beep(440,.1);lastL=s.left;}}
// rest timer (strength blocks)
var RT=LS.get("wo_rest",null);
function autoRest(){return LS.get("wo_autorest",true)!==false;}
function startRest(sec,label){RT={end:Date.now()+sec*1000,dur:sec,label:label||"Rest"};LS.set("wo_rest",RT);unlock();wake();restTick(0);}
function stopRest(){RT=null;LS.del("wo_rest");$("rbar").classList.remove("show","zero");$("rbtn").hidden=!!T;relWake();}
function restAdj(d){if(!RT)return;RT.end=Math.max(Date.now()+1000,RT.end+d*1000);LS.set("wo_rest",RT);restTick(0);}
function restTick(gap){var rb=$("rbar");if(!RT){rb.classList.remove("show");$("rbtn").hidden=!!T;return;}$("rbtn").hidden=true;rb.classList.add("show");var left=Math.ceil((RT.end-Date.now())/1000);
if(left<=0){if(!RT.z){RT.z=Date.now();LS.set("wo_rest",RT);rb.classList.add("zero");$("rtime").textContent="0:00";$("rlab").textContent="Rest over · next set";beep(988,.25);setTimeout(function(){beep(988,.25);},300);setTimeout(function(){beep(1175,.5);},600);flash("rbar");}else if(Date.now()-RT.z>6000)stopRest();return;}
$("rtime").textContent=fmt(left);$("rlab").textContent=RT.label;if(left<=3&&RT.ll>left)beep(440,.08);RT.ll=left;}
setInterval(loop,250);
// rendering
function ticks(s){return Object.keys(s.t).filter(function(k){return s.t[k];}).length;}
function score(k){var S=S_(k);if(!S||S.rest)return null;var s=P(k),d=0;items(S);S.blocks.forEach(function(b){if(b.k=="ex")b.items.forEach(function(it){for(var r=0;r<b.n;r++)if(s.t[it.gi+"_"+r])d++;});var tid=b.k=="timer"?b.id:b.timer?b.timer.id:null;if(tid&&sdone(k,tid))d++;});return{d:d,t:S.nt};}
function setsTotal(S){var n=0;S.blocks.forEach(function(b){if(b.k=="ex")n+=b.items.length*b.n;});return n;}
function prog(){var k=isOpen?sel:today,sc=score(k),f=sc?Math.min(1,sc.d/sc.t):0;$("rg").style.strokeDashoffset=194.8*(1-f);$("pct").textContent=sc?Math.round(f*100)+"%":"–";}
var EDK=null,MO={},SM={};
function unitOf(it){return it.ru=="s"?"s":it.ru=="m"?"m":"";}
function rxOf(b,it){return b.n+" × "+it.rp+(it.ru=="s"?" s":it.ru=="m"?" m":"")+(it.side?" each side":"");}
function repV(s,k,it){return s.rp&&s.rp[k]!=null?s.rp[k]:it.rp;}
function stepOf(it){return it.ru?5:1;}
function renderSess(){var S=S_(sel),s=P(sel),r=R(sel),h="",n=0;
S.blocks.forEach(function(b){
 if(b.k=="rest"){h+='<div class="card"><div class="name">'+b.name+'</div><div class="note">'+b.note+'</div></div>';return;}
 if(b.k=="fields"){h+='<h2>Optional</h2><div class="card lock"><label class="l">'+(b.dist||"Distance (km)")+'<input class="f" id="r_d" type="number" inputmode="decimal" step="0.01"></label><label class="l">How it felt (1–10)<input class="f" id="r_f" type="number" inputmode="numeric" min="1" max="10"></label><label class="l">Notes<textarea class="f" id="r_n" rows="3"></textarea></label></div>';return;}
 n++;b=VB(b);var tt=b.timer||b,D=dur(tt.segs);
 if(b.k=="timer"){h+='<h2>'+n+' · '+b.h+' · '+mmss(D)+'</h2><div class="card tcard'+(sdone(sel,b.id)?" done":"")+'" id="c_'+b.id+'"><div class="name">'+b.name+'</div>'+(b.note?'<div class="note">'+b.note+'</div>':'');
  var mvl=function(a){return '<ul class="lst">'+a.map(function(x){var hk=hkey(x);return "<li>"+(HT[hk]?'<button class="mv" data-h="'+esc(hk)+'">'+x+'</button>':x)+"</li>";}).join("")+'</ul>';};
  if(b.groups)h+=b.groups.map(function(g){return '<div class="rg"><div class="rgh">'+g[0]+' <span>each side</span></div><ul class="lst rgl">'+g[1].map(function(m){var hk=hkey(m[0]);return '<li>'+(HT[hk]?'<button class="mv" data-h="'+esc(hk)+'">'+m[1]+'</button>':m[1])+' <b>×'+m[2]+'</b></li>';}).join("")+'</ul></div>';}).join("");
  else if(b.list&&!b.flow)h+=mvl(b.list);
  else if(b.list){var op=SM[b.id];h+='<button class="sm" data-sm="'+b.id+'">'+(op?"Hide moves":"Show "+b.list.length+" moves")+'</button>';if(op)h+=mvl(b.list);}
  h+=sps(b.small);
  var dn=sdone(sel,b.id);h+='<button class="btn lock'+(dn?" gt dn":"")+'" data-t="'+b.id+'">'+(dn?"✓ Done · run guided timer again":b.flow?"Start guided flow":"Start guided timer")+' · '+mmss(D)+'</button>'+(b.counter?'<button class="btn ghost lock" id="brkb">+1 walk break · <span id="brk">'+r.b+'</span></button>':'')+'</div>';return;}
 // exercise group
 if(b.rr){var one=b.items.length==1;h+='<div class="bh"><h2>'+n+' · '+b.h+' · '+b.n+(one?' sets':' rounds')+'</h2></div>';
  h+='<div class="gn rx">Each '+(one?'set':'round')+': '+b.items.map(function(it){return it.lab;}).join(" → ")+'. Rest '+b.rr[0]+'–'+b.rr[1]+' s.</div>'+sps([autoRest()?(one?"Tick a set to start the rest timer.":"Tick the last move of a round to start the rest timer."):"",b.fill?"Optional in the rest: "+b.fill+".":""]);}
 else h+='<div class="bh"><h2>'+n+' · '+b.h+(D?' · '+mmss(D):'')+'</h2></div>';
 if(b.gn)h+='<div class="gn">'+b.gn+'</div>';
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
  h+='<div class="mx"'+(mo?'':' hidden')+'>'+(it.cue?'<div class="cue">'+it.cue+'</div>':'')+'<div class="note">'+(e[3]?(last?'Last: '+esc(last.v)+' kg ('+sdl(last.d)+')'+(cur!=null&&+cur>+last.v?' <span class="up">↑</span>':''):'Suggested: '+e[1]):e[1])+'</div><button class="how" data-h="'+it.x+'">How to</button></div></div>';});
 if(b.rest&&!b.mode)h+='<button class="btn lock" data-t="rest:'+b.rk+'">'+b.btn+'</button>';
 if(b.timer)h+='<button class="btn lock gt'+(sdone(sel,b.timer.id)?" dn":"")+'" data-t="'+b.timer.id+'" id="c_'+b.timer.id+'">'+(sdone(sel,b.timer.id)?"✓ Done · run guided timer again":"Start guided timer")+' · '+mmss(D)+'</button>';});
$("sess").innerHTML=h;["d","f","n"].forEach(function(k){var el=$("r_"+k);if(el)el.value=r[k]||"";});}
function sps(a){return [].concat(a||[]).filter(Boolean).map(function(x){return '<div class="sp">'+x+'</div>';}).join("");}
function maybeRest(S,s,k){if(!autoRest()||mode(sel)!="today"||(T&&T.date==sel))return;var gi=+k.split("_")[0],q=+k.split("_")[1];S.blocks.forEach(function(b){if(b.mode!="sup"||!b.items.some(function(it){return it.gi==gi;}))return;if(!b.items.every(function(it){return s.t[it.gi+"_"+q];}))return;if(q>=b.n-1)return;startRest(b.rest,b.h.split(" · ")[0]+" · rest before round "+(q+2)+(b.fill?" · optional "+b.fill:""));});}
function itemByGi(S,gi){var a=items(S);for(var i=0;i<a.length;i++)if(a[i].gi==gi)return a[i];return null;}
function renderPanel(){var S=S_(sel),m=mode(sel);if(!S)return;$("acts").hidden=!!S.rest;
$("safe1").textContent=S.safe;document.querySelector(".safe .stop").hidden=!!S.tbc;$("panel").classList.toggle("ro",m=="future");
var lg=!S.rest?logFor(sel,S.name):null,lab=sdl(sel);
$("dnote").textContent=(m=="future"?"Planned · "+lab:m=="past"?(S.rest?"":lg?"Logged · ":"Not logged · ")+lab:"Today")+(S.tot>0&&!S.tbc?" · "+(S.est?"≈ ":"")+Math.round(S.tot/60)+" min":"");
$("fin").textContent=lg?"Update log":"Finish workout";
var o=LS.get("wo_plan",{})||{},hasBk=!!(BK[sel]&&SESS[BK[sel]]&&o[sel]!="Rest"&&sel>LEGACY_END),on=altOn(sel);$("dctl").hidden=!(hasBk||m=="today"||m=="future")||!!S.tbc;
var hasQ=!!(QK[sel]&&SESS[QK[sel]]&&o[sel]!="Rest"),qo=qOn(sel);$("qk").hidden=!hasQ;if(hasQ){$("qk").textContent=qo?"↩ Back to main: "+SESS[baseSid(sel)].name:"Quick option: "+SESS[QK[sel]].name;$("qk").classList.toggle("on",qo);$("dctl").hidden=false;}
$("alt").hidden=!hasBk;if(hasBk){on=on&&!qo;$("alt").textContent=on?"↩ Back to main: "+SESS[baseSid(sel)].name:"Use backup session: "+SESS[BK[sel]].name.replace("Backup · ","");$("alt").classList.toggle("on",on);}
if(m=="today")wake();$("swap").hidden=!(m=="today"||m=="future");var hr=hasRI(S);$("ri").hidden=!hr;if(hr){var ro=riOn(sel);$("ri").textContent=ro?"↩ Back to "+(sid(sel)=="row"?"row":"Assault Runner / walk"):"Run instead (outdoor run)";$("ri").classList.toggle("on",ro);if(hr)$("dctl").hidden=false;}renderSess();hist();}
function title(){var k=isOpen?sel:today,S=S_(k);$("ttl").textContent=S?S.name:"Pump + Cardio";$("date").textContent=new Date().toLocaleDateString("en-GB",{weekday:"long",day:"numeric",month:"long"});}
function monday(){var d=pd(today),off=(d.getDay()+6)%7;return addDays(today,-off+weekOff*7);}
function editable(k){return k>=today&&k>=SD&&(k<=LEGACY_END||!!baseSid(k));}
function week(){var m=monday(),h="",done={};logs().forEach(function(e){done[e.date]=1;});
for(var i=0;i<7;i++){var k=addDays(m,i),d=pd(k),md=mode(k),dn=d.toLocaleDateString("en-GB",{weekday:"short"});
if(md=="pre"){h+='<div class="day pre"><div class="dn">'+dn+'</div><div class="dd">'+d.getDate()+'</div><div class="pl">–</div></div>';continue;}
h+='<button class="day '+md+(k==today?" today":"")+(isOpen&&k==sel?" sel":"")+(editable(k)?" ed":"")+'" data-d="'+k+'"><div class="dn">'+dn+'</div><div class="dd">'+d.getDate()+'</div><div class="pl">'+plan(k)+'</div>'+(done[k]?'<span class="ok">✓</span>':"")+"</button>";}
$("week").innerHTML=h;$("week").classList.toggle("editing",editing);$("prev").disabled=m<=SD;$("wlab").textContent=weekOff==0?"This week":weekOff==1?"Next week":weekOff==-1?"Last week":pd(m).toLocaleDateString("en-GB",{day:"numeric",month:"short"});}
function nm(id){return X[id]?X[id][0]:id;}
function repLine(id,kg,r){return nm(id)+(kg?" "+kg+" kg":"")+" · "+r.v.join("/")+(r.u?" "+r.u:"");}
function hist(){var h=logs().slice().reverse().map(function(e){var w;if(e.wt&&Object.keys(e.wt).length)w=Object.keys(e.wt).filter(function(i){return e.wt[i];}).map(function(i){return nm(i)+": "+esc(e.wt[i])+" kg";}).join(", ");else w=Object.keys(e.w||{}).filter(function(i){return e.w[i]&&PUMPIDS[i];}).map(function(i){return nm(PUMPIDS[i])+": "+esc(e.w[i])+" kg";}).join(", ");if(e.rp&&Object.keys(e.rp).length)w=Object.keys(e.rp).map(function(i){return esc(repLine(i,e.wt&&e.wt[i],e.rp[i]));}).join("<br>");var x=[];if(e.sets!=null)x.push(e.sets+"/"+(e.of||18)+" sets");if(e.km)x.push(esc(e.km)+" km");if(e.feel)x.push("felt "+esc(e.feel)+"/10");if(e.breaks)x.push(e.breaks+" walk breaks");if(e.notes)x.push(esc(e.notes));if(x.length)w=(w?w+", ":"")+x.join(" · ");var op=typeOpts(e.date),ed=op.length>1?'<label class="hed">Edit: <select data-hd="'+e.date+'" data-hn="'+esc(e.name||"")+'">'+op.map(function(o){return '<option value="'+o[0]+'"'+((e.type||"main")==o[0]?" selected":"")+">"+o[1]+"</option>";}).join("")+"</select></label>":"";return "<li><b>"+e.date+"</b> · "+esc(e.name||"Pump + Cardio")+" – "+e.min+" min"+(w?"<br><small>"+w+"</small>":"")+ed+"</li>";}).join("");$("hist").innerHTML=h||"<li>No workouts yet</li>";}
function typeOpts(d){if(d<=LEGACY_END)return [];var b=baseSid(d);if(!b||!SESS[b])return [];var o=[["main","Main"]];if(BK[d]&&SESS[BK[d]])o.push(["backup","Backup"]);if(hasRI(SESS[b]))o.push(["run","Run instead"]);if(QK[d]&&SESS[QK[d]])o.push(["quick",SESS[QK[d]].name]);return o;}
function setType(d,t,oldName){setAlt(d,t=="backup");setRI(d,t=="run");setQ(d,t=="quick");var l=logs(),S=S_(d);for(var i=0;i<l.length;i++){var e=l[i];if(e.date==d&&(e.name||"")==oldName){e.type=t;e.sid=sid(d);e.name=S.name;delete e.custom;if(t=="run")e.ri=1;else delete e.ri;}}LS.set("wo_log",l);all();hist();}
function all(){title();week();if(isOpen)renderPanel();prog();}
function openDay(k){EDK=null;if(mode(k)=="pre")return;if(isOpen&&k==sel){closeP();return;}sel=k;isOpen=true;renderPanel();$("panel").classList.add("open");$("hint").classList.add("hid");all();}
function closeP(){isOpen=false;setTimeout(relWake,0);$("panel").classList.remove("open");$("hint").classList.remove("hid");all();}
function cyc(k){if(!editable(k))return;var o=LS.get("wo_plan",{})||{};if(k<=LEGACY_END){var n={Pump:"Run",Run:"Rest",Rest:"Pump"};o[k]=n[plan(k)];}else if(o[k]=="Rest")delete o[k];else o[k]="Rest";LS.set("wo_plan",o);all();}
// events
var lpT=null,lp=false,sx=0,sy=0,moved=false;
$("week").addEventListener("pointerdown",function(e){var b=e.target.closest("button.day");sx=e.clientX;sy=e.clientY;moved=false;lp=false;clearTimeout(lpT);if(!b)return;var k=b.dataset.d;if(editable(k))lpT=setTimeout(function(){lp=true;cyc(k);},550);});
$("week").addEventListener("pointermove",function(e){if(Math.abs(e.clientX-sx)>10||Math.abs(e.clientY-sy)>10){moved=true;clearTimeout(lpT);}});
$("week").addEventListener("pointerup",function(e){clearTimeout(lpT);var dx=e.clientX-sx;if(moved&&Math.abs(dx)>50&&Math.abs(dx)>Math.abs(e.clientY-sy)){if(dx<0)weekOff++;else if(!$("prev").disabled)weekOff--;week();}});
$("week").addEventListener("pointercancel",function(){clearTimeout(lpT);});
$("week").addEventListener("contextmenu",function(e){e.preventDefault();});
$("week").addEventListener("click",function(e){var b=e.target.closest("button.day");if(!b||lp||moved){lp=false;return;}var k=b.dataset.d;if(editing){cyc(k);return;}openDay(k);});
$("prev").onclick=function(){if(!this.disabled){weekOff--;week();}};$("next").onclick=function(){weekOff++;week();};
$("ed").onclick=function(){editing=!editing;this.textContent=editing?"Done":"Edit plan";week();};
$("close").onclick=closeP;$("stop").onclick=stopT;$("tpause").onclick=tPause;$("tback").onclick=tBack;$("tnext").onclick=tNext;
$("tqy").onclick=function(){doneT();};$("tqn").onclick=function(){doneT(true);};
$("rskip").onclick=stopRest;$("rm15").onclick=function(){restAdj(-15);};$("rp15").onclick=function(){restAdj(15);};
$("rbtn").onclick=function(){startRest(+LS.get("wo_restlast",90)||90,"Rest");};
$("snd").onclick=function(){unlock();};
(function(){var c=$("autorest");c.checked=autoRest();c.onchange=function(){LS.set("wo_autorest",c.checked);if(isOpen)renderSess();};})();
var SX=$("sess");
SX.addEventListener("click",function(e){var hb=e.target.closest("[data-h]");if(hb){howto(hb.dataset.h);return;}
var mo=e.target.closest("[data-mo]");if(mo){MO[mo.dataset.mo]=!MO[mo.dataset.mo];renderSess();return;}
var smb=e.target.closest("[data-sm]");if(smb){SM[smb.dataset.sm]=!SM[smb.dataset.sm];renderSess();return;}if(mode(sel)=="future")return;var t=e.target.closest("[data-t]");if(t){startT(t.dataset.t);return;}
if(e.target.closest("#brkb")){var r=R(sel);r.b++;LS.set("wo_run_"+sel,r);$("brk").textContent=r.b;return;}
var st=e.target.closest("[data-st]");if(st&&EDK){var S0=S_(sel),s0=P(sel),it0=itemByGi(S0,+EDK.split("_")[0]),c=st.dataset.st;s0.rp=s0.rp||{};
 if(c=="u"){s0.t[EDK]=false;delete s0.rp[EDK];EDK=null;}else if(c=="x"){EDK=null;}else{var v=repV(s0,EDK,it0)+(+c)*stepOf(it0);s0.rp[EDK]=Math.max(0,Math.min(99*stepOf(it0),v));}
 LS.set("wo_"+sel,s0);renderSess();prog();return;}
var pl=e.target.closest(".pill");if(pl){var S1=S_(sel),s1=P(sel),k1=pl.dataset.k,it1=itemByGi(S1,+k1.split("_")[0]);s1.rp=s1.rp||{};if(!s1.start)s1.start=Date.now();
 if(!s1.t[k1]){s1.t[k1]=true;if(s1.rp[k1]==null)s1.rp[k1]=it1.rp;EDK=k1;maybeRest(S1,s1,k1);if(X[it1.x][3]&&dayW(it1.x,sel)==null){var lw1=lastW(it1.x,sel);if(lw1)setW(it1.x,sel,lw1.v);}}else EDK=EDK==k1?null:k1;
 LS.set("wo_"+sel,s1);renderSess();prog();return;}
var b=e.target.closest("[data-k]"),a=e.target.closest("[data-a]"),S=S_(sel),s;
if(b){s=P(sel);var k=b.dataset.k;s.t[k]=!s.t[k];if(!s.start)s.start=Date.now();LS.set("wo_"+sel,s);if(s.t[k]){maybeRest(S,s,k);var gi=+k.split("_")[0],it=itemByGi(S,gi);if(it&&X[it.x][3]&&dayW(it.x,sel)==null){var lw=lastW(it.x,sel);if(lw){setW(it.x,sel,lw.v);var ip=SX.querySelector('input[data-w="'+gi+'"]');if(ip)ip.classList.remove("pf");}}}b.classList.toggle("on",s.t[k]);b.textContent=s.t[k]?"✓":(+k.split("_")[1]+1);prog();}
if(a){var it2=itemByGi(S,+a.dataset.a),inp=document.createElement("input");inp.className="w lock";inp.type="number";inp.inputMode="decimal";inp.placeholder=X[it2.x][2];inp.dataset.w=a.dataset.a;a.replaceWith(inp);inp.focus();}});
SX.addEventListener("input",function(e){if(mode(sel)=="future")return;var el=e.target;if(el.dataset.w!=null){var it=itemByGi(S_(sel),+el.dataset.w);if(it){setW(it.x,sel,el.value);el.classList.remove("pf");}return;}
var m=/^r_([dfn])$/.exec(el.id||"");if(m){var r=R(sel);r[m[1]]=el.value;LS.set("wo_run_"+sel,r);}});

SX.addEventListener("change",function(e){var el=e.target;if(el.dataset.w==null)return;var it=itemByGi(S_(sel),+el.dataset.w),last=it&&lastW(it.x,sel),c=el.closest(".card");if(!last||!c)return;var up=c.querySelector(".up"),hi=el.value!==""&&+el.value>+last.v;if(hi&&!up){var sp=document.createElement("span");sp.className="up";sp.textContent="↑";var nt=c.querySelectorAll(".note");nt[nt.length-1].append(" ",sp);}else if(!hi&&up)up.remove();});
function howto(k){var h=HT[k];if(!h)return;var nm0=X[k]?X[k][0]:k;$("hs_t").textContent=nm0;$("hs_u").textContent=h.u||"";
$("hs_b").innerHTML='<ol class="hs_s">'+h.s.map(function(x,i){return '<li><span class="hn">'+(i+1)+'</span><span>'+esc(x)+'</span></li>';}).join("")+'</ol><div class="hs_h">Form tips</div><ul class="hs_c">'+h.c.map(function(x){return "<li>"+esc(x)+"</li>";}).join("")+'</ul><p class="hs_m"><b>Avoid:</b> '+esc(h.m)+'</p>'+(h.z?'<p class="hs_m hs_z"><b>Safety:</b> '+esc(h.z)+'</p>':'');
$("hs_b").scrollTop=0;$("hs_l").href=demoURL(h.q||nm0);$("hs").classList.add("show");}
var hy=null;document.addEventListener("pointerdown",function(e){if(e.target.closest(".hs_g,.hs_top"))hy=e.clientY;});document.addEventListener("pointerup",function(e){if(hy!=null&&e.clientY-hy>60)hclose();hy=null;});
function hclose(){$("hs").classList.remove("show");}
$("hs").addEventListener("click",function(e){if(e.target===this||e.target.id=="hs_x")hclose();});
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
window.__wk={BK:BK,OVR:OVR,PROG:PROG,swapHref:swapHref};
var finBusy=false,ovAt=0;
$("fin").onclick=function(){var d=sel,S=S_(d),m=mode(d);if(finBusy||m=="future"||m=="pre"||!S||S.rest)return;finBusy=true;setTimeout(function(){finBusy=false;},1500);
var name=S.name,l=logs(),old=null,idx=-1;for(var i=0;i<l.length;i++)if(sameE(l[i],d,name)){old=l[i];idx=i;}
var s=P(d),r=R(d),st0=+LS.get("wo_runstart_"+d,0)||s.start||0,e={name:name,date:d},x=[],tot=setsTotal(S);
if(tot){var w={},wt={};items(S).forEach(function(it){var v=dayW(it.x,d);if(v!=null&&X[it.x][3]){wt[it.x]=v;if(sid(d)=="pump")w[it.gi]=v;}});e.w=w;e.wt=wt;e.sets=ticks(s);e.of=tot;x.push(e.sets+" of "+tot+" sets ticked");
 var rp={},ln=[];S.blocks.forEach(function(b){if(b.k=="ex")b.items.forEach(function(it){if(!it.rp)return;var a=[],any=false;for(var q=0;q<b.n;q++){var k=it.gi+"_"+q;if(s.t[k]){any=true;a.push(repV(s,k,it));}else a.push("–");}if(any){rp[it.x]={v:a,u:it.ru||""};ln.push(repLine(it.x,wt[it.x],rp[it.x]));}});});if(ln.length){e.rp=rp;x=x.concat(ln);}}
if(S.blocks.some(function(b){return b.k=="fields";})){e.km=r.d||"";e.feel=r.f||"";e.notes=r.n||"";if(e.km)x.push(e.km+" "+(sid(d)=="row"?"distance":"km"));if(e.feel)x.push("felt "+e.feel+"/10");}
if(S.blocks.some(function(b){return VB(b).counter;})){e.breaks=r.b;x.push(r.b+" walk breaks");}e.type=curType(d);e.sid=sid(d);if(S.isRun){e.ri=1;x.push("run instead");}else delete e.ri;if(old&&old.custom&&old.type==e.type){e.name=old.name;e.custom=1;}else if(old&&old.name&&old.name!=name&&isName(old.name,name))e.name=old.name;
if(!x.length)x.push(score(d).d+" of "+score(d).t+" parts done");
var mins=st0?Math.round((Date.now()-st0)/60000):0;if(d!=today||mins>180||!st0)mins=old?old.min:(d==today?Math.min(mins,180):30);e.min=mins;
if(idx>=0)l[idx]=e;else l.push(e);LS.set("wo_log",l);
$("o_n").textContent=name+(d!=today?" · "+d:"");$("o_t").textContent=e.min+" min";$("o_d").innerHTML=x.map(esc).join("<br>");$("o_e").textContent=(old?"Log updated. ":"")+ENC[Math.floor(Math.random()*ENC.length)];$("ov").classList.add("show");ovAt=Date.now();all();};
$("o_done").onclick=function(){if(Date.now()-ovAt<700)return;$("ov").classList.remove("show");};$("ov").onclick=function(e){if(e.target===this&&Date.now()-ovAt>700)this.classList.remove("show");};
$("rst").onclick=function(){var d=sel,S=S_(d);if(mode(d)=="future"||!S)return;if(!confirm("Reset "+(d==today?"today":d)+"'s ticks, timers and weights?"))return;LS.del("wo_"+d);LS.del("wo_run_"+d);LS.del("wo_runstart_"+d);items(S).forEach(function(it){setW(it.x,d,"");});if(T&&T.date==d)stopT();all();};
document.addEventListener("visibilitychange",function(){if(document.visibilityState=="visible"){unlock();if(T||RT||wantWake())wake();checkDay();loop();}});
function checkDay(){var n=ymd(new Date());if(n!=today){today=n;weekOff=0;all();}}
setInterval(checkDay,30000);
migrate();if(T&&(!T.segs||!T.t0))stopT();if(T){lastI=-2;wake();}
all();loop();
if("serviceWorker" in navigator&&/^https?:/.test(location.protocol)){var reload=false;navigator.serviceWorker.addEventListener("controllerchange",function(){if(reload)return;reload=true;location.reload();});
navigator.serviceWorker.register("sw.js").then(function(reg){function show(){var u=$("upd");u.style.display="block";u.onclick=function(){if(reg.waiting)reg.waiting.postMessage("skip");else location.reload();};}
if(reg.waiting&&navigator.serviceWorker.controller)show();reg.addEventListener("updatefound",function(){var w=reg.installing;if(w)w.addEventListener("statechange",function(){if(w.state=="installed"&&navigator.serviceWorker.controller)show();});});
setInterval(function(){reg.update().catch(function(){});},3600000);document.addEventListener("visibilitychange",function(){if(document.visibilityState=="visible")reg.update().catch(function(){});});}).catch(function(){});}
window.__app={get today(){return today;},get sel(){return sel;},checkDay:checkDay,sid:sid,view:function(){return S_(sel);},posOf:posOf};
})();
</script></body></html>
