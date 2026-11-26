"""Customizable grade calculator page (/tools/grade-calculator/). The page script is tools/grade_calc.js."""
import json, os
from grades_content import GROUPS, NEW_TABLE, OLD_TABLE, CSS

SCALES = {
 'letter': [[93, 'A'], [90, 'A−'], [87, 'B+'], [83, 'B'], [80, 'B−'], [77, 'C+'], [73, 'C'], [70, 'C−'], [67, 'D+'], [63, 'D'], [60, 'D−'], [0, 'F']],
 'gpa': [[93, 'A · 4.0'], [90, 'A− · 3.7'], [87, 'B+ · 3.3'], [83, 'B · 3.0'], [80, 'B− · 2.7'], [77, 'C+ · 2.3'], [73, 'C · 2.0'], [70, 'C− · 1.7'], [67, 'D+ · 1.3'], [63, 'D · 1.0'], [60, 'D− · 0.7'], [0, 'F · 0.0']],
 'desc': [[90, 'Advancing'], [80, 'Benchmarking'], [75, 'Connecting'], [65, 'Developing'], [0, 'Emerging']],
 'desc15': [[90, 'Outstanding'], [85, 'Very Satisfactory'], [80, 'Satisfactory'], [75, 'Fairly Satisfactory'], [0, 'Did Not Meet Expectations']],
 'pct': [],
}
SCALE_OPTS = [('letter', 'Letters A to F'), ('gpa', 'Letters with 4.0 GPA points'), ('desc', 'K to 12 descriptors (2026)'),
              ('desc15', 'K to 12 descriptors (2015)'), ('pct', 'Numbers only, no labels'), ('custom', 'Custom labels')]

def C(n, w, parts=None): return dict(n=n, w=w, parts=[dict(n=a, w=b) for a, b in parts] if parts else None)

def presets():
    P = [
     dict(id='simple', group='General', label='Weighted: Homework, Quizzes, Projects, Final exam', name='Homework, quizzes, projects and final',
          cats=[C('Homework', 20), C('Quizzes', 30), C('Projects', 20), C('Final exam', 30)], scale='letter', **{'pass': 60}, conv='none', dec=1, terms=1, tname='Term'),
     dict(id='midfinal', group='General', label='Coursework 50%, Exams 50% (Midterm and Final)', name='Coursework and exams',
          cats=[C('Coursework', 50), C('Exams', 50, [('Midterm', 40), ('Final', 60)])], scale='letter', **{'pass': 60}, conv='none', dec=1, terms=1, tname='Term'),
     dict(id='points', group='General', label='Total points (all work counts the same)', name='Total points',
          cats=[C('All work', 100)], scale='letter', **{'pass': 60}, conv='none', dec=1, terms=1, tname='Term'),
     dict(id='custom', group='General', label='Start from scratch', name='My grading setup',
          cats=[C('Category 1', 50), C('Category 2', 50)], scale='pct', **{'pass': None}, conv='none', dec=1, terms=1, tname='Term'),
    ]
    for g, items in GROUPS:
        if g == 'Other': continue
        old = g.startswith('Old')
        for k, lab, w, pt, x, m in items:
            cats = [C('Written Works', w), C('Performance Tasks', pt)]
            if x:
                cats.append(C('Exams', x, [('Summative Test 1', 30), ('Summative Test 2', 30), ('Term Exam', 40)]) if m == 'split'
                            else C('Quarterly Assessment' if m == 'qa' else 'Term Exam', x))
            pre = '' if old or g == 'Grades 4–10' else ('SHS: ' if g.startswith('Senior') else g + ': ')
            P.append(dict(id=k, group='K to 12, old table (2015)' if old else 'K to 12 three-term grading (2026)',
                          label=f'{pre}{lab} ({w}/{pt}/{x})', name=f'K to 12 {"2015" if old else "2026"}: {lab}', cats=cats,
                          scale='desc15' if old else 'desc', **{'pass': 75}, conv='2015' if old else '2026', dec=0,
                          terms=4 if old else 3, tname='Quarter' if old else 'Term'))
    return P

