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
<a href="/practice/percent-sprint/"><b>Percent &amp; Estimation Sprint</b>Percentages, discounts, tips, fractions and quick estimates. Everyday math for high school and college.</a>
<a href="/practice/spot-the-fallacy/"><b>Spot the Fallacy</b>For college students: read short arguments and name the logical fallacy. Learn 12 common fallacies with examples.</a>
<a href="https://drafttrail.telarlabs.net/practice/word-choice/"><b>Word Choice Check</b>Affect or effect? Fewer or less? Practice commonly confused words for essays. On our writing app, DraftTrail.</a>
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

BEFORE = ('/before-your-quiz/', 'Before Your Online Quiz: A Quick Checklist for Students',
 'What to do before an online quiz on your phone or laptop: a quick checklist, what QuizPolice can and can’t see, and what to do if something goes wrong.',
'''<p class="lead">Got a few minutes before your quiz starts? Read this quick checklist so nothing surprises you, then warm up with a practice game.</p>

<h2>The 2-minute checklist</h2>
<ul><li><b>Battery:</b> at least half charged, or plug in your charger now.</li>
<li><b>Internet:</b> sit where your Wi-Fi or mobile signal is strong. Don’t start a big download.</li>
<li><b>Other apps:</b> close games, videos and chat apps. Turn on <b>Do Not Disturb</b> so messages and calls don’t pop up.</li>
<li><b>Your name:</b> type your full name exactly the way your teacher knows you, and choose the right section.</li>
<li><b>Paper and pencil:</b> if your teacher allows scratch paper, have it ready so you don’t need another app.</li>
<li><b>Ask now:</b> if you’re allowed to use a calculator or notes, check with your teacher <i>before</i> you start.</li></ul>

<h2>What QuizPolice can see, and what it can’t</h2>
<p>Many teachers use QuizPolice to keep online quizzes fair. It’s good to know exactly what it does:</p>
<ul><li>It <b>can</b> see when you leave the quiz page on the device you joined with: switching to another app or tab, going to your home screen, or clicking outside the quiz window. Your teacher sees when it happened and how long you were away.</li>
<li>It <b>can’t</b> see your screen, your photos, your messages, other devices, or what you search. Nothing outside the quiz page is monitored.</li></ul>
<p>Your teacher may set a number of exits allowed. If you leave too many times, the quiz locks and you’ll need to ask your teacher to unlock it.</p>

<h2>Things that can count as leaving, even by accident</h2>
<ul><li>Tapping a notification that pops up at the top of the screen.</li>
<li>Answering a call, or opening the calculator or camera app.</li>
<li>Swiping up to the home screen or switching apps with a gesture.</li>
<li>On a computer, clicking on another window or the taskbar.</li></ul>
<p>That’s why Do Not Disturb matters. If something happens by accident, don’t panic: just come straight back and tell your teacher what happened.</p>

<h2>During the quiz</h2>
<ul><li><b>Watch the timer</b> if your quiz has one. You’ll see reminders when time is almost up.</li>
<li><b>If the quiz doesn’t load,</b> stay on the page and tell your teacher. Don’t open the quiz in another tab, because that counts as leaving.</li>
<li><b>If your internet drops,</b> reconnect and open the quiz page again. If it asks, join with the same name. Then tell your teacher.</li></ul>

<h2>When you finish</h2>
<ol><li>Press <b>Submit</b> on the quiz itself (in Google Forms, Microsoft Forms or Wayground) and wait for the confirmation message.</li>
<li>Then press <b>I’ve submitted</b> in QuizPolice, so your teacher sees that you’re done.</li></ol>
<p>For a writing task, press <b>Hand in my writing</b> when you’re finished.</p>

<h2>Early? Warm up</h2>
<p>A short warm-up gets your brain going. Try a 60-second <a href="/practice/math-sprint/">Math Sprint</a> or a round of <a href="/practice/geography/">Geography Practice</a>. Just make sure you’re back on the quiz page before it starts.</p>
<p>Want to do better on your next quiz? Read <a href="/guides/how-to-study-for-a-quiz/">How to Study for a Quiz: 7 Tips That Actually Work</a>.</p>

<h2>Good luck!</h2>
<p>Take a slow breath, read every question to the end, and do your best. You’ve got this.</p>''')

