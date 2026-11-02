#!/usr/bin/env python3
"""Builds QuizPolice's information pages into public/. The apps are public/teacher/ and public/join/.
Run: python3 tools/build.py   (standard library only)"""
import json, os, html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
CFG = json.load(open(os.path.join(ROOT, 'site.config.json')))
E = lambda s: html.escape(str(s), quote=True)
URL = CFG['site_url'].rstrip('/'); NAME = CFG['site_name']; ST = CFG['studio']; MAIL = CFG['contact_email']
LOGO = ('<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><path d="M20 3l14 5v10c0 9-6 16-14 19C12 34 6 27 6 18V8z" fill="#1C2F5E"/>'
        '<path d="M20 11l2.6 5.3 5.8.8-4.2 4.1 1 5.8L20 24.3 14.8 27l1-5.8-4.2-4.1 5.8-.8z" fill="#E8A317"/></svg>')


import hashlib as _h
CSSV = _h.md5(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public', 'assets', 'site.css'), 'rb').read()).hexdigest()[:8]

# ---------------------------------------------------------------- Telar Labs family links
FAMILY = [f for f in CFG.get('family', []) if f['name'] != CFG['site_name']]
HUB = CFG.get('studio_url', '')

def slug_app(n): return ''.join(ch for ch in n.lower() if ch.isalnum())

def family_row():
    if not FAMILY: return ''
    head = f'<a href="{E(HUB)}">More from {E(CFG["studio"])}</a>' if HUB else f'More from {E(CFG["studio"])}'
    links = ''.join(f'<a class="app-{slug_app(f["name"])}" href="{E(f["url"])}" title="{E(f["blurb"])}">{E(f["name"])}</a>' for f in FAMILY)
    return f'<div class="wrap family"><span class="family-h">{head}:</span>{links}</div>'

def family_promo(title):
    if not FAMILY: return ''
    links = ''.join(f'<a class="app-{slug_app(f["name"])}" href="{E(f["url"])}"><b>{E(f["name"])}</b><span>{E(f["blurb"])}</span></a>' for f in FAMILY)
    return f'<section class="wrap section family-promo"><h2>{title}</h2><div class="family-links">{links}</div></section>'

def ad(key):
    slot = CFG['ad_slots'].get(key, '')
    if not (CFG['adsense_client'] and slot): return ''
    return (f'<div class="ad"><span class="ad-label">Advertisement</span><ins class="adsbygoogle" style="display:block" data-ad-client="{E(CFG["adsense_client"])}" '
            f'data-ad-slot="{E(slot)}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')

def page(path, title, desc, body):
    full = title if NAME in title else f'{title} | {NAME}'
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={E(CFG["adsense_client"])}" crossorigin="anonymous"></script>'
           if CFG['adsense_client'] else '')
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(URL + path)}">
<meta property="og:title" content="{E(full)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{E(URL + path)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#1C2F5E">
<link rel="preload" href="/assets/fonts/source-sans-3-400.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/site.css?v={CSSV}">
{ads}
</head>
<body>
<header class="top"><div class="wrap top-in">
  <a class="logo" href="/">{LOGO}<span>{E(NAME)}</span></a>
  <nav class="nav"><a href="/how-it-works/">How it works</a><a href="/supported-quizzes/">Supported quizzes</a><a href="/faq/">FAQ</a></nav>
  <a class="btn btn-ghost btn-sm" href="/join/">I'm a student</a><a class="btn btn-sm" href="/teacher/">Teacher dashboard</a>
</div></header>
<main>
{body}
</main>
<footer class="foot"><div class="wrap foot-in">
  <div><a class="logo" href="/">{LOGO}<span>{E(NAME)}</span></a><p class="muted">Free quiz monitoring for Google Forms, Microsoft Forms and Wayground. Part of the {E(ST)} teacher tools.</p></div>
  <div class="foot-cols">
    <div><h4>Use it</h4><a href="/teacher/">Teacher dashboard</a><a href="/join/">Join a quiz</a><a href="/how-it-works/">How it works</a><a href="/supported-quizzes/">Supported quizzes</a><a href="/faq/">FAQ</a></div>
    <div><h4>{E(ST)}</h4><a href="/about/">About</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a><a href="/contact/">Contact</a></div>
  </div>
