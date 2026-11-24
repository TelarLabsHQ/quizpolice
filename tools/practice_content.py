"""Practice games for students (/practice/): Math Sprint and Geography. Rendered by build.py.
Each page is a small game at the top and a real article below it. Ads never sit inside the game card."""

GAME_CSS = '''<style>
.game{max-width:620px;margin:8px auto 34px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 10px 30px rgba(20,27,43,.08)}
.game h2{margin:0 0 4px;font-size:22px}.game .gsub{margin:0 0 14px;color:var(--muted);font-size:15px}
.gchips{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 14px}
.gchips button{border:2px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font:inherit;font-size:15px;font-weight:700;color:var(--fg);cursor:pointer}
.gchips button.on{border-color:var(--brand);background:var(--brand);color:#fff}
.glabel{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:4px 0 0}
.gbtn{display:block;width:100%;background:var(--brand);color:#fff;border:0;border-radius:12px;padding:14px;font:inherit;font-size:18px;font-weight:800;cursor:pointer}
.gbtn.ghost{background:transparent;color:var(--brand);border:2px solid var(--brand)}
.gbar{height:8px;background:#E6EAF2;border-radius:99px;overflow:hidden;margin-bottom:12px}.gbar i{display:block;height:100%;background:var(--badge);width:100%}
.gtop{display:flex;justify-content:space-between;font-weight:700;color:var(--muted);font-size:15px;margin-bottom:6px}
.gq{font-family:var(--head);font-weight:800;font-size:44px;text-align:center;margin:6px 0 4px;color:var(--fg)}
.gin{font-family:var(--head);font-weight:800;font-size:36px;text-align:center;min-height:54px;border:2px solid var(--line);border-radius:12px;margin:0 auto 12px;max-width:220px;background:var(--bg)}
.gin.ok{border-color:#2e9e5b;background:#e5f6ec}.gin.bad{border-color:#d64545;background:#fdeaea}
.pad{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:320px;margin:0 auto}
.pad button{font:inherit;font-size:24px;font-weight:800;padding:12px 0;border-radius:12px;border:1px solid var(--line);background:#fff;color:var(--fg);cursor:pointer;touch-action:manipulation}
.pad button:active{background:#E6EAF2}.pad .go{background:var(--brand);color:#fff;border-color:var(--brand)}
.gopts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0}
.gopts button{font:inherit;font-size:17px;font-weight:700;padding:14px 10px;border-radius:12px;border:2px solid var(--line);background:#fff;color:var(--fg);cursor:pointer;min-height:62px;touch-action:manipulation}
.gopts button.ok{border-color:#2e9e5b;background:#e5f6ec}.gopts button.bad{border-color:#d64545;background:#fdeaea}
.gopts button:disabled{cursor:default;opacity:1}
.gq2{font-family:var(--head);font-weight:800;font-size:24px;text-align:center;margin:8px 0 0;line-height:1.3}
.gres{text-align:center}.gbig{font-family:var(--head);font-weight:800;font-size:56px;color:var(--brand);line-height:1.1;margin:6px 0}
.gmiss{text-align:left;margin:14px 0;padding:0;list-style:none;border-top:1px solid var(--line)}
.gmiss li{padding:8px 4px;border-bottom:1px solid var(--line);font-size:16px}
.grow{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.gfb{text-align:center;min-height:26px;font-weight:700;margin-top:2px}
.ptiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:18px 0}
.ptiles a{display:block;border:1px solid var(--line);border-radius:14px;padding:18px;background:var(--card);text-decoration:none;color:var(--fg)}
.ptiles b{display:block;font-size:20px;color:var(--brand);margin-bottom:4px}
@media(max-width:480px){.game{padding:16px 14px}.gq{font-size:38px}.gopts{grid-template-columns:1fr}}
</style>'''

