(function(){
// Flash card maker: decks are saved in this browser only; a share link carries the whole deck (compressed) after the # so nothing is sent to a server.
var $=function(s){return document.querySelector(s)},$$=function(s){return [].slice.call(document.querySelectorAll(s))};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function br(s){return esc(s).replace(/\n/g,'<br>')}
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,6)}
function shuf(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
var SAMPLE={id:'sample',t:'Science vocabulary',c:[['Photosynthesis','How plants use sunlight, water and carbon dioxide to make food'],['Evaporation','When a liquid turns into a gas, like water drying in the sun'],['Gravity','The force that pulls objects toward each other, like things falling to the ground'],['Habitat','The natural home of a plant or animal'],['Mammal','A warm-blooded animal with hair that feeds its young with milk'],['Atom','The smallest unit of an element'],['Ecosystem','Living things and their environment, working together'],['Condensation','When a gas turns into a liquid, like drops on a cold glass']]};
var D=keep('qp-flash')||{decks:[SAMPLE],cur:'sample'};if(!D.decks.length)D.decks=[SAMPLE];
function deck(){return D.decks.filter(function(d){return d.id===D.cur})[0]||D.decks[0]}
function cards(){return deck().c.filter(function(x){return String(x[0]).trim()||String(x[1]).trim()})}
function save(){keep('qp-flash',D)}
var tab='make';
// ---------- share links ----------
function b64u(bytes){var s='';for(var i=0;i<bytes.length;i++)s+=String.fromCharCode(bytes[i]);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'')}
function unb64u(s){s=s.replace(/-/g,'+').replace(/_/g,'/');var b=atob(s),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return a}
async function pack(obj){var raw=new TextEncoder().encode(JSON.stringify(obj));
  if(window.CompressionStream){try{var cs=new Blob([raw]).stream().pipeThrough(new CompressionStream('deflate-raw'));return 'z'+b64u(new Uint8Array(await new Response(cs).arrayBuffer()))}catch(e){}}return 'b'+b64u(raw)}
async function unpack(s){var k=s.charAt(0),bytes=unb64u(s.slice(1));
  if(k==='z'){var ds=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('deflate-raw'));bytes=new Uint8Array(await new Response(ds).arrayBuffer())}return JSON.parse(new TextDecoder().decode(bytes))}
// ---------- deck picker ----------
function drawDecks(){$('#fcDeck').innerHTML=D.decks.map(function(d){return '<option value="'+d.id+'"'+(d.id===deck().id?' selected':'')+'>'+esc(d.t||'Untitled deck')+' ('+d.c.length+')</option>'}).join('')}
$('#fcDeck').onchange=function(){D.cur=this.value;save();resetStudy();draw()};
$('#fcNew').onclick=function(){var d={id:uid(),t:'',c:[['',''],['',''],['','']]};D.decks.unshift(d);D.cur=d.id;save();tab='make';draw();$('#fcTitle').focus()};
$('#fcDel').onclick=function(){if(!window.confirm('Delete the deck “'+(deck().t||'Untitled deck')+'” from this device?'))return;D.decks=D.decks.filter(function(d){return d.id!==deck().id});if(!D.decks.length)D.decks=[{id:uid(),t:'',c:[['','']]}];D.cur=D.decks[0].id;save();resetStudy();draw()};
$('#fcShare').onclick=async function(){var c=cards();if(!c.length)return;var b=this,s=await pack({t:deck().t,c:c}),u=location.origin+location.pathname+'#d='+s;
  function ok(){b.textContent='✓ Link copied';setTimeout(function(){b.textContent='🔗 Share this deck'},2200)}
  $('#fcLinkNote').hidden=false;$('#fcLinkNote').textContent=u.length>6000?'This deck makes a long link ('+Math.round(u.length/1000)+'k characters). It works in most apps, but some chats may cut it. Splitting the deck in two is safer.':'Anyone with the link gets a copy of this deck. Their changes won’t affect yours.';
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(ok,function(){window.prompt('Copy this link:',u)});else window.prompt('Copy this link:',u)};
// ---------- make ----------
function make(){var d=deck();
  return '<label class="fc-l">Deck title<input id="fcTitle" maxlength="80" value="'+esc(d.t)+'" placeholder="e.g. Spanish greetings, Chapter 3 vocabulary"></label>'+
   '<div class="fc-rows">'+d.c.map(function(x,i){return '<div class="fc-row"><span class="fc-n">'+(i+1)+'</span><textarea rows="2" data-i="'+i+'" data-j="0" placeholder="Front: term or question" aria-label="Card '+(i+1)+' front">'+esc(x[0])+'</textarea><textarea rows="2" data-i="'+i+'" data-j="1" placeholder="Back: answer or meaning" aria-label="Card '+(i+1)+' back">'+esc(x[1])+'</textarea><button type="button" class="fc-x" data-del="'+i+'" aria-label="Delete card '+(i+1)+'">✕</button></div>'}).join('')+'</div>'+
   '<div class="fc-btns"><button type="button" class="fc-b" id="fcAdd">+ Add a card</button><span class="muted small">'+cards().length+' cards · saved on this device as you type</span></div>'+
   '<details class="fc-paste"><summary>Paste a list or two columns from a spreadsheet</summary><p class="muted small">One card per line. Put the front and back in two columns from Excel or Google Sheets, or separate them with a dash ( - ), a colon or a tab.</p><textarea id="fcBulk" rows="6" placeholder="Hola - Hello&#10;Gracias - Thank you&#10;Adiós - Goodbye"></textarea><div class="fc-btns"><button type="button" class="fc-b pri" id="fcBulkGo">Add these cards</button><span class="muted small" id="fcBulkMsg"></span></div></details>'}