# ---------------------------------------------------------------- Spot the Fallacy (college level)
FALLACIES = {
 'straw':  ('Straw man', 'Twisting someone’s point into a weaker or more extreme version, then attacking that instead.'),
 'dilemma':('False dilemma', 'Pretending there are only two options when there are more.'),
 'slope':  ('Slippery slope', 'Claiming one small step will lead to a chain of extreme results, without showing why.'),
 'hominem':('Ad hominem', 'Attacking the person making the argument instead of the argument itself.'),
 'auth':   ('Appeal to authority', 'Treating someone’s opinion as proof, especially when they aren’t an expert on the topic.'),
 'hasty':  ('Hasty generalization', 'Drawing a big conclusion from too few examples.'),
 'wagon':  ('Bandwagon', 'Saying something is true or good because many people believe or do it.'),
 'posthoc':('False cause', 'Assuming that because B happened after A, A must have caused B.'),
 'circle': ('Circular reasoning', 'Using the conclusion as the reason for the conclusion.'),
 'herring':('Red herring', 'Changing the subject to something that doesn’t answer the question.'),
 'tuq':    ('Tu quoque', 'Rejecting advice or criticism because the other person does the same thing (“you do it too”).'),
 'nature': ('Appeal to nature', 'Assuming something is good because it’s “natural”, or bad because it isn’t.'),
}
# pairs that overlap, so they are never offered together as answer choices
FAL_CLASH = [('hominem', 'tuq'), ('posthoc', 'hasty')]
FAL_Q = [
 ('Mei: “We should spend a bit less on the sports budget this year.” Jason: “So Mei wants to get rid of sports and make everyone sit inside all day.”', 'straw',
  'Mei only suggested spending less. Jason attacks a much more extreme position she never took.'),
 ('Professor: “Please cite your sources more carefully.” Student: “So now we’re not allowed to use anyone else’s ideas at all? That’s ridiculous.”', 'straw',
  'The professor asked for careful citing, not a ban on using sources. The student argues against a claim nobody made.'),
 ('“You think the app needs a dark mode? So you’re saying the whole design is garbage and we wasted a year.”', 'straw',
  'Asking for one feature isn’t the same as rejecting the whole design. The reply exaggerates the request to dismiss it.'),
 ('“Either you pull an all-nighter tonight, or you’re going to fail the exam.”', 'dilemma',
  'There are other options: studying in shorter sessions, focusing on key topics, or asking for help.'),
 ('“You’re either with the club’s new plan, or you don’t care about the club.”', 'dilemma',
  'Someone can care about the club and still disagree with this plan, or want changes to it.'),
 ('“The college can either raise tuition or close the library. There’s no other way.”', 'dilemma',
  'Budgets have many other options, like cutting other costs or finding new funding. Only two are presented.'),
 ('“If we let students retake one quiz, soon they’ll expect to retake every exam, and grades will mean nothing.”', 'slope',
  'One retake policy doesn’t automatically lead to unlimited retakes. The chain of events is assumed, not shown.'),
 ('“If I skip the gym today, I’ll skip tomorrow too, and by next month I’ll have given up on my health completely.”', 'slope',
  'Missing one day doesn’t force a chain of failures. Each step in the chain is just assumed.'),
 ('“If the café lets people use laptops, they’ll stay all day, nobody will buy anything, and the café will go out of business.”', 'slope',
  'Each step might happen, but none is shown to follow. Many cafés allow laptops and do fine.'),
 ('“Why should we take Kevin’s budget plan seriously? He can’t even keep his own room clean.”', 'hominem',
  'Kevin’s room says nothing about whether his budget plan is good. The reply attacks Kevin instead of the plan.'),
 ('“Her analysis of the survey data doesn’t count. She’s only a first-year student.”', 'hominem',
  'The analysis is right or wrong on its own merits. Being a first-year student doesn’t make the numbers wrong.'),
 ('“Of course Lucas thinks the essay deadline is too short. He’s just lazy.”', 'hominem',
  'Calling Lucas lazy doesn’t answer whether the deadline is reasonable. It attacks him, not his point.'),
 ('“A famous actor says this supplement improves memory, so it must work.”', 'auth',
  'Acting fame isn’t evidence about supplements. What matters is research on the supplement itself.'),
 ('“My economics professor says this is the best movie ever made, so it is.”', 'auth',
  'Being an expert in economics doesn’t make someone an authority on film, and taste isn’t proof anyway.'),
 ('“A star football player recommends this new crypto coin, so it must be a safe investment.”', 'auth',
  'A sports star isn’t an expert on investing, and an endorsement isn’t evidence that something is safe.'),
 ('“I met two rude people from that city, so everyone there must be rude.”', 'hasty',
  'Two people can’t represent a whole city. The sample is far too small for such a big conclusion.'),
 ('“My first online class was boring, so online classes are a waste of time.”', 'hasty',
  'One class is too small a sample to judge every online class.'),
 ('“Three of my friends got A’s without studying, so studying doesn’t really matter.”', 'hasty',
  'Three friends aren’t enough to draw a general rule, and they may be unusual in other ways.'),
 ('“Everyone in our dorm is buying this laptop, so it must be the best one.”', 'wagon',
  'Popularity in one dorm doesn’t prove quality. Specs, price and reviews would be better reasons.'),
 ('“Millions of people use this diet app, so its advice must be right.”', 'wagon',
  'A large number of users doesn’t make advice correct. That needs evidence about the advice itself.'),
 ('“Nobody in our class reads the syllabus, so it can’t be important.”', 'wagon',
  'What most people do isn’t proof of what matters. The syllabus might still contain key information.'),
 ('“I wore my lucky hoodie and got an A. The hoodie works!”', 'posthoc',
  'The A came after wearing the hoodie, but that doesn’t mean the hoodie caused it. Studying is a likelier cause.'),
 ('“Sales went up the month after we changed the logo, so the new logo caused the increase.”', 'posthoc',
  'Many things could explain the rise, like the season or a promotion. Timing alone doesn’t prove cause.'),
 ('“I drank an energy drink right before the exam and did well, so energy drinks make you smarter.”', 'posthoc',
  'Doing well after the drink doesn’t mean the drink caused it. The student also prepared for the exam.'),
 ('“This is the best university in the country because it’s the top school in the nation.”', 'circle',
  '“Best” and “top” mean the same thing here. The claim is used as its own reason.'),
 ('“You can trust this website because it says it’s a trustworthy source.”', 'circle',
  'The website’s trustworthiness is the thing in question, so its own claim can’t prove it.'),
 ('“Professor Chen is always right because she never makes mistakes.”', 'circle',
  '“Never makes mistakes” is just another way of saying “always right”. No real reason is given.'),
 ('Teammate: “Why is the group report late?” Reply: “Well, did you see how much work I did on last semester’s project?”', 'herring',
  'Last semester’s project has nothing to do with why this report is late. The reply changes the subject.'),
 ('Reporter: “Will campus parking fees go up next year?” Manager: “Our campus has won three awards for its beautiful gardens.”', 'herring',
  'The gardens don’t answer the question about parking fees. The topic is quietly switched.'),
 ('When asked why the app keeps crashing, the developer talks about how many people downloaded it last year.', 'herring',
  'Download numbers don’t explain the crashes. It’s a distraction from the real question.'),
 ('“You told me to stop using my phone in class, but you were on your phone yesterday.”', 'tuq',
  'Whether the advice is good doesn’t depend on whether the person giving it follows it.'),
 ('“My roommate says I should eat healthier, but he eats instant noodles every night.”', 'tuq',
  'The roommate’s own habits don’t make the advice wrong. Pointing out “you do it too” avoids the point.'),
 ('Mom: “You should stop staying up so late before exams.” Leo: “You stay up late watching shows all the time!”', 'tuq',
  'Mom’s own habits don’t make her advice wrong. Leo dodges the advice by saying “you do it too”.'),
 ('“This herbal tea is natural, so it can’t have any side effects.”', 'nature',
  'Many natural substances have side effects or are harmful. “Natural” doesn’t mean safe.'),
 ('“This shampoo has only natural ingredients and no chemicals, so it must be better for your hair.”', 'nature',
  'Everything, including natural ingredients, is made of chemicals. Being natural doesn’t make something better.'),
 ('“Air conditioning isn’t natural, so it must be bad for you.”', 'nature',
  'Something being man-made doesn’t make it harmful. Its effects need to be judged on evidence.'),
]

