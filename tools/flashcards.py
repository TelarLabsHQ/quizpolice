"""Flash card maker (/practice/flashcards/): make, study, quiz, print and share decks. Script: tools/js/flashcards.js."""
import os

STYLE = '''<style>
.fc{max-width:760px;margin:8px auto 34px;background:var(--card,#fff);border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:0 10px 30px rgba(20,27,43,.08);display:flex;flex-direction:column;gap:12px}
.fc [hidden]{display:none!important}
.fc-top{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.fc-top select{flex:1 1 220px;min-height:44px;border:1px solid var(--line);border-radius:10px;padding:8px 10px;font:inherit;background:#fff}
.fc-b{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 14px;font:inherit;font-size:15px;font-weight:700;cursor:pointer;color:var(--fg)}.fc-b.pri{background:var(--brand);border-color:var(--brand);color:#fff}.fc-b:disabled{opacity:.45;cursor:default}
.fc-b.got{background:var(--ok-bg,#E3F4EA);border-color:#9fd2b6;color:var(--ok,#1E7F4E)}.fc-b.learn{background:var(--warn-bg,#FFF0D9);border-color:#e3c08f;color:var(--warn,#A35A00)}
.fc-tabs{display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:10px}.fc-tabs button{border:2px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font:inherit;font-size:15px;font-weight:700;cursor:pointer;color:var(--fg)}
.fc-tabs button[aria-pressed=true]{background:var(--brand);border-color:var(--brand);color:#fff}
.fc-shared{background:var(--ok-bg,#E3F4EA);color:var(--ok,#1E7F4E);border-radius:10px;padding:8px 12px;margin:0;font-size:15px}
.fc-l{display:flex;flex-direction:column;gap:5px;font-weight:700;font-size:14px}.fc input[type=text],.fc-l input,.fc textarea{font:inherit;font-size:16px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;min-width:0;width:100%;box-sizing:border-box;resize:vertical}
.fc-rows{display:flex;flex-direction:column;gap:8px}.fc-row{display:grid;grid-template-columns:22px minmax(0,1fr) minmax(0,1fr) 28px;gap:8px;align-items:start}
@media(max-width:560px){.fc-row{grid-template-columns:22px minmax(0,1fr) 28px}.fc-row textarea[data-j="1"]{grid-column:2}.fc-row .fc-x{grid-row:1;grid-column:3}}
.fc-n{color:var(--muted);font-weight:700;font-size:13px;padding-top:12px;text-align:right}.fc-x{border:0;background:none;color:var(--muted);font-size:17px;cursor:pointer;padding-top:10px}
.fc-btns{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.fc-paste summary{cursor:pointer;font-weight:700}.fc-paste{border:1px dashed var(--line);border-radius:12px;padding:10px 12px}
.fc-opts{display:flex;gap:14px;flex-wrap:wrap;align-items:center}.fc-chk{display:flex;gap:8px;align-items:flex-start;font-weight:600;font-size:15px}.fc-chk input{width:20px;height:20px;flex:none;margin-top:1px}
.fc-bar{height:8px;background:#E6EAF2;border-radius:99px;overflow:hidden}.fc-bar i{display:block;height:100%;background:var(--badge,#E8A317);transition:width .3s}
.fc-card{display:block;width:100%;height:300px;perspective:1200px;background:none;border:0;padding:0;cursor:pointer;font:inherit;color:inherit}
.fc-in{position:relative;display:block;width:100%;height:100%;transition:transform .45s;transform-style:preserve-3d}.fc-card.flip .fc-in{transform:rotateY(180deg)}
.fc-face{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:22px;border-radius:18px;border:2px solid var(--line);background:#fff;backface-visibility:hidden;-webkit-backface-visibility:hidden;box-shadow:0 8px 22px rgba(20,27,43,.08);overflow:auto}
.fc-face small{position:absolute;top:12px;left:16px;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.fc-face b{font-size:clamp(20px,4.2vw,30px);line-height:1.3;text-align:center}.fc-back{transform:rotateY(180deg);background:#F5F8FF;border-color:#c8d5f2}.fc-back b{font-weight:600;font-size:clamp(17px,3.4vw,23px)}
.fc-judge{justify-content:center}.fc-judge .fc-b{min-width:130px;padding:12px 16px}
.fc-q{font-family:var(--head);font-weight:800;font-size:clamp(22px,4.5vw,30px);text-align:center;padding:16px 8px}
.fc-choices{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:560px){.fc-choices{grid-template-columns:1fr}}
.fc-ch{border:2px solid var(--line);background:#fff;border-radius:12px;padding:12px;font:inherit;font-size:15.5px;text-align:left;cursor:pointer;color:var(--fg);line-height:1.35}
.fc-ch.ok{border-color:#1E7F4E;background:#E3F4EA;font-weight:700}.fc-ch.no{border-color:#B4232F;background:#FDE5E7}
.fc-done{text-align:center;padding:10px}.fc-done h3{font-size:34px;margin:0 0 6px}.fc-miss{text-align:left;background:#F7F8FB;border-radius:12px;padding:10px 14px;margin:10px 0;display:flex;flex-direction:column;gap:6px;font-size:15px}
.fc-pl{display:flex;flex-direction:column;gap:10px}
#fcPrint{display:none}
@media print{body *{visibility:hidden}#fcPrint,#fcPrint *{visibility:visible}#fcPrint{display:block;position:absolute;left:0;top:0;width:100%}@page{margin:10mm}
 .fcp-page{break-after:page;page-break-after:always;font-family:Arial,sans-serif;color:#111}.fcp-page:last-child{break-after:auto;page-break-after:auto}.fcp-h{font-size:10px;color:#777;margin-bottom:4px}
 .fcp-row{display:grid;grid-template-columns:1fr 1fr;border:1px dashed #999;border-bottom:0;height:31mm}.fcp-row:last-child{border-bottom:1px dashed #999}.fcp-row div{display:flex;align-items:center;justify-content:center;text-align:center;padding:4mm;font-size:13pt}.fcp-row div:first-child{border-right:1px dashed #bbb;font-weight:700}
 .fcp-grid{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:52mm;border-top:1px dashed #999;border-left:1px dashed #999}.fcp-grid div{border-right:1px dashed #999;border-bottom:1px dashed #999;display:flex;align-items:center;justify-content:center;text-align:center;padding:5mm;font-size:14pt}}
</style>'''

