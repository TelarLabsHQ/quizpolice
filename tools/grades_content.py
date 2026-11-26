"""Grade tools on QuizPolice: grade calculator (DO 015 s. 2026, three terms), transmutation tables, weighted grade calculator.
Everything runs in the browser; nothing is stored on a server (only in the visitor's own browser, to keep their numbers)."""

# DepEd Order No. 015, s. 2026: adjusted transmutation table for SY 2026-2027 (lowest initial grade of each band -> grade)
NEW_TABLE = [(99.50, 100), (98.32, 99), (97.14, 98), (95.96, 97), (94.78, 96), (93.60, 95), (92.42, 94), (91.24, 93), (90.06, 92), (88.88, 91),
             (87.70, 90), (86.52, 89), (85.34, 88), (84.16, 87), (82.98, 86), (81.80, 85), (80.62, 84), (79.44, 83), (78.26, 82), (77.08, 81),
             (75.90, 80), (74.72, 79), (73.54, 78), (72.36, 77), (71.18, 76), (70.00, 75), (65.34, 74), (60.67, 73), (56.01, 72), (51.34, 71),
             (46.67, 70), (42.01, 69), (37.34, 68), (32.68, 67), (28.01, 66), (23.35, 65), (18.68, 64), (14.01, 63), (9.35, 62), (4.68, 61), (0.00, 60)]
# DepEd Order No. 8, s. 2015 (the old table): 100 -> 100, then bands of 1.60 down to 60 (= 75), then bands of 4.00
OLD_TABLE = [(100.0, 100)] + [(round(60 + 1.6 * k, 2), 75 + k) for k in range(24, -1, -1)] + [(round(4.0 * k, 2), 60 + k) for k in range(14, -1, -1)]

def _ranges(t):
    out = []
    for i, (lo, g) in enumerate(t):
        hi = 100.0 if i == 0 else round(t[i - 1][0] - 0.01, 2)
        out.append((lo, hi, g))
    return out

def table_html(t, cap):
    rows = ''.join(f'<tr><td>{lo:.2f} – {hi:.2f}</td><td><b>{g}</b></td></tr>' for lo, hi, g in _ranges(t))
    return f'<table class="ttab"><caption>{cap}</caption><thead><tr><th>Initial grade</th><th>Transmuted grade</th></tr></thead><tbody>{rows}</tbody></table>'

# weights: (label, WW, PT, EX, exam mode) exam mode: 'split' = ST1 30% + ST2 30% + Term exam 40%; 'te' = term exam only; 'qa' = one quarterly assessment (old order)
GROUPS = [
 ('Grades 4–10 (DO 015, s. 2026)', [
   ('g4a', 'English, Filipino, Math, Science, AP, GMRC / Values Education', 20, 50, 30, 'split'),
   ('g4b', 'EPP / TLE, MAPEH', 20, 60, 20, 'split')]),
 ('Grades 2–3 (DO 015, s. 2026)', [
   ('g2a', 'Makabansa and other graded subjects', 20, 50, 30, 'split')]),
 ('Senior High School, strengthened curriculum (DO 015, s. 2026)', [
   ('s1', 'Core subjects and other academic electives', 20, 50, 30, 'split'),
   ('s2', 'Field Exposure, Arts Apprenticeship, Creative Production and Innovation', 15, 70, 15, 'te'),
   ('s3', 'Arts, Sports, Health and Wellness electives', 20, 60, 20, 'split'),
   ('s4', 'Research electives, Design and Innovation', 40, 60, 0, 'split'),
   ('s5', 'TechPro electives', 15, 65, 20, 'split'),
   ('s6', 'Work Immersion', 20, 80, 0, 'split')]),
 ('Old weights (DO 8, s. 2015), e.g. Grade 12 not yet on the strengthened curriculum', [
   ('o1', 'Grades 1–10: Languages, AP, EsP', 30, 50, 20, 'qa'),
   ('o2', 'Grades 1–10: Science, Math', 40, 40, 20, 'qa'),
   ('o3', 'Grades 1–10: MAPEH, EPP / TLE', 20, 60, 20, 'qa'),
   ('o4', 'SHS: Core subjects', 25, 50, 25, 'qa'),
   ('o5', 'SHS Academic track: all other subjects', 25, 45, 30, 'qa'),
   ('o6', 'SHS Academic track: Work Immersion, Research, Business Enterprise Simulation, Exhibit, Performance', 35, 40, 25, 'qa'),
   ('o7', 'SHS TVL, Sports, Arts and Design tracks: all subjects', 20, 60, 20, 'qa')]),
 ('Other', [('cu', 'Custom weights', 30, 50, 20, 'qa')]),
]