def fallacy_game():
    import json
    F = json.dumps({k: v[0] for k, v in FALLACIES.items()}, ensure_ascii=False)
    Q = json.dumps(FAL_Q, ensure_ascii=False)
    C = json.dumps(FAL_CLASH)
    return '''<div class="game" id="fg">
 <div id="fgSetup">
  <h2>Spot the Fallacy</h2><p class="gsub">Read the argument. Which logical fallacy is it? 10 questions a round.</p>
  <p class="glabel">How it works</p>
  <p style="margin:4px 0 14px;font-size:16px">Each question shows a short argument and four fallacy names. After you answer, you’ll see why. The guide below explains all 12 fallacies.</p>
  <button class="gbtn" id="fgStart">Start</button>
 </div>
 <div id="fgPlay" hidden>
  <div class="gtop"><span id="fgNum"></span><span>Score: <b id="fgScore">0</b></span></div>
  <div class="gbar"><i id="fgBar"></i></div>
  <blockquote class="farg" id="fgQ"></blockquote>
  <div class="gopts" id="fgOpts"></div>
  <div class="gfb fexp" id="fgFb"></div>
  <button class="gbtn" id="fgNext" hidden>Next</button>
 </div>
 <div id="fgEnd" class="gres" hidden>
  <p class="glabel">Round complete</p><div class="gbig" id="fgFinal"></div><p id="fgNote" class="muted"></p>
  <ul class="gmiss" id="fgMiss"></ul>
  <div class="grow"><button class="gbtn" id="fgAgain">Play again</button><a class="gbtn ghost" href="#guide" style="text-align:center;text-decoration:none">Read the guide</a></div>
 </div>
</div>
<style>.farg{margin:12px 0 4px;padding:14px 16px;background:var(--bg);border-left:4px solid var(--badge);border-radius:8px;font-size:18px;line-height:1.5}
.fexp{text-align:left;font-weight:400;font-size:16px;line-height:1.5;margin:4px 0 12px}.fexp b{display:block}</style>
<script>
(()=>{const F=''' + F + ''',Q=''' + Q + ''',CL=''' + C + ''';
const $=i=>document.getElementById(i),sh=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const get=k=>{try{return +localStorage.getItem(k)||0}catch(e){return 0}},put=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
const clash=(a,b)=>CL.some(p=>(p[0]===a&&p[1]===b)||(p[0]===b&&p[1]===a));
let qs=[],n=0,score=0,miss=[],locked=false;
function start(){qs=sh(Q).slice(0,10);n=0;score=0;miss=[];$('fgScore').textContent=0;$('fgSetup').hidden=true;$('fgEnd').hidden=true;$('fgPlay').hidden=false;ask();$('fg').scrollIntoView({block:'nearest'})}
function ask(){const q=qs[n];locked=false;$('fgNum').textContent='Question '+(n+1)+' of '+qs.length;$('fgBar').style.width=(n/qs.length*100)+'%';$('fgQ').textContent=q[0];
 const wrong=sh(Object.keys(F).filter(k=>k!==q[1]&&!clash(k,q[1]))).slice(0,3);const opts=sh([q[1],...wrong]);
 $('fgOpts').innerHTML='';$('fgFb').innerHTML='';$('fgNext').hidden=true;
 opts.forEach(k=>{const b=document.createElement('button');b.textContent=F[k];b.dataset.k=k;b.onclick=()=>choose(b,k===q[1]);$('fgOpts').appendChild(b)})}
function choose(b,ok){if(locked)return;locked=true;const q=qs[n];
 document.querySelectorAll('#fgOpts button').forEach(x=>{x.disabled=true;if(x.dataset.k===q[1])x.classList.add('ok')});
 if(ok){score++;$('fgScore').textContent=score}else{b.classList.add('bad');miss.push(q)}
 $('fgFb').innerHTML='<b style="color:'+(ok?'#2e9e5b':'#b23a3a')+'">'+(ok?'Correct! ':'Not quite. ')+'It’s '+F[q[1]].toLowerCase()+'.</b>'+q[2];
 $('fgNext').textContent=n+1<qs.length?'Next':'See my score';$('fgNext').hidden=false}
$('fgNext').onclick=()=>{n++;if(n<qs.length)ask();else end()};
document.addEventListener('keydown',e=>{if($('fgPlay').hidden)return;const bs=document.querySelectorAll('#fgOpts button');
 if(!locked&&/^[1-4]$/.test(e.key)&&bs[+e.key-1]){bs[+e.key-1].click();e.preventDefault()}else if(locked&&e.key==='Enter'){$('fgNext').click();e.preventDefault()}});
function end(){$('fgBar').style.width='100%';$('fgPlay').hidden=true;$('fgEnd').hidden=false;const best=get('qp-fal');
 $('fgFinal').textContent=score+' / '+qs.length;$('fgNote').textContent=score===10?'Perfect round. Sharp thinking!':score>best?'New best score!':'Your best: '+best+' / 10';if(score>best)put('qp-fal',score);
 $('fgMiss').innerHTML=miss.length?'<li><b>Review these:</b></li>'+miss.map(q=>'<li><b>'+F[q[1]]+':</b> '+q[0]+'</li>').join(''):'<li>No misses. Play again for new questions.</li>'}
$('fgStart').onclick=start;$('fgAgain').onclick=start;})();
</script>'''