</div>{family_row()}<div class="wrap fine">&copy; {date.today().year} {E(ST)}.</div></footer>
</body>
</html>'''
    out = os.path.join(PUB, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(PUB, path.strip('/'))
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(doc)

def prose(path, title, desc, inner): page(path, title, desc, f'<article class="wrap prose">{inner}</article>')

FEATS = [('Works with the quizzes you already have', 'Paste a Google Forms, Microsoft Forms or Wayground link. No need to rebuild your questions.'),
         ('See who leaves the quiz', 'Switching tabs, opening another app or clicking outside the quiz is recorded with the time and how long they were away.'),
         ('Lock after too many exits', 'Choose how many exits are allowed. Locked students wait for you to unlock them from your dashboard.'),
         ('Timers and scheduled exams', 'Add a time limit, schedule an exam for the whole class at the same time, or open a quiz between two dates for homework. Students see a countdown.'),
         ('Live dashboard', 'A class list that updates every few seconds: answering, left the quiz, locked, or submitted.'),
         ('Join with a code or QR', 'Students type a 6-digit code or scan the QR code. No student accounts needed.'),
         ('Results you can keep', 'Download a CSV of names, sections, exits and time away for your records.')]

def home():
    f = ''.join(f'<div class="feat"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in FEATS)
    body = f'''
<section class="hero"><div class="wrap hero-in">
  <div><p class="eyebrow">Free · No student accounts · Works on phones</p>
  <h1>Keep online quizzes honest</h1>
  <p class="hero-sub">QuizPolice shows your Google Forms, Microsoft Forms or Wayground quiz inside a monitored page and tells you, live, when students leave it.</p>
  <div class="cta"><a class="btn btn-big" href="/teacher/#new">Set up a quiz</a><a class="btn btn-ghost btn-big" href="/join/">Join a quiz</a></div></div>
  <div class="mock"><div class="mrow"><b>Science 7 · Quiz 2</b><span class="code">482 915</span></div>
    <div class="mchips"><span class="c-info">18<br><small>Answering</small></span><span class="c-warn">2<br><small>Left now</small></span><span class="c-bad">1<br><small>Locked</small></span><span class="c-ok">9<br><small>Submitted</small></span></div>
    <div class="mlist"><div><b>Emily R.</b><span class="pill p-lock">Locked · 3 exits</span></div><div><b>Jacob M.</b><span class="pill p-away">Left the quiz · 0:34</span></div><div><b>Olivia S.</b><span class="pill p-ans">Answering</span></div><div><b>Ethan B.</b><span class="pill p-done">Submitted</span></div></div></div>
</div></section>
<section class="wrap section"><h2>What QuizPolice does</h2><div class="feats">{f}</div></section>
{ad("home")}
<section class="wrap section"><h2>How it works in class</h2>
<ol class="steps"><li><h3>Create the quiz</h3><p>Open the <a href="/teacher/#new">teacher dashboard</a>, name your quiz and paste its link. Choose how many exits are allowed, and when students take it: anytime, as a scheduled exam, or within an open period.</p></li>
<li><h3>Students join</h3><p>Show the code or QR on the board. Students type their name and section, then answer inside QuizPolice.</p></li>
<li><h3>Watch and act</h3><p>See exits and time left as they happen, unlock students or give extra time, and download the results when the quiz is done.</p></li></ol></section>
<section class="wrap section"><div class="callout"><h2>Honest about what it can and can't see</h2><p>QuizPolice only knows when a student leaves the quiz page on the same device. It can't see other phones, the student's screen, or what they search. It's a strong reminder and a record, not mind-reading, and we tell students exactly what is monitored before they start.</p><a class="btn" href="/how-it-works/">Read how it works</a></div></section>'''
    body += family_promo('More free tools for teachers')
    page('/', f'{NAME} – Free Quiz Monitor for Google Forms, Microsoft Forms & Wayground',
         'Free online quiz monitoring for teachers. See when students leave a Google Forms, Microsoft Forms or Wayground quiz, lock after too many exits, and download results.', body)

def pages():
    prose('/how-it-works/', 'How QuizPolice Works', 'How QuizPolice detects students leaving an online quiz, and what it can and cannot see.', f'''