def _opts():
    return ''.join(f'<optgroup label="{g}">' + ''.join(f'<option value="{k}">{lab} ({w}/{p}/{x})</option>' for k, lab, w, p, x, m in items) + '</optgroup>' for g, items in GROUPS)

def _js_groups():
    import json
    return json.dumps({k: [w, p, x, m] for g, items in GROUPS for k, lab, w, p, x, m in items})

CSS = '''<style>
.gc{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;display:flex;flex-direction:column;gap:14px;margin:16px 0 24px}
.gc label{display:flex;flex-direction:column;gap:5px;font-weight:700;font-size:15px}.gc select,.gc input{font:inherit;font-size:16px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--fg);min-width:0}
.gc [hidden]{display:none!important}.gc select{width:100%;max-width:100%;text-overflow:ellipsis}.gc label{min-width:0}
.gc .row2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px}@media(max-width:560px){.gc .row2{grid-template-columns:1fr}}
.comp{border:1px solid var(--line);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:8px}.comp h3{font-size:17px;margin:0;display:flex;justify-content:space-between;gap:8px}.comp h3 span{font-family:var(--body);font-weight:600;color:var(--muted);font-size:14px}
.items{display:flex;flex-direction:column;gap:6px}.it{display:grid;grid-template-columns:1fr auto 1fr auto;gap:6px;align-items:center}.it span{color:var(--muted);font-size:14px}.it input{width:100%}
.x{border:0;background:none;color:var(--muted);font-size:18px;cursor:pointer;padding:4px 6px}
.addit{align-self:flex-start;border:1px dashed var(--line);background:none;border-radius:9px;padding:6px 12px;font:inherit;font-size:14px;color:var(--info);cursor:pointer}
.res{background:var(--info-bg);border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:6px}.res table{width:100%;border-collapse:collapse;font-size:14px;table-layout:fixed}.res th{font-size:13px;color:var(--muted);font-weight:600}.res td,.res th{padding:4px 6px;text-align:right;border-bottom:1px solid #cdd9f2}.res td:first-child,.res th:first-child{text-align:left}
.big{display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}.big b{font-family:var(--head);font-size:40px;line-height:1}.big .tag{background:var(--brand);color:#fff;border-radius:99px;padding:4px 12px;font-weight:700;font-size:15px}
.ttab{border-collapse:collapse;width:100%;font-size:15px;background:var(--card)}.ttab caption{text-align:left;font-weight:800;padding:6px 0}.ttab td,.ttab th{border:1px solid var(--line);padding:5px 8px;text-align:left}.ttab tbody tr:nth-child(even){background:#f7f9fc}
.tts{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}@media(max-width:700px){.tts{grid-template-columns:1fr}}
.note2{font-size:14px;color:var(--muted)}
.gtools{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}.gtools a{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;text-decoration:none;color:var(--fg)}.gtools a b{display:block}.gtools a span{color:var(--muted);font-size:14px}
</style>'''

COMMON_JS = '''<script>
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
function num(v){var n=parseFloat(String(v).replace(',','.'));return isNaN(n)?null:n}
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
</script>'''

