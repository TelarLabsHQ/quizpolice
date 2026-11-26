(function(){
var $=function(s){return document.querySelector(s)};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
var RULES='Phones off and inside your bag\nNo talking during the exam\nWrite your name and section on every page\nRaise your hand if you have a question\nStay seated until your paper is collected';
var S=keep('qp-clock')||{title:'',sub:'',mode:'dur',dur:60,end:'10:00',rules:RULES,w10:true,w5:true,sound:true,run:null};
$('#ecTitle').value=S.title;$('#ecSub').value=S.sub;$('#ecMode').value=S.mode;$('#ecDur').value=S.dur;$('#ecEnd').value=S.end;$('#ecRulesIn').value=S.rules;$('#ecW10').checked=S.w10;$('#ecW5').checked=S.w5;$('#ecSound').checked=S.sound;
function modeUI(){$('#ecDurL').hidden=S.mode!=='dur';$('#ecEndL').hidden=S.mode!=='end'}modeUI();
function read(){S.title=$('#ecTitle').value;S.sub=$('#ecSub').value;S.mode=$('#ecMode').value;S.dur=+$('#ecDur').value||60;S.end=$('#ecEnd').value||'10:00';S.rules=$('#ecRulesIn').value;S.w10=$('#ecW10').checked;S.w5=$('#ecW5').checked;S.sound=$('#ecSound').checked;keep('qp-clock',S)}
['ecTitle','ecSub','ecDur','ecEnd','ecRulesIn','ecW10','ecW5','ecSound'].forEach(function(id){$('#'+id).addEventListener('input',read);$('#'+id).addEventListener('change',read)});
$('#ecMode').onchange=function(){read();modeUI()};
var ac=null,lock=null,tick=null;
function beep(n){if(!S.sound)return;try{ac=ac||new (window.AudioContext||window.webkitAudioContext)();for(var i=0;i<n;i++){var o=ac.createOscillator(),g=ac.createGain(),t=ac.currentTime+i*.35;o.frequency.value=880;o.connect(g);g.connect(ac.destination);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.3,t+.02);g.gain.linearRampToValueAtTime(0,t+.25);o.start(t);o.stop(t+.3)}}catch(e){}}
function tfmt(d){return d.toLocaleTimeString([],{hour:'numeric',minute:'2-digit'})}
function left(){var R=S.run;if(!R)return 0;return Math.max(0,(R.paused||Date.now())<R.end?R.end-(R.paused||Date.now()):0)}
function mmss(ms){var s=Math.ceil(ms/1000),h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;return (h?h+':'+String(m).padStart(2,'0'):String(m).padStart(2,'0'))+':'+String(x).padStart(2,'0')}
function start(){read();var now=Date.now(),end;
  if(S.mode==='end'){var p=S.end.split(':'),d=new Date();d.setHours(+p[0],+p[1],0,0);if(d.getTime()<=now)d.setDate(d.getDate()+1);end=d.getTime()}else end=now+S.dur*60000;
  S.run={start:now,end:end,paused:null,w:{}};keep('qp-clock',S);try{ac=ac||new (window.AudioContext||window.webkitAudioContext)()}catch(e){}show(true)}
function show(full){$('#ecRun').hidden=false;document.body.style.overflow='hidden';$('#ecT').textContent=S.title||'Exam';$('#ecS').textContent=S.sub||'';$('#ecS').hidden=!S.sub;
  $('#ecRules').innerHTML=S.rules.split('\n').map(function(x){return x.trim()}).filter(Boolean).map(function(x){return '<li>'+esc(x)+'</li>'}).join('');
  if(full)try{document.documentElement.requestFullscreen().catch(function(){})}catch(e){}
  try{if(navigator.wakeLock)navigator.wakeLock.request('screen').then(function(l){lock=l},function(){})}catch(e){}
  clearInterval(tick);tick=setInterval(upd,250);upd()}
function hide(){$('#ecRun').hidden=true;document.body.style.overflow='';clearInterval(tick);try{if(lock)lock.release();lock=null;if(document.fullscreenElement)document.exitFullscreen()}catch(e){}
  $('#ecResume').hidden=!(S.run&&left()>0)}
function upd(){var R=S.run;if(!R)return;var ms=left(),run=$('#ecRun'),min=ms/60000;
  $('#ecBig').textContent=ms>0?mmss(ms):'00:00';$('#ecNow').textContent='Now '+tfmt(new Date());$('#ecEnds').textContent=R.paused?'Paused':'Ends at '+tfmt(new Date(R.end));
  var tot=R.end-R.start;$('#ecBar i').style.width=(tot>0?Math.min(100,(1-ms/tot)*100):100)+'%';
  var cls=ms<=0?'over':(S.w5&&min<=5)?'w5':(S.w10&&min<=10)?'w10':'';run.className=cls+(R.paused?' paused':'');
  var b=$('#ecBanner');b.hidden=!cls;b.textContent=cls==='over'?'Time is up. Please stop writing.':cls==='w5'?'5 minutes left':cls==='w10'?'10 minutes left':'';
  if(!R.paused){var w=R.w||(R.w={});if(cls&&!w[cls]){w[cls]=1;keep('qp-clock',S);if(ms>-2000)beep(cls==='over'?3:cls==='w5'?2:1)}}}
function pause(){var R=S.run;if(!R)return;if(R.paused){R.end+=Date.now()-R.paused;R.paused=null;$('#ecPause').textContent='❚❚ Pause'}else{R.paused=Date.now();$('#ecPause').textContent='▶ Resume'}keep('qp-clock',S);upd()}
function add(m){var R=S.run;if(!R)return;R.end+=m*60000;if(m>0){var mn=left()/60000;if(mn>10)delete R.w.w10;if(mn>5)delete R.w.w5;if(mn>0)delete R.w.over}keep('qp-clock',S);upd()}
function full(){try{if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen()}catch(e){}}
$('#ecStart').onclick=function(){if(S.run&&left()>0&&!window.confirm('Start a new exam clock? The one running now will end.'))return;start()};
$('#ecPause').onclick=pause;$('#ecPlus').onclick=function(){add(5)};$('#ecMinus').onclick=function(){add(-5)};$('#ecFull').onclick=full;
$('#ecStop').onclick=function(){if(!window.confirm('End the exam clock?'))return;S.run=null;keep('qp-clock',S);hide()};$('#ecHide').onclick=hide;$('#ecBack').onclick=function(){show(false)};
document.addEventListener('keydown',function(e){if($('#ecRun').hidden||/INPUT|TEXTAREA/.test(e.target.tagName))return;if(e.key===' '){e.preventDefault();pause()}else if(e.key==='f'||e.key==='F')full();else if(e.key==='+'||e.key==='=')add(5);else if(e.key==='-')add(-5)});
document.addEventListener('visibilitychange',function(){if(!document.hidden&&!$('#ecRun').hidden)try{if(navigator.wakeLock)navigator.wakeLock.request('screen').then(function(l){lock=l},function(){})}catch(e){}});
if(S.run&&left()>0){$('#ecResume').hidden=false;$('#ecPause').textContent=S.run.paused?'▶ Resume':'❚❚ Pause'}
})();