function parseBulk(t){return t.replace(/\r/g,'').split('\n').map(function(l){l=l.trim();if(!l)return null;var m;
  if(l.indexOf('\t')>=0){m=l.split('\t');return [m[0].trim(),m.slice(1).join(' ').trim()]}
  m=l.match(/^(.+?)\s+[-–—=]\s+(.+)$/)||l.match(/^(.+?)\s*[:;]\s+(.+)$/)||l.match(/^(.+?)\s*,\s*(.+)$/);return m?[m[1].trim(),m[2].trim()]:[l,'']}).filter(Boolean)}
function wireMake(){var d=deck();
  $('#fcTitle').oninput=function(){d.t=this.value;save();drawDecks()};
  $$('.fc-rows textarea').forEach(function(x){x.oninput=function(){d.c[+x.dataset.i][+x.dataset.j]=x.value;save()};x.onchange=drawDecks});
  $$('[data-del]').forEach(function(b){b.onclick=function(){d.c.splice(+b.dataset.del,1);if(!d.c.length)d.c.push(['','']);save();drawDecks();draw()}});
  $('#fcAdd').onclick=function(){d.c.push(['','']);save();draw();var l=$$('.fc-rows textarea[data-j="0"]');l[l.length-1].focus()};
  $('#fcBulkGo').onclick=function(){var n=parseBulk($('#fcBulk').value);if(!n.length)return;d.c=d.c.filter(function(x){return String(x[0]).trim()||String(x[1]).trim()}).concat(n);save();drawDecks();draw();
    $('#fcBulkMsg').textContent='✓ Added '+n.length+' cards'}}
// ---------- study ----------
var ST=null;
function resetStudy(){ST=null}
function startStudy(only){var c=cards(),idx=c.map(function(_,i){return i});if(only)idx=only;if($('#fcShuf')&&$('#fcShuf').checked)idx=shuf(idx);ST={q:idx,i:0,flip:false,got:[],learn:[],rev:ST?ST.rev:false,shuf:ST?ST.shuf:false}}
function study(){var c=cards();if(!c.length)return '<p class="muted">Add some cards first.</p>';if(!ST)startStudy();
  if(ST.i>=ST.q.length)return '<div class="fc-done"><h3>Round done! 🎉</h3><p><b>'+ST.got.length+'</b> got it · <b>'+ST.learn.length+'</b> still learning</p><div class="fc-btns" style="justify-content:center">'+(ST.learn.length?'<button type="button" class="fc-b pri" id="fcAgainL">Study the '+ST.learn.length+' still-learning cards</button>':'')+'<button type="button" class="fc-b" id="fcAgain">Study all again</button><button type="button" class="fc-b" id="fcToQuiz">Take the quiz</button></div></div>';
  var x=c[ST.q[ST.i]],f=ST.rev?x[1]:x[0],b=ST.rev?x[0]:x[1];
  return '<div class="fc-opts"><label class="fc-chk"><input type="checkbox" id="fcShuf"'+(ST.shuf?' checked':'')+'> Shuffle</label><label class="fc-chk"><input type="checkbox" id="fcRev"'+(ST.rev?' checked':'')+'> Show the back first</label><span class="muted small">Card '+(ST.i+1)+' of '+ST.q.length+' · ✓ '+ST.got.length+'</span></div>'+
   '<div class="fc-bar"><i style="width:'+Math.round(ST.i/ST.q.length*100)+'%"></i></div>'+
   '<button type="button" class="fc-card'+(ST.flip?' flip':'')+'" id="fcCard" aria-live="polite" aria-label="Flash card. Tap to flip."><span class="fc-in"><span class="fc-face fc-front"><small>'+(ST.rev?'Back':'Front')+'</small><b>'+br(f)+'</b></span><span class="fc-face fc-back"><small>'+(ST.rev?'Front':'Back')+'</small><b>'+br(b)+'</b></span></span></button>'+
   '<p class="muted small" style="text-align:center;margin:6px 0 0">Tap the card or press Space to flip. Arrow keys move.</p>'+
   (ST.flip?'<div class="fc-btns fc-judge"><button type="button" class="fc-b learn" id="fcLearn">↻ Still learning</button><button type="button" class="fc-b got" id="fcGot">✓ Got it</button></div>':'<div class="fc-btns fc-judge"><button type="button" class="fc-b" id="fcPrev"'+(ST.i?'':' disabled')+'>◀ Back</button><button type="button" class="fc-b pri" id="fcFlip">Flip</button><button type="button" class="fc-b" id="fcSkip">Next ▶</button></div>')}