def deped_calc():
    import json
    nt = json.dumps(NEW_TABLE); ot = json.dumps(OLD_TABLE)
    return CSS + COMMON_JS + f'''
<div class="gc" id="gc">
  <div class="row2">
    <label>Grading rules<select id="mode"><option value="new">SY 2026–2027: adjusted table (DO 015, s. 2026)</option><option value="none">SY 2027–2028 on: no transmutation</option><option value="old">Old table (DO 8, s. 2015)</option></select></label>
    <label>Subject and weights (WW / PT / Exam)<select id="grp">{_opts()}</select></label>
  </div>
  <div class="row2" id="cw" hidden><label>Written Work %<input id="cww" inputmode="decimal" value="30"></label><label>Performance Tasks %<input id="cpt" inputmode="decimal" value="50"></label><label>Exam %<input id="cex" inputmode="decimal" value="20"></label></div>
  <div class="comp" data-c="ww"><h3>Written Work <span id="lww"></span></h3><div class="items"></div><button class="addit" type="button">+ Add a score</button></div>
  <div class="comp" data-c="pt"><h3>Performance Tasks <span id="lpt"></span></h3><div class="items"></div><button class="addit" type="button">+ Add a score</button></div>
  <div class="comp" id="exbox"><h3><span style="color:var(--fg);font-family:var(--head);font-weight:800;font-size:17px" id="exh">Exams</span> <span id="lex"></span></h3>
    <div class="exrow" id="exrows"></div></div>
  <div class="res" id="res"></div>
  <p class="note2">Your scores stay on this device. Always check against your school’s official e-Class Record.</p>
</div>
<h2>Final grade and general average</h2>
<div class="gc">
  <p class="note2" style="margin:0" id="fgnote">Type the term grades for one subject to get its final grade.</p>
  <div class="row2" id="terms"></div>
  <div class="res" id="fgres"></div>
</div>
<script>
var NEW={nt},OLD={ot},G={_js_groups()};
var DESC_NEW=[[90,'Advancing (Namumukod-tangi)'],[80,'Benchmarking (Napamamalas)'],[75,'Connecting (Natutungo)'],[65,'Developing (Napauunlad)'],[0,'Emerging (Nagsisimula)']];
var DESC_OLD=[[90,'Outstanding'],[85,'Very Satisfactory'],[80,'Satisfactory'],[75,'Fairly Satisfactory'],[0,'Did Not Meet Expectations']];
var S=keep('qp-grades')||{{mode:'new',grp:'g4a',ww:[['',''],['',''],['','']],pt:[['',''],['','']],ex:{{st1:['',''],st2:['',''],te:['',''],qa:['','']}},cw:[30,50,20],terms:['','','','']}};
$('#mode').value=S.mode;$('#grp').value=S.grp;
function itemRow(v,i,c){{return '<div class="it"><input inputmode="decimal" placeholder="Score" value="'+(v[0]||'')+'" data-k="'+c+'" data-i="'+i+'" data-j="0" aria-label="Score"><span>out of</span><input inputmode="decimal" placeholder="Highest" value="'+(v[1]||'')+'" data-k="'+c+'" data-i="'+i+'" data-j="1" aria-label="Highest possible score"><button class="x" type="button" data-del="'+c+'" data-i="'+i+'" aria-label="Remove">✕</button></div>'}}
function exRow(k,lab,v){{return '<div class="it"><input inputmode="decimal" placeholder="'+lab+'" value="'+(v[0]||'')+'" data-e="'+k+'" data-j="0" aria-label="'+lab+' score"><span>out of</span><input inputmode="decimal" placeholder="Highest" value="'+(v[1]||'')+'" data-e="'+k+'" data-j="1" aria-label="'+lab+' highest possible"><span></span></div>'}}
function trans(ig){{var t=S.mode==='old'?OLD:NEW;for(var i=0;i<t.length;i++)if(ig>=t[i][0]-1e-9)return t[i][1];return 60}}
function desc(g){{var d=S.mode==='old'?DESC_OLD:DESC_NEW;for(var i=0;i<d.length;i++)if(g>=d[i][0])return d[i][1]}}
function wts(){{if(S.grp==='cu')return [num(S.cw[0])||0,num(S.cw[1])||0,num(S.cw[2])||0,'qa'];var g=G[S.grp];return g}}
function ps(list){{var s=0,h=0,n=0;list.forEach(function(r){{var a=num(r[0]),b=num(r[1]);if(a!==null&&b){{s+=a;h+=b;n++}}}});return n?{{ps:s/h*100,s:s,h:h}}:null}}
function draw(){{var w=wts(),m=w[3];
  $('#cw').hidden=S.grp!=='cu';$('#lww').textContent=w[0]+'%';$('#lpt').textContent=w[1]+'%';$('#lex').textContent=w[2]+'%';$('#exbox').hidden=!w[2];
  ['ww','pt'].forEach(function(c){{var b=$('.comp[data-c='+c+'] .items');b.innerHTML=S[c].map(function(v,i){{return itemRow(v,i,c)}}).join('')}});
  $('#exh').textContent=m==='qa'?'Quarterly Assessment':m==='te'?'Term Exam':'Exams';
  $('#exrows').innerHTML=m==='split'?'<p class="note2" style="margin:0">Summative Test 1 (30%), Summative Test 2 (30%), Term Exam (40%)</p>'+exRow('st1','Summative Test 1',S.ex.st1)+exRow('st2','Summative Test 2',S.ex.st2)+exRow('te','Term Exam',S.ex.te):m==='te'?exRow('te','Term Exam',S.ex.te):exRow('qa','Quarterly Assessment',S.ex.qa);
  var nT=S.mode==='old'?4:3;$('#terms').innerHTML=Array.from({{length:nT}},function(_,i){{return '<label>'+(S.mode==='old'?'Quarter ':'Term ')+(i+1)+'<input inputmode="decimal" data-t="'+i+'" value="'+(S.terms[i]||'')+'"></label>'}}).join('');
  wire();calc()}}
function calc(){{var w=wts(),m=w[3],r=$('#res');
  var a=ps(S.ww),b=ps(S.pt),ex=null;
  if(m==='split'){{var t1=ps([S.ex.st1]),t2=ps([S.ex.st2]),te=ps([S.ex.te]);if(t1&&t2&&te)ex={{ps:t1.ps*.3+t2.ps*.3+te.ps*.4}}}}else ex=ps([m==='te'?S.ex.te:S.ex.qa]);
  var need=[a,b].concat(w[2]?[ex]:[]);
  var rows='<table><tr><th>Component</th><th>Percentage score</th><th>Weight</th><th>Weighted score</th></tr>'+[['Written Work',a,w[0]],['Performance Tasks',b,w[1]]].concat(w[2]?[[m==='qa'?'Quarterly Assessment':'Exams',ex,w[2]]]:[]).map(function(x){{return '<tr><td>'+x[0]+'</td><td>'+(x[1]?x[1].ps.toFixed(2):'–')+'</td><td>'+x[2]+'%</td><td>'+(x[1]?(x[1].ps*x[2]/100).toFixed(2):'–')+'</td></tr>'}}).join('')+'</table>';
  var tw=w[0]+w[1]+w[2];
  if(need.some(function(x){{return !x}})){{r.innerHTML=rows+'<p class="note2" style="margin:4px 0 0">Enter at least one score and its highest possible score in each part.</p>';return}}
  var ig=Math.round((a.ps*w[0]+b.ps*w[1]+(w[2]?ex.ps*w[2]:0))/100*100)/100;
  var tg=S.mode==='none'?Math.round(ig):trans(ig);
  r.innerHTML=rows+(Math.abs(tw-100)>0.01?'<p class="note2" style="color:var(--bad)">The weights add up to '+tw+'%, not 100%.</p>':'')+'<div class="big"><span>Initial grade <b style="font-size:26px">'+ig.toFixed(2)+'</b></span><span>'+(S.mode==='old'?'Quarterly':'Term')+' grade <b>'+tg+'</b></span><span class="tag">'+desc(tg)+'</span></div>'+
   '<p class="note2" style="margin:0">'+(S.mode==='none'?'No transmutation: the initial grade, rounded, is the term grade.':'Transmuted with the '+(S.mode==='old'?'DO 8, s. 2015':'SY 2026–2027 adjusted')+' table. '+(tg>=75?'Passing.':'Below the passing grade of 75.'))+'</p>';
  keep('qp-grades',S)}}
function calcFG(){{var nT=S.mode==='old'?4:3,v=[];for(var i=0;i<nT;i++){{var x=num(S.terms[i]);if(x!==null)v.push(x)}}
  var r=$('#fgres');if(v.length<nT){{r.innerHTML='<span class="note2">Final grade = the average of the '+nT+' '+(S.mode==='old'?'quarterly':'term')+' grades, rounded to a whole number.</span>';return}}
  var fg=Math.round(v.reduce(function(s,x){{return s+x}},0)/nT);r.innerHTML='<div class="big"><span>Final grade <b>'+fg+'</b></span><span class="tag">'+desc(fg)+'</span></div><span class="note2">'+(fg>=75?'Passed: meets the minimum standard of 75.':'Below 75.')+' The general average is the average of all final grades.</span>';keep('qp-grades',S)}}
function wire(){{
  $$('#gc .items input').forEach(function(x){{x.oninput=function(){{S[x.dataset.k][+x.dataset.i][+x.dataset.j]=x.value;calc()}}}});
  $$('[data-del]').forEach(function(b){{b.onclick=function(){{var c=b.dataset.del;if(S[c].length>1){{S[c].splice(+b.dataset.i,1);draw()}}}}}});
  $$('#exrows input').forEach(function(x){{x.oninput=function(){{S.ex[x.dataset.e][+x.dataset.j]=x.value;calc()}}}});
  $$('#terms input').forEach(function(x){{x.oninput=function(){{S.terms[+x.dataset.t]=x.value;calcFG()}}}});calcFG()}}
$$('.addit').forEach(function(b){{b.onclick=function(){{var c=b.parentNode.dataset.c;S[c].push(['','']);draw();var l=$$('.comp[data-c='+c+'] .items input');l[l.length-2].focus()}}}});
$('#mode').onchange=function(){{S.mode=this.value;draw()}};$('#grp').onchange=function(){{S.grp=this.value;draw()}};
['cww','cpt','cex'].forEach(function(k,i){{$('#'+k).value=S.cw[i];$('#'+k).oninput=function(){{S.cw[i]=this.value;var w=wts();$('#lww').textContent=w[0]+'%';$('#lpt').textContent=w[1]+'%';$('#lex').textContent=w[2]+'%';$('#exbox').hidden=!w[2];calc()}}}});
draw();
</script>'''

