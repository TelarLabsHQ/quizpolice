"""Send visitors of the old *.pages.dev address to the real domain, same page.
Only when this browser has nothing saved on the old address (no quiz, draft, board, story or organizer data),
so nobody loses work. Added to the <head> of every HTML page by the build."""
import os, re, sys
MARK = '<!--home-domain-->'
SNIPPET = MARK + '''<script>(function(){var M={"quizpolice.pages.dev":"quizpolice.telarlabs.net","tixward.pages.dev":"tixward.telarlabs.net","drafttrail.pages.dev":"drafttrail.telarlabs.net","drafttrail-c4t.pages.dev":"drafttrail.telarlabs.net","pizarrapad.pages.dev":"pizarrapad.telarlabs.net","telarclips.pages.dev":"clips.telarlabs.net","telar-clips.pages.dev":"clips.telarlabs.net","telarlabs-home.pages.dev":"telarlabs.net","telar-stories.pages.dev":"stories.telarlabs.net"},to=M[location.hostname];if(!to)return;
function go(){location.replace("https://"+to+location.pathname+location.search+location.hash)}
try{if(localStorage.length||sessionStorage.length)return}catch(e){return}
if(window.indexedDB&&indexedDB.databases){indexedDB.databases().then(function(d){if(!d.length)go()},function(){})}else go()})();</script>'''

def inject(root):
    n = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.html'): continue
            p = os.path.join(dp, f); s = open(p, encoding='utf-8').read()
            if MARK in s:
                s2 = re.sub(re.escape(MARK) + r'<script>.*?</script>', lambda m: SNIPPET, s, count=1, flags=re.S)
            else:
                m = re.search(r'<head[^>]*>', s, re.I)
                if not m: continue
                i = m.end(); cm = re.search(r'<meta charset[^>]*>', s[i:i + 300], re.I)
                if cm: i += cm.end()
                s2 = s[:i] + SNIPPET + s[i:]
            if s2 != s: open(p, 'w', encoding='utf-8').write(s2); n += 1
    return n

if __name__ == '__main__':
    for r in sys.argv[1:]: print(r, inject(r))
