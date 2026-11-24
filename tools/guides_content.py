"""QuizPolice help guides: practical articles for teachers (rendered by build.py under /guides/)."""

LEAD = 'Practical, step-by-step guides for giving honest online quizzes and exams with the tools you already use.'

GUIDES = [
dict(slug='stop-tab-switching-google-forms', updated='2026-11-23',
     title='How to Stop Students from Switching Tabs in Google Forms',
     short='Stop tab switching in Google Forms',
     desc='Can Google Forms detect when students switch tabs? What locked mode does, who can use it, and how to see or limit tab switching on any device.',
     body='''<p class="lead">Google Forms can’t tell when a student opens another tab, except in one special case. Here is what each option really does, and how to choose.</p>

<p>Students switch tabs during online quizzes for the same reason they used to glance at a neighbor’s paper: it’s easy and nobody sees it. A search engine, a group chat or an AI chatbot is one tap away. The good news is that you have several ways to deal with it, from settings that block it on some devices to tools that make it visible on every device.</p>

<h2>Can Google Forms detect tab switching?</h2>
<p>No. A normal Google Form doesn’t know what else is open on the student’s device. It only receives the answers when the student presses Submit. There is no setting that warns you when a student leaves the form and comes back.</p>
<p>The one exception is <b>locked mode</b>, described below. It doesn’t detect switching; it prevents it, and only on certain devices.</p>

<h2>Option 1: Locked mode (school Chromebooks only)</h2>
<p>Locked mode keeps students inside the quiz: they can’t open other tabs or apps until they submit. To use it, all of these must be true:</p>
<ul><li>You and your students use a <b>Google Workspace for Education</b> account from your school.</li>
<li>Students take the quiz on <b>Chromebooks managed by the school</b>.</li>
<li>The form is set up as a quiz.</li></ul>
<p>To turn it on, open the form, go to <b>Settings</b>, open the <b>Quizzes</b> section, and turn on <b>locked mode</b>. If you don’t see the option, your account or your school’s settings don’t support it.</p>
<p>Locked mode doesn’t work on phones, tablets, Windows laptops or Macs. In many classrooms, especially where students use their own phones, that rules it out.</p>

<h2>Option 2: Make tab switching visible on any device</h2>
<p>If students use phones or a mix of devices, you can’t block other apps, but you can make leaving the quiz visible. That’s what <a href="/">QuizPolice</a> does:</p>
<ol><li>Create your quiz in Google Forms as usual.</li>
<li>Open the <a href="/teacher/#new">QuizPolice teacher dashboard</a>, give the quiz a name, and paste the form link. Press <b>Check this link</b>.</li>
<li>Choose how many exits are allowed before a student is locked, for example 3.</li>
<li>Show the 6-digit code or QR code on the board. Students type their name and answer the form inside QuizPolice.</li>
<li>Your dashboard shows, live, who is answering, who just left the quiz, for how long, and who is locked.</li></ol>
<p>Before they start, students see that leaving is recorded. In practice, that warning does most of the work: most students simply stay.</p>
<p>Two settings in the form matter for this to work: turn off <i>Restrict to users in your organization</i>, and don’t use <i>Collect email addresses: Verified</i>. Both require a sign-in that browsers often block when the form is shown inside another site. The <a href="/supported-quizzes/">supported quizzes page</a> explains why.</p>

<h2>Option 3: Make switching less useful</h2>
<p>Even with no monitoring at all, you can make a quick search much less helpful:</p>
<ul><li><b>Shuffle question order</b> and <b>shuffle option order</b>, so answers can’t be passed around as “number 4 is B”.</li>
<li><b>Release grades later</b>, after everyone has finished, so early finishers can’t share the answer key.</li>
<li><b>Write questions that apply ideas</b> to a new situation, a local example or a graph you made. These are much harder to search than definitions.</li>
<li><b>Use a time limit.</b> Searching every question takes time. QuizPolice can add a timer or schedule the quiz so everyone starts and ends together.</li></ul>
<p>Our guide to <a href="https://telarlabs.net/guides/google-forms-quiz-settings/">Google Forms quiz settings that reduce cheating</a> walks through each setting.</p>

<h2>Which option should you use?</h2>
<table class="tbl"><thead><tr><th>Your classroom</th><th>Best choice</th></tr></thead><tbody>
<tr><td>School-managed Chromebooks and school Google accounts</td><td>Locked mode, plus good question design</td></tr>
<tr><td>Students’ own phones, tablets or laptops</td><td>QuizPolice to see and limit exits, plus shuffling and a time limit</td></tr>
<tr><td>A mix of devices</td><td>QuizPolice for everyone, so all students follow the same rules</td></tr>
<tr><td>Homework quizzes taken at home</td><td>An open period in QuizPolice with a time limit, and lower stakes for the quiz</td></tr></tbody></table>

<h2>What no tool can stop</h2>
<p>No software on one device can see a second phone under the desk, a friend sitting nearby, or notes on paper. Walk around the room, ask for phones not in use to be put away, and talk about honesty before the quiz. A record of exits is a reason to ask a student what happened, not proof that they cheated.</p>

<h2>Quick checklist</h2>
<ol><li>Decide: locked mode (school Chromebooks) or QuizPolice (any device).</li>
<li>Turn on shuffling and release grades later.</li>
<li>Turn off sign-in requirements if you use QuizPolice.</li>
<li>Set a fair time limit.</li>
<li>Tell students what is recorded, and supervise the room.</li></ol>'''),

dict(slug='microsoft-forms-quiz-settings', updated='2026-11-23',
     title='Microsoft Forms Quiz Settings for Tests: A Teacher’s Checklist',
     short='Microsoft Forms quiz settings for tests',
     desc='The Microsoft Forms settings that matter for quizzes and tests: who can respond, start and end dates, shuffling, showing results, and how to monitor students.',
     body='''<p class="lead">Microsoft Forms is free with a Microsoft account and included in most school Microsoft 365 plans. A few settings make a big difference when you use it for a real test.</p>

<h2>1. Start with a Quiz, not a Form</h2>
<p>Choose <b>New Quiz</b> rather than New Form. A quiz lets you mark the correct answer for each question, give points, and add feedback that students see after their results are released. You can still add any question type: choice, text, rating, date and more.</p>

<h2>2. Set points and correct answers</h2>
<ul><li>For each choice question, tick the correct option and set the <b>points</b>.</li>
<li>For text answers, you can add accepted answers for short responses, or grade longer answers yourself in <b>Responses → Review answers</b>.</li>
<li>Add short feedback to tricky questions. It’s a quick way to teach from mistakes once results are shown.</li></ul>

<h2>3. Shuffle the options</h2>
<p>On each choice question, open the <b>…</b> menu on the question and choose <b>Shuffle options</b>. Each student then sees the choices in a different order, so “the answer to number 4 is B” means nothing.</p>

<h2>4. Open the settings</h2>
<p>Open the <b>…</b> menu at the top right of the form and choose <b>Settings</b>. These are the options to check:</p>
<table class="tbl"><thead><tr><th>Setting</th><th>What it does</th><th>Suggestion for tests</th></tr></thead><tbody>
<tr><td><b>Who can fill out this form</b></td><td><i>Only people in my organization</i> requires a school sign-in and can record names. <i>Anyone can respond</i> needs no sign-in.</td><td>Use <i>Anyone can respond</i> if students take it inside QuizPolice, and ask for the name in QuizPolice or as the first question.</td></tr>
<tr><td><b>Start date and End date</b></td><td>The form only accepts responses between these times.</td><td>Set both for a scheduled test, as a backup to your own timing.</td></tr>
<tr><td><b>Shuffle questions</b></td><td>Shows the questions in a different order for each student.</td><td>Turn on, unless questions build on each other. You can keep some fixed if you use sections.</td></tr>
<tr><td><b>Show results automatically</b></td><td>Students see their score and the correct answers right after submitting.</td><td>Turn off for tests, so early finishers can’t share answers. Release results after everyone has finished.</td></tr>
<tr><td><b>Accept responses</b></td><td>Turns the form on or off.</td><td>Turn off as soon as the test ends.</td></tr></tbody></table>
<p>Some options, like recording names or limiting to one response per person, only appear when sign-in is required. Microsoft adds and moves settings from time to time, so if you don’t see one, check the latest Microsoft Forms help for your account type.</p>

<h2>5. Using it inside QuizPolice</h2>
<p>When a form needs a school sign-in, that sign-in often fails inside another site, because browsers block the cookies it needs. So for <a href="/">QuizPolice</a>, set <b>Who can fill out this form</b> to <b>Anyone can respond</b>. Then:</p>
<ol><li>Copy the link from <b>Collect responses</b>.</li>
<li>Create a quiz on the <a href="/teacher/#new">QuizPolice dashboard</a>, paste the link and press <b>Check this link</b>.</li>
<li>Choose the exit limit and timing: anytime, a scheduled exam, or an open period.</li>
<li>Students join with the code, type their name and section, and answer inside QuizPolice. You see who leaves the quiz, live.</li></ol>
<p>Answers still go straight to your Microsoft form, so grading in <b>Responses</b> works exactly as before.</p>

<h2>6. Test it before the class does</h2>
<ul><li>Open the form in a private browser window, not signed in, and answer it once as a student would.</li>
<li>Check that your test response arrives in Responses, then delete it.</li>
<li>Read every question on a phone screen. Long matching tables and small images are hard to read on phones; split them into shorter questions.</li></ul>

<h2>7. After the test</h2>
<ul><li>Turn off <b>Accept responses</b>.</li>
<li>Review open answers in <b>Review answers</b>, then share results with students the way your class usually does.</li>
<li>Download your QuizPolice results (names, sections, exits and time away) for your records, and talk privately with any student whose record raises questions.</li></ul>
<p>More ideas: <a href="https://telarlabs.net/guides/reduce-cheating-online-quizzes/">how to reduce cheating in online quizzes</a>.</p>'''),

dict(slug='online-exam-on-students-phones', updated='2026-11-23',
     title='How to Give an Online Exam on Students’ Phones',
     short='Give an online exam on students’ phones',
     desc='A practical plan for online exams on students’ own phones: preparing the quiz, mobile data and battery, timing, supervision, and what to do when something goes wrong.',
     body='''<p class="lead">In many schools, students’ phones are the only devices every class has. Phones can work well for online exams, as long as you plan for small screens, weak signals and batteries.</p>

<h2>Before exam day</h2>
<h3>Write the exam for a small screen</h3>
<ul><li><b>Keep questions short.</b> One idea per question. Long passages are better on paper or shown on the board.</li>
<li><b>Avoid big tables and grids.</b> Matching grids and wide tables are hard to read and tap on a phone. Split them into separate multiple-choice questions.</li>
<li><b>Make pictures large and clear.</b> Crop diagrams tightly and avoid tiny labels.</li>
<li><b>Use sections.</b> Splitting a long exam into a few pages makes it less tiring to scroll, and students lose less if something goes wrong.</li></ul>

<h3>Check the settings</h3>
<ul><li>Don’t require sign-in if students will take it inside a monitor like QuizPolice. See <a href="/supported-quizzes/">supported quizzes</a> for the exact settings.</li>
<li>Shuffle questions and options, and release scores after everyone has finished.</li>
<li>Try the exam yourself on a low-cost phone, not only on your laptop.</li></ul>

<h3>Tell students what to prepare</h3>
<ul><li>A charged phone, at least 50%, and a charger if there are outlets in the room.</li>
<li>Enough mobile data or a working Wi-Fi connection. A form-based quiz uses little data, but pictures and videos use more.</li>
<li>Other apps closed and notifications silenced. On most phones, Do Not Disturb or Focus mode does this.</li></ul>

<h2>Set up the exam in QuizPolice</h2>
<ol><li>On the <a href="/teacher/#new">teacher dashboard</a>, name the exam and paste the quiz link. Press <b>Check this link</b>.</li>
<li>Choose <b>Scheduled exam</b>, set the start time and length. Students who open the link early wait on a countdown, and everyone starts and ends together.</li>
<li>Choose how many exits are allowed before a student is locked. Three is a fair start for phones, because a notification or a call can pull a student out by accident.</li>
<li>Choose what happens when time runs out. The default gives students 1 more minute to press Submit, and marks late submissions on your dashboard.</li></ol>

<h2>On exam day</h2>
<ul><li><b>Show the code and QR on the board.</b> Students scan or type the 6-digit code, then their name and section.</li>
<li><b>Seat students with space between them</b> if the room allows, and ask for bags and second phones to be put away.</li>
<li><b>Keep your dashboard open</b> on your laptop or phone. You see who is answering, who left the quiz, who is locked and who has submitted.</li>
<li><b>Walk around.</b> The dashboard shows you where to look; your presence does the rest.</li></ul>

<h2>When something goes wrong</h2>
<table class="tbl"><thead><tr><th>Problem</th><th>What to do</th></tr></thead><tbody>
<tr><td>A student’s phone died or the browser closed.</td><td>They join again with the same code and name. They may appear twice on your dashboard, the old entry and the new one, which also shows you what happened. Answers that were never submitted on the form are usually lost, so give extra time if needed with <b>+5 minutes</b>.</td></tr>
<tr><td>A student was locked after a call or notification.</td><td>Ask what happened, then press <b>Unlock</b> on your dashboard if you’re satisfied.</td></tr>
<tr><td>A student’s data or Wi-Fi ran out.</td><td>Let them share a classmate’s hotspot after that classmate has submitted, or use a school device.</td></tr>
<tr><td>Some students were absent or couldn’t finish.</td><td>Use <b>Open make-up quiz</b> on the dashboard for a later time with its own timing.</td></tr>
<tr><td>A student has no phone.</td><td>Lend a school device, pair them with a student who finished, or give a paper copy of the same questions.</td></tr></tbody></table>

<h2>After the exam</h2>
<ul><li>Turn off <b>Accepting responses</b> on the form.</li>
<li>Check the official answers in the form’s own Responses. QuizPolice doesn’t see answers; it records joins, exits, locks and submissions.</li>
<li>Download the QuizPolice results as a CSV for your records.</li>
<li>Talk privately with students whose records raise questions. An exit is a reason to ask, not proof.</li></ul>

<h2>Making it fair for everyone</h2>
<p>Not every student has the same phone or the same data plan. Keep a few school devices or paper copies ready, avoid questions that need fast internet, and don’t let a technical problem lower a student’s score. When students see that the exam is fair to everyone, they are also less tempted to cheat.</p>
<p>See also: <a href="/guides/stop-tab-switching-google-forms/">how to stop students from switching tabs in Google Forms</a>.</p>'''),
dict(slug='how-to-study-for-a-quiz', updated='2026-11-24',
     title='How to Study for a Quiz: 7 Tips That Actually Work',
     short='How to study for a quiz',
     desc='Simple study tips for students: practice remembering, spread out your study time, mix topics, sleep well, and what to do during an online quiz.',
     body='''<p class="lead">Reading your notes again and again feels like studying, but it isn’t the best way to remember. These seven tips work for any subject and any age, and most of them take less time, not more.</p>

<h2>1. Test yourself instead of rereading</h2>
<p>When you read your notes, everything looks familiar, so it feels like you know it. The real test is whether you can bring it back <b>without looking</b>. Close your notebook and try:</p>
<ul><li>Write down everything you remember about the topic on a blank page, then check what you missed.</li>
<li>Cover the answers in your notes or flashcards and say them out loud.</li>
<li>Answer the questions at the end of the chapter, or old quizzes your teacher gave you.</li></ul>
<p>Learning scientists call this <b>retrieval practice</b>. Each time you pull an answer out of your memory, it becomes easier to find again during the quiz.</p>

<h2>2. Study a little on several days</h2>
<p>Three short sessions on three different days beat one long session the night before. If your quiz is on Friday, try 20 minutes on Tuesday, 20 on Wednesday and a quick review on Thursday. Your brain keeps things longer when you come back to them after a break. This is called <b>spaced practice</b>.</p>

<h2>3. Mix different kinds of questions</h2>
<p>If you practice ten questions of the same type in a row, you stop thinking about <i>which</i> method to use. In a real quiz, the questions come mixed. So in math, for example, mix fraction, decimal and percent problems in one practice set. It feels harder, and that’s exactly why it works.</p>

<h2>4. Explain it in your own words</h2>
<p>Try to explain the topic to a friend, a parent, or even to an empty chair, as if you were the teacher. Ask yourself <i>why</i> and <i>how</i>: why does this happen, and how is it connected to what we learned last week? The parts where you get stuck are the parts to study again.</p>

<h2>5. Find your mistakes before the quiz does</h2>
<p>Look at your old quizzes and homework. Which questions did you get wrong, and why? Was it a fact you didn’t know, a step you skipped, or a question you read too fast? Write your three most common mistakes on a sticky note and look at it before the quiz.</p>

<h2>6. Sleep, eat and move</h2>
<p>Your brain saves what you learned while you sleep. Staying up late to cram often makes you remember <b>less</b>. Get a normal night’s sleep, eat something before the quiz, and if you feel nervous, take a few slow breaths: in for four counts, out for six.</p>

<h2>7. Have a plan for the quiz itself</h2>
<ul><li><b>Read every question to the end.</b> Small words like <i>not</i>, <i>always</i> or <i>except</i> change the answer.</li>
<li><b>Do the easy ones first.</b> If you’re stuck, skip it and come back later.</li>
<li><b>Watch the time.</b> Glance at the clock halfway through so you’re not rushing at the end.</li>
<li><b>Check before you submit.</b> Make sure you answered every question.</li></ul>

<h2>Taking a quiz online, on a phone or laptop</h2>
<p>Online quizzes have a few extra things to get right:</p>
<ul><li><b>Charge your device</b> the night before, and bring a charger if you can.</li>
<li><b>Close other apps and tabs</b> before you start, and turn on Do Not Disturb so messages don’t pop up.</li>
<li><b>Stay on the quiz page.</b> Many teachers use a monitor, like <a href="/">QuizPolice</a>, that shows when you leave the quiz. Opening another app, even by accident, can count as leaving.</li>
<li><b>Know what to do if the internet drops.</b> Don’t panic. Reconnect, open the same link and tell your teacher what happened.</li>
<li><b>Press Submit on the quiz itself</b> before you leave. Then make sure you see the confirmation message.</li></ul>

<h2>After the quiz</h2>
<p>When you get your score back, don’t just look at the number. Go through every mistake and find the right answer. That’s free retrieval practice for the next quiz, and the next test will often ask about the same ideas.</p>

<h2>A quick study plan you can copy</h2>
<ol><li><b>3 days before:</b> make flashcards or a list of questions from your notes. Test yourself once.</li>
<li><b>2 days before:</b> test yourself again, mixed order. Study only the ones you missed.</li>
<li><b>1 day before:</b> explain the main ideas out loud. Look at your mistake list. Sleep on time.</li>
<li><b>Quiz day:</b> eat, breathe, read every question to the end, and check before you submit.</li></ol>
<p><i>For teachers:</i> you can share this page with your class before a quiz. See also our guide on <a href="/guides/online-exam-on-students-phones/">giving an online exam on students’ phones</a>.</p>'''),
]