MATH_GAME = '''<div class="game" id="ms">
 <div id="msSetup">
  <h2>Math Sprint</h2><p class="gsub">Answer as many as you can in 60 seconds.</p>
  <p class="glabel">Choose a level</p>
  <div class="gchips" id="msLv"></div>
  <button class="gbtn" id="msStart">Start</button>
 </div>
 <div id="msPlay" hidden>
  <div class="gtop"><span id="msLvName"></span><span>Score: <b id="msScore">0</b></span></div>
  <div class="gbar"><i id="msBar"></i></div>
  <div class="gq" id="msQ"></div>
  <div class="gin" id="msIn"></div>
  <div class="pad" id="msPad"></div>
 </div>
 <div id="msEnd" class="gres" hidden>
  <p class="glabel">Time’s up!</p><div class="gbig" id="msFinal"></div><p id="msNote" class="muted"></p>
  <ul class="gmiss" id="msMiss"></ul>
  <div class="grow"><button class="gbtn" id="msAgain">Play again</button><button class="gbtn ghost" id="msBack">Change level</button></div>
 </div>
</div>
<script>
(()=>{const $=i=>document.getElementById(i),r=(a,b)=>a+Math.floor(Math.random()*(b-a+1)),pick=a=>a[Math.floor(Math.random()*a.length)];
const LV={add:['Add to 20',()=>{const a=r(0,10),b=r(0,10);return[a+' + '+b,a+b]}],
 sub:['Subtract to 20',()=>{const a=r(1,20),b=r(0,a);return[a+' − '+b,a-b]}],
 h:['Add & subtract to 100',()=>{if(Math.random()<.5){const a=r(10,89),b=r(2,100-a);return[a+' + '+b,a+b]}const a=r(20,100),b=r(2,a);return[a+' − '+b,a-b]}],
 mul:['Times tables',()=>{const a=r(2,12),b=r(2,12);return[a+' × '+b,a*b]}],
 div:['Division',()=>{const b=r(2,12),q=r(2,12);return[(b*q)+' ÷ '+b,q]}],
 mix:['Mix it up',()=>LV[pick(['add','sub','h','mul','div'])][1]()]};
let lv='add',score=0,miss=[],cur=null,typed='',t0=0,raf=0,on=false;const T=60;
const get=k=>{try{return +localStorage.getItem(k)||0}catch(e){return 0}},put=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
Object.entries(LV).forEach(([k,[n]])=>{const b=document.createElement('button');b.textContent=n;b.dataset.k=k;if(k===lv)b.className='on';b.onclick=()=>{lv=k;document.querySelectorAll('#msLv button').forEach(x=>x.classList.toggle('on',x===b))};$('msLv').appendChild(b)});
['1','2','3','4','5','6','7','8','9','⌫','0','✓'].forEach(k=>{const b=document.createElement('button');b.textContent=k;b.type='button';if(k==='✓')b.className='go';b.setAttribute('aria-label',k==='⌫'?'Delete':k==='✓'?'Check':k);b.onclick=()=>key(k);$('msPad').appendChild(b)});
function next(){let q;do{q=LV[lv][1]()}while(cur&&q[0]===cur[0]);cur=q;typed='';$('msQ').textContent=q[0]+' = ?';show()}
function show(c){const e=$('msIn');e.textContent=typed;e.className='gin'+(c?' '+c:'')}
function key(k){if(!on)return;if(k==='⌫'){typed=typed.slice(0,-1);show();return}
 if(k==='✓'){if(!typed)return;miss.push([cur[0],cur[1],typed]);show('bad');on=false;setTimeout(()=>{on=true;next()},350);return}
 if(typed.length>=4)return;typed+=k;
 if(+typed===cur[1]){score++;$('msScore').textContent=score;show('ok');on=false;setTimeout(()=>{if(performance.now()-t0<T*1000){on=true;next()}},160)}else show()}
document.addEventListener('keydown',e=>{if($('msPlay').hidden)return;if(/^[0-9]$/.test(e.key)){key(e.key);e.preventDefault()}else if(e.key==='Backspace'){key('⌫');e.preventDefault()}else if(e.key==='Enter'){key('✓');e.preventDefault()}});
function tick(){const left=T-(performance.now()-t0)/1000;$('msBar').style.width=Math.max(0,left/T*100)+'%';if(left<=0)return end();raf=requestAnimationFrame(tick)}
function start(){score=0;miss=[];cur=null;$('msScore').textContent=0;$('msLvName').textContent=LV[lv][0];$('msSetup').hidden=true;$('msEnd').hidden=true;$('msPlay').hidden=false;on=true;next();t0=performance.now();cancelAnimationFrame(raf);tick();$('ms').scrollIntoView({block:'nearest'})}
function end(){on=false;$('msPlay').hidden=true;$('msEnd').hidden=false;const k='qp-ms-'+lv,best=get(k),tot=score+miss.length;
 $('msFinal').textContent=score+' right';
 $('msNote').textContent=LV[lv][0]+(score>best?' · New best score!':' · Your best: '+best)+(tot?' · '+Math.round(score/tot*100)+'% correct':'');if(score>best)put(k,score);
 $('msMiss').innerHTML=miss.length?'<li><b>Practice these:</b></li>'+miss.slice(0,8).map(m=>'<li>'+m[0]+' = <b>'+m[1]+'</b> <span class="muted">(you wrote '+m[2]+')</span></li>').join(''):'<li>No mistakes. Great work! Try a harder level.</li>'}
$('msStart').onclick=start;$('msAgain').onclick=start;$('msBack').onclick=()=>{$('msEnd').hidden=true;$('msSetup').hidden=false};})();
</script>'''

