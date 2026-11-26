"""Grade tools on QuizPolice: shared tables and styles, and the transmutation table page (the calculator is in grade_calc_page.py).
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
 ('Grades 4–10', [
   ('g4a', 'English, Filipino, Math, Science, AP, GMRC / Values Education', 20, 50, 30, 'split'),
   ('g4b', 'EPP / TLE, MAPEH', 20, 60, 20, 'split')]),
 ('Grades 2–3', [
   ('g2a', 'Makabansa and other graded subjects', 20, 50, 30, 'split')]),
 ('Senior High School, strengthened curriculum', [
   ('s1', 'Core subjects and other academic electives', 20, 50, 30, 'split'),
   ('s2', 'Field Exposure, Arts Apprenticeship, Creative Production and Innovation', 15, 70, 15, 'te'),
   ('s3', 'Arts, Sports, Health and Wellness electives', 20, 60, 20, 'split'),
   ('s4', 'Research electives, Design and Innovation', 40, 60, 0, 'split'),
   ('s5', 'TechPro electives', 15, 65, 20, 'split'),
   ('s6', 'Work Immersion', 20, 80, 0, 'split')]),
 ('Old weights (2015), e.g. Grade 12 not yet on the strengthened curriculum', [
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

def trans_page():
    import json
    return CSS + COMMON_JS + f'''
<div class="gc"><div class="row2"><label>Initial grade<input id="ig" inputmode="decimal" placeholder="e.g. 82.08"></label><label>Table<select id="tb"><option value="new">SY 2026–2027 adjusted</option><option value="old">Old table (2015)</option></select></label></div>
<div class="res" id="tr"><span class="note2">Type an initial grade to see its transmuted grade.</span></div></div>
<script>var NEW={json.dumps(NEW_TABLE)},OLD={json.dumps(OLD_TABLE)};
function go(){{var v=num($('#ig').value),t=$('#tb').value==='old'?OLD:NEW,r=$('#tr');if(v===null||v<0||v>100){{r.innerHTML='<span class="note2">Type an initial grade from 0 to 100.</span>';return}}
var g=60;for(var i=0;i<t.length;i++)if(v>=t[i][0]-1e-9){{g=t[i][1];break}}r.innerHTML='<div class="big"><span>Transmuted grade <b>'+g+'</b></span><span class="note2">'+(g>=75?'Passing':'Below 75')+'</span></div>'}}
$('#ig').oninput=go;$('#tb').onchange=go;</script>
<div class="tts">{table_html(NEW_TABLE, 'SY 2026–2027 adjusted table')}{table_html(OLD_TABLE, 'Old table (2015)')}</div>'''

TRANS_TEXT = '''
<h2>What changed</h2>
<p>Under the old table (2015), an initial grade of <b>60</b> was transmuted to a passing 75. Under the adjusted table for SY 2026–2027, an initial grade of <b>70</b> is needed for 75. From SY 2027–2028, Grades 4 to 12 drop transmutation entirely: an initial grade of 75 is a final 75. Kindergarten to Grade 3 move to descriptive ratings over the same period.</p>
<p>The stated aim of the change is to make grades reflect what learners actually know, not to make passing harder. Teachers can plan support earlier when grades are more accurate.</p>
<h2>How to use the table</h2>
<ol><li>Compute the initial grade: the sum of the weighted scores of Written Work, Performance Tasks and Exams.</li><li>Find the band it falls in, and read the transmuted grade.</li></ol>
<p>Easier: the <a href="/tools/grade-calculator/">grade calculator</a> does all the steps for you. Pick the K to 12 three-term setup, type the raw scores, and get the term and final grades.</p>
<p class="note2">Always confirm with your school’s official records.</p>'''