FAL_EX = {
 'straw': '“You want fewer cars downtown? So you want to ban cars completely?”',
 'dilemma': '“Either we cancel the trip or everyone gets soaked.” (You could bring umbrellas or change the plan.)',
 'slope': '“If we allow one late submission, nobody will ever submit on time again.”',
 'hominem': '“Don’t listen to his idea about the schedule. He’s always late himself.”',
 'auth': '“A famous singer says this phone is the most secure, so it is.”',
 'hasty': '“The first two restaurants on this street were bad, so the whole street is bad.”',
 'wagon': '“Everyone’s taking this elective, so it must be the most useful one.”',
 'posthoc': '“I started using a new pen and my grades went up, so the pen helped.”',
 'circle': '“This source is reliable because it’s a source you can rely on.”',
 'herring': 'Asked about a rent increase, the landlord talks about the new lobby paint.',
 'tuq': '“You can’t tell me to save money. You bought a new phone last month.”',
 'nature': '“It’s natural, so it’s healthy.”',
}
FAL_TIP = {
 'straw': 'Restate their real point first: “I think you’re saying X. Is that right?”',
 'dilemma': 'Ask: “Are these really the only two options?” and name a third.',
 'slope': 'Ask for evidence that each step actually leads to the next.',
 'hominem': 'Separate the person from the claim: would the argument be wrong if someone else made it?',
 'auth': 'Check whether the person is an expert in this topic, and what the evidence says.',
 'hasty': 'Ask how many examples there are, and whether they represent the whole group.',
 'wagon': 'Ask why it’s popular, and whether popularity says anything about whether it’s true.',
 'posthoc': 'Look for other explanations and for evidence beyond timing.',
 'circle': 'Ask: “What’s the reason, apart from the claim itself?”',
 'herring': 'Bring it back: “That’s interesting, but it doesn’t answer the question.”',
 'tuq': 'Ask whether the advice is good, regardless of who gives it.',
 'nature': 'Judge the thing by its effects, not by whether it’s natural or man-made.',
}

