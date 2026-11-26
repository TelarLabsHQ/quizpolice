"""Exam tools on QuizPolice: test set shuffler, exam seating chart, exam clock. All in the browser; saved only in the visitor's browser."""
import os
from grades_content import CSS

def _js(name):
    return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js', name), encoding='utf-8').read()

ECSS = '''<style>
.et-tabs{display:flex;gap:6px;flex-wrap:wrap}.et-tabs button{border:1px solid var(--line);background:#fff;border-radius:99px;padding:7px 14px;font:inherit;font-size:15px;font-weight:600;cursor:pointer;color:var(--fg)}.et-tabs button[aria-pressed=true]{background:var(--brand);border-color:var(--brand);color:#fff}
.gc textarea{font:inherit;font-size:15px;padding:10px;border:1px solid var(--line);border-radius:10px;width:100%;box-sizing:border-box;line-height:1.45}
.gc .chk{flex-direction:row;align-items:center;font-weight:600;gap:8px}.gc .chk input{width:20px;height:20px;flex:none}
.gc-btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 14px;font:inherit;font-size:15px;font-weight:700;cursor:pointer;color:var(--fg)}.gc-btn.pri{background:var(--brand);border-color:var(--brand);color:#fff}
.gc-top{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.row3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}@media(max-width:560px){.row3{grid-template-columns:1fr 1fr}}
.warnbox{background:var(--warn-bg);color:var(--warn);border-radius:10px;padding:8px 12px;font-size:15px;margin:0}
</style>'''

# ---------------- test set shuffler ----------------
SHUFFLER = ECSS + '''<style>
.sheet{background:#fff;border:1px solid var(--line);border-radius:10px;padding:28px 30px;color:#111;font-family:"Source Sans 3",Arial,sans-serif;font-size:15.5px;line-height:1.45}
.sheet h3{font-family:inherit;font-size:19px;margin:0;text-align:center}.sheet .sub{text-align:center;margin:2px 0 10px;font-weight:700}
.sheet .who{display:grid;grid-template-columns:2fr 1fr;gap:6px 18px;margin:12px 0}.sheet .who span{border-bottom:1px solid #444;padding-top:10px;font-size:14px}
.sheet .ins{font-style:italic;margin:6px 0 10px}.sheet h4{font-size:16px;margin:14px 0 6px}
.sheet ol.qs{padding-left:26px;margin:0}.sheet ol.qs>li{margin:0 0 10px;break-inside:avoid}.sheet .ch{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px 18px;margin-top:3px}.sheet .ch.one{grid-template-columns:1fr}
.sheet .blank{display:inline-block;min-width:110px;border-bottom:1px solid #444}
.keys{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:4px 14px;font-size:15px}.keys small{color:#666}
#tsOut{display:flex;flex-direction:column;gap:14px}
@media print{body *{visibility:hidden}#tsPrint,#tsPrint *{visibility:visible}#tsPrint{position:absolute;left:0;top:0;width:100%}
 #tsPrint .sheet{border:0;border-radius:0;padding:0;break-after:page;page-break-after:always}#tsPrint .sheet:last-child{break-after:auto;page-break-after:auto}}
</style>
<div class="gc">
  <div class="row2"><label>Test title<input id="tsTitle" maxlength="120" placeholder="e.g. Science 7 · Second Quarter Test"></label><label>School or class (optional)<input id="tsSchool" maxlength="120" placeholder="e.g. Riverside High School"></label></div>
  <label>Instructions (optional)<input id="tsIns" maxlength="240" placeholder="e.g. Choose the letter of the best answer. Write your answers on the answer sheet."></label>
  <label>Questions<textarea id="tsText" rows="16" spellcheck="false"></textarea></label>
  <details><summary style="cursor:pointer;font-weight:700">How to type the questions</summary><ul class="note2" style="margin:8px 0 0;padding-left:20px">
   <li>Leave a <b>blank line</b> between questions.</li><li>Put each choice on its own line, starting with a letter: <code>a)</code>, <code>A.</code> or <code>(a)</code>.</li>
   <li>Mark the correct choice with a <b>*</b> at the end, or add a line <code>Answer: B</code>. For questions without choices, <code>Answer: photosynthesis</code> goes into the key.</li>
   <li>Start a line with <b>#</b> for a part heading, like <code># Part II. True or False</code>. Questions are shuffled within each part, and parts keep their order.</li>
   <li>Choices like “All of the above”, “Both A and B” or True/False keep their order.</li><li>Tip: copy your questions from Word or Google Docs and paste them here.</li></ul></details>
  <div class="row3"><label>Number of sets<select id="tsSets"><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6</option></select></label>
   <label class="chk" style="align-self:end"><input type="checkbox" id="tsQ" checked> Shuffle question order</label><label class="chk" style="align-self:end"><input type="checkbox" id="tsC" checked> Shuffle the choices</label></div>
  <label class="chk"><input type="checkbox" id="tsA" checked> Keep Set A in the original order</label>
  <p class="warnbox" id="tsWarn" hidden></p>
  <div class="gc-top"><button class="gc-btn pri" type="button" id="tsGo">Make the sets</button><button class="gc-btn" type="button" id="tsRe">🔀 Shuffle again</button><span class="note2" id="tsInfo"></span></div>
</div>
<div id="tsRes" hidden>
  <div class="gc-top" style="margin-bottom:10px"><div class="et-tabs" id="tsTabs"></div></div>
  <div class="gc-top" style="margin-bottom:12px"><select id="tsWhat" class="gc-btn" aria-label="What to print"></select><button class="gc-btn pri" type="button" id="tsPrintBtn">🖨 Print</button><button class="gc-btn" type="button" id="tsCopy">Copy this set as text</button></div>
  <div id="tsOut"></div>
</div>
<div id="tsPrint" aria-hidden="true"></div>
<script>''' + '__JS_SHUFFLE__' + '''</script>'''

