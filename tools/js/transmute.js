(function(){
var $=function(s){return document.querySelector(s)},$$=function(s){return [].slice.call(document.querySelectorAll(s))};
function num(v){var n=parseFloat(String(v).replace(',','.'));return isNaN(n)?null:n}
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
var TAB={'2026':__T2026__,'2015':__T2015__};
var S=keep('qp-trans')||{mode:'own',pp:60,pg:75,lg:60,tg:100,items:40,view:'bands'};
var m=location.hash.match(/[#&]r=([\d.,-]+)/);if(m){var a=m[1].split(',').map(num);if(a.length===4&&a.every(function(x){return x!==null})){S.mode='own';S.pp=a[0];S.pg=a[1];S.lg=a[2];S.tg=a[3];$('#tmShared').hidden=false}history.replaceState(null,'',location.pathname)}
function r2(x){return Math.round(x*100+1e-9)/100}
function build(){ // [[lowest initial grade, transmuted grade]], highest first
  if(S.mode!=='own')return TAB[S.mode];
  var pp=num(S.pp),pg=Math.round(num(S.pg)),lg=Math.round(num(S.lg)),tg=Math.round(num(S.tg));
  if(pp===null||isNaN(pg)||isNaN(lg)||isNaN(tg)||!(pp>0&&pp<100)||!(lg<pg&&pg<tg))return null;
  var t=[];for(var g=tg;g>=lg;g--){var lo=g>=pg?pp+(g-pg)*(100-pp)/(tg-pg):(g-lg)*pp/(pg-lg);t.push([r2(lo),g])}return t}
function conv(t,x){for(var i=0;i<t.length;i++)if(x>=t[i][0]-1e-9)return t[i][1];return t[t.length-1][1]}
function fmt(x){return Number(x).toFixed(2)}
function draw(){var t=build(),own=S.mode==='own';$('#tmOwn').hidden=!own;
  $$('#tmModes button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.m===S.mode))});
  $$('#tmViews button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.v===S.view))});$('#tmItemsL').hidden=S.view!=='items';
  var w=$('#tmWarn');if(!t){w.hidden=false;w.textContent='Check the numbers: the passing score must be between 0 and 100, and the grades must go lowest < passing < highest.';$('#tmTable').innerHTML='';return}w.hidden=true;
  var pg=own?Math.round(num(S.pg)):75,h;
  $('#tmCap').textContent=(own?'Passing score '+S.pp+'% → '+pg+', from '+S.lg+' to '+S.tg:S.mode==='2026'?'K to 12 adjusted table (2026–2027)':'K to 12 table (2015)')+(S.view==='items'?' · '+S.items+' items':'');
  if(S.view==='items'){var n=Math.max(1,Math.min(500,Math.round(num(S.items)||1))),rows='';for(var s=n;s>=0;s--){var p=s/n*100,g=conv(t,p);rows+='<tr'+(g>=pg?'':' class="fail"')+'><td>'+s+'</td><td>'+fmt(p)+'%</td><td><b>'+g+'</b></td></tr>'}
    h='<thead><tr><th>Score</th><th>Percentage</th><th>Grade</th></tr></thead><tbody>'+rows+'</tbody>'}
  else h='<thead><tr><th>Initial grade (%)</th><th>Grade</th></tr></thead><tbody>'+t.map(function(r,i){var hi=i===0?100:r2(t[i-1][0]-0.01);return '<tr'+(r[1]>=pg?'':' class="fail"')+'><td>'+(i===0&&r[0]>=100?'100.00':fmt(r[0])+' – '+fmt(Math.max(r[0],hi)))+'</td><td><b>'+r[1]+'</b></td></tr>'}).join('')+'</tbody>';
  $('#tmTable').innerHTML=h;look();keep('qp-trans',S)}
function look(){var t=build(),v=num($('#tmIg').value),r=$('#tmLook');if(!t||v===null||v<0||v>100){r.innerHTML='<span class="note2">Type a percentage or initial grade from 0 to 100.</span>';return}
  var g=conv(t,v),pg=S.mode==='own'?Math.round(num(S.pg)):75;r.innerHTML='<div class="big"><span>Grade <b>'+g+'</b></span><span class="note2">'+(g>=pg?'Passing':'Below passing')+'</span></div>'}
$$('#tmModes button').forEach(function(b){b.onclick=function(){S.mode=b.dataset.m;draw()}});
$$('#tmViews button').forEach(function(b){b.onclick=function(){S.view=b.dataset.v;draw()}});
[['tmPp','pp'],['tmPg','pg'],['tmLg','lg'],['tmTg','tg'],['tmItems','items']].forEach(function(x){var el=$('#'+x[0]);el.value=S[x[1]];el.oninput=function(){S[x[1]]=this.value;draw()}});
$('#tmIg').oninput=look;
$('#tmPrint').onclick=function(){window.print()};
$('#tmCopy').onclick=function(){var rows=$$('#tmTable tr').map(function(tr){return [].slice.call(tr.children).map(function(td){return td.textContent}).join('\t')}).join('\n'),b=this;
  function ok(){b.textContent='✓ Copied';setTimeout(function(){b.textContent='Copy table'},1800)}if(navigator.clipboard)navigator.clipboard.writeText(rows).then(ok,function(){})};
$('#tmUse').onclick=function(){var t=build();if(!t)return;var s=t.map(function(r){return r[0]+':'+r[1]}).join(',');location.href='/tools/grade-calculator/#t='+encodeURIComponent(s)+'&pass='+(S.mode==='own'?Math.round(num(S.pg)):75)};
$('#tmLink').onclick=function(){var u=location.origin+location.pathname+'#r='+[S.pp,S.pg,S.lg,S.tg].join(','),b=this;function ok(){b.textContent='✓ Link copied';setTimeout(function(){b.textContent='🔗 Copy link to my rule'},2000)}
  if(navigator.clipboard)navigator.clipboard.writeText(u).then(ok,function(){window.prompt('Copy this link:',u)});else window.prompt('Copy this link:',u)};
draw();
})();