MATH_TEXT = '''<h2>How to play</h2>
<ol><li>Choose a level. Start with an easy one to warm up.</li>
<li>Press <b>Start</b>. You have 60 seconds.</li>
<li>Type the answer with the number pad, or with your keyboard on a computer. A correct answer moves on by itself.</li>
<li>Not sure? Type your best guess and press <b>✓</b> to move on. You’ll see the right answers at the end.</li></ol>

<h2>The levels</h2>
<ul><li><b>Add to 20</b> and <b>Subtract to 20</b>: number facts that young learners use every day.</li>
<li><b>Add &amp; subtract to 100</b>: two-digit sums and differences, good practice for mental math.</li>
<li><b>Times tables</b>: every table from 2 to 12, mixed together.</li>
<li><b>Division</b>: the times tables backwards, always with whole-number answers.</li>
<li><b>Mix it up</b>: a bit of everything, so you have to think about which operation to use.</li></ul>

<h2>Why a 60-second sprint helps</h2>
<p>When basic facts like 7 × 8 come to mind instantly, your brain has more room for the hard part of a problem: understanding the question, planning the steps and checking the answer. Short, frequent practice is the best way to get there. A few sprints a day for a week does more than one long session.</p>
<p>The sprint also shows you exactly what to practice. The list at the end only includes facts you got wrong, so you can write them on a card and try them again tomorrow.</p>

<h2>Tips to beat your best score</h2>
<ul><li><b>Accuracy first, then speed.</b> A wrong answer costs more time than a careful right one.</li>
<li><b>Learn the tricky facts on purpose.</b> For most people these are 6 × 7, 6 × 8, 7 × 8, 8 × 12 and the 9s.</li>
<li><b>Use patterns.</b> 9 × 7 is 10 × 7 minus 7. 12 × 6 is 10 × 6 plus 2 × 6.</li>
<li><b>Play the same level a few days in a row.</b> Your best score is saved on this device, so you can see yourself improve.</li></ul>

<h2>For teachers and parents</h2>
<p>Math Sprint is free, needs no sign-up and works on phones, tablets and computers. Use it as a warm-up at the start of a lesson, as a quick homework task (“three sprints a day, write down your best score”), or as a calm activity at home. Scores stay on the device. Nothing is sent to us.</p>
<p>Want students to practice remembering in other subjects too? Our guide <a href="/guides/how-to-study-for-a-quiz/">How to Study for a Quiz: 7 Tips That Actually Work</a> explains self-testing and spaced practice in simple words. When it’s time for the real quiz, <a href="/">QuizPolice</a> helps teachers keep online quizzes fair.</p>

<h2>Questions</h2>
<p><b>Is it free?</b> Yes, completely.</p>
<p><b>Does it save my score?</b> Your best score for each level is saved in this browser only. Clearing your browser data removes it.</p>
<p><b>Why are there no negative numbers?</b> The subtraction levels always give answers of zero or more, so they match what most students learn first.</p>'''