def fallacy_text():
    items = ''.join(f'<h3>{i}. {n}</h3><p>{d}</p><p><i>Example:</i> {FAL_EX[k]}</p><p><i>How to respond:</i> {FAL_TIP[k]}</p>'
                    for i, (k, (n, d)) in enumerate(FALLACIES.items(), 1))
    return f'''<h2 id="guide">What is a logical fallacy?</h2>
<p>A logical fallacy is a mistake in reasoning: an argument that sounds convincing but doesn’t actually support its conclusion. Fallacies show up everywhere, from group chats and ads to debates, news comments and even research papers. Learning to spot them helps you write stronger essays, argue more fairly, and avoid being fooled.</p>
<p>One important point: an argument with a fallacy can still have a true conclusion. The fallacy only means <i>that argument</i> doesn’t prove it. Saying “your argument has a fallacy, so you’re wrong” is a fallacy too.</p>

<h2>12 common fallacies, with examples</h2>
{items}

<h2>Why this matters in college</h2>
<ul><li><b>Essays and research papers:</b> professors look for arguments supported by evidence. Fallacies are one of the most common reasons a strong-sounding paragraph loses marks.</li>
<li><b>Debates, seminars and group projects:</b> naming a fallacy calmly (“that feels like a false dilemma, are there other options?”) moves a discussion forward without attacking anyone.</li>
<li><b>Everyday life:</b> ads, viral posts and sales pitches often rely on bandwagon, false cause and appeals to authority. Spotting them is a practical defense.</li></ul>

<h2>Tips for avoiding fallacies in your own writing</h2>
<ul><li>For each claim, ask: what’s my evidence, and is it enough?</li>
<li>Describe opposing views fairly before you answer them.</li>
<li>Be careful with words like <i>always</i>, <i>never</i>, <i>everyone</i> and <i>only</i>.</li>
<li>Look for other explanations before claiming one thing caused another.</li>
<li>Read your argument as if you were your toughest critic.</li></ul>
<p>Writing an essay in class? Teachers can use <a href="https://drafttrail.telarlabs.net/">DraftTrail</a> to see how a piece of writing was built, step by step.</p>

<h2>For teachers</h2>
<p>Spot the Fallacy works as a warm-up for critical thinking, philosophy, English, debate or media literacy classes. Ask students to play a round, then pick the example they found hardest and explain it to a partner, or write their own example of each fallacy. It’s free, needs no accounts and works on phones. Scores stay on the student’s device.</p>

<h2>Questions</h2>
<p><b>Can one argument have more than one fallacy?</b> Yes. Some overlap, like ad hominem and tu quoque. In the game, the answer choices never include two fallacies that would both be correct.</p>
<p><b>Are there more than 12 fallacies?</b> Many more. These 12 are among the most common and the most useful to recognize first.</p>
<p><b>Is it free?</b> Yes, completely, with no sign-up.</p>'''