DEPED_TEXT = '''
<h2>How grades are computed under DO 015, s. 2026</h2>
<p>Starting School Year 2026–2027, public schools follow <b>DepEd Order No. 015, s. 2026</b>, which replaces DO 8, s. 2015. The school year has <b>three terms</b>, only summative work counts toward grades (daily formative quizzes don’t), and transmutation is being phased out.</p>
<ol>
<li><b>Percentage score</b> for each component = total raw score ÷ total highest possible score × 100.</li>
<li><b>Exams</b> (for most subjects) combine Summative Test 1 (30%), Summative Test 2 (30%) and the Term Exam (40%).</li>
<li><b>Weighted score</b> = percentage score × the component’s weight.</li>
<li><b>Initial grade</b> = the sum of the weighted scores.</li>
<li><b>Term grade</b> = the initial grade transmuted with the SY 2026–2027 adjusted table, rounded to a whole number. From SY 2027–2028, Grades 4 to 12 use the initial grade itself, with no transmutation.</li>
<li><b>Final grade</b> = the average of the three term grades, rounded. The <b>general average</b> is the average of all final grades.</li>
</ol>
<h2>Example</h2>
<p>A Grade 7 Math student has 82% in Written Work, 80% in Performance Tasks and 85.6% in Exams. With weights of 20%, 50% and 30%: 16.40 + 40.00 + 25.68 = an initial grade of <b>82.08</b>. On the SY 2026–2027 table, 81.80–82.97 becomes <b>85</b>, which is “Benchmarking.”</p>
<h2>Descriptors (Grades 4 to 12)</h2>
<table class="ttab"><thead><tr><th>Grade</th><th>Descriptor</th></tr></thead><tbody><tr><td>90–100</td><td>Advancing (Namumukod-tangi)</td></tr><tr><td>80–89</td><td>Benchmarking (Napamamalas)</td></tr><tr><td>75–79</td><td>Connecting (Natutungo)</td></tr><tr><td>65–74</td><td>Developing (Napauunlad)</td></tr><tr><td>Below 65</td><td>Emerging (Nagsisimula)</td></tr></tbody></table>
<p>The passing grade is <b>75</b>. Kindergarten to Grade 1 use descriptive ratings instead of numbers this school year, with Grades 2 and 3 following in the next two school years.</p>
<h2>Questions</h2>
<h3>Is this an official computation?</h3><p>QuizPolice is an independent tool and is not affiliated with the Department of Education. It follows DepEd Order No. 015, s. 2026 as published, including the SY 2026–2027 adjusted transmutation table. Small differences can come from how your school rounds percentage scores. Always confirm with your school’s official e-Class Record.</p>
<h3>Can I still use the old table?</h3><p>Yes. Choose “Old table (DO 8, s. 2015)” and the old weights, for example for Grade 12 learners who are not yet on the strengthened SHS curriculum, or for schools that still use it.</p>
<h3>Are my scores saved?</h3><p>Only in your own browser, so they’re still here when you come back. Nothing is sent to QuizPolice.</p>
<p class="note2">Sources: DepEd Order No. 015, s. 2026 (Revised Classroom Assessment and Grading Guidelines) and DepEd Order No. 8, s. 2015.</p>'''