STYLE = '''<style>
.gc-top{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.gc-top select{flex:1 1 260px}
.gc-btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 12px;font:inherit;font-size:15px;font-weight:600;cursor:pointer;color:var(--fg)}
.gc-shared{background:var(--ok-bg);color:var(--ok);border-radius:10px;padding:8px 12px;font-size:15px;margin:0}
details.gc-setup{border:1px solid var(--line);border-radius:12px;padding:0 12px}details.gc-setup>summary{cursor:pointer;font-weight:800;padding:12px 0}details.gc-setup[open]{padding-bottom:12px}
.gc-setup h4{margin:16px 0 6px;font-size:15px}.gc .sc-row{grid-template-columns:minmax(0,1fr) 72px auto auto}.gc .sc-band{grid-template-columns:auto 72px minmax(0,1fr) auto}
.sc-cat{display:flex;flex-direction:column;gap:6px;padding:8px 0;border-bottom:1px dashed var(--line)}.sc-parts{margin-left:18px;display:flex;flex-direction:column;gap:6px}.gc .sc-split{font-size:13px;padding:3px 10px}
.gc textarea{font:inherit;font-size:15px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;width:100%;min-height:120px;box-sizing:border-box}
.pf{border-radius:99px;padding:4px 12px;font-weight:700;font-size:15px}.pf.ok{background:var(--ok-bg);color:var(--ok)}.pf.bad{background:var(--bad-bg);color:var(--bad)}
.gc .chk{flex-direction:row;align-items:center;font-weight:600}.gc .chk input{width:20px;height:20px}
@media print{header.top,footer.foot,.gc-top,details.gc-setup,.addit,.x,.gmeta,.calc-text,h2.more,ul.more{display:none!important}.gc{border:0;padding:0}}
</style>'''

HTML = '''
<div class="gc" id="gc">
  <p class="gc-shared" id="gcShared" hidden>Using a shared setup: <b></b>. Your scores stay on this device.</p>
  <div class="gc-top"><select id="gcPreset" aria-label="Ready setups"></select><button class="gc-btn" type="button" id="gcLink">🔗 Copy setup link</button></div>
  <details class="gc-setup" id="gcSetup"><summary>Grading setup: categories, weights and scale</summary>
    <label>Setup name<input id="gcName" maxlength="80"></label>
    <h4>Categories and weights</h4><div id="gcCats"></div><button class="addit" type="button" id="gcAddCat">+ Add a category</button><p class="note2" id="gcTot" style="margin:4px 0 0"></p>
    <h4>Grade scale</h4><div class="row2"><label>Labels<select id="gcScale">__SOPTS__</select></label><label>Pass mark (optional)<input id="gcPass" inputmode="decimal" placeholder="e.g. 60 or 75"></label></div>
    <div id="gcBands" class="items" style="margin-top:8px"></div><button class="addit" type="button" id="gcAddBand" style="margin-top:6px">+ Add a label</button>
    <h4>Conversion table (transmutation)</h4><div class="row2"><label>Convert the grade<select id="gcConv"><option value="none">No conversion</option><option value="2026">K to 12 adjusted table (2026–2027)</option><option value="2015">K to 12 table (2015)</option><option value="custom">My own table</option></select></label>
    <label>Round the grade to<select id="gcDec"><option value="0">Whole number</option><option value="1">1 decimal</option><option value="2">2 decimals</option></select></label></div>
    <div id="gcCtabBox" hidden><label>Your table: one line per band, the lowest initial grade then the converted grade<textarea id="gcCtab" placeholder="70 75&#10;71.18 76"></textarea></label></div>
    <h4>Terms</h4><div class="row2"><label>Number of terms<select id="gcTerms"><option value="1">1 (just this grade)</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option></select></label>
    <label>Call them<select id="gcTname"><option>Term</option><option>Quarter</option><option>Semester</option><option>Trimester</option><option>Grading period</option></select></label></div>
    <div id="gcTwBox"><label class="chk"><input type="checkbox" id="gcTwEq"> All terms count the same</label><div class="row2" id="gcTw"></div></div>
  </details>
  <div id="gcScores" style="display:flex;flex-direction:column;gap:12px"></div>
  <div class="res" id="gcRes"></div>
  <div class="res" id="gcNeed" hidden><b>What do I need on the rest?</b><span class="note2">Still to come: <span id="gcNeedWhat"></span></span><label style="font-weight:700">Grade I want<input id="gcTarget" inputmode="decimal" placeholder="e.g. 90" style="max-width:160px"></label><div id="gcNeedRes"></div></div>
  <div class="gc-top"><button class="gc-btn" type="button" id="gcClear">Clear scores</button><button class="gc-btn" type="button" onclick="window.print()">🖨 Print</button></div>
  <p class="note2" style="margin:0">Your setup and scores stay on this device. The setup link shares the setup only, never the scores.</p>
</div>
<div class="gc" id="gcFinal" hidden><h2 style="margin:0">Final grade</h2><p class="note2" style="margin:0">Type each <span id="gcTermName">term</span> grade, or add the grade from above.</p>
  <div class="row2" id="gcTermIn"></div><div class="gc-top"><button class="gc-btn" type="button" id="gcUse">⬇ Add the grade from above</button></div><div class="res" id="gcFRes"></div></div>
'''