PAGES.append(('/practice/spot-the-fallacy/', 'Spot the Fallacy: Logical Fallacies Quiz Game with Examples',
  'A free logical fallacies game for college students: read short arguments, spot the fallacy, and learn 12 common fallacies with examples.',
  'Spot the Fallacy', fallacy_game, fallacy_text()))

# ---------------------------------------------------------------- Percent & Estimation Sprint
PCT_GAME = '''<div class="game" id="ps">
 <div id="psSetup">
  <h2>Percent &amp; Estimation Sprint</h2><p class="gsub">Everyday math, fast. Tap the right answer. 60 seconds.</p>
  <p class="glabel">Choose a level</p>
  <div class="gchips" id="psLv"></div>
  <button class="gbtn" id="psStart">Start</button>
 </div>
 <div id="psPlay" hidden>
  <div class="gtop"><span id="psLvName"></span><span>Score: <b id="psScore">0</b></span></div>
  <div class="gbar"><i id="psBar"></i></div>
  <div class="gq2" id="psQ" style="min-height:64px"></div>
  <div class="gopts" id="psOpts"></div>
 </div>
 <div id="psEnd" class="gres" hidden>
  <p class="glabel">Time’s up!</p><div class="gbig" id="psFinal"></div><p id="psNote" class="muted"></p>
  <ul class="gmiss" id="psMiss"></ul>
  <div class="grow"><button class="gbtn" id="psAgain">Play again</button><button class="gbtn ghost" id="psBack">Change level</button></div>
 </div>
</div>
<script>
(()=>{const $=i=>document.getElementById(i),r=(a,b)=>a+Math.floor(Math.random()*(b-a+1)),pick=a=>a[Math.floor(Math.random()*a.length)];
const sh=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const num=v=>(Math.round(v*100)/100).toLocaleString('en-US',{maximumFractionDigits:2});
const usd=v=>'$'+(Math.round(v*100)%100?(Math.round(v*100)/100).toFixed(2):Math.round(v).toLocaleString('en-US'));
function mk(q,a,cands,f){f=f||num;const A=f(a),seen=new Set([A]),o=[];for(const c of cands){if(!(c>0))continue;const s=f(c);if(!seen.has(s)){seen.add(s);o.push(s)}if(o.length===3)break}
 let k=1;while(o.length<3){const s=f(a*(1+k*0.2));if(!seen.has(s)){seen.add(s);o.push(s)}k++}return[q,A,sh([A,...o])]}
const FR=[['1/2','0.5','50%'],['1/4','0.25','25%'],['3/4','0.75','75%'],['1/5','0.2','20%'],['2/5','0.4','40%'],['3/5','0.6','60%'],['4/5','0.8','80%'],['1/8','0.125','12.5%'],['3/8','0.375','37.5%'],['5/8','0.625','62.5%'],['7/8','0.875','87.5%'],['1/10','0.1','10%'],['3/10','0.3','30%'],['1/20','0.05','5%'],['3/20','0.15','15%'],['1/3','0.333…','33⅓%'],['2/3','0.666…','66⅔%'],['1/25','0.04','4%']];
const LV={
 pct:['Percent of a number',()=>{const p=pick([5,10,15,20,25,30,40,50,60,75]),n=20*r(1,20),a=p*n/100;return mk(p+'% of '+n+' = ?',a,sh([p*n/10,a+n/10,n-a,a*2,a/2]))}],
 money:['Discounts & tips',()=>{if(Math.random()<.55){const pr=10*r(2,30),off=pick([10,20,25,30,40,50]),d=pr*off/100;
   return mk('A '+usd(pr)+' item is '+off+'% off. What’s the sale price?',pr-d,sh([d,pr-off,pr+d,pr-d*2]),usd)}
  const b=5*r(2,20),t=pick([10,15,20]),a=b*t/100;return mk('A '+t+'% tip on a '+usd(b)+' bill is…',a,sh([a*2,a/2,b*(t===15?.2:.15),b*t/1000*10+1]),usd)}],
 frac:['Fractions, decimals, percents',()=>{const e=pick(FR),t=pick([[0,1],[0,2],[1,0],[2,0]]),o=sh(FR.filter(x=>x!==e)).slice(0,3).map(x=>x[t[1]]);
   return[e[t[0]]+' = ?',e[t[1]],sh([e[t[1]],...o])]}],
 est:['Estimation',()=>{const k=r(0,2);
  if(k===0){const A=10*r(2,9),B=10*r(2,9),a=A+pick([-2,-1,1,2]),b=B+pick([-2,-1,1,2]),e=A*B;return['Which is closest to '+a+' × '+b+'?',num(e),sh([num(e),num(e*10),num(e/10),num(e*2)])]}
  if(k===1){const T=5*r(4,16),p1=r(150,T*40)/100,p2=r(150,Math.max(160,(T-p1)*50))/100,p3=T-p1-p2+(r(-40,40)/100);if(p3<1)return LV.est[1]();
   return['About how much is '+usd(p1)+' + '+usd(p2)+' + '+usd(p3)+'?',usd(T),sh([usd(T),usd(T+10),usd(Math.max(5,T-10)),usd(T+20)])]}
  const P=pick([10,20,25,50]),B=100*r(2,9),p=P+pick([-1,1]),b=B+r(-4,4),e=P*B/100;return['About how much is '+p+'% of '+b+'?',num(e),sh([num(e),num(e*2),num(e/2),num(e*10)])]}],
 mix:['Mix it up',()=>LV[pick(['pct','money','frac','est'])][1]()]};
let lv='pct',score=0,miss=[],cur=null,t0=0,raf=0,on=false;const T=60;
const get=k=>{try{return +localStorage.getItem(k)||0}catch(e){return 0}},put=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
Object.entries(LV).forEach(([k,[n]])=>{const b=document.createElement('button');b.textContent=n;if(k===lv)b.className='on';b.onclick=()=>{lv=k;document.querySelectorAll('#psLv button').forEach(x=>x.classList.toggle('on',x===b))};$('psLv').appendChild(b)});
function next(){let q;do{q=LV[lv][1]()}while(cur&&q[0]===cur[0]);cur=q;$('psQ').textContent=q[0];$('psOpts').innerHTML='';
 q[2].forEach(o=>{const b=document.createElement('button');b.textContent=o;b.onclick=()=>choose(b,o);$('psOpts').appendChild(b)})}
function choose(b,o){if(!on)return;on=false;const ok=o===cur[1];document.querySelectorAll('#psOpts button').forEach(x=>{if(x.textContent===cur[1])x.classList.add('ok')});
 if(ok){score++;$('psScore').textContent=score}else{b.classList.add('bad');miss.push([cur[0],cur[1],o])}
 setTimeout(()=>{if(performance.now()-t0<T*1000){on=true;next()}},ok?260:900)}
document.addEventListener('keydown',e=>{if($('psPlay').hidden)return;const bs=document.querySelectorAll('#psOpts button');if(/^[1-4]$/.test(e.key)&&bs[+e.key-1]){bs[+e.key-1].click();e.preventDefault()}});
function tick(){const left=T-(performance.now()-t0)/1000;$('psBar').style.width=Math.max(0,left/T*100)+'%';if(left<=0)return end();raf=requestAnimationFrame(tick)}
function start(){score=0;miss=[];cur=null;$('psScore').textContent=0;$('psLvName').textContent=LV[lv][0];$('psSetup').hidden=true;$('psEnd').hidden=true;$('psPlay').hidden=false;on=true;next();t0=performance.now();cancelAnimationFrame(raf);tick();$('ps').scrollIntoView({block:'nearest'})}
function end(){on=false;$('psPlay').hidden=true;$('psEnd').hidden=false;const k='qp-ps-'+lv,best=get(k),tot=score+miss.length;
 $('psFinal').textContent=score+' right';$('psNote').textContent=LV[lv][0]+(score>best?' · New best score!':' · Your best: '+best)+(tot?' · '+Math.round(score/tot*100)+'% correct':'');if(score>best)put(k,score);
 $('psMiss').innerHTML=miss.length?'<li><b>Practice these:</b></li>'+miss.slice(0,8).map(m=>'<li>'+m[0]+' <b>'+m[1]+'</b> <span class="muted">(you chose '+m[2]+')</span></li>').join(''):'<li>No mistakes. Try a harder level or Mix it up.</li>'}
$('psStart').onclick=start;$('psAgain').onclick=start;$('psBack').onclick=()=>{$('psEnd').hidden=true;$('psSetup').hidden=false};})();
</script>'''

