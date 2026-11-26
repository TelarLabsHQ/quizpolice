(function(){
var $=function(s){return document.querySelector(s)},$$=function(s){return [].slice.call(document.querySelectorAll(s))};
function num(v){var n=parseFloat(String(v).replace(',','.'));return isNaN(n)?null:n}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
var TAB={'2026':__T2026__,'2015':__T2015__},SCALES=__SCALES__;
var S=keep('qp-quick')||{n:40,count:'wrong',step:1,scale:'letter',conv:'none',pass:60,dec:1};
var m=location.hash.match(/[#&]q=([^&]+)/);if(m){var a=decodeURIComponent(m[1]).split(',');if(a.length>=7){S={n:+a[0]||40,count:a[1]==='right'?'right':'wrong',step:+a[2]===.5?.5:1,scale:a[3],conv:a[4],pass:a[5]===''?null:num(a[5]),dec:+a[6]||0};$('#qgShared').hidden=false}history.replaceState(null,'',location.pathname)}
function ownTable(){var r=keep('qp-trans');if(!r)r={pp:60,pg:75,lg:60,tg:100};var pp=num(r.pp),pg=Math.round(num(r.pg)),lg=Math.round(num(r.lg)),tg=Math.round(num(r.tg));
  if(!(pp>0&&pp<100&&lg<pg&&pg<tg))return null;var t=[];for(var g=tg;g>=lg;g--)t.push([Math.round((g>=pg?pp+(g-pg)*(100-pp)/(tg-pg):(g-lg)*pp/(pg-lg))*100)/100,g]);return t}
function table(){return S.conv==='none'?null:S.conv==='own'?ownTable():TAB[S.conv]}
function conv(t,x){for(var i=0;i<t.length;i++)if(x>=t[i][0]-1e-9)return t[i][1];return t[t.length-1][1]}
function label(g){var b=SCALES[S.scale]||[];for(var i=0;i<b.length;i++)if(g>=b[i][0]-1e-9)return b[i][1];return ''}
function grade(p){var t=table(),d=S.dec;if(t){var g=conv(t,p),l=(S.scale==='desc'||S.scale==='desc15')?label(g):'';return {v:g,txt:g+(l?' '+l:'')}}
  var r=Math.round(p*Math.pow(10,d))/Math.pow(10,d);return {v:p,txt:(S.scale==='pct'?r.toFixed(d)+'%':label(p)||r.toFixed(d)+'%')}}
function passes(g){return S.pass===null||S.pass===''||g.v>=num(S.pass)-1e-9}
function rows(){var n=S.n,st=S.step,out=[];for(var k=0;k<=n+1e-9;k+=st){var right=S.count==='wrong'?n-k:k,p=right/n*100;out.push({k:k,p:p,g:grade(p)})}if(S.count==='right')out.reverse();return out}
function fk(k){return (Math.round(k*2)/2).toString()}
function draw(){var n=S.n;$('#qgCap').textContent=n+' items · '+(S.count==='wrong'?'number wrong':'number right')+(S.conv!=='none'?' · '+({'2026':'K to 12 adjusted table','2015':'K to 12 table (2015)','own':'your transmutation rule'}[S.conv]):'');
  if(S.conv==='own'&&!ownTable()){$('#qgChart').innerHTML='<p class="warnbox">Your transmutation rule isn’t set up. Make one in the <a href="/tools/transmutation-table/">transmutation table maker</a>.</p>';return}
  $('#qgChart').innerHTML=rows().map(function(r){return '<div class="qg-c'+(passes(r.g)?'':' fail')+'"><b>'+fk(r.k)+'</b><span>'+r.p.toFixed(S.dec)+'%</span><i>'+esc(r.g.txt)+'</i></div>'}).join('');
  $('#qgHead').innerHTML='<span>'+(S.count==='wrong'?'Wrong':'Right')+'</span><span>%</span><span>Grade</span>';look();keep('qp-quick',S)}
function look(){var v=num($('#qgK').value),r=$('#qgLook'),n=S.n;if(v===null||v<0||v>n){r.innerHTML='<span class="note2">Type the number '+(S.count==='wrong'?'wrong':'right')+', 0 to '+n+'.</span>';return}
  var p=(S.count==='wrong'?n-v:v)/n*100,g=grade(p);r.innerHTML='<div class="big"><span>'+(n-(S.count==='wrong'?v:n-v))+'/'+n+' · <b style="font-size:26px">'+p.toFixed(S.dec)+'%</b></span><span>Grade <b>'+esc(g.txt)+'</b></span>'+(S.pass!==null&&S.pass!==''?'<span class="note2">'+(passes(g)?'Passing':'Below passing')+'</span>':'')+'</div>'}
function sync(){$('#qgN').value=S.n;$('#qgCount').value=S.count;$('#qgStep').value=String(S.step);$('#qgScale').value=S.scale;$('#qgConv').value=S.conv;$('#qgPass').value=S.pass==null?'':S.pass;$('#qgDec').value=String(S.dec);$('#qgKL').firstChild.textContent=S.count==='wrong'?'Number wrong':'Number right'}
$('#qgN').oninput=function(){var v=Math.round(num(this.value));if(v>=1&&v<=500){S.n=v;draw()}};
$('#qgCount').onchange=function(){S.count=this.value;sync();draw()};$('#qgStep').onchange=function(){S.step=+this.value;draw()};
$('#qgScale').onchange=function(){S.scale=this.value;draw()};
$('#qgConv').onchange=function(){S.conv=this.value;if(this.value!=='none'){S.dec=Math.min(S.dec,1);if(S.pass===null||S.pass===''||num(S.pass)===60)S.pass=75;if(S.scale==='letter'||S.scale==='gpa')S.scale=this.value==='2015'?'desc15':this.value==='2026'?'desc':'pct'}else{if(S.scale==='desc'||S.scale==='desc15')S.scale='letter';if(num(S.pass)===75)S.pass=60}sync();draw()};
$('#qgPass').oninput=function(){S.pass=this.value===''?null:this.value;draw()};$('#qgDec').onchange=function(){S.dec=+this.value;draw()};$('#qgK').oninput=look;
$('#qgPrint').onclick=function(){window.print()};
$('#qgLink').onclick=function(){var u=location.origin+location.pathname+'#q='+encodeURIComponent([S.n,S.count,S.step,S.scale,S.conv,S.pass==null?'':S.pass,S.dec].join(',')),b=this;
  function ok(){b.textContent='✓ Link copied';setTimeout(function(){b.textContent='🔗 Copy link'},2000)}if(navigator.clipboard)navigator.clipboard.writeText(u).then(ok,function(){window.prompt('Copy this link:',u)});else window.prompt('Copy this link:',u)};
sync();draw();
})();