<h1>How {E(NAME)} works</h1>
<p class="lead">Your quiz stays on Google Forms, Microsoft Forms or Wayground. QuizPolice shows it inside a page that notices when a student leaves.</p>
<h2>What counts as leaving</h2>
<ul><li>Switching to another browser tab or window.</li><li>Opening another app on a phone or tablet, or going to the home screen.</li>
<li>Clicking outside the quiz on a computer (for example, into another window side by side).</li></ul>
<p>Each exit is recorded with the time, and when the student comes back, how many seconds they were away.</p>
<h2>Locking</h2>
<p>With <b>Lock after</b> turned on, a student who reaches the exit limit sees "Quiz locked" and can't continue until you press <b>Unlock</b> on your dashboard. You can change the limit during the quiz.</p>
<h2>Timers and schedules</h2>
<p>When you set up a quiz, choose <b>When do students take it?</b></p>
<ul><li><b>Anytime:</b> students start whenever you share the code. You can add a time limit (10 minutes to 3 hours) that starts when each student joins.</li>
<li><b>Scheduled exam:</b> pick the date, start time and length. Students who open the link early wait on a countdown screen. The quiz appears for everyone at the start time and ends for everyone together. Students who join late get only the time that is left.</li>
<li><b>Open period:</b> pick an opening and a closing date, for example Monday 8 am to Friday 5 pm. Students can start any time in between, with an optional time limit for each student that never runs past the closing time.</li></ul>
<p>Students see a countdown above the quiz, with reminders at 5 minutes and 1 minute left. When time runs out, the quiz is covered with a <b>Time's up</b> screen. On your dashboard you see each student's time left, and you can <b>Start now</b>, give one student <b>+5 minutes</b>, or <b>End the quiz for everyone</b>. Times are set in your time zone; students see them in their own.</p>
<p><b>Important:</b> QuizPolice can't press Submit on the Google or Microsoft form for the student. Answers that weren't submitted before the time ran out are not sent, so remind students to submit before the end. For a hard cut-off, you can also turn off "Accepting responses" on the form itself.</p>
<h2>What it can't see</h2>
<ul><li>Another phone or a book on the desk.</li><li>Screenshots, or what is happening on the student's screen.</li>
<li>Whether the student actually pressed Submit on the form. Students tap <b>I've submitted</b>; check the form's own responses for the official answers.</li></ul>
<h2>Tips for fewer problems</h2>
<ul><li>Use <b>Check this link</b> when you set up the quiz. It warns you if the quiz requires sign-in or can't be shown inside other sites.</li>
<li>Ask students to close other apps before joining and to keep the phone plugged in.</li><li>Tell students that leaving is recorded. Most cheating stops once students know.</li></ul>''')
    prose('/supported-quizzes/', 'Supported Quiz Platforms', 'Which quiz links work with QuizPolice: Google Forms, Microsoft Forms and Wayground, and the settings to check.', f'''