def grade_calc():
    js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grade_calc.js'), encoding='utf-8').read()
    js = (js.replace('__PRESETS__', json.dumps(presets(), ensure_ascii=False)).replace('__T2026__', json.dumps(NEW_TABLE))
            .replace('__T2015__', json.dumps(OLD_TABLE)).replace('__SCALES__', json.dumps(SCALES, ensure_ascii=False)))
    return CSS + STYLE + HTML.replace('__SOPTS__', ''.join(f'<option value="{k}">{v}</option>' for k, v in SCALE_OPTS)) + '<script>' + js + '</script>'

TEXT = '''<div class="calc-text">
<h2>How to use it</h2>
<ol>
<li><b>Choose a ready setup</b>, or open <b>Grading setup</b> to make your own: name your categories (homework, quizzes, labs, exams…) and give each a weight. A category can be split into parts, like Midterm 40% and Final 60%.</li>
<li><b>Pick a grade scale:</b> letters A to F, letters with GPA points, numbers only, or your own labels with the lowest grade for each. Add a pass mark if your school has one.</li>
<li><b>Type the scores</b> as “score out of total”, like 18 out of 20. Add as many as you need. The calculator adds them up, so a 50-point test counts more than a 10-point quiz in the same category.</li>
<li><b>Read the grade.</b> If some work isn’t graded yet, you’ll see the grade so far and what you need on the rest to reach your target.</li>
<li><b>More than one term?</b> Set the number of terms to get the final grade, with equal or different weights.</li>
</ol>
<h2>Share the same setup with your class or department</h2>
<p>Tap <b>Copy setup link</b> and send it. Everyone who opens it gets your categories, weights, scale and terms, ready to type their own scores. Students can check their grade the same way you compute it. The link carries the setup only. Scores stay on each person’s own device, and nothing is stored on our servers.</p>
<h2>How the grade is computed</h2>
<ol>
<li><b>Category score</b> = total points earned ÷ total points possible × 100. For a category with parts, each part is scored on its own, then combined by its weight.</li>
<li><b>Weighted score</b> = category score × its weight. The grade is the sum of the weighted scores.</li>
<li><b>Conversion (optional).</b> Some schools convert this “initial grade” with a table, also called transmutation. You can use a ready table or type your own.</li>
<li><b>Final grade</b> = the average of the term grades, or their weighted average if the terms count differently.</li>
</ol>
<h2>Examples</h2>
<p><b>Weighted course:</b> homework 92% (20%), quizzes 85% (30%), projects 88% (20%) and a final exam 80% (30%): 18.4 + 25.5 + 17.6 + 24.0 = <b>85.5%</b>, a B on the A to F scale.</p>
<p><b>Three terms with a conversion table:</b> with the K to 12 three-term setup for Grades 4–10 Math, Written Works 82%, Performance Tasks 80% and Exams 85.6% give 16.40 + 40.00 + 25.68 = an initial grade of <b>82.08</b>, which the 2026–2027 adjusted table converts to <b>85</b> (Benchmarking). See the full <a href="/tools/transmutation-table/">transmutation table</a>.</p>
<h2>Questions</h2>
<h3>Is this an official calculator?</h3><p>No. QuizPolice is an independent tool and is not affiliated with any school system or government agency. The ready setups follow published rules as closely as we can, but small differences can come from how a school rounds scores. Always check against your school’s official records.</p>
<h3>Can I change a ready setup?</h3><p>Yes. Pick it, then open <b>Grading setup</b> and change anything: names, weights, labels, the pass mark or the conversion table.</p>
<h3>Are my scores saved?</h3><p>Only in your own browser, so they’re still here when you come back on the same device. Clearing your browser data removes them.</p>
<h3>Can I print it?</h3><p>Yes. Tap <b>Print</b> for a clean page with the scores and the grade.</p>
</div>'''

from grades_content import trans_page, TRANS_TEXT
TOOLS = [
 ('/tools/grade-calculator/', 'Grade Calculator: Weighted Categories, Your Own Grade Scale and Terms',
  'Free grade calculator for teachers and students. Set your own categories, weights, grade scale and pass mark, or start from a ready setup. Find what you need on the rest, add terms for a final grade, and share your setup as a link.',
  'Grade calculator', grade_calc, TEXT, 'Your own categories, weights and grade scale, or a ready setup. Share it as a link.'),
 ('/tools/transmutation-table/', 'Transmutation Table 2026–2027 and the Old 2015 Table',
  'The transmutation table for SY 2026–2027 next to the old 2015 table, with an instant lookup. See what changed and when transmutation ends.',
  'Transmutation table', trans_page, TRANS_TEXT, 'The 2026–2027 adjusted table and the old 2015 table, with a quick lookup.'),
]