def trans_page():
    import json
    return CSS + COMMON_JS + f'''
<div class="gc"><div class="row2"><label>Initial grade<input id="ig" inputmode="decimal" placeholder="e.g. 82.08"></label><label>Table<select id="tb"><option value="new">SY 2026–2027 adjusted (DO 015, s. 2026)</option><option value="old">Old table (DO 8, s. 2015)</option></select></label></div>
<div class="res" id="tr"><span class="note2">Type an initial grade to see its transmuted grade.</span></div></div>
<script>var NEW={json.dumps(NEW_TABLE)},OLD={json.dumps(OLD_TABLE)};
function go(){{var v=num($('#ig').value),t=$('#tb').value==='old'?OLD:NEW,r=$('#tr');if(v===null||v<0||v>100){{r.innerHTML='<span class="note2">Type an initial grade from 0 to 100.</span>';return}}
var g=60;for(var i=0;i<t.length;i++)if(v>=t[i][0]-1e-9){{g=t[i][1];break}}r.innerHTML='<div class="big"><span>Transmuted grade <b>'+g+'</b></span><span class="note2">'+(g>=75?'Passing':'Below 75')+'</span></div>'}}
$('#ig').oninput=go;$('#tb').onchange=go;</script>
<div class="tts">{table_html(NEW_TABLE, 'SY 2026–2027 adjusted table (DO 015, s. 2026)')}{table_html(OLD_TABLE, 'Old table (DO 8, s. 2015)')}</div>'''