function wireStudy(){var on=function(id,f){var e=$('#'+id);if(e)e.onclick=f};
  on('fcCard',function(){ST.flip=!ST.flip;draw()});on('fcFlip',function(){ST.flip=true;draw()});
  on('fcGot',function(){ST.got.push(ST.q[ST.i]);ST.i++;ST.flip=false;draw()});on('fcLearn',function(){ST.learn.push(ST.q[ST.i]);ST.i++;ST.flip=false;draw()});
  on('fcSkip',function(){ST.i++;ST.flip=false;draw()});on('fcPrev',function(){if(ST.i){ST.i--;ST.flip=false;draw()}});
  on('fcAgain',function(){startStudy();draw()});on('fcAgainL',function(){startStudy(ST.learn.slice());draw()});on('fcToQuiz',function(){tab='quiz';QZ=null;draw()});
  var s=$('#fcShuf');if(s)s.onchange=function(){ST.shuf=this.checked;var r=ST.rev,sh=ST.shuf;startStudy();ST.rev=r;ST.shuf=sh;draw()};
  var r=$('#fcRev');if(r)r.onchange=function(){ST.rev=this.checked;ST.flip=false;draw()}}
// ---------- quiz ----------
var QZ=null;
function startQuiz(){var c=cards(),n=Math.min(10,c.length);QZ={q:shuf(c.map(function(_,i){return i})).slice(0,n),i:0,score:0,miss:[],pick:null,opts:null}}
function quiz(){var c=cards();if(c.length<4)return '<p class="muted">The quiz needs at least 4 cards, so there are wrong answers to choose from.</p>';if(!QZ)startQuiz();
  if(QZ.i>=QZ.q.length)return '<div class="fc-done"><h3>'+QZ.score+' / '+QZ.q.length+'</h3><p>'+(QZ.score===QZ.q.length?'Perfect score! 🌟':QZ.score>=QZ.q.length*.7?'Great job!':'Keep practicing, you’re getting there.')+'</p>'+
    (QZ.miss.length?'<div class="fc-miss"><b>Review:</b>'+QZ.miss.map(function(i){return '<div><b>'+br(c[i][0])+'</b> → '+br(c[i][1])+'</div>'}).join('')+'</div>':'')+
    '<div class="fc-btns" style="justify-content:center">'+(QZ.miss.length?'<button type="button" class="fc-b pri" id="fcStudyMiss">Study the ones I missed</button>':'')+'<button type="button" class="fc-b" id="fcQAgain">New quiz</button></div></div>';
  var k=QZ.q[QZ.i],x=c[k];if(!QZ.opts){var others=shuf(c.map(function(_,i){return i}).filter(function(i){return i!==k&&String(c[i][1]).trim()!==String(x[1]).trim()})).slice(0,3);QZ.opts=shuf(others.concat([k]))}
  return '<div class="fc-opts"><span class="muted small">Question '+(QZ.i+1)+' of '+QZ.q.length+' · Score '+QZ.score+'</span></div><div class="fc-bar"><i style="width:'+Math.round(QZ.i/QZ.q.length*100)+'%"></i></div>'+
   '<div class="fc-q">'+br(x[0])+'</div><div class="fc-choices">'+QZ.opts.map(function(o){var cls=QZ.pick===null?'':o===k?' ok':o===QZ.pick?' no':'';return '<button type="button" class="fc-ch'+cls+'" data-o="'+o+'"'+(QZ.pick!==null?' disabled':'')+'>'+br(c[o][1])+'</button>'}).join('')+'</div>'+
   (QZ.pick!==null?'<div class="fc-btns" style="justify-content:center"><button type="button" class="fc-b pri" id="fcNext">'+(QZ.i+1<QZ.q.length?'Next question ▶':'See my score')+'</button></div>':'')}