# country, capital, region. Only countries with one clear, widely taught capital.
GEO = [
('Afghanistan','Kabul','Asia'),('Bahrain','Manama','Asia'),('Bangladesh','Dhaka','Asia'),('Bhutan','Thimphu','Asia'),('Brunei','Bandar Seri Begawan','Asia'),
('Cambodia','Phnom Penh','Asia'),('China','Beijing','Asia'),('India','New Delhi','Asia'),('Iran','Tehran','Asia'),('Iraq','Baghdad','Asia'),('Japan','Tokyo','Asia'),
('Jordan','Amman','Asia'),('Kazakhstan','Astana','Asia'),('Kuwait','Kuwait City','Asia'),('Kyrgyzstan','Bishkek','Asia'),('Laos','Vientiane','Asia'),
('Lebanon','Beirut','Asia'),('Malaysia','Kuala Lumpur','Asia'),('Maldives','Malé','Asia'),('Mongolia','Ulaanbaatar','Asia'),('Myanmar','Naypyidaw','Asia'),
('Nepal','Kathmandu','Asia'),('North Korea','Pyongyang','Asia'),('Oman','Muscat','Asia'),('Pakistan','Islamabad','Asia'),('Philippines','Manila','Asia'),
('Qatar','Doha','Asia'),('Saudi Arabia','Riyadh','Asia'),('South Korea','Seoul','Asia'),('Syria','Damascus','Asia'),('Tajikistan','Dushanbe','Asia'),
('Thailand','Bangkok','Asia'),('Timor-Leste','Dili','Asia'),('Turkmenistan','Ashgabat','Asia'),('United Arab Emirates','Abu Dhabi','Asia'),
('Uzbekistan','Tashkent','Asia'),('Vietnam','Hanoi','Asia'),
('Albania','Tirana','Europe'),('Austria','Vienna','Europe'),('Belarus','Minsk','Europe'),('Belgium','Brussels','Europe'),('Bosnia and Herzegovina','Sarajevo','Europe'),
('Bulgaria','Sofia','Europe'),('Croatia','Zagreb','Europe'),('Czechia','Prague','Europe'),('Denmark','Copenhagen','Europe'),('Estonia','Tallinn','Europe'),
('Finland','Helsinki','Europe'),('France','Paris','Europe'),('Germany','Berlin','Europe'),('Greece','Athens','Europe'),('Hungary','Budapest','Europe'),
('Iceland','Reykjavík','Europe'),('Ireland','Dublin','Europe'),('Italy','Rome','Europe'),('Latvia','Riga','Europe'),('Lithuania','Vilnius','Europe'),
('Malta','Valletta','Europe'),('Moldova','Chișinău','Europe'),('Montenegro','Podgorica','Europe'),('Netherlands','Amsterdam','Europe'),
('North Macedonia','Skopje','Europe'),('Norway','Oslo','Europe'),('Poland','Warsaw','Europe'),('Portugal','Lisbon','Europe'),('Romania','Bucharest','Europe'),
('Russia','Moscow','Europe'),('Serbia','Belgrade','Europe'),('Slovakia','Bratislava','Europe'),('Slovenia','Ljubljana','Europe'),('Spain','Madrid','Europe'),
('Sweden','Stockholm','Europe'),('Switzerland','Bern','Europe'),('Ukraine','Kyiv','Europe'),('United Kingdom','London','Europe'),
('Algeria','Algiers','Africa'),('Angola','Luanda','Africa'),('Botswana','Gaborone','Africa'),('Burkina Faso','Ouagadougou','Africa'),('Cameroon','Yaoundé','Africa'),
('Chad','N’Djamena','Africa'),('DR Congo','Kinshasa','Africa'),('Egypt','Cairo','Africa'),('Eritrea','Asmara','Africa'),('Ethiopia','Addis Ababa','Africa'),
('Gabon','Libreville','Africa'),('Ghana','Accra','Africa'),('Guinea','Conakry','Africa'),('Kenya','Nairobi','Africa'),('Liberia','Monrovia','Africa'),
('Libya','Tripoli','Africa'),('Madagascar','Antananarivo','Africa'),('Malawi','Lilongwe','Africa'),('Mali','Bamako','Africa'),('Mauritania','Nouakchott','Africa'),
('Morocco','Rabat','Africa'),('Mozambique','Maputo','Africa'),('Namibia','Windhoek','Africa'),('Niger','Niamey','Africa'),('Nigeria','Abuja','Africa'),
('Rwanda','Kigali','Africa'),('Senegal','Dakar','Africa'),('Sierra Leone','Freetown','Africa'),('Somalia','Mogadishu','Africa'),('South Sudan','Juba','Africa'),
('Sudan','Khartoum','Africa'),('Tunisia','Tunis','Africa'),('Uganda','Kampala','Africa'),('Zambia','Lusaka','Africa'),('Zimbabwe','Harare','Africa'),
('Argentina','Buenos Aires','Americas'),('Bahamas','Nassau','Americas'),('Belize','Belmopan','Americas'),('Brazil','Brasília','Americas'),('Canada','Ottawa','Americas'),
('Chile','Santiago','Americas'),('Colombia','Bogotá','Americas'),('Costa Rica','San José','Americas'),('Cuba','Havana','Americas'),
('Dominican Republic','Santo Domingo','Americas'),('Ecuador','Quito','Americas'),('El Salvador','San Salvador','Americas'),('Guatemala','Guatemala City','Americas'),
('Guyana','Georgetown','Americas'),('Haiti','Port-au-Prince','Americas'),('Honduras','Tegucigalpa','Americas'),('Jamaica','Kingston','Americas'),
('Mexico','Mexico City','Americas'),('Nicaragua','Managua','Americas'),('Panama','Panama City','Americas'),('Paraguay','Asunción','Americas'),('Peru','Lima','Americas'),
('Suriname','Paramaribo','Americas'),('Trinidad and Tobago','Port of Spain','Americas'),('United States','Washington, D.C.','Americas'),
('Uruguay','Montevideo','Americas'),('Venezuela','Caracas','Americas'),
('Australia','Canberra','Oceania'),('Fiji','Suva','Oceania'),('Marshall Islands','Majuro','Oceania'),('Micronesia','Palikir','Oceania'),
('New Zealand','Wellington','Oceania'),('Papua New Guinea','Port Moresby','Oceania'),('Samoa','Apia','Oceania'),('Solomon Islands','Honiara','Oceania'),
('Tonga','Nukuʻalofa','Oceania'),('Tuvalu','Funafuti','Oceania'),('Vanuatu','Port Vila','Oceania'),
]