<h1>Supported quizzes</h1>
<table class="tbl"><thead><tr><th>Platform</th><th>Works?</th><th>Settings to check</th></tr></thead><tbody>
<tr><td><b>Google Forms</b></td><td>Yes</td><td>Turn off <i>Restrict to users in your organization</i> and <i>Collect email addresses: Verified</i>. Use <i>Responder input</i> for emails instead. Signing in inside another site often fails because browsers block the needed cookies.</td></tr>
<tr><td><b>Microsoft Forms</b></td><td>Yes</td><td>Set <i>Who can fill out this form</i> to <i>Anyone can respond</i>. "Only people in my organization" requires a sign-in that may not work inside QuizPolice.</td></tr>
<tr><td><b>Wayground</b></td><td>Depends</td><td>Some Wayground pages don't allow being shown inside other sites. Use <b>Check this link</b> when you create the quiz; if it's blocked, use a Google or Microsoft form instead.</td></tr>
<tr><td>Other sites</td><td>Maybe</td><td>Any quiz page that allows embedding will work. Check this link will tell you.</td></tr></tbody></table>''')
    faq = [('Is QuizPolice free?', 'Yes. Teachers and students don\'t pay or create accounts.'),
           ('Do students need an account?', 'No. They type the code, their name and section.'),
           ('Where are my quizzes saved?', 'Your quiz list is saved in your browser on this device, together with a secret key that lets only you see the results. To open a dashboard on another device, use the private teacher link on the dashboard (copy it, send it with Gmail or Outlook, or scan its QR code with your phone). Keep that link private: anyone who has it can see the results.'),
           ('I used a shared or school computer. What should I do?', 'When you\'re done, open My quizzes and tap Remove from this device (or Remove all). The results are not deleted. You can still open them with your private teacher link on your own phone or laptop, so save that link first.'),
           ('How long is student data kept?', 'Quizzes and student results are deleted automatically 30 days after the quiz is created. You can delete a quiz and its results any time from the dashboard.'),
           ('Can I set a time limit or schedule an exam?', 'Yes. When you create a quiz, choose Anytime (with an optional time limit), Scheduled exam (everyone starts and ends together at a set date and time) or Open period (students start any time between two dates). Students see a countdown, and you can give extra time or end the quiz for everyone from your dashboard.'),
           ('What happens when the time runs out?', 'The quiz is covered with a Time\'s up screen and the student is marked "Time\'s up" on your dashboard. QuizPolice can\'t submit the form for them, so answers that weren\'t submitted are not sent. Give the student +5 minutes if they need more time; the quiz comes back by itself.'),
           ('Does it work on phones?', 'Yes. Students can join on phones, tablets or computers. Detection is strongest when the quiz is opened in Chrome, Safari or Edge.'),
           ('Can students cheat anyway?', 'A determined student with a second device can. QuizPolice is a deterrent and a record, best combined with good quiz design and supervision.'),
           ('Does it see the students\' answers?', 'No. Answers go straight to your Google or Microsoft form. QuizPolice only sees joins, exits, returns, locks and "I\'ve submitted".')]
    prose('/faq/', 'Frequently Asked Questions', f'Answers to common questions about {NAME}.', '<h1>Frequently asked questions</h1>' + ''.join(f'<h2>{E(q)}</h2><p>{E(a)}</p>' for q, a in faq))
    prose('/about/', 'About', f'About {NAME} by {ST}.', f'''
<h1>About {E(NAME)}</h1>
<p class="lead">{E(NAME)} is a free tool for teachers who give quizzes online, made by {E(ST)}, a small independent studio.</p>
<p>Many teachers already use free Google Forms or Microsoft Forms for quizzes, but those can't tell when a student switches to another tab to search for answers. Exam lockdown tools are usually expensive, need installs, or require accounts for every student. {E(NAME)} adds a simple, honest layer of monitoring to the quizzes teachers already have.</p>
<h2>Our promises</h2><ul><li>Free for teachers and students, no accounts.</li><li>We collect only what the teacher needs: name, section and quiz activity.</li><li>Student data is deleted after 30 days.</li><li>No ads on the student quiz screen or the teacher dashboard.</li></ul>
<h2>Other {E(ST)} tools</h2><p><a href="https://pizarrapad.telarlabs.net">PizarraPad</a>, a free whiteboard for teachers, <a href="https://drafttrail.telarlabs.net">DraftTrail</a>, a writing-process recorder, and <a href="https://clips.telarlabs.net">Telar Clips</a>, free motion backgrounds for videos.</p>''')
    prose('/privacy/', 'Privacy Policy', f'Privacy policy for {NAME}.', f'''
