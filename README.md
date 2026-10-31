# QuizPolice

Free quiz monitoring for Google Forms, Microsoft Forms and Wayground, by Telar Labs.

- `public/teacher/` – teacher dashboard (create quiz, live class list, unlock, CSV)
- `public/join/` – student screen (code + name, quiz shown inside, exit detection)
- `functions/api/[[path]].js` – the API (Cloudflare Pages Function) using a D1 database bound as `DB`; tables are created automatically
- `tools/build.py` – builds the information pages (home, how it works, supported quizzes, FAQ, privacy, terms…)

## Deploy on Cloudflare Pages
1. Storage & databases → D1 → Create database → name `quizpolice`.
2. Workers & Pages → Create → Pages → Import Git repository → `quizpolice`.
   Build command `python3 tools/build.py`, output directory `public`.
3. Project → Settings → Bindings → Add → D1 database: variable name `DB`, database `quizpolice`. Redeploy.

Free-tier note: D1 allows 100,000 writes per day; a 40-student quiz uses a few hundred. Student data is deleted 30 days after a quiz is created.

## Local testing
    npm install
    npm run dev