HTML = '''
<div class="fc">
  <p class="fc-shared" id="fcShared" hidden>📥 You opened a shared deck: <b></b>. It’s saved on this device as your own copy.</p>
  <div class="fc-top"><select id="fcDeck" aria-label="My decks"></select><button type="button" class="fc-b" id="fcNew">+ New deck</button><button type="button" class="fc-b" id="fcShare">🔗 Share this deck</button><button type="button" class="fc-b" id="fcDel" aria-label="Delete this deck">🗑</button></div>
  <p class="muted small" id="fcLinkNote" hidden style="margin:0"></p>
  <div class="fc-tabs" id="fcTabs"><button type="button" data-t="make">✏️ Make</button><button type="button" data-t="study">🃏 Study</button><button type="button" data-t="quiz">❓ Quiz</button><button type="button" data-t="print">🖨 Print</button></div>
  <div id="fcPane"></div>
</div>
<div id="fcPrint" aria-hidden="true"></div>'''

def game():
    js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js', 'flashcards.js'), encoding='utf-8').read()
    return STYLE + HTML + '<script>' + js + '</script>'

TEXT = '''
<h2>How to make flash cards</h2>
<ol><li><b>Make a deck.</b> Type a term on the front and its meaning on the back. Or open <b>Paste a list</b> and paste two columns from Excel or Google Sheets, or lines like “Hola - Hello”.</li>
<li><b>Study.</b> Tap a card to flip it, then mark it <b>Got it</b> or <b>Still learning</b>. At the end of a round, study only the cards you’re still learning.</li>
<li><b>Quiz yourself.</b> Ten multiple-choice questions from your own cards, with a review of the ones you missed.</li>
<li><b>Print</b> cut-out cards, or <b>share the deck</b> with a link.</li></ol>
<h2>Tips for studying with flash cards</h2>
<ul><li><b>Say the answer before you flip.</b> Trying to remember, even when you get it wrong, makes the memory stronger than just reading.</li>
<li><b>Keep cards short:</b> one idea per card. Split long answers into two cards.</li>
<li><b>Study a little every day.</b> Ten minutes a day for a week works better than an hour the night before.</li>
<li><b>Mix it up.</b> Turn on Shuffle, and try <b>Show the back first</b> to practice in the other direction, like English to Spanish.</li>
<li><b>Focus on the hard ones.</b> After each round, study the still-learning cards until they’re all “got it”.</li></ul>
<h2>For teachers</h2>
<ul><li><b>Share a deck with your class:</b> make it once, tap <b>Share this deck</b>, and post the link in your class group or learning platform. Each student gets their own copy to study.</li>
<li><b>Paste from your lesson plan:</b> copy a vocabulary table from a document or spreadsheet into <b>Paste a list</b>.</li>
<li><b>Print for the classroom:</b> fold cards work on any printer. For card stock, use double-sided printing.</li>
<li>Before a test, students can also warm up with the <a href="/practice/">practice games</a>.</li></ul>
<h2>Questions</h2>
<h3>Do I need an account?</h3><p>No. Your decks are saved in this browser on this device. To move a deck to another phone or computer, open its share link there.</p>
<h3>How does the share link work?</h3><p>The whole deck is packed into the link itself, so nothing is uploaded to our servers. Anyone who opens it gets their own copy, and their changes don’t affect yours.</p>
<h3>Can I add pictures?</h3><p>Not yet. Cards can have text, line breaks and emoji.</p>
<h3>How many cards can a deck have?</h3><p>As many as you like on your device. For sharing, decks of up to about 200 short cards make links that work in most apps.</p>'''

PAGE = ('/practice/flashcards/', 'Free Flash Card Maker: Make, Study, Quiz and Print Flashcards Online',
        'Make flash cards online for free: type or paste your terms, flip and study, quiz yourself, print cut-out cards, and share a deck with your class by link. No sign-up.',
        'Flash card maker', game, TEXT)