TRANS_TEXT = '''
<h2>What changed</h2>
<p>Under the old table (DO 8, s. 2015), an initial grade of <b>60</b> was transmuted to a passing 75. Under the adjusted table for SY 2026–2027 (DO 015, s. 2026), an initial grade of <b>70</b> is needed for 75. From SY 2027–2028, Grades 4 to 12 drop transmutation entirely: an initial grade of 75 is a final 75. Kindergarten to Grade 3 move to descriptive ratings over the same period.</p>
<p>DepEd says the change is meant to make grades reflect what learners actually know, not to make passing harder. Teachers can plan support earlier when grades are more accurate.</p>
<h2>How to use the table</h2>
<ol><li>Compute the initial grade: the sum of the weighted scores of Written Work, Performance Tasks and Exams.</li><li>Find the band it falls in, and read the transmuted grade.</li></ol>
<p>Easier: the <a href="/tools/grade-calculator/">K to 12 grade calculator</a> does all the steps for you, from raw scores to the term and final grade.</p>
<p class="note2">Sources: DepEd Order No. 015, s. 2026 and DepEd Order No. 8, s. 2015. Always confirm with your school’s official e-Class Record.</p>'''

def weighted_calc():
    return CSS + COMMON_JS + '''
<div class="gc" id="wc">
  <div class="items" id="cats"></div><button class="addit" type="button" id="addc">+ Add a category</button>
  <div class="res" id="wres"></div>
</div>
<h2>What do I need on the final?</h2>
<div class="gc"><div class="row2"><label>Current grade (%)<input id="cur" inputmode="decimal" placeholder="e.g. 84"></label><label>Final exam weight (%)<input id="fw" inputmode="decimal" placeholder="e.g. 30"></label><label>Grade you want (%)<input id="want" inputmode="decimal" placeholder="e.g. 90"></label></div><div class="res" id="need"></div></div>
<script>
var C=keep('qp-weighted')||[['Homework','20','92'],['Quizzes','30','85'],['Projects','20','88'],['Final exam','30','']];
function letter(g){return g>=93?'A':g>=90?'A−':g>=87?'B+':g>=83?'B':g>=80?'B−':g>=77?'C+':g>=73?'C':g>=70?'C−':g>=67?'D+':g>=60?'D':'F'}
function drawC(){$('#cats').innerHTML='<div class="it" style="grid-template-columns:2fr 1fr 1fr auto"><span>Category</span><span>Weight %</span><span>Score %</span><span></span></div>'+C.map(function(c,i){return '<div class="it" style="grid-template-columns:2fr 1fr 1fr auto"><input value="'+c[0]+'" data-i="'+i+'" data-j="0" aria-label="Category"><input inputmode="decimal" value="'+c[1]+'" data-i="'+i+'" data-j="1" aria-label="Weight"><input inputmode="decimal" value="'+c[2]+'" data-i="'+i+'" data-j="2" placeholder="–" aria-label="Score"><button class="x" type="button" data-d="'+i+'" aria-label="Remove">✕</button></div>'}).join('');
 $$('#cats input').forEach(function(x){x.oninput=function(){C[+x.dataset.i][+x.dataset.j]=x.value;calcW()}});$$('[data-d]').forEach(function(b){b.onclick=function(){if(C.length>1){C.splice(+b.dataset.d,1);drawC()}}});calcW()}
function calcW(){var tw=0,sw=0,all=0;C.forEach(function(c){var w=num(c[1]),s=num(c[2]);if(w){all+=w;if(s!==null){tw+=w;sw+=w*s}}});var r=$('#wres');
 if(!tw){r.innerHTML='<span class="note2">Type a weight and score for at least one category.</span>';return}var g=sw/tw;
 r.innerHTML='<div class="big"><span>'+(tw<all?'Grade so far':'Final grade')+' <b>'+g.toFixed(1)+'%</b></span><span class="tag">'+letter(g)+'</span></div><span class="note2">'+(tw<all?'Based on '+tw+'% of the course that has scores. ':'')+(Math.abs(all-100)>0.01?'The weights add up to '+all+'%. ':'')+'Letter grade on a common US scale; your school’s scale may differ.</span>';
 if(tw<all&&!$('#cur').value){$('#cur').placeholder=g.toFixed(1)}keep('qp-weighted',C)}
function calcN(){var c=num($('#cur').value||$('#cur').placeholder),f=num($('#fw').value),w=num($('#want').value),r=$('#need');if(c===null||!f||w===null||f>=100){r.innerHTML='<span class="note2">Type your current grade, how much the final counts, and the grade you want.</span>';return}
 var n=(w-c*(1-f/100))/(f/100);r.innerHTML='<div class="big"><span>You need <b>'+n.toFixed(1)+'%</b> on the final</span></div><span class="note2">'+(n>100?'That’s above 100%, so this target isn’t reachable with the final alone.':n<=0?'You’ve already reached this grade, even with a 0 on the final.':'Score at least this on the final to finish with '+w+'%.')+'</span>'}
$('#addc').onclick=function(){C.push(['','','']);drawC()};['cur','fw','want'].forEach(function(k){$('#'+k).oninput=calcN});drawC();calcN();
</script>'''