def geo_game():
    import json
    data = json.dumps(GEO, ensure_ascii=False)
    return '''<div class="game" id="gg">
 <div id="ggSetup">
  <h2>Geography Practice</h2><p class="gsub">10 questions about countries and their capital cities.</p>
  <p class="glabel">Question type</p>
  <div class="gchips" id="ggMode"><button class="on" data-m="cap">Name the capital</button><button data-m="cty">Name the country</button></div>
  <p class="glabel">Region</p>
  <div class="gchips" id="ggReg"></div>
  <button class="gbtn" id="ggStart">Start</button>
 </div>
 <div id="ggPlay" hidden>
  <div class="gtop"><span id="ggNum"></span><span>Score: <b id="ggScore">0</b></span></div>
  <div class="gbar"><i id="ggBar"></i></div>
  <div class="gq2" id="ggQ"></div>
  <div class="gopts" id="ggOpts"></div>
  <div class="gfb" id="ggFb"></div>
  <button class="gbtn" id="ggNext" hidden>Next</button>
 </div>
 <div id="ggEnd" class="gres" hidden>
  <p class="glabel">Round complete</p><div class="gbig" id="ggFinal"></div><p id="ggNote" class="muted"></p>
  <ul class="gmiss" id="ggMiss"></ul>
  <div class="grow"><button class="gbtn" id="ggAgain">Play again</button><button class="gbtn ghost" id="ggBack">Change settings</button></div>
 </div>
</div>
<script>
(()=>{const D=''' + data + ''';
const $=i=>document.getElementById(i),sh=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const get=k=>{try{return +localStorage.getItem(k)||0}catch(e){return 0}},put=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
let mode='cap',reg='World',qs=[],n=0,score=0,miss=[],locked=false;
['World','Asia','Europe','Africa','Americas','Oceania'].forEach(r=>{const b=document.createElement('button');b.textContent=r;if(r===reg)b.className='on';b.onclick=()=>{reg=r;document.querySelectorAll('#ggReg button').forEach(x=>x.classList.toggle('on',x===b))};$('ggReg').appendChild(b)});
document.querySelectorAll('#ggMode button').forEach(b=>b.onclick=()=>{mode=b.dataset.m;document.querySelectorAll('#ggMode button').forEach(x=>x.classList.toggle('on',x===b))});
function start(){const pool=D.filter(d=>reg==='World'||d[2]===reg);qs=sh(pool).slice(0,10);n=0;score=0;miss=[];$('ggScore').textContent=0;
 $('ggSetup').hidden=true;$('ggEnd').hidden=true;$('ggPlay').hidden=false;ask();$('gg').scrollIntoView({block:'nearest'})}
function ask(){const d=qs[n];locked=false;$('ggNum').textContent='Question '+(n+1)+' of '+qs.length;$('ggBar').style.width=(n/qs.length*100)+'%';
 const a=mode==='cap'?1:0;$('ggQ').textContent=mode==='cap'?'What is the capital of '+d[0]+'?':d[1]+' is the capital of which country?';
 const others=sh(D.filter(x=>x[2]===d[2]&&x!==d)).slice(0,3).map(x=>x[a]);const opts=sh([d[a],...others]);
 $('ggOpts').innerHTML='';$('ggFb').textContent='';$('ggNext').hidden=true;
 opts.forEach(o=>{const b=document.createElement('button');b.textContent=o;b.onclick=()=>choose(b,o===d[a]);$('ggOpts').appendChild(b)})}
function choose(b,ok){if(locked)return;locked=true;const d=qs[n],a=mode==='cap'?1:0;
 document.querySelectorAll('#ggOpts button').forEach(x=>{x.disabled=true;if(x.textContent===d[a])x.classList.add('ok')});
 if(ok){score++;$('ggScore').textContent=score;$('ggFb').textContent='Correct!';$('ggFb').style.color='#2e9e5b'}
 else{b.classList.add('bad');miss.push(d);$('ggFb').textContent=mode==='cap'?'The capital of '+d[0]+' is '+d[1]+'.':d[1]+' is the capital of '+d[0]+'.';$('ggFb').style.color='#b23a3a'}
 $('ggNext').textContent=n+1<qs.length?'Next':'See my score';$('ggNext').hidden=false}
$('ggNext').onclick=()=>{n++;if(n<qs.length)ask();else end()};
document.addEventListener('keydown',e=>{if($('ggPlay').hidden)return;const bs=document.querySelectorAll('#ggOpts button');
 if(!locked&&/^[1-4]$/.test(e.key)&&bs[+e.key-1]){bs[+e.key-1].click();e.preventDefault()}else if(locked&&e.key==='Enter'){$('ggNext').click();e.preventDefault()}});
function end(){$('ggBar').style.width='100%';$('ggPlay').hidden=true;$('ggEnd').hidden=false;const k='qp-geo-'+mode+'-'+reg,best=get(k);
 $('ggFinal').textContent=score+' / '+qs.length;$('ggNote').textContent=reg+' · '+(mode==='cap'?'Name the capital':'Name the country')+(score>best?' · New best score!':' · Your best: '+best+' / 10');if(score>best)put(k,score);
 $('ggMiss').innerHTML=miss.length?'<li><b>Remember these:</b></li>'+miss.map(d=>'<li>'+d[0]+' → <b>'+d[1]+'</b></li>').join(''):'<li>Perfect round! Try another region.</li>'}
$('ggStart').onclick=start;$('ggAgain').onclick=start;$('ggBack').onclick=()=>{$('ggEnd').hidden=true;$('ggSetup').hidden=false};})();
</script>'''

