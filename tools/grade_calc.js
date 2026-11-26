(function(){
// Customizable grade calculator. Setup (categories, scale, conversion, terms) + scores live in this browser only;
// "Copy setup link" puts the setup (never the scores) in the link's #s= part, so nothing is sent to a server.
var P=__PRESETS__,TAB={'2026':__T2026__,'2015':__T2015__},SCALES=__SCALES__;
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
function num(v){if(v===null||v===undefined)return null;var n=parseFloat(String(v).replace(',','.'));return isNaN(n)?null:n}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
function clone(o){return JSON.parse(JSON.stringify(o))}
function fromPreset(id){var p=clone(P.filter(function(x){return x.id===id})[0]||P[0]);p.bands=p.bands||clone(SCALES[p.scale]||SCALES.pct);delete p.label;delete p.group;return p}
function blankScores(st){return st.cats.map(function(c){return c.parts?c.parts.map(function(){return ['','']}):[['',''],['',''],['','']]})}
function fit(){ // keep score lists in step with the categories
  D.sc=D.st.cats.map(function(c,i){var old=D.sc[i]||[];if(c.parts)return c.parts.map(function(_,j){return old[j]||['','']});return old.length?old:[['',''],['','']]});
  var n=D.st.terms||1;D.tg=(D.tg||[]).slice(0,n);while(D.tg.length<n)D.tg.push('')}
var D=keep('qp-gc2'),shared=null;
try{var m=location.hash.match(/[#&]s=([^&]+)/);if(m){var j=decodeURIComponent(escape(atob(m[1].replace(/-/g,'+').replace(/_/g,'/'))));shared=JSON.parse(j)}}catch(e){shared=null}
if(!D||!D.st)D={st:fromPreset(P[0].id),sc:null,tg:[],target:''};
if(shared&&shared.cats){var keepScores=D.st&&JSON.stringify(D.st.cats)===JSON.stringify(shared.cats);D.st=shared;if(!D.st.bands)D.st.bands=clone(SCALES[D.st.scale]||SCALES.pct);if(!keepScores)D.sc=null;
  $('#gcShared').hidden=false;$('#gcShared b').textContent=shared.name||'a shared setup';history.replaceState(null,'',location.pathname+location.search)}
if(!D.sc)D.sc=blankScores(D.st);fit();
function save(){keep('qp-gc2',D)}
function total(){return D.st.cats.reduce(function(s,c){return s+(num(c.w)||0)},0)}
function pct(list){var s=0,h=0,n=0;list.forEach(function(r){var a=num(r[0]),b=num(r[1]);if(a!==null&&b){s+=a;h+=b;n++}});return n?s/h*100:null}
function catPct(i){var c=D.st.cats[i],sc=D.sc[i];if(!c.parts)return {p:pct(sc),done:pct(sc)!==null?1:0};
  var tw=0,sw=0,dw=0;c.parts.forEach(function(pt,j){var w=num(pt.w)||0,p=pct([sc[j]]);tw+=w;if(p!==null){sw+=w*p;dw+=w}});
  return {p:dw&&dw>=tw-1e-9?sw/tw:null,part:dw?{sw:sw,dw:dw,tw:tw}:null,done:tw?dw/tw:0}}
function convTable(){var c=D.st.conv;if(c==='none'||!c)return null;if(c==='custom')return (D.st.ctab||[]).slice().sort(function(a,b){return b[0]-a[0]});return TAB[c]}
function convert(ig){var t=convTable();if(!t)return null;for(var i=0;i<t.length;i++)if(ig>=t[i][0]-1e-9)return t[i][1];return t.length?t[t.length-1][1]:null}
function minFor(g){var t=convTable();if(!t)return g;var best=null;t.forEach(function(r){if(r[1]>=g&&(best===null||r[0]<best))best=r[0]});return best}
function rnd(x,d){var f=Math.pow(10,d);return Math.round(x*f+1e-9)/f}
function label(g){var b=(D.st.bands||[]).slice().sort(function(a,b){return b[0]-a[0]});for(var i=0;i<b.length;i++)if(g>=num(b[i][0])-1e-9)return b[i][1];return ''}
function fmt(x,d){return x===null||x===undefined?'–':Number(x).toFixed(d)}

// ---------- setup editor ----------
function drawSetup(){var st=D.st;
  $('#gcName').value=st.name||'';
  $('#gcCats').innerHTML=st.cats.map(function(c,i){return '<div class="sc-cat"><div class="it sc-row"><input value="'+esc(c.n)+'" data-ci="'+i+'" data-f="n" aria-label="Category name"><input inputmode="decimal" value="'+esc(c.w)+'" data-ci="'+i+'" data-f="w" aria-label="Weight in percent"><span>%</span><button class="x" type="button" data-cdel="'+i+'" aria-label="Remove category">✕</button></div>'+
    (c.parts?'<div class="sc-parts"><span class="note2">Parts of '+esc(c.n||'this category')+' (their % add up to 100):</span>'+c.parts.map(function(p,j){return '<div class="it sc-row"><input value="'+esc(p.n)+'" data-ci="'+i+'" data-pj="'+j+'" data-f="n" aria-label="Part name"><input inputmode="decimal" value="'+esc(p.w)+'" data-ci="'+i+'" data-pj="'+j+'" data-f="w" aria-label="Part weight"><span>%</span><button class="x" type="button" data-pdel="'+i+'.'+j+'" aria-label="Remove part">✕</button></div>'}).join('')+'<button class="addit" type="button" data-padd="'+i+'">+ Add a part</button></div>'
      :'<button class="addit sc-split" type="button" data-split="'+i+'">Split into parts (e.g. Midterm 50%, Final 50%)</button>')+'</div>'}).join('');
  var t=total();$('#gcTot').innerHTML='Total: <b>'+rnd(t,2)+'%</b>'+(Math.abs(t-100)>.01?' <span style="color:var(--bad)">(should be 100%)</span>':' ✓');
  $('#gcScale').value=st.scale in SCALES?st.scale:'custom';
  $('#gcBands').innerHTML=(st.bands||[]).map(function(b,i){return '<div class="it sc-band"><span>From</span><input inputmode="decimal" value="'+esc(b[0])+'" data-bi="'+i+'" data-bj="0" aria-label="Lowest grade for this label"><input value="'+esc(b[1])+'" data-bi="'+i+'" data-bj="1" aria-label="Label"><button class="x" type="button" data-bdel="'+i+'" aria-label="Remove">✕</button></div>'}).join('');
  $('#gcPass').value=st.pass==null?'':st.pass;$('#gcConv').value=st.conv||'none';$('#gcDec').value=String(st.dec==null?1:st.dec);
  $('#gcCtabBox').hidden=st.conv!=='custom';$('#gcCtab').value=(st.ctab||[]).map(function(r){return r[0]+' '+r[1]}).join('\n');
  $('#gcTerms').value=String(st.terms||1);$('#gcTname').value=st.tname||'Term';
  $('#gcTwBox').hidden=(st.terms||1)<2;$('#gcTwEq').checked=!st.tw;
  $('#gcTw').hidden=!st.tw;$('#gcTw').innerHTML=st.tw?st.tw.map(function(w,i){return '<label>'+esc(st.tname||'Term')+' '+(i+1)+' %<input inputmode="decimal" value="'+esc(w)+'" data-tw="'+i+'"></label>'}).join(''):'';
  wireSetup()}
function changed(structure){if(structure)fit();save();drawScores();calc()}
function wireSetup(){var st=D.st;
  $$('#gcCats input').forEach(function(x){x.oninput=function(){var c=st.cats[+x.dataset.ci],o=x.dataset.pj!=null?c.parts[+x.dataset.pj]:c;o[x.dataset.f]=x.value;
    var t=total();$('#gcTot').innerHTML='Total: <b>'+rnd(t,2)+'%</b>'+(Math.abs(t-100)>.01?' <span style="color:var(--bad)">(should be 100%)</span>':' ✓');changed()}});
  $$('[data-cdel]').forEach(function(b){b.onclick=function(){if(st.cats.length<2)return;var i=+b.dataset.cdel;st.cats.splice(i,1);D.sc.splice(i,1);drawSetup();changed(1)}});
  $$('[data-split]').forEach(function(b){b.onclick=function(){var i=+b.dataset.split;st.cats[i].parts=[{n:'Part 1',w:50},{n:'Part 2',w:50}];D.sc[i]=[['',''],['','']];drawSetup();changed(1)}});
  $$('[data-padd]').forEach(function(b){b.onclick=function(){var i=+b.dataset.padd;st.cats[i].parts.push({n:'Part '+(st.cats[i].parts.length+1),w:''});drawSetup();changed(1)}});
  $$('[data-pdel]').forEach(function(b){b.onclick=function(){var a=b.dataset.pdel.split('.'),i=+a[0],j=+a[1],c=st.cats[i];c.parts.splice(j,1);D.sc[i].splice(j,1);if(c.parts.length<2){c.parts=null;D.sc[i]=[['',''],['','']]}drawSetup();changed(1)}});
  $$('#gcBands input').forEach(function(x){x.oninput=function(){st.bands[+x.dataset.bi][+x.dataset.bj]=x.dataset.bj==='0'?x.value:x.value;st.scale='custom';$('#gcScale').value='custom';changed()}});
  $$('[data-bdel]').forEach(function(b){b.onclick=function(){st.bands.splice(+b.dataset.bdel,1);st.scale='custom';drawSetup();changed()}});
  $$('#gcTw input').forEach(function(x){x.oninput=function(){st.tw[+x.dataset.tw]=x.value;changed()}})}
$('#gcName').oninput=function(){D.st.name=this.value;save()};
$('#gcAddCat').onclick=function(){D.st.cats.push({n:'Category '+(D.st.cats.length+1),w:'',parts:null});D.sc.push([['',''],['','']]);drawSetup();changed(1)};
$('#gcScale').onchange=function(){D.st.scale=this.value;if(this.value!=='custom')D.st.bands=clone(SCALES[this.value]);drawSetup();changed()};
$('#gcAddBand').onclick=function(){D.st.bands.push(['','']);D.st.scale='custom';drawSetup()};
$('#gcPass').oninput=function(){D.st.pass=this.value===''?null:this.value;changed()};
$('#gcConv').onchange=function(){D.st.conv=this.value;if(this.value==='custom'&&!(D.st.ctab||[]).length)D.st.ctab=clone(TAB['2026']);drawSetup();changed()};
$('#gcCtab').oninput=function(){D.st.ctab=this.value.split(/\n+/).map(function(l){var a=l.trim().split(/[\s,;→>-]+/).map(num);return a.length>=2&&a[0]!==null&&a[1]!==null?[a[0],a[1]]:null}).filter(Boolean);changed()};
$('#gcDec').onchange=function(){D.st.dec=+this.value;changed()};
$('#gcTerms').onchange=function(){D.st.terms=+this.value;if(D.st.tw){D.st.tw=D.st.tw.slice(0,D.st.terms);while(D.st.tw.length<D.st.terms)D.st.tw.push('')}drawSetup();changed(1)};
$('#gcTname').onchange=function(){D.st.tname=this.value;drawSetup();changed(1)};
$('#gcTwEq').onchange=function(){D.st.tw=this.checked?null:Array.from({length:D.st.terms},function(){return rnd(100/D.st.terms,2)});drawSetup();changed()};

// ---------- presets ----------
(function(){var groups={};P.forEach(function(p){(groups[p.group]=groups[p.group]||[]).push(p)});
  $('#gcPreset').innerHTML='<option value="">Choose a ready setup…</option>'+Object.keys(groups).map(function(g){return '<optgroup label="'+esc(g)+'">'+groups[g].map(function(p){return '<option value="'+p.id+'">'+esc(p.label)+'</option>'}).join('')+'</optgroup>'}).join('')})();
$('#gcPreset').onchange=function(){if(!this.value)return;var has=D.sc.some(function(l){return l.some(function(r){return r[0]!==''})});
  if(has&&!window.confirm('Switch to this setup? Scores you typed for the current setup will be cleared.')){this.value='';return}
  D.st=fromPreset(this.value);D.sc=blankScores(D.st);D.tg=[];fit();this.value='';$('#gcShared').hidden=true;drawSetup();changed();
  $('#gcSetup').open=D.st.id==='custom'};
$('#gcLink').onclick=function(){var st=clone(D.st);if(st.scale!=='custom')delete st.bands;if(st.conv!=='custom')delete st.ctab;
  var s=btoa(unescape(encodeURIComponent(JSON.stringify(st)))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
  var u=location.origin+location.pathname+'#s='+s,b=this;function ok(){b.textContent='✓ Link copied';setTimeout(function(){b.textContent='🔗 Copy setup link'},2000)}
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(ok,function(){window.prompt('Copy this link:',u)});else window.prompt('Copy this link:',u)};
$('#gcClear').onclick=function(){if(!window.confirm('Clear all scores? Your setup stays.'))return;D.sc=blankScores(D.st);D.tg=[];fit();changed()};

// ---------- scores ----------
function row(i,j,v,lab){return '<div class="it"><input inputmode="decimal" placeholder="'+(lab?esc(lab):'Score')+'" value="'+esc(v[0])+'" data-si="'+i+'" data-sj="'+j+'" data-k="0" aria-label="'+(lab?esc(lab)+' score':'Score')+'"><span>out of</span><input inputmode="decimal" placeholder="Total" value="'+esc(v[1])+'" data-si="'+i+'" data-sj="'+j+'" data-k="1" aria-label="Highest possible score"><button class="x" type="button" '+(lab?'disabled style="visibility:hidden"':'data-sdel="'+i+'.'+j+'"')+' aria-label="Remove">✕</button></div>'}
function drawScores(){$('#gcScores').innerHTML=D.st.cats.map(function(c,i){var sc=D.sc[i];
  return '<div class="comp"><h3>'+esc(c.n||'Category '+(i+1))+' <span>'+esc(c.w===''?'?':c.w)+'%</span></h3>'+(c.parts?'<p class="note2" style="margin:0">'+c.parts.map(function(p){return esc(p.n)+' '+esc(p.w)+'%'}).join(' · ')+'</p>':'')+
   '<div class="items">'+(c.parts?c.parts.map(function(p,j){return row(i,j,sc[j],p.n)}).join(''):sc.map(function(v,j){return row(i,j,v)}).join(''))+'</div>'+
   (c.parts?'':'<button class="addit" type="button" data-sadd="'+i+'">+ Add a score</button>')+'</div>'}).join('');
  $$('#gcScores input').forEach(function(x){x.oninput=function(){D.sc[+x.dataset.si][+x.dataset.sj][+x.dataset.k]=x.value;calc()}});
  $$('[data-sdel]').forEach(function(b){b.onclick=function(){var a=b.dataset.sdel.split('.'),l=D.sc[+a[0]];if(l.length>1){l.splice(+a[1],1);drawScores();calc()}}});
  $$('[data-sadd]').forEach(function(b){b.onclick=function(){var i=+b.dataset.sadd;D.sc[i].push(['','']);drawScores();var l=$$('[data-si="'+i+'"][data-k="0"]');l[l.length-1].focus()}});
  var n=D.st.terms||1;$('#gcFinal').hidden=n<2;
  $('#gcTermIn').innerHTML=Array.from({length:n},function(_,i){return '<label>'+esc(D.st.tname||'Term')+' '+(i+1)+(D.st.tw?' ('+esc(D.st.tw[i])+'%)':'')+'<input inputmode="decimal" data-tg="'+i+'" value="'+esc(D.tg[i])+'"></label>'}).join('');
  $$('#gcTermIn input').forEach(function(x){x.oninput=function(){D.tg[+x.dataset.tg]=x.value;calcFinal()}});
  $('#gcTermName').textContent=(D.st.tname||'Term').toLowerCase()}

// ---------- results ----------
function gradeOf(ig){var c=convert(ig),d=D.st.dec==null?1:D.st.dec;return c!==null?c:rnd(ig,d)}
function verdict(g){var p=num(D.st.pass),l=label(g);return (l?'<span class="tag">'+esc(l)+'</span>':'')+(p!==null?'<span class="pf '+(g>=p-1e-9?'ok':'bad')+'">'+(g>=p-1e-9?'Passing':'Below the pass mark of '+p)+'</span>':'')}
function calc(){var st=D.st,W=total(),done=0,dw=0,rows=[],rem=[];
  st.cats.forEach(function(c,i){var w=num(c.w)||0,r=catPct(i);
    if(r.p!==null){done+=w*r.p;dw+=w}else if(r.part){done+=w*r.part.sw/r.part.tw;dw+=w*r.part.dw/r.part.tw;rem.push(esc(c.n)+' (remaining parts)')}else rem.push(esc(c.n)+' ('+w+'%)');
    rows.push('<tr><td>'+esc(c.n)+'</td><td>'+fmt(r.p,2)+'</td><td>'+w+'%</td><td>'+(r.p!==null?fmt(r.p*w/100,2):'–')+'</td></tr>')});
  var html='<table><tr><th>Category</th><th>Score %</th><th>Weight</th><th>Weighted</th></tr>'+rows.join('')+'</table>',out=$('#gcRes');
  if(Math.abs(W-100)>.01)html+='<p class="note2" style="color:var(--bad);margin:0">The weights add up to '+rnd(W,2)+'%, not 100%. Results are scaled to 100%.</p>';
  if(!dw){out.innerHTML=html+'<p class="note2" style="margin:0">Type a score and the total possible score in at least one category.</p>';$('#gcNeed').hidden=true;save();return}
  var full=dw>=W-1e-6,ig=rnd(done/(full?W:dw),2),g=gradeOf(ig),conv=convTable();
  html+='<div class="big"><span>'+(full?'':'So far ')+(conv?'Initial grade <b style="font-size:26px">'+fmt(ig,2)+'</b></span><span>Grade <b>'+g+'</b>':'Grade <b>'+fmt(g,st.dec==null?1:st.dec)+'</b>')+'</span>'+verdict(g)+'</div>';
  html+='<p class="note2" style="margin:0">'+(full?'':'Based on the '+rnd(dw,2)+'% of the grade that has scores so far. ')+(conv?'Converted with the '+({'2026':'2026–2027 adjusted','2015':'2015','custom':'your'}[st.conv])+' table. ':'')+'</p>';
  out.innerHTML=html;
  $('#gcNeed').hidden=full;if(!full){$('#gcNeedWhat').innerHTML=rem.join(', ');need(done,dw,W)}save()}
function need(done,dw,W){var t=num(D.target),r=$('#gcNeedRes');$('#gcTarget').value=D.target||'';
  if(t===null){r.innerHTML='<span class="note2">Type the grade you’re aiming for.</span>';return}
  var tig=minFor(t);if(tig===null){r.innerHTML='<span class="note2">That grade isn’t on the conversion table.</span>';return}
  var n=(tig*W-done)/(W-dw);
  r.innerHTML='<div class="big"><span>You need about <b>'+fmt(Math.max(0,n),1)+'%</b></span></div><span class="note2">'+(n>100?'That’s above 100%, so this target can’t be reached with the remaining work alone.':n<=0?'You’ve already reached it, even with zero on the rest.':'That’s the average score needed on the remaining work to reach '+t+(convTable()?' (an initial grade of '+fmt(tig,2)+')':'')+'.')+'</span>'}
$('#gcTarget').oninput=function(){D.target=this.value;calc()};
function calcFinal(){var n=D.st.terms||1,v=[],ws=[];for(var i=0;i<n;i++){var x=num(D.tg[i]);if(x!==null){v.push(x);ws.push(D.st.tw?num(D.st.tw[i])||0:1)}}
  var r=$('#gcFRes');save();if(v.length<n){r.innerHTML='<span class="note2">Type all '+n+' '+esc((D.st.tname||'term').toLowerCase())+' grades. The final grade is their '+(D.st.tw?'weighted ':'')+'average.</span>';return}
  var sw=ws.reduce(function(a,b){return a+b},0),f=v.reduce(function(a,x,i){return a+x*ws[i]},0)/sw,d=D.st.dec==null?1:D.st.dec,fg=rnd(f,d);
  r.innerHTML='<div class="big"><span>Final grade <b>'+fmt(fg,d)+'</b></span>'+verdict(fg)+'</div>'}
$('#gcUse').onclick=function(){var txt=$$('#gcRes .big b');if(!txt.length)return;var val=txt[txt.length-1].textContent;var i=D.tg.findIndex(function(x){return x===''});if(i<0)i=0;D.tg[i]=val;drawScores();calcFinal();$('#gcFinal').scrollIntoView({behavior:'smooth',block:'center'})};
drawSetup();drawScores();calc();calcFinal();
if(D.st.id==='custom')$('#gcSetup').open=true;
})();