WEIGHTED_TEXT = '''
<h2>How a weighted grade works</h2>
<p>Most courses don’t count everything equally. A final exam might be worth 30% of the grade while homework is worth 20%. A weighted grade multiplies each category’s score by its weight, adds them up, and divides by the total weight.</p>
<p><b>Example:</b> homework 92% (20%), quizzes 85% (30%), projects 88% (20%) and a final exam 80% (30%): 18.4 + 25.5 + 17.6 + 24.0 = <b>85.5%</b>, a B on a common scale.</p>
<h2>What score do I need on my final?</h2>
<p>Required final score = (the grade you want − current grade × (1 − final weight)) ÷ final weight. For example, to finish with 90% when you have 86% and the final counts for 30%, you need (90 − 86 × 0.7) ÷ 0.3 = <b>99.3%</b>.</p>
<h2>Tips</h2>
<ul><li>Check your syllabus for the exact weights; categories don’t always add up to 100%.</li><li>Leave a score empty for work that isn’t graded yet. The calculator shows your grade so far from what’s done.</li><li>Studying for that final? See <a href="/guides/how-to-study-for-a-quiz/">how to study for a quiz</a>, and warm up with the free <a href="/practice/">practice games</a>.</li></ul>
<p>In the Philippines? Use the <a href="/tools/grade-calculator/">K to 12 grade calculator</a> for the DO 015, s. 2026 computation.</p>'''