GEO_TEXT = '''<h2>How to play</h2>
<ol><li>Choose a question type. <b>Name the capital</b> shows a country and asks for its capital. <b>Name the country</b> works the other way around.</li>
<li>Choose a region, or <b>World</b> for questions from everywhere.</li>
<li>Press <b>Start</b> and pick one of four answers. If you get it wrong, you’ll see the right answer straight away.</li>
<li>After 10 questions you’ll see your score and a list of the ones to remember.</li></ol>
<p>On a computer you can also press the keys <b>1</b> to <b>4</b> to answer and <b>Enter</b> for the next question.</p>

<h2>What’s included</h2>
<p>The game includes about 150 countries from Asia, Europe, Africa, the Americas and Oceania. The wrong answers always come from the same region as the right one, so you can’t guess just by knowing the continent.</p>
<p>A few countries are left out on purpose because their capital is complicated: some have more than one official capital (like South Africa and Bolivia), and some are moving their government to a new city. Those make great questions for a class discussion, but not for a quick quiz.</p>

<h2>Tips for remembering capitals</h2>
<ul><li><b>Practice one region at a time.</b> Master Asia, then add Europe. It’s easier than learning the whole world at once.</li>
<li><b>Play both ways.</b> Knowing that Canberra is the capital of Australia is different from being asked which country Canberra belongs to. Doing both makes the memory stronger.</li>
<li><b>Look for clues in the names.</b> Kuwait City, Mexico City, Guatemala City and Panama City share their country’s name. Others are famous traps: the capital of Australia is Canberra, not Sydney, and the capital of Canada is Ottawa, not Toronto.</li>
<li><b>Make a story.</b> Linking a capital to a picture or a silly sentence helps it stick.</li>
<li><b>Come back tomorrow.</b> Replaying the ones you missed after a day or two is one of the most effective ways to remember them.</li></ul>

<h2>For teachers and parents</h2>
<p>Geography Practice is free and works on phones, tablets and computers, with no sign-up. Use one round as a lesson warm-up, set “score 10/10 in your region” as homework, or let students compete for the best score in class. Scores stay on the device. Nothing is sent to us.</p>
<p>For more ways to help students remember, see <a href="/guides/how-to-study-for-a-quiz/">How to Study for a Quiz: 7 Tips That Actually Work</a>. When it’s time for a real quiz online, <a href="/">QuizPolice</a> helps teachers keep it fair.</p>

<h2>Questions</h2>
<p><b>Is it free?</b> Yes, completely.</p>
<p><b>Does it save my score?</b> Your best score for each region and question type is saved in this browser only.</p>
<p><b>I think an answer is wrong.</b> Please <a href="/contact/">tell us</a>. Capitals sometimes change, and we’ll update the list.</p>'''

