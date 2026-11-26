(function(){
var $=function(s){return document.querySelector(s)},$$=function(s){return [].slice.call(document.querySelectorAll(s))};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;var t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function shuf(a,r){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(r()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
var L='ABCDEFGHIJ';
var SAMPLE='# Part I. Multiple choice\nWhat is the largest planet in our solar system?\na) Earth\nb) Jupiter *\nc) Mars\nd) Saturn\n\nWhich gas do plants take in to make food?\na) Oxygen\nb) Nitrogen\nc) Carbon dioxide *\nd) Hydrogen\n\nWhat is the boiling point of water at sea level?\na) 50 °C\nb) 90 °C\nc) 100 °C *\nd) 120 °C\n\nWhich of these are mammals?\na) Whales\nb) Bats\nc) Both A and B *\nd) Neither A nor B\n\n# Part II. True or false\nThe Pacific is the largest ocean on Earth.\na) True *\nb) False\n\nSound travels faster than light.\na) True\nb) False *\n\n# Part III. Identification\nWhat do you call the process by which plants make food from sunlight?\nAnswer: Photosynthesis';
var S=keep('qp-shuffler')||{title:'',school:'',ins:'Choose the letter of the best answer.',text:SAMPLE,sets:3,q:true,c:true,a:true,seed:Date.now()%1e9};
$('#tsTitle').value=S.title;$('#tsSchool').value=S.school;$('#tsIns').value=S.ins;$('#tsText').value=S.text;$('#tsSets').value=String(S.sets);$('#tsQ').checked=S.q;$('#tsC').checked=S.c;$('#tsA').checked=S.a;
function read(){S.title=$('#tsTitle').value;S.school=$('#tsSchool').value;S.ins=$('#tsIns').value;S.text=$('#tsText').value;S.sets=+$('#tsSets').value;S.q=$('#tsQ').checked;S.c=$('#tsC').checked;S.a=$('#tsA').checked;keep('qp-shuffler',S)}

var CH=/^\(?([a-jA-J])\s*[\).:]\s*(.*)$/,ANS=/^(answer|ans|key|correct answer)\s*[:\-]\s*(.+)$/i,PIN=/(all|none|both|neither) of (the )?(above|these)|^(both|neither)\s+[a-j]\s+(and|nor)\s+[a-j]\b|^[a-j]\s+and\s+[a-j]$|^(true|false|yes|no)$/i;
function parse(text){var parts=[{h:'',qs:[]}],warn=[];
  text.replace(/\r/g,'').split(/\n\s*\n/).forEach(function(block){var lines=block.split('\n').map(function(l){return l.trim()}).filter(Boolean);if(!lines.length)return;
    var q={t:[],ch:[],ans:null,key:'',n:0};
    lines.forEach(function(l){var m;
      if(l.charAt(0)==='#'){if(q.t.length||q.ch.length){push(q);q={t:[],ch:[],ans:null,key:'',n:0}}parts.push({h:l.replace(/^#+\s*/,''),qs:[]});return}
      if((m=l.match(ANS))){var a=m[2].trim();if(q.ch.length&&/^[a-j]$/i.test(a.replace(/[\).]$/,'')))q.ans=L.indexOf(a.charAt(0).toUpperCase());else q.key=a;return}
      if(q.t.length&&(m=l.match(CH))&&m[2]){var t=m[2],star=/\s*\*$/.test(t)||/^\*\s*/.test(t);t=t.replace(/\s*\*$/,'').replace(/^\*\s*/,'');if(star)q.ans=q.ch.length;q.ch.push(t);return}
      if(q.ch.length){push(q);q={t:[],ch:[],ans:null,key:'',n:0}}
      q.t.push(q.t.length?l:l.replace(/^\d+\s*[\).]\s*/,''))});
    if(q.t.length||q.ch.length)push(q)});
  function push(q){q.pin=q.ch.some(function(c){return PIN.test(c)});parts[parts.length-1].qs.push(q)}
  parts=parts.filter(function(p){return p.qs.length||p.h});var n=0;parts.forEach(function(p){p.qs.forEach(function(q){q.n=++n;if(q.ch.length&&q.ans===null)warn.push(n)})});
  return {parts:parts,n:n,warn:warn}}

var R=null,view=0;
function make(){read();var P=parse(S.text);if(!P.n){$('#tsWarn').hidden=false;$('#tsWarn').textContent='Type or paste at least one question.';$('#tsRes').hidden=true;return}
  $('#tsWarn').hidden=!P.warn.length;$('#tsWarn').textContent=P.warn.length?'No answer marked for question'+(P.warn.length>1?'s ':' ')+P.warn.join(', ')+'. Add a * after the correct choice, or the key will show a dash.':'';
  var sets=[];for(var s=0;s<S.sets;s++){var r=rng(S.seed+s*7919),orig=S.a&&s===0;
    sets.push(P.parts.map(function(p){var qs=(S.q&&!orig)?shuf(p.qs,r):p.qs.slice();
      return {h:p.h,qs:qs.map(function(q){var idx=q.ch.map(function(_,i){return i});if(S.c&&!orig&&!q.pin)idx=shuf(idx,r);return {q:q,idx:idx}})}}))}
  R={P:P,sets:sets};$('#tsRes').hidden=false;$('#tsInfo').textContent=P.n+' questions, '+S.sets+' sets.';
  $('#tsTabs').innerHTML=sets.map(function(_,i){return '<button type="button" data-v="'+i+'">Set '+L[i]+'</button>'}).join('')+'<button type="button" data-v="k">Answer keys</button>';
  $$('#tsTabs button').forEach(function(b){b.onclick=function(){view=b.dataset.v==='k'?'k':+b.dataset.v;show()}});
  $('#tsWhat').innerHTML='<option value="all">All sets, then the answer keys</option><option value="sets">All sets (no keys)</option>'+sets.map(function(_,i){return '<option value="'+i+'">Set '+L[i]+' only</option>'}).join('')+'<option value="k">Answer keys only</option>';
  if(view!=='k'&&view>=sets.length)view=0;show()}
function sheet(i){var set=R.sets[i],n=0;
  return '<div class="sheet">'+(S.school?'<div class="sub" style="font-weight:600">'+esc(S.school)+'</div>':'')+'<h3>'+esc(S.title||'Test')+'</h3><div class="sub">Set '+L[i]+'</div>'+
   '<div class="who"><span>Name:</span><span>Score:</span><span>Section / Class:</span><span>Date:</span></div>'+(S.ins?'<p class="ins">'+esc(S.ins)+'</p>':'')+
   set.map(function(p){var start=n+1;var body='<ol class="qs" start="'+start+'">'+p.qs.map(function(x){n++;var q=x.q,longc=q.ch.some(function(c){return c.length>38});
     return '<li>'+q.t.map(esc).join('<br>')+(q.ch.length?'<div class="ch'+(longc?' one':'')+'">'+x.idx.map(function(ci,k){return '<span>'+L[k]+'. '+esc(q.ch[ci])+'</span>'}).join('')+'</div>':' <span class="blank"></span>')+'</li>'}).join('')+'</ol>';
     return (p.h?'<h4>'+esc(p.h)+'</h4>':'')+body}).join('')+'</div>'}
function keyOf(i){var out=[],n=0;R.sets[i].forEach(function(p){p.qs.forEach(function(x){n++;var q=x.q,a;
   if(q.ch.length)a=q.ans===null?'–':L[x.idx.indexOf(q.ans)];else a=q.key?esc(q.key):'–';
   out.push('<span><b>'+n+'.</b> '+a+' <small>(Q'+q.n+')</small></span>')})});return out.join('')}
function keys(){return '<div class="sheet"><h3>'+esc(S.title||'Test')+': answer keys</h3><p class="sub" style="font-weight:400">(Q#) is the question’s number in the original list, for item analysis.</p>'+R.sets.map(function(_,i){return '<h4>Set '+L[i]+'</h4><div class="keys">'+keyOf(i)+'</div>'}).join('')+'</div>'}
function show(){$$('#tsTabs button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.v===String(view)))});$('#tsOut').innerHTML=view==='k'?keys():sheet(view);$('#tsCopy').hidden=view==='k'}
function txt(i){var n=0,o=[(S.title||'Test')+' – Set '+L[i],''];R.sets[i].forEach(function(p){if(p.h)o.push(p.h,'');p.qs.forEach(function(x){n++;o.push(n+'. '+x.q.t.join(' '));x.idx.forEach(function(ci,k){o.push('   '+L[k]+'. '+x.q.ch[ci])});o.push('')})});return o.join('\n')}
$('#tsGo').onclick=make;$('#tsRe').onclick=function(){S.seed=(S.seed*31+12345)%1e9;make()};
['tsTitle','tsSchool','tsIns'].forEach(function(id){$('#'+id).oninput=function(){read();if(R)show()}});
$('#tsCopy').onclick=function(){var t=txt(view),b=this;function ok(){b.textContent='✓ Copied';setTimeout(function(){b.textContent='Copy this set as text'},1800)}if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,function(){});};
$('#tsPrintBtn').onclick=function(){var w=$('#tsWhat').value,h='';if(w==='all'||w==='sets')h=R.sets.map(function(_,i){return sheet(i)}).join('');else if(w!=='k')h=sheet(+w);if(w==='all'||w==='k')h+=keys();$('#tsPrint').innerHTML=h;window.print()};
if(S.text)make();
})();