TOOLS = [
 ('/tools/grade-calculator/', 'Grade Calculator 2026: Three-Term Grading with Transmutation (DO 015, s. 2026)',
  'Free K to 12 grade calculator for SY 2026–2027: Written Work, Performance Tasks and Exams with the new weights, the adjusted transmutation table, three terms, final grade and descriptors. Also works with the old DO 8 table.',
  'K to 12 grade calculator', deped_calc, DEPED_TEXT, 'Compute term and final grades with the new DO 015, s. 2026 rules.'),
 ('/tools/transmutation-table/', 'Transmutation Table 2026–2027 (DO 015, s. 2026) and the Old DO 8 Table',
  'The transmutation table for SY 2026–2027 under DO 015, s. 2026, next to the old DO 8, s. 2015 table, with an instant lookup. See what changed and when transmutation ends.',
  'Transmutation table', trans_page, TRANS_TEXT, 'The SY 2026–2027 adjusted table and the old table, with a quick lookup.'),
 ('/tools/weighted-grade-calculator/', 'Weighted Grade Calculator and Final Exam Grade Calculator',
  'Free weighted grade calculator: add categories with weights and scores to get your course grade and letter grade, then find the score you need on your final exam.',
  'Weighted grade calculator', weighted_calc, WEIGHTED_TEXT, 'Course grade from weighted categories, and the score you need on the final.'),
]