SHUFFLER_TEXT = '''
<h2>Why use different test sets?</h2>
<p>When students sit close together, a different order of questions and choices makes copying from a neighbor much harder. Set A’s answer to number 5 is a different question on Set B. Combined with an <a href="/tools/exam-seating-chart/">exam seating chart</a> that puts different sets side by side, it’s one of the simplest ways to keep a paper test fair.</p>
<h2>How it works</h2>
<ol><li><b>Paste your questions</b> with their choices, and mark the answers with a *.</li><li><b>Choose 2 to 6 sets.</b> Each set gets its own order of questions, and of choices within each question.</li>
<li><b>Print</b> all the sets, one at a time, and the answer keys. Each key also shows the question’s original number, which helps with item analysis.</li></ol>
<h2>Tips</h2>
<ul><li><b>Keep Set A in the original order</b> so it matches your table of specifications.</li><li>Write choices so they make sense in any order. Avoid “the answer above” or “see number 3”.</li>
<li>For matching-type or essay parts, put them in their own part (with <b>#</b>) and keep it short, or add them by hand after printing.</li>
<li>Giving the test online? Google Forms and Microsoft Forms can shuffle questions themselves, and <a href="/teacher/">QuizPolice</a> shows you when students leave the quiz.</li></ul>
<h2>Questions</h2>
<h3>Are my questions uploaded?</h3><p>No. Everything happens in your browser. Your questions are saved only on this device so they’re here next time.</p>
<h3>Can I make the same sets again?</h3><p>Yes. The sets stay the same until you tap <b>Shuffle again</b>, even if you close the page.</p>'''

