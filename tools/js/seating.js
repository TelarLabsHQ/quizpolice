(function(){
var $=function(s){return document.querySelector(s)},$$=function(s){return [].slice.call(document.querySelectorAll(s))};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;var t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function shuf(a,r){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(r()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
var L='ABCD';
var S=keep('qp-seating')||{title:'',rows:5,cols:6,sets:2,names:'',order:'random',gap:'all',blocked:[],seed:Date.now()%1e9,seats:null,setOf:null};
$('#scTitle').value=S.title;$('#scRows').value=S.rows;$('#scCols').value=S.cols;$('#scSets').value=String(S.sets);$('#scNames').value=S.names;$('#scOrder').value=S.order;$('#scGap').value=S.gap;
function names(){return S.names.split(/\n/).map(function(x){return x.trim()}).filter(Boolean)}
function read(){S.title=$('#scTitle').value;S.rows=Math.max(1,Math.min(20,+$('#scRows').value||1));S.cols=Math.max(1,Math.min(20,+$('#scCols').value||1));S.sets=+$('#scSets').value;S.names=$('#scNames').value;S.order=$('#scOrder').value;S.gap=$('#scGap').value}
function save(){keep('qp-seating',S)}
function key(r,c){return r+'-'+c}
function usable(r,c){if(S.blocked.indexOf(key(r,c))>=0)return false;if(S.gap==='alt')return (r+c)%2===0;if(S.gap==='row')return r%2===0;return true}
function assignSets(list){ // greedy: each seat takes the set least like its neighbors, keeping the counts even
  var setOf={},count=[0,0,0,0];if(S.sets<2){list.forEach(function(k){setOf[k]=0});return setOf}
  list.forEach(function(k){var a=k.split('-').map(Number),best=-1,bs=1e9;
    for(var s=0;s<S.sets;s++){var sc=0;for(var dr=-2;dr<=2;dr++)for(var dc=-2;dc<=2;dc++){if(!dr&&!dc)continue;var o=setOf[key(a[0]+dr,a[1]+dc)];if(o===s){var d=Math.max(Math.abs(dr),Math.abs(dc));sc+=d===1?(dr===0||dc===0?10:6):1}}
      sc+=count[s]*0.01;if(sc<bs){bs=sc;best=s}}
    setOf[k]=best;count[best]++});return setOf}
function make(){read();var ns=names(),r=rng(S.seed);
  if(S.order==='random')ns=shuf(ns,r);else if(S.order==='alpha')ns=ns.slice().sort(function(a,b){var la=a.split(/\s+/).pop(),lb=b.split(/\s+/).pop();return la.localeCompare(lb)||a.localeCompare(b)});
  var seats=[];for(var i=0;i<S.rows;i++)for(var j=0;j<S.cols;j++)if(usable(i,j))seats.push(key(i,j));
  S.seats={};ns.slice(0,seats.length).forEach(function(n,i){S.seats[seats[i]]=n});
  S.setOf=assignSets(seats.filter(function(k){return S.seats[k]}));save();draw()}
var mode='swap',sel=null;
function label(k){var a=k.split('-').map(Number);return 'Row '+(a[0]+1)+', Seat '+(a[1]+1)}
function draw(){var ns=names(),placed=Object.keys(S.seats||{}).length,miss=ns.length-placed;
  $('#scRes').hidden=false;$('#scHead').textContent=S.title||'Exam seating chart';
  $('#scWarn').hidden=miss<=0;$('#scWarn').textContent=miss>0?miss+' student'+(miss>1?'s don’t':' doesn’t')+' have a seat. Add rows or seats, or use less spacing.':'';
  var counts=[0,0,0,0];Object.keys(S.seats).forEach(function(k){counts[S.setOf[k]||0]++});
  $('#scInfo').textContent=placed+' students seated'+(S.sets>1?' · '+counts.slice(0,S.sets).map(function(c,i){return 'Set '+L[i]+': '+c}).join(', '):'');
  var g=$('#scGrid');g.style.gridTemplateColumns='repeat('+S.cols+',minmax(86px,1fr))';var h='';
  for(var i=0;i<S.rows;i++)for(var j=0;j<S.cols;j++){var k=key(i,j),n=S.seats[k],b=S.blocked.indexOf(k)>=0,st=S.setOf&&S.setOf[k];
    h+='<button type="button" class="seat'+(b?' block':n?'':' empty')+(n&&S.sets>1?' t'+st:'')+(sel===k?' sel':'')+'" data-k="'+k+'" aria-label="'+label(k)+(n?': '+esc(n):b?': blocked':': empty')+'"><b>'+(b?'Blocked':n?esc(n):'')+'</b><small><span>R'+(i+1)+' S'+(j+1)+'</span>'+(n&&S.sets>1?'<span class="st s'+st+'">'+L[st]+'</span>':'')+'</small></button>'}
  g.innerHTML=h;$$('.seat').forEach(function(b){b.onclick=function(){tap(b.dataset.k)}});
  var list=Object.keys(S.seats).map(function(k){return [S.seats[k],k]}).sort(function(a,b){return a[0].localeCompare(b[0])});
  $('#scList').innerHTML=list.map(function(x){return '<li><b>'+esc(x[0])+'</b> · '+label(x[1])+(S.sets>1?' · Set '+L[S.setOf[x[1]]]:'')+'</li>'}).join('')}
function tap(k){if(mode==='block'){var i=S.blocked.indexOf(k);if(i>=0)S.blocked.splice(i,1);else{S.blocked.push(k);if(S.seats[k]){var n=S.seats[k];delete S.seats[k];var free=null;
      for(var r=0;r<S.rows&&!free;r++)for(var c=0;c<S.cols&&!free;c++){var kk=key(r,c);if(usable(r,c)&&!S.seats[kk])free=kk}if(free)S.seats[free]=n}}
    S.setOf=assignSets(Object.keys(S.seats).sort(function(a,b){var x=a.split('-').map(Number),y=b.split('-').map(Number);return x[0]-y[0]||x[1]-y[1]}));save();draw();return}
  if(S.blocked.indexOf(k)>=0)return;
  if(!sel){if(!S.seats[k])return;sel=k;draw();return}
  if(sel===k){sel=null;draw();return}
  var a=S.seats[sel],b=S.seats[k];if(b)S.seats[sel]=b;else delete S.seats[sel];S.seats[k]=a;
  if(S.setOf[k]===undefined){S.setOf=assignSets(Object.keys(S.seats).sort(function(a,b){var x=a.split('-').map(Number),y=b.split('-').map(Number);return x[0]-y[0]||x[1]-y[1]}))}
  sel=null;save();draw()}
$('#scGo').onclick=function(){S.blocked=S.blocked.filter(function(k){var a=k.split('-').map(Number);return a[0]<+$('#scRows').value&&a[1]<+$('#scCols').value});make()};
$('#scRe').onclick=function(){S.seed=(S.seed*31+12345)%1e9;if($('#scOrder').value!=='random')$('#scOrder').value='random';make()};
$('#scModeSwap').onclick=function(){mode='swap';sel=null;this.setAttribute('aria-pressed','true');$('#scModeBlock').setAttribute('aria-pressed','false');draw()};
$('#scModeBlock').onclick=function(){mode='block';sel=null;this.setAttribute('aria-pressed','true');$('#scModeSwap').setAttribute('aria-pressed','false');draw()};
$('#scProj').onclick=function(){document.body.classList.add('sc-proj');document.documentElement.classList.add('sc-proj');try{document.documentElement.requestFullscreen()}catch(e){}};
$('#scExit').onclick=function(){document.body.classList.remove('sc-proj');document.documentElement.classList.remove('sc-proj');try{if(document.fullscreenElement)document.exitFullscreen()}catch(e){}};
document.addEventListener('keydown',function(e){if(e.key==='Escape'){document.body.classList.remove('sc-proj');document.documentElement.classList.remove('sc-proj')}});
$('#scPrintBtn').onclick=function(){window.print()};
['scTitle'].forEach(function(id){$('#'+id).oninput=function(){S.title=this.value;save();if(S.seats)$('#scHead').textContent=S.title||'Exam seating chart'}});
if(S.seats&&Object.keys(S.seats).length)draw();
})();