function wireQuiz(){$$('.fc-ch').forEach(function(b){b.onclick=function(){var o=+b.dataset.o,k=QZ.q[QZ.i];QZ.pick=o;if(o===k)QZ.score++;else QZ.miss.push(k);draw()}});
  var n=$('#fcNext');if(n){n.onclick=function(){QZ.i++;QZ.pick=null;QZ.opts=null;draw()};n.focus()}
  var a=$('#fcQAgain');if(a)a.onclick=function(){startQuiz();draw()};var m=$('#fcStudyMiss');if(m)m.onclick=function(){var l=QZ.miss.slice();tab='study';startStudy(l);draw()}}
// ---------- print ----------
function print(){var c=cards();
  return '<p class="muted small" style="margin:0">Print on A4 or Letter, then cut along the dashed lines.</p><div class="fc-pl"><label class="fc-chk"><input type="radio" name="fcLay" value="fold" checked> <span><b>Fold cards</b> · front and back side by side. Cut each row and fold it in the middle. Works on any printer.</span></label>'+
   '<label class="fc-chk"><input type="radio" name="fcLay" value="duplex"> <span><b>Double-sided</b> · fronts on one page, backs on the next, lined up for printing on both sides (flip on the long edge).</span></label></div>'+
   '<div class="fc-btns"><button type="button" class="fc-b pri" id="fcPrintGo">🖨 Print or save as PDF ('+c.length+' cards)</button></div>'}
function printHTML(lay){var c=cards(),t=esc(deck().t||'Flash cards'),h='';
  if(lay==='fold'){for(var i=0;i<c.length;i+=8){h+='<div class="fcp-page"><div class="fcp-h">'+t+'</div><div class="fcp-fold">'+c.slice(i,i+8).map(function(x){return '<div class="fcp-row"><div>'+br(x[0])+'</div><div>'+br(x[1])+'</div></div>'}).join('')+'</div></div>'}}
  else{for(var j=0;j<c.length;j+=10){var g=c.slice(j,j+10);while(g.length<10)g.push(['','']);
    h+='<div class="fcp-page"><div class="fcp-h">'+t+' · fronts</div><div class="fcp-grid">'+g.map(function(x){return '<div>'+br(x[0])+'</div>'}).join('')+'</div></div>';
    var back=[];for(var r=0;r<5;r++){back.push(g[r*2+1],g[r*2])}   // mirror each row so backs line up when printed on the other side
    h+='<div class="fcp-page"><div class="fcp-h">'+t+' · backs</div><div class="fcp-grid">'+back.map(function(x){return '<div>'+br(x[1])+'</div>'}).join('')+'</div></div>'}}
  return h}
function wirePrint(){$('#fcPrintGo').onclick=function(){var lay=($$('input[name="fcLay"]').filter(function(r){return r.checked})[0]||{}).value||'fold';$('#fcPrint').innerHTML=printHTML(lay);window.print()}}
window.addEventListener('afterprint',function(){$('#fcPrint').innerHTML=''});
// ---------- tabs ----------
function draw(){drawDecks();$$('#fcTabs button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.t===tab))});var p=$('#fcPane');
  if(tab==='make'){p.innerHTML=make();wireMake()}else if(tab==='study'){p.innerHTML=study();wireStudy()}else if(tab==='quiz'){p.innerHTML=quiz();wireQuiz()}else{p.innerHTML=print();wirePrint()}}
$$('#fcTabs button').forEach(function(b){b.onclick=function(){tab=b.dataset.t;if(tab==='study')resetStudy();if(tab==='quiz')QZ=null;draw()}});
document.addEventListener('keydown',function(e){if(tab!=='study'||!ST||/INPUT|TEXTAREA|SELECT/.test(e.target.tagName))return;
  if(e.key===' '||e.key==='Enter'){e.preventDefault();ST.flip=!ST.flip;draw()}else if(e.key==='ArrowRight'){ST.i=Math.min(ST.q.length,ST.i+1);ST.flip=false;draw()}else if(e.key==='ArrowLeft'&&ST.i){ST.i--;ST.flip=false;draw()}});
// open a shared deck from the link
var m=location.hash.match(/[#&]d=([A-Za-z0-9_-]+)/);
if(m){unpack(m[1]).then(function(o){if(o&&o.c&&o.c.length){var sig=JSON.stringify(o.c),ex=D.decks.filter(function(d){return JSON.stringify(d.c)===sig})[0];
    if(ex)D.cur=ex.id;else{var d={id:uid(),t:o.t||'Shared deck',c:o.c};D.decks.unshift(d);D.cur=d.id}save();tab='study';resetStudy();$('#fcShared').hidden=false;$('#fcShared b').textContent=o.t||'a shared deck'}
    history.replaceState(null,'',location.pathname);draw()},function(){history.replaceState(null,'',location.pathname);draw()})}else draw();
})();