# ---------------- exam seating chart ----------------
SEATING = ECSS + '''<style>
.sc-room{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px;overflow-x:auto}
.sc-front{text-align:center;font-weight:800;letter-spacing:.08em;font-size:13px;color:var(--muted);background:var(--bg);border-radius:8px;padding:6px;margin-bottom:10px}
.sc-grid{display:grid;gap:6px;min-width:min-content}
.seat{min-width:86px;min-height:58px;border:1.5px solid var(--line);border-radius:9px;padding:5px 6px;display:flex;flex-direction:column;justify-content:space-between;cursor:pointer;background:#fff;font:inherit;text-align:left;color:var(--fg)}
.seat b{font-size:14px;line-height:1.2;word-break:break-word}.seat small{font-size:11.5px;color:var(--muted);display:flex;justify-content:space-between;gap:4px}
.seat .st{font-weight:800;border-radius:5px;padding:0 5px;color:#fff}
.seat.empty{background:var(--bg);border-style:dashed}.seat.block{background:repeating-linear-gradient(45deg,#eef0f4,#eef0f4 6px,#e2e6ee 6px,#e2e6ee 12px);border-style:dashed}.seat.block b{color:var(--muted);font-weight:600}
.seat.sel{outline:3px solid var(--info);outline-offset:1px}
.s0{background:#2457B8}.s1{background:#B4232F}.s2{background:#1E7F4E}.s3{background:#A35A00}
.seat.t0{border-color:#9db4e3}.seat.t1{border-color:#e7a2a8}.seat.t2{border-color:#9fd2b6}.seat.t3{border-color:#e3c08f}
.sc-list{columns:3 220px;font-size:15px;margin:0;padding:0;list-style:none}.sc-list li{break-inside:avoid;padding:3px 0;border-bottom:1px dotted var(--line)}
.sc-proj .sc-room{position:fixed;inset:0;z-index:50;border-radius:0;overflow:auto;padding:18px}.sc-proj .seat{min-width:120px;min-height:80px}.sc-proj .seat b{font-size:20px}.sc-proj .seat small{font-size:14px}
.sc-x{display:none}.sc-proj .sc-x{display:inline-flex;position:fixed;top:10px;right:12px;z-index:51}
@media print{body *{visibility:hidden}#scPrint,#scPrint *{visibility:visible}#scPrint{position:absolute;left:0;top:0;width:100%}.sc-room{border:0;padding:0;overflow:visible}.seat{min-width:0;break-inside:avoid}@page{size:landscape;margin:10mm}}
</style>
<div class="gc">
  <label>Exam or class (optional)<input id="scTitle" maxlength="100" placeholder="e.g. Grade 9 · Math periodical test · Room 204"></label>
  <div class="row3"><label>Rows (front to back)<input id="scRows" type="number" min="1" max="20" value="5"></label><label>Seats in each row<input id="scCols" type="number" min="1" max="20" value="6"></label>
   <label>Test sets<select id="scSets"><option value="1">1 (no sets)</option><option value="2" selected>2 (A, B)</option><option value="3">3 (A, B, C)</option><option value="4">4 (A to D)</option></select></label></div>
  <label>Students, one per line<textarea id="scNames" rows="8" placeholder="Emily Rogers&#10;Jacob Miller&#10;Olivia Smith"></textarea></label>
  <div class="row2"><label>Order<select id="scOrder"><option value="random">Random</option><option value="alpha">Alphabetical</option><option value="list">As listed</option></select></label>
   <label>Spacing<select id="scGap"><option value="all">Use every seat</option><option value="alt">Leave a seat between students (staggered)</option><option value="row">Leave every other row empty</option></select></label></div>
  <p class="warnbox" id="scWarn" hidden></p>
  <div class="gc-top"><button class="gc-btn pri" type="button" id="scGo">Make the seating chart</button><button class="gc-btn" type="button" id="scRe">🔀 Shuffle again</button></div>
</div>
<div id="scRes" hidden>
  <div class="gc-top" style="margin-bottom:8px"><div class="et-tabs"><button type="button" id="scModeSwap" aria-pressed="true">Tap two seats to swap</button><button type="button" id="scModeBlock" aria-pressed="false">Tap a seat to block it</button></div></div>
  <div class="gc-top" style="margin-bottom:10px"><button class="gc-btn" type="button" id="scProj">📽 Show on projector</button><button class="gc-btn pri" type="button" id="scPrintBtn">🖨 Print chart and list</button><span class="note2" id="scInfo"></span></div>
  <div id="scPrint"><h2 id="scHead" style="margin:0 0 8px;font-size:20px"></h2><div id="scWrap"><div class="sc-room"><button class="gc-btn sc-x" type="button" id="scExit">✕ Close</button><div class="sc-front">FRONT · BOARD · TEACHER’S DESK</div><div class="sc-grid" id="scGrid"></div></div></div>
  <h3 style="margin:18px 0 8px">Seats by name</h3><ul class="sc-list" id="scList"></ul></div>
</div>
<script>''' + '__JS_SEATING__' + '''</script>'''

