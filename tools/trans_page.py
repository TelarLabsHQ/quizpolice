"""Transmutation table maker (/tools/transmutation-table/): your own rule, or the K to 12 tables. Script: tools/js/transmute.js."""
import json, os
from grades_content import CSS, NEW_TABLE, OLD_TABLE, table_html

STYLE = '''<style>
.et-tabs{display:flex;gap:6px;flex-wrap:wrap}.et-tabs button{border:1px solid var(--line);background:#fff;border-radius:99px;padding:7px 14px;font:inherit;font-size:15px;font-weight:600;cursor:pointer;color:var(--fg)}.et-tabs button[aria-pressed=true]{background:var(--brand);border-color:var(--brand);color:#fff}
.gc-btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 14px;font:inherit;font-size:15px;font-weight:700;cursor:pointer;color:var(--fg)}.gc-btn.pri{background:var(--brand);border-color:var(--brand);color:#fff}
.gc-top{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.row4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;align-items:end}@media(max-width:640px){.row4{grid-template-columns:1fr 1fr}}
.warnbox{background:var(--warn-bg);color:var(--warn);border-radius:10px;padding:8px 12px;font-size:15px;margin:0}.okbox{background:var(--ok-bg);color:var(--ok);border-radius:10px;padding:8px 12px;font-size:15px;margin:0}
#tmTable{max-width:520px}#tmTable tr.fail td{color:var(--bad)}#tmTable td:last-child,#tmTable th:last-child{text-align:center}
@media print{body *{visibility:hidden}#tmPrintArea,#tmPrintArea *{visibility:visible}#tmPrintArea{position:absolute;left:0;top:0;width:100%}#tmTable{max-width:none;font-size:12px}#tmTable td{padding:2px 6px}}
</style>'''

HTML = '''
<div class="gc">
  <p class="okbox" id="tmShared" hidden>Showing a shared transmutation rule.</p>
  <div class="et-tabs" id="tmModes"><button type="button" data-m="own">My own rule</button><button type="button" data-m="2026">K to 12 adjusted (2026–2027)</button><button type="button" data-m="2015">K to 12 (2015)</button></div>
  <div id="tmOwn"><div class="row4">
    <label>Passing score (%)<input id="tmPp" inputmode="decimal"></label><label>becomes the grade<input id="tmPg" inputmode="decimal"></label>
    <label>A score of 0% becomes<input id="tmLg" inputmode="decimal"></label><label>A score of 100% becomes<input id="tmTg" inputmode="decimal"></label></div>
    <p class="note2" style="margin:6px 0 0">Scores between are spread evenly: one band for each whole grade above the passing grade, and one for each below it.</p></div>
  <p class="warnbox" id="tmWarn" hidden></p>
  <div class="row2"><label>Look up a score or initial grade (%)<input id="tmIg" inputmode="decimal" placeholder="e.g. 82.08"></label><div class="res" id="tmLook"></div></div>
  <div class="gc-top"><div class="et-tabs" id="tmViews"><button type="button" data-v="bands">Full table</button><button type="button" data-v="items">For a test with…</button></div>
    <label id="tmItemsL" style="flex-direction:row;align-items:center;gap:8px" hidden><input id="tmItems" type="number" min="1" max="500" style="width:90px"> items</label></div>
  <div id="tmPrintArea"><h3 id="tmCap" style="margin:4px 0 8px;font-size:17px"></h3><table class="ttab" id="tmTable"></table></div>
  <div class="gc-top"><button class="gc-btn pri" type="button" id="tmUse">Use it in the grade calculator</button><button class="gc-btn" type="button" id="tmPrint">🖨 Print</button><button class="gc-btn" type="button" id="tmCopy">Copy table</button><button class="gc-btn" type="button" id="tmLink">🔗 Copy link to my rule</button></div>
  <p class="note2" style="margin:0">Grades below passing are shown in red. Copy table pastes neatly into Excel or Google Sheets.</p>
</div>'''

def trans_page():
    js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js', 'transmute.js'), encoding='utf-8').read()
    js = js.replace('__T2026__', json.dumps(NEW_TABLE)).replace('__T2015__', json.dumps(OLD_TABLE))
    return CSS + STYLE + HTML + '<script>' + js + '</script>'

TRANS_TEXT = '''
<h2>What is a transmutation table?</h2>
<p>A transmutation table turns a raw percentage into a grade on your school’s scale. Many schools don’t want 60% of the items correct to show up as a “60”, so the passing score is set to a passing grade, like 60% becoming 75, and the scores above and below are spread out from there.</p>
<h2>How to make your own</h2>
<ol><li>Type your <b>passing score</b> as a percentage, and the <b>grade</b> it should become.</li>
<li>Type the grades for a score of <b>0%</b> and <b>100%</b>. The lowest grade is often 60 or 65, so no one gets a zero for trying.</li>
<li>Read the full table, or choose <b>For a test with…</b> and type the number of items to get every raw score with its grade, ready to use while checking papers.</li>
<li>Print it, copy it into a spreadsheet, send the link to colleagues, or use it straight away in the <a href="/tools/grade-calculator/">grade calculator</a>.</li></ol>
<h2>Example</h2>
<p>With a passing score of 60% becoming 75, 0% becoming 60 and 100% becoming 100, the 25 grades from 75 to 100 share the scores from 60% to 100%, so each band is 1.60 points wide. Below passing, the 15 grades from 60 to 74 share 0% to 60%, 4 points each. That’s the same rule as the K to 12 table from 2015.</p>
<h2>The K to 12 tables</h2>
<p>Both K to 12 tables are ready to use above. In the 2026–2027 adjusted table, an initial grade of <b>70</b> is needed for a passing 75, compared with <b>60</b> in the 2015 table. From school year 2027–2028, Grades 4 to 12 no longer transmute: an initial grade of 75 is a final 75.</p>
<details><summary style="cursor:pointer;font-weight:700">See both K to 12 tables in full</summary><div class="tts" style="margin-top:10px">''' + table_html(NEW_TABLE, 'Adjusted table (2026–2027)') + table_html(OLD_TABLE, 'Table (2015)') + '''</div></details>
<h2>Questions</h2>
<h3>Is this an official table?</h3><p>The tool is independent and not affiliated with any school system or agency. The two K to 12 tables follow the published tables; always confirm with your school’s official records.</p>
<h3>Is my table saved?</h3><p>Your rule is saved in this browser only. The link to your rule carries just the four numbers, so anyone who opens it sees the same table.</p>'''