<h1>Privacy policy</h1>
<p class="lead">{E(NAME)} is run by {E(ST)}. We collect as little as possible and delete it quickly.</p>
<h2>What we collect from students</h2>
<ul><li>The name and section the student types when joining.</li><li>Quiz activity: when they joined, left the quiz page, came back, were locked or unlocked, ran out of time or were given extra time, and tapped "I've submitted".</li></ul>
<p>We do <b>not</b> collect quiz answers (those go directly to the teacher's form), email addresses, location, or anything that happens outside the quiz page.</p>
<h2>What we collect from teachers</h2><p>The quiz name, quiz link and settings. There are no teacher accounts; a secret key stored in the teacher's browser gives access to the dashboard.</p>
<h2>Who can see it</h2><p>Only the teacher who created the quiz (the browser holding its secret key). We don't sell or share the data.</p>
<h2>How long we keep it</h2><p>Everything about a quiz is deleted automatically 30 days after it was created. Teachers can delete a quiz and its results earlier from the dashboard.</p>
<h2>Advertising</h2><p>The information pages of this site may show ads from Google AdSense, which uses cookies; you can manage personalized ads in <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>. <b>The student quiz screen and the teacher dashboard never show ads.</b></p>
<h2>Children</h2><p>{E(NAME)} is used in schools, including by students under 18. We only process the minimum needed for the teacher to run the quiz, and teachers are responsible for following their school's rules about using online tools with their students.</p>
<h2>Analytics</h2><p>We use Cloudflare Web Analytics to count page visits. It does not use cookies and does not track you across websites.</p>
<h2>Hosting</h2><p>The site and data are hosted on Cloudflare.</p>
<h2>Contact</h2><p><a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p class="muted">Last updated {E(CFG.get("updated", CFG["launch_date"]))}.</p>''')
    prose('/terms/', 'Terms of Use', f'Terms of use for {NAME}.', f'''
<h1>Terms of use</h1><ul>
<li>{E(NAME)} is free to use for quizzes, tests and practice.</li><li>Teachers should tell students that the quiz is monitored (QuizPolice also shows this before every quiz).</li>
<li>Use it fairly: exits are a sign to talk with a student, not automatic proof of cheating.</li>
<li>The service is provided as it is, without warranty. Download your results after each quiz; data is deleted after 30 days.</li></ul>
<p>Questions: <a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p class="muted">Last updated {E(CFG.get("updated", CFG["launch_date"]))}.</p>''')
    prose('/contact/', 'Contact', f'Contact {NAME}.', f'<h1>Contact us</h1><p class="lead">Questions, problems or ideas?</p><p>Email: <a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p>If a quiz link doesn\'t work, include the platform (Google Forms, Microsoft Forms or Wayground) and the device students use.</p>')

def extras():
    open(os.path.join(PUB, 'favicon.svg'), 'w').write(LOGO.replace('class="logo-mark" ', 'xmlns="http://www.w3.org/2000/svg" '))
    urls = ['/', '/how-it-works/', '/supported-quizzes/', '/faq/', '/about/', '/privacy/', '/terms/', '/contact/']
    open(os.path.join(PUB, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{URL}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(PUB, 'robots.txt'), 'w').write(f'User-agent: *\nDisallow: /api/\nDisallow: /teacher/\nDisallow: /join/\nSitemap: {URL}/sitemap.xml\n')
    if CFG['adsense_client']:
        open(os.path.join(PUB, 'ads.txt'), 'w').write(f'google.com, {CFG["adsense_client"].replace("ca-", "")}, DIRECT, f08c47fec0942fa0\n')
    page('/404.html', 'Page not found', 'Page not found.', '<section class="wrap prose"><h1>Page not found</h1><p><a class="btn" href="/">Go home</a></p></section>')

if __name__ == '__main__':
    home(); pages(); extras(); print('Built QuizPolice pages')