SEATING_TEXT = '''
<h2>How to use it</h2>
<ol><li>Type the number of <b>rows</b> (front to back) and <b>seats in each row</b>, then paste your class list.</li>
<li>Choose the <b>number of test sets</b>. The chart gives neighbors different sets, so the student beside, in front of or behind has a different paper whenever the room allows it.</li>
<li>Choose <b>spacing</b> if you have room: a staggered gap between students, or empty rows.</li>
<li><b>Fix it by tapping:</b> swap two students, or block a broken or reserved seat. Then print it, or show it on the projector as students come in.</li></ol>
<h2>Tips for a fair exam room</h2>
<ul><li>Post the <b>seats by name</b> list at the door so students find their seat quickly.</li><li>Shuffle a new chart for each exam, so students don’t sit by the same friends every time.</li>
<li>Pair it with the <a href="/tools/test-set-shuffler/">test set shuffler</a> to make Sets A, B, C, and the <a href="/tools/exam-clock/">exam clock</a> on the projector.</li></ul>
<h2>Questions</h2>
<h3>How are sets given out?</h3><p>Seat by seat, the chart picks the set that differs most from the students nearby, and keeps the number of each set even. With 2 sets, students side by side and front to back get different sets; with 4 sets, every neighbor, even diagonally, does.</p>
<h3>Is my class list saved?</h3><p>Only in this browser on this device. Nothing is uploaded.</p>'''

# ---------------- exam clock ----------------
CLOCK = ECSS + '''<style>
#ecRun{position:fixed;inset:0;z-index:60;background:#0f1a33;color:#fff;display:flex;flex-direction:column;padding:3vh 4vw;gap:2vh;font-family:"Archivo","Segoe UI",sans-serif}
#ecRun[hidden]{display:none}#ecRun .t1{font-size:clamp(22px,4vw,54px);font-weight:800;text-align:center;line-height:1.15}#ecRun .t2{font-size:clamp(16px,2.2vw,30px);text-align:center;opacity:.8}
#ecBig{font-size:clamp(80px,19vw,300px);font-weight:800;text-align:center;line-height:1;font-variant-numeric:tabular-nums;letter-spacing:.02em}
#ecMeta{display:flex;justify-content:center;gap:4vw;flex-wrap:wrap;font-size:clamp(16px,2.4vw,32px);opacity:.9;font-variant-numeric:tabular-nums}
#ecBar{height:12px;background:rgba(255,255,255,.15);border-radius:99px;overflow:hidden;margin:0 auto;width:min(1100px,100%)}#ecBar i{display:block;height:100%;width:0;background:#E8A317;transition:width 1s linear}
#ecRules{margin:0 auto;max-width:1100px;width:100%;font-size:clamp(16px,2.2vw,30px);line-height:1.4;columns:2 420px;column-gap:4vw;padding-left:1.2em;font-family:"Source Sans 3",sans-serif}
#ecBanner{text-align:center;font-size:clamp(22px,3.6vw,48px);font-weight:800;border-radius:16px;padding:1vh 2vw;align-self:center}#ecBanner[hidden]{display:none}
#ecRun.w10{background:#4a3507}#ecRun.w10 #ecBanner{background:#E8A317;color:#1b1206}#ecRun.w5{background:#5a1218}#ecRun.w5 #ecBanner{background:#fff;color:#B4232F}
#ecRun.over{background:#B4232F}#ecRun.paused #ecBig{opacity:.45}
#ecCtl{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:auto;opacity:.35;transition:opacity .2s}#ecCtl:hover,#ecCtl:focus-within{opacity:1}
#ecCtl button{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:10px;padding:8px 14px;font:inherit;font-size:16px;cursor:pointer}
</style>
<div class="gc">
  <div class="row2"><label>Exam title<input id="ecTitle" maxlength="100" placeholder="e.g. Math 9 · Periodical Test"></label><label>Class or room (optional)<input id="ecSub" maxlength="100" placeholder="e.g. Grade 9 Mabini · Room 204"></label></div>
  <div class="row3"><label>Time<select id="ecMode"><option value="dur">Length in minutes</option><option value="end">Ends at a time</option></select></label>
   <label id="ecDurL">Minutes<input id="ecDur" type="number" min="1" max="600" value="60"></label><label id="ecEndL" hidden>Ends at<input id="ecEnd" type="time" value="10:00"></label></div>
  <label>Rules to show on screen, one per line<textarea id="ecRulesIn" rows="5"></textarea></label>
  <div class="row3"><label class="chk"><input type="checkbox" id="ecW10" checked> Warn at 10 minutes left</label><label class="chk"><input type="checkbox" id="ecW5" checked> Warn at 5 minutes left</label><label class="chk"><input type="checkbox" id="ecSound" checked> Beep at warnings</label></div>
  <div class="gc-top"><button class="gc-btn pri" type="button" id="ecStart">▶ Start the exam clock</button><span class="note2">It opens full screen. Press F for full screen, Space to pause.</span></div>
  <p class="warnbox" id="ecResume" hidden>An exam clock is still running. <button class="gc-btn" type="button" id="ecBack" style="margin-left:6px">Show it</button></p>
</div>
<div id="ecRun" hidden>
  <div class="t1" id="ecT"></div><div class="t2" id="ecS"></div>
  <div id="ecBanner" hidden></div>
  <div id="ecBig">00:00</div>
  <div id="ecBar"><i></i></div>
  <div id="ecMeta"><span id="ecNow"></span><span id="ecEnds"></span></div>
  <ul id="ecRules"></ul>
  <div id="ecCtl"><button type="button" id="ecPause">❚❚ Pause</button><button type="button" id="ecPlus">+5 min</button><button type="button" id="ecMinus">−5 min</button><button type="button" id="ecFull">⛶ Full screen</button><button type="button" id="ecStop">■ End</button><button type="button" id="ecHide">Back to setup</button></div>
</div>
<script>''' + '__JS_CLOCK__' + '''</script>'''