HUB_TEXT = '''<p class="lead">Free, quick practice games for students. No sign-up, no downloads, and they work on any phone or computer.</p>
<div class="ptiles">
<a href="/practice/math-sprint/"><b>Math Sprint</b>60 seconds of quick math: adding, subtracting, times tables and division. Beat your best score.</a>
<a href="/practice/geography/"><b>Geography Practice</b>Countries and capital cities from every continent, 10 questions at a time.</a>
</div>
<h2>Why short practice works</h2>
<p>A few minutes of practice on most days beats a long session once a week. Each time you bring an answer back from memory, it gets easier to find the next time. These games are built for exactly that: short rounds, instant feedback, and a list of the answers to remember.</p>
<p>For more tips, read <a href="/guides/how-to-study-for-a-quiz/">How to Study for a Quiz: 7 Tips That Actually Work</a>.</p>
<h2>For teachers</h2>
<p>Share a game link with your class as a warm-up or homework. Students don’t need accounts, and their scores are saved only on their own device. When it’s time for a real quiz, <a href="/teacher/">QuizPolice</a> lets you monitor Google Forms, Microsoft Forms and Wayground quizzes for free.</p>'''

PAGES = [
 ('/practice/math-sprint/', 'Math Sprint: Free 60-Second Math Practice Game',
  'A free 60-second math game for students: addition, subtraction, times tables and division. No sign-up, works on phones and computers.',
  'Math Sprint', lambda: MATH_GAME, MATH_TEXT),
 ('/practice/geography/', 'Geography Practice: Countries and Capitals Quiz Game',
  'A free geography game for students: name the capital or the country, by region or for the whole world. 10 questions a round, no sign-up.',
  'Geography Practice', geo_game, GEO_TEXT),
]
