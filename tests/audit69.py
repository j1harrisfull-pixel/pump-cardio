# shared by test_v69: contrast and name sweeps over the visible page
AUD = r"""() => {
 function parse(c){var m=(c||'').match(/[\d.]+/g);if(!m)return {r:0,g:0,b:0,a:0};m=m.map(Number);return {r:m[0],g:m[1],b:m[2],a:m.length>3?m[3]:1};}
 function lum(c){var f=function(v){v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b);}
 function blend(t,b){var a=t.a;return {r:t.r*a+b.r*(1-a),g:t.g*a+b.g*(1-a),b:t.b*a+b.b*(1-a),a:1};}
 function bgOf(el){var st=[];for(var e=el;e;e=e.parentElement){var cs=getComputedStyle(e),c=parse(cs.backgroundColor);if(c.a>0)st.push(c);if(c.a>=1)break;}
  var bg=st.length&&st[st.length-1].a>=1?st.pop():{r:255,g:255,b:255,a:1};while(st.length)bg=blend(st.pop(),bg);return bg;}
 function op(el){var o=1;for(var e=el;e;e=e.parentElement)o*=+getComputedStyle(e).opacity;return o;}
 var bad=[],names=[];
 var all=document.querySelectorAll('body *');
 all.forEach(function(e){
  var r=e.getBoundingClientRect();if(r.width<2||r.height<2)return;var cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none')return;
  if(e.closest('.vh,[hidden],#cue,#hxl,#snda'))return;if(op(e)<.05||getComputedStyle(e).pointerEvents==='none')return;
  if(r.bottom<0||r.top>innerHeight*3)return;
  if(e.tagName==='BUTTON'&&!e.disabled){var nm=(e.textContent||'').trim()||e.getAttribute('aria-label')||e.getAttribute('title');if(!nm)names.push((e.id||e.className||'button')+'');}
  var own=[].some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim().length>0});if(!own)return;
  if(e.disabled)return;
  var fg=parse(cs.color),bg=bgOf(e),o=op(e);fg=blend({r:fg.r,g:fg.g,b:fg.b,a:fg.a*o},bg);
  var L1=lum(fg),L2=lum(bg),ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05),fs=parseFloat(cs.fontSize),bold=+cs.fontWeight>=700;
  var need=(fs>=24||(fs>=18.66&&bold))?3:4.5;
  if(ratio<need)bad.push([(e.id?'#'+e.id:'')+'.'+(typeof e.className==='string'?e.className.split(' ')[0]:'')+' "'+(e.textContent||'').trim().slice(0,22)+'"',Math.round(ratio*100)/100,need]);
 });
 return {bad:bad,names:names,hscroll:document.documentElement.scrollWidth>innerWidth+1};
}"""