CLOCK_TEXT = '''
<h2>How to use it</h2>
<ol><li>Type the exam title and either its <b>length</b> or the <b>time it ends</b>.</li><li>Add the <b>rules</b> students should see the whole time.</li>
<li>Tap <b>Start</b> and put it on the projector or TV. Students see the time left, the end time and the rules in big letters.</li>
<li>At <b>10 and 5 minutes left</b>, the screen changes color with a short beep. At zero it says the time is up.</li></ol>
<h2>Good to know</h2>
<ul><li><b>Keyboard:</b> Space pauses, F goes full screen, + and − add or remove 5 minutes.</li><li>If the page is closed or refreshed, the clock picks up where it was, because the end time is saved in this browser.</li>
<li>The screen is kept awake while the clock runs, on browsers that allow it.</li>
<li>Giving the exam online too? Set it up in <a href="/teacher/">QuizPolice</a> with a time limit, so each student’s quiz closes on time and you see who leaves it.</li></ul>
<h2>More for exam day</h2>
<p>Make Sets A, B, C with the <a href="/tools/test-set-shuffler/">test set shuffler</a> and seat students with the <a href="/tools/exam-seating-chart/">exam seating chart</a>.</p>'''

def page_tool(html, jsname, key):
    return lambda: CSS + html.replace(key, _js(jsname))

TOOLS = [
 ('/tools/test-set-shuffler/', 'Test Set Shuffler: Make Sets A, B, C with Answer Keys (Free)',
  'Paste your test questions and make Sets A, B, C with shuffled questions and choices, each with its own answer key. Print-ready, free, no sign-up, nothing uploaded.',
  'Test set shuffler', page_tool(SHUFFLER, 'shuffler.js', '__JS_SHUFFLE__'), SHUFFLER_TEXT, 'Sets A, B, C with shuffled questions and choices, and their answer keys.'),
 ('/tools/exam-seating-chart/', 'Exam Seating Chart Maker: Spread Students Out and Alternate Test Sets',
  'Make an exam seating chart in seconds: rows and seats, your class list, random order, gaps between students, and Sets A and B side by side. Print it or show it on the projector.',
  'Exam seating chart', page_tool(SEATING, 'seating.js', '__JS_SEATING__'), SEATING_TEXT, 'Random seats with gaps, and different test sets side by side.'),
 ('/tools/exam-clock/', 'Exam Clock for the Projector: Countdown Timer with Rules and Warnings',
  'A free full-screen exam countdown for the classroom projector: time left, end time, your exam rules, and warnings at 10 and 5 minutes. No sign-up.',
  'Exam clock', page_tool(CLOCK, 'clock.js', '__JS_CLOCK__'), CLOCK_TEXT, 'A big countdown with the end time, your rules and 10- and 5-minute warnings.'),
]
