"""Quick grader (/tools/quick-grader/): a chart of every score on one test. Script: tools/js/quickgrader.js."""
import json, os
from grades_content import CSS, NEW_TABLE, OLD_TABLE
from grade_calc_page import SCALES

STYLE = '''<style>
.gc-btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 14px;font:inherit;font-size:15px;font-weight:700;cursor:pointer;color:var(--fg)}.gc-btn.pri{background:var(--brand);border-color:var(--brand);color:#fff}
.gc-top{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.row4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;align-items:end}@media(max-width:640px){.row4{grid-template-columns:1fr 1fr}}
.warnbox{background:var(--warn-bg);color:var(--warn);border-radius:10px;padding:8px 12px;font-size:15px;margin:0}.okbox{background:var(--ok-bg);color:var(--ok);border-radius:10px;padding:8px 12px;font-size:15px;margin:0}
.qg-wrap{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px}
#qgChart,#qgHeadRow{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:4px 14px}
.qg-c,#qgHead{display:grid;grid-template-columns:3.8em 4.8em 1fr;gap:8px;align-items:baseline;padding:3px 6px;border-bottom:1px dotted var(--line);font-variant-numeric:tabular-nums;font-size:15px}
#qgHead{font-size:12px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;border:0}#qgHead span:nth-child(-n+2){text-align:right}.qg-c b{text-align:right}.qg-c span{color:var(--muted);text-align:right}.qg-c i{font-style:normal;font-weight:700}
.qg-c.fail i,.qg-c.fail b{color:var(--bad)}
@media print{body *{visibility:hidden}#qgPrintArea,#qgPrintArea *{visibility:visible}#qgPrintArea{position:absolute;left:0;top:0;width:100%}.qg-wrap{border:0;padding:0}.qg-c{font-size:11px;padding:1px 4px}#qgChart{grid-template-columns:repeat(4,1fr)}#qgHeadRow{display:none}}
</style>'''

HTML = '''
<div class="gc">
  <p class="okbox" id="qgShared" hidden>Using shared quick grader settings.</p>
  <div class="row4"><label>Number of items<input id="qgN" type="number" min="1" max="500" inputmode="numeric"></label>
   <label>Count<select id="qgCount"><option value="wrong">Number wrong</option><option value="right">Number right</option></select></label>
   <label>Points<select id="qgStep"><option value="1">Whole points</option><option value="0.5">Half points too</option></select></label>
   <label>Show % with<select id="qgDec"><option value="0">0 decimals</option><option value="1">1 decimal</option><option value="2">2 decimals</option></select></label></div>
  <div class="row4"><label>Grade<select id="qgScale"><option value="letter">Letters A to F</option><option value="gpa">Letters with GPA points</option><option value="pct">Percentage only</option><option value="desc">K to 12 descriptors (2026)</option><option value="desc15">K to 12 descriptors (2015)</option></select></label>
   <label>Transmutation<select id="qgConv"><option value="none">None</option><option value="2026">K to 12 adjusted (2026–2027)</option><option value="2015">K to 12 (2015)</option><option value="own">My rule (from the table maker)</option></select></label>
   <label>Pass mark (optional)<input id="qgPass" inputmode="decimal" placeholder="e.g. 60"></label>
   <label id="qgKL">Number wrong<input id="qgK" inputmode="decimal" placeholder="Look up one"></label></div>
  <div class="res" id="qgLook"></div>
  <div id="qgPrintArea"><h3 id="qgCap" style="margin:4px 0 8px;font-size:17px"></h3><div class="qg-wrap"><div id="qgHeadRow"><div id="qgHead"></div></div><div id="qgChart"></div></div></div>
  <div class="gc-top"><button class="gc-btn pri" type="button" id="qgPrint">🖨 Print the chart</button><button class="gc-btn" type="button" id="qgLink">🔗 Copy link</button><span class="note2">Grades below the pass mark are in red.</span></div>
</div>'''

def quick_page():
    js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js', 'quickgrader.js'), encoding='utf-8').read()
    js = js.replace('__T2026__', json.dumps(NEW_TABLE)).replace('__T2015__', json.dumps(OLD_TABLE)).replace('__SCALES__', json.dumps(SCALES, ensure_ascii=False))
    return CSS + STYLE + HTML + '<script>' + js + '</script>'

TEXT = '''
<h2>How to use the quick grader</h2>
<ol><li>Type the <b>number of items</b> on the test.</li><li>Choose whether you count the number <b>wrong</b> or <b>right</b>. Most teachers count mistakes, since there are fewer.</li>
<li>Pick how to show the grade: a letter, a percentage, or a converted grade from a transmutation table.</li>
<li>Print the chart and keep it beside you while checking. Count the mistakes, find the number, write the grade.</li></ol>
<h2>Example</h2>
<p>On a 40-item test, each item is worth 2.5%. A student with 3 wrong got 37 right: 37 ÷ 40 = <b>92.5%</b>, an A− on the A to F scale. With 12 wrong, 28 ÷ 40 = 70%, a C−.</p>
<h2>Tips</h2>
<ul><li><b>Half points:</b> for questions with partial credit, choose “Half points too” and the chart adds 0.5, 1.5, 2.5 and so on.</li>
<li><b>Your school’s own conversion:</b> make your table in the <a href="/tools/transmutation-table/">transmutation table maker</a>, then choose “My rule” here.</li>
<li><b>Same chart for the whole department:</b> tap <b>Copy link</b> and share it.</li>
<li>To combine test scores with homework, projects and exams, use the <a href="/tools/grade-calculator/">grade calculator</a>.</li></ul>
<h2>Questions</h2>
<h3>Is this like an EZ grader?</h3><p>Yes. It does the same job as a paper slide grader or an “EZ grader” chart, but you can set the number of items, the grade scale and the pass mark, and print it.</p>
<h3>Is anything saved or uploaded?</h3><p>Your settings stay in this browser so the chart is ready next time. Nothing is sent to a server.</p>'''