PCT_TEXT = '''<h2>How to play</h2>
<ol><li>Choose a level, or <b>Mix it up</b> for a bit of everything.</li>
<li>Press <b>Start</b>. You have 60 seconds.</li>
<li>Tap the right answer. A wrong answer shows the correct one for a moment, then the game moves on.</li>
<li>At the end, review the ones you missed.</li></ol>

<h2>The levels</h2>
<ul><li><b>Percent of a number:</b> 15% of 240, 75% of 60, and so on.</li>
<li><b>Discounts &amp; tips:</b> sale prices and tips, the percent math you actually use when you shop or eat out.</li>
<li><b>Fractions, decimals, percents:</b> 3/8 = 0.375 = 37.5%. These come up constantly in statistics, science and finance.</li>
<li><b>Estimation:</b> pick the closest answer without calculating exactly, like 49 × 31 or the total of three prices.</li></ul>

<h2>Shortcuts that make percents easy</h2>
<ul><li><b>10% is just moving the decimal point.</b> 10% of 240 is 24. Then 5% is half of that (12), and 15% is 24 + 12 = 36.</li>
<li><b>Percents can be flipped.</b> 8% of 50 is the same as 50% of 8, which is 4.</li>
<li><b>25% is a quarter, 50% is a half, 75% is three quarters.</b> 75% of 60 = 60 − 15 = 45.</li>
<li><b>Sale price = price × what’s left.</b> 30% off means you pay 70%: 0.7 × $80 = $56.</li>
<li><b>Know the eighths.</b> 1/8 = 12.5%, so 3/8 = 37.5%, 5/8 = 62.5% and 7/8 = 87.5%.</li></ul>

<h2>Why estimation is a real skill</h2>
<p>Estimating is how you catch mistakes. If a calculator says 49 × 31 = 15,190, a quick estimate (50 × 30 = 1,500) tells you a digit slipped. Good estimators round to easy numbers, calculate, and then ask whether the answer makes sense. It’s useful in exams, in lab work, in budgeting and when checking a bill.</p>
<ul><li>Round each number to one or two easy digits before multiplying.</li>
<li>For a total of prices, round each price to the nearest dollar.</li>
<li>For “about 19% of 503”, think “20% of 500”, which is 100.</li></ul>

<h2>Who it’s for</h2>
<p>High school and college students preparing for exams in statistics, business, economics, nursing or science, and anyone who wants faster mental math for daily life. Teachers can use one round as a warm-up. It’s free, there’s no sign-up, and scores stay on your device.</p>
<p>Prefer basic facts first? Try <a href="/practice/math-sprint/">Math Sprint</a> for adding, subtracting, times tables and division.</p>'''

PAGES.append(('/practice/percent-sprint/', 'Percent & Estimation Sprint: Mental Math Practice Game',
  'A free 60-second mental math game: percentages, discounts and tips, fractions to decimals, and estimation. For high school and college students.',
  'Percent & Estimation Sprint', lambda: PCT_GAME, PCT_TEXT))
