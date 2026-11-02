// QuizPolice API — Cloudflare Pages Function with a D1 database bound as `DB`.
// Teachers are identified by a secret teacher key saved in their browser (no accounts).
// Students get a participant token when they join. Data is deleted 30 days after a quiz is created.

const SCHEMA = [
  `CREATE TABLE IF NOT EXISTS sessions (code TEXT PRIMARY KEY, teacher_key TEXT NOT NULL, title TEXT NOT NULL, quiz_url TEXT NOT NULL,
     embed_url TEXT NOT NULL, platform TEXT, sections TEXT, max_exits INTEGER NOT NULL DEFAULT 3, strict INTEGER NOT NULL DEFAULT 1,
     created_at INTEGER NOT NULL, closed INTEGER NOT NULL DEFAULT 0)`,
  `CREATE TABLE IF NOT EXISTS participants (id TEXT PRIMARY KEY, code TEXT NOT NULL, token TEXT NOT NULL, name TEXT NOT NULL, section TEXT,
     status TEXT NOT NULL DEFAULT 'ans', exits INTEGER NOT NULL DEFAULT 0, away_ms INTEGER NOT NULL DEFAULT 0, left_at INTEGER,
     last_seen INTEGER NOT NULL, joined_at INTEGER NOT NULL)`,
  `CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT NOT NULL, participant_id TEXT NOT NULL,
     kind TEXT NOT NULL, detail TEXT, at INTEGER NOT NULL)`,
  `CREATE INDEX IF NOT EXISTS idx_part_code ON participants(code)`,
  `CREATE INDEX IF NOT EXISTS idx_ev_code ON events(code, id)`,
];
// Columns added later (timers and schedules); added to older databases automatically.
const ADD = {
  sessions: { timing: "TEXT NOT NULL DEFAULT 'any'", start_at: 'INTEGER', end_at: 'INTEGER', limit_min: 'INTEGER NOT NULL DEFAULT 0', stop_at: 'INTEGER' },
  participants: { extra_ms: 'INTEGER NOT NULL DEFAULT 0' },
};
let ready = false;
async function ensure(db) {
  if (ready) return;
  await db.batch(SCHEMA.map(s => db.prepare(s)));
  for (const [t, cols] of Object.entries(ADD)) {
    const have = new Set((await db.prepare(`PRAGMA table_info(${t})`).all()).results.map(r => r.name));
    for (const [c, def] of Object.entries(cols)) if (!have.has(c)) await db.prepare(`ALTER TABLE ${t} ADD COLUMN ${c} ${def}`).run();
  }
  ready = true;
}

// ---------- timing ----------
// any: join any time, optional time limit from when the student starts.
// scheduled: everyone together; starts at start_at, ends at start_at + limit_min (late joiners get the time that is left).
// window: students may start between start_at and end_at; optional per-student limit, never past end_at.
// stop_at: the teacher pressed "End for everyone". extra_ms: extra time the teacher gave one student.
const MIN = 60000;
function deadlineOf(s, p) {
  const lim = (s.limit_min || 0) * MIN;
  let d = null;
  if (s.timing === 'scheduled') d = s.start_at && lim ? s.start_at + lim : null;
  else if (s.timing === 'window') { d = s.end_at || null; if (lim && p) d = d ? Math.min(d, p.joined_at + lim) : p.joined_at + lim; }
  else if (lim && p) d = p.joined_at + lim;
  if (s.stop_at) d = d == null ? s.stop_at : Math.min(d, s.stop_at);
  if (d != null && p) d += p.extra_ms || 0;
  return d;
}
function joinBlock(s, t) {
  if (s.closed) return 'This quiz is closed.';
  if (s.stop_at && t >= s.stop_at) return 'This quiz has ended.';
  if (s.timing === 'scheduled' && s.start_at && t >= s.start_at + (s.limit_min || 0) * MIN) return 'This exam has already ended.';
  if (s.timing === 'window') {
    if (s.start_at && t < s.start_at) return 'not_open';
    if (s.end_at && t >= s.end_at) return 'This quiz is no longer open.';
  }
  return null;
}
const timingPub = s => ({ timing: s.timing || 'any', start_at: s.start_at, end_at: s.end_at, limit_min: s.limit_min || 0, stop_at: s.stop_at });
async function timeup(db, s, p) {
  const d = deadlineOf(s, p), t = now();
  if (d == null || t < d || !['ans', 'away', 'lock'].includes(p.status)) return p;
  const gone = p.status === 'away' && p.left_at ? Math.max(0, Math.min(t, d) - p.left_at) : 0;
  const r = await db.prepare("UPDATE participants SET status = 'time', away_ms = away_ms + ? WHERE id = ? AND status IN ('ans','away','lock')").bind(gone, p.id).run();
  if (r.meta.changes) await (await log(db, p, 'timeup', "Time's up")).run();
  return { ...p, status: 'time', away_ms: p.away_ms + gone };
}
function stuPayload(s, p) {
  return { status: p.status, exits: p.exits, max_exits: s.max_exits, strict: !!s.strict, closed: !!s.closed, embed_url: s.embed_url, title: s.title,
    name: p.name, joined_at: p.joined_at, deadline: deadlineOf(s, p), server_time: now(), ...timingPub(s) };
}
function readTiming(body) {
  const timing = ['any', 'scheduled', 'window'].includes(body.timing) ? body.timing : 'any';
  const lim = Math.min(600, Math.max(0, parseInt(body.limit_min) || 0));
  const st = parseInt(body.start_at) || null, en = parseInt(body.end_at) || null;
  if (timing === 'scheduled') {
    if (!st) return { error: 'Please choose the date and time the exam starts.' };
    if (!lim) return { error: 'Please choose how long the exam lasts.' };
    return { timing, start_at: st, end_at: st + lim * MIN, limit_min: lim };
  }
  if (timing === 'window') {
    if (!st || !en) return { error: 'Please choose when the quiz opens and when it closes.' };
    if (en <= st) return { error: 'The closing time must be after the opening time.' };
    return { timing, start_at: st, end_at: en, limit_min: lim };
  }
  return { timing, start_at: null, end_at: null, limit_min: lim };
}

const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
const bad = (msg, status = 400) => json({ error: msg }, status);
const rid = (n = 24) => { const a = new Uint8Array(n); crypto.getRandomValues(a); return [...a].map(b => (b % 36).toString(36)).join(''); };
const clean = (s, max) => String(s ?? '').replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, max);
const now = () => Date.now();
const DAY = 86400000;

// Turn a quiz link into something that can be shown inside QuizPolice.
export function toEmbed(raw) {
  let u; try { u = new URL(raw.trim()); } catch { return null; }
  if (u.protocol !== 'https:') return null;
  const h = u.hostname.toLowerCase();
  if (h === 'docs.google.com' && u.pathname.includes('/forms/')) {
    u.pathname = u.pathname.replace(/\/(edit|viewform|formResponse|prefill)?\/?$/, '/viewform');
    u.searchParams.set('embedded', 'true');
    return { platform: 'Google Forms', embed: u.toString() };
  }
  if (h === 'forms.gle') return { platform: 'Google Forms (short link)', embed: u.toString(), resolve: true };
  if (h.endsWith('forms.office.com') || h === 'forms.microsoft.com' || h.endsWith('forms.cloud.microsoft')) {
    u.searchParams.set('embed', 'true');
    return { platform: 'Microsoft Forms', embed: u.toString() };
  }
  if (h.endsWith('wayground.com') || h.endsWith('quizizz.com')) return { platform: 'Wayground', embed: u.toString() };
  return { platform: 'Other', embed: u.toString() };
}

async function checkFrame(url) {
  // Follows redirects and reports whether the page allows being shown in a frame.
  try {
    const r = await fetch(url, { redirect: 'follow', headers: { 'user-agent': 'Mozilla/5.0 QuizPolice link check' } });
    const xfo = (r.headers.get('x-frame-options') || '').toLowerCase();
    const csp = (r.headers.get('content-security-policy') || '').toLowerCase();
    const fa = /frame-ancestors([^;]*)/.exec(csp);
    let blocked = xfo.includes('deny') || xfo.includes('sameorigin');
    if (fa && !/\*|https:/.test(fa[1])) blocked = true;
    const signin = /accounts\.google\.com|login\.microsoftonline\.com/.test(r.url);
    return { ok: r.ok, final: r.url, blocked, signin };
  } catch (e) { return { ok: false, error: 'Could not open the link' }; }
}

async function getSession(db, code) {
  return db.prepare('SELECT * FROM sessions WHERE code = ?').bind(code).first();
}
async function teacherSession(db, code, key) {
  const s = await getSession(db, code);
  if (!s || s.teacher_key !== key) return null;
  return s;
}
async function participant(db, token) {
  return db.prepare('SELECT * FROM participants WHERE token = ?').bind(token).first();
}
async function log(db, p, kind, detail = '') {
  return db.prepare('INSERT INTO events (code, participant_id, kind, detail, at) VALUES (?,?,?,?,?)').bind(p.code, p.id, kind, detail, now());
}

export async function onRequest(ctx) {
  const { request, env } = ctx;
  const db = env.DB;
  if (!db) return bad('Database is not connected yet (add a D1 binding named DB in Cloudflare Pages settings).', 503);
  await ensure(db);
  const url = new URL(request.url);
  const parts = url.pathname.replace(/^\/api\/?/, '').split('/').filter(Boolean);
  const method = request.method;
  let body = {};
  if (method === 'POST') { try { body = await request.json(); } catch { body = {}; } }

  try {
    // ---------- teacher ----------
    if (method === 'POST' && parts[0] === 'check-link') {
      const e = toEmbed(clean(body.url, 2000));
      if (!e) return bad('Please paste a full https:// link to your quiz.');
      const c = await checkFrame(e.embed);
      let embed = e.embed;
      if (e.resolve && c.final) { const e2 = toEmbed(c.final); if (e2) embed = e2.embed; }
      return json({ platform: e.platform, embed, ...c });
    }
    if (method === 'POST' && parts[0] === 'sessions' && parts.length === 1) {
      const title = clean(body.title, 120), quiz = clean(body.quiz_url, 2000);
      const e = toEmbed(quiz);
      if (!title) return bad('Please give your quiz a name.');
      if (!e) return bad('Please paste a full https:// link to your quiz.');
      const embed = clean(body.embed_url, 2000) || e.embed;
      const sections = (Array.isArray(body.sections) ? body.sections : []).map(s => clean(s, 60)).filter(Boolean).slice(0, 30);
      const maxExits = Math.min(20, Math.max(1, parseInt(body.max_exits) || 3));
      const strict = body.strict ? 1 : 0;
      const tm = readTiming(body);
      if (tm.error) return bad(tm.error);
      await db.prepare('DELETE FROM events WHERE code IN (SELECT code FROM sessions WHERE created_at < ?)').bind(now() - 30 * DAY).run();
      await db.prepare('DELETE FROM participants WHERE code IN (SELECT code FROM sessions WHERE created_at < ?)').bind(now() - 30 * DAY).run();
      await db.prepare('DELETE FROM sessions WHERE created_at < ?').bind(now() - 30 * DAY).run();
      let code;
      for (let i = 0; i < 8; i++) {
        code = String(100000 + (crypto.getRandomValues(new Uint32Array(1))[0] % 900000));
        if (!(await getSession(db, code))) break;
      }
      const key = rid(32);
      await db.prepare('INSERT INTO sessions (code, teacher_key, title, quiz_url, embed_url, platform, sections, max_exits, strict, created_at, timing, start_at, end_at, limit_min) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
        .bind(code, key, title, quiz, embed, e.platform, JSON.stringify(sections), maxExits, strict, now(), tm.timing, tm.start_at, tm.end_at, tm.limit_min).run();
      return json({ code, teacher_key: key });
    }
    if (parts[0] === 'sessions' && parts[1]) {
      const code = parts[1];
      const key = request.headers.get('x-teacher-key') || '';
      const s = await teacherSession(db, code, key);
      if (!s) return bad('Quiz not found, or this browser is not the teacher of this quiz.', 404);
      if (method === 'GET' && parts[2] === 'dashboard') {
        const since = parseInt(url.searchParams.get('since')) || 0;
        let ps = (await db.prepare('SELECT id, name, section, status, exits, away_ms, left_at, last_seen, joined_at, extra_ms FROM participants WHERE code = ? ORDER BY joined_at').bind(code).all()).results;
        ps = await Promise.all(ps.map(async p => { const q = await timeup(db, s, { ...p, code }); return { ...q, deadline: deadlineOf(s, q) }; }));
        const evs = (await db.prepare('SELECT id, participant_id, kind, detail, at FROM events WHERE code = ? AND id > ? ORDER BY id DESC LIMIT 300').bind(code, since).all()).results;
        s.deadline = deadlineOf(s, null);
        const { teacher_key, ...pub } = s;
        return json({ session: { ...pub, sections: JSON.parse(s.sections || '[]') }, participants: ps, events: evs, server_time: now() });
      }
      if (method === 'POST' && parts[2] === 'settings') {
        const maxExits = Math.min(20, Math.max(1, parseInt(body.max_exits) || s.max_exits));
        const strict = body.strict === undefined ? s.strict : (body.strict ? 1 : 0);
        const closed = body.closed === undefined ? s.closed : (body.closed ? 1 : 0);
        await db.prepare('UPDATE sessions SET max_exits = ?, strict = ?, closed = ? WHERE code = ?').bind(maxExits, strict, closed, code).run();
        if (body.start_now && s.timing === 'scheduled') { const t = now(); await db.prepare('UPDATE sessions SET start_at = ?, end_at = ? WHERE code = ?').bind(t, t + (s.limit_min || 0) * MIN, code).run(); }
        if (body.end_now) await db.prepare('UPDATE sessions SET stop_at = ? WHERE code = ?').bind(now(), code).run();
        if (body.undo_end) await db.prepare('UPDATE sessions SET stop_at = NULL WHERE code = ?').bind(code).run();
        return json({ ok: true });
      }
      if (method === 'POST' && parts[2] === 'unlock' && parts[3]) {
        const p = await db.prepare('SELECT * FROM participants WHERE id = ? AND code = ?').bind(parts[3], code).first();
        if (!p) return bad('Student not found', 404);
        await db.batch([db.prepare("UPDATE participants SET status = 'ans', exits = 0 WHERE id = ?").bind(p.id), await log(db, p, 'unlock', 'Unlocked by teacher')]);
        return json({ ok: true });
      }
      if (method === 'POST' && parts[2] === 'extra' && parts[3]) {
        const p = await db.prepare('SELECT * FROM participants WHERE id = ? AND code = ?').bind(parts[3], code).first();
        if (!p) return bad('Student not found', 404);
        const m = Math.min(120, Math.max(1, parseInt(body.min) || 5));
        let add = m * MIN;
        // if time already ran out, count the extra minutes from now
        const d = deadlineOf(s, p); if (d != null && d < now()) add += now() - d;
        await db.batch([db.prepare("UPDATE participants SET extra_ms = extra_ms + ?, status = CASE WHEN status = 'time' THEN 'ans' ELSE status END WHERE id = ?").bind(add, p.id),
          await log(db, p, 'extra', `Given ${m} more minute${m > 1 ? 's' : ''}`)]);
        return json({ ok: true });
      }
      if (method === 'POST' && parts[2] === 'delete') {
        await db.batch([db.prepare('DELETE FROM events WHERE code = ?').bind(code), db.prepare('DELETE FROM participants WHERE code = ?').bind(code), db.prepare('DELETE FROM sessions WHERE code = ?').bind(code)]);
        return json({ ok: true });
      }
    }

    // ---------- student ----------
    if (method === 'GET' && parts[0] === 'quiz' && parts[1]) {
      const s = await getSession(db, parts[1]);
      if (!s) return bad('No quiz with that code. Check the code with your teacher.', 404);
      return json({ code: s.code, title: s.title, platform: s.platform, sections: JSON.parse(s.sections || '[]'), max_exits: s.max_exits, strict: !!s.strict, closed: !!s.closed,
        ...timingPub(s), block: joinBlock(s, now()), server_time: now() });
    }
    if (method === 'POST' && parts[0] === 'join') {
      const s = await getSession(db, clean(body.code, 10));
      if (!s) return bad('No quiz with that code. Check the code with your teacher.', 404);
      const blk = joinBlock(s, now());
      if (blk) return bad(blk === 'not_open' ? 'This quiz is not open yet.' : blk, 403);
      const name = clean(body.name, 80), section = clean(body.section, 60);
      if (!name) return bad('Please type your name.');
      const p = { id: rid(12), code: s.code, token: rid(32) };
      await db.batch([
        db.prepare('INSERT INTO participants (id, code, token, name, section, last_seen, joined_at) VALUES (?,?,?,?,?,?,?)').bind(p.id, s.code, p.token, name, section, now(), now()),
        await log(db, p, 'join', section ? `Joined (${section})` : 'Joined'),
      ]);
      const np = await participant(db, p.token);
      return json({ token: p.token, ...stuPayload(s, np) });
    }
    if (parts[0] === 'me') {
      const token = request.headers.get('x-student-token') || '';
      let p = await participant(db, token);
      if (!p) return bad('Please join the quiz again.', 401);
      const s = await getSession(db, p.code);
      if (!s) return bad('This quiz was deleted.', 404);
      p = await timeup(db, s, p);
      if (method === 'GET') {
        await db.prepare('UPDATE participants SET last_seen = ? WHERE id = ?').bind(now(), p.id).run();
        return json(stuPayload(s, p));
      }
      if (method === 'POST' && parts[1] === 'event') {
        const kind = body.kind, t = now();
        if (kind === 'leave' && p.status === 'ans' && s.timing === 'scheduled' && s.start_at && now() < s.start_at) return json({ status: p.status, exits: p.exits, deadline: deadlineOf(s, p) });
        if (kind === 'leave' && p.status === 'ans') {
          const exits = p.exits + 1;
          const r = await db.prepare("UPDATE participants SET status = 'away', exits = ?, left_at = ?, last_seen = ? WHERE id = ? AND status = 'ans'").bind(exits, t, t, p.id).run();
          if (r.meta.changes) { await (await log(db, p, 'leave', `Left the quiz (exit ${exits})${body.how ? ' – ' + clean(body.how, 40) : ''}`)).run(); return json({ status: 'away', exits, deadline: deadlineOf(s, p) }); }
          const cur = await participant(db, token); return json({ status: cur.status, exits: cur.exits });
        }
        if (kind === 'back' && p.status === 'away') {
          const gone = Math.max(0, t - (p.left_at || t));
          const lock = s.strict && p.exits >= s.max_exits;
          const st = lock ? 'lock' : 'ans';
          const r = await db.prepare("UPDATE participants SET status = ?, away_ms = away_ms + ?, last_seen = ? WHERE id = ? AND status = 'away'").bind(st, gone, t, p.id).run();
          if (r.meta.changes) {
            const stmts = [await log(db, p, 'back', `Came back after ${Math.round(gone / 1000)}s`)];
            if (lock) stmts.push(await log(db, p, 'lock', 'Locked: reached the exit limit'));
            await db.batch(stmts);
            return json({ status: st, exits: p.exits, away_s: Math.round(gone / 1000) });
          }
          const cur = await participant(db, token); return json({ status: cur.status, exits: cur.exits });
        }
        if (kind === 'done' && p.status !== 'done') {
          // finishing also closes an open "away" period so time away stays correct
          const gone = p.status === 'away' && p.left_at ? Math.max(0, t - p.left_at) : 0;
          await db.batch([db.prepare("UPDATE participants SET status = 'done', away_ms = away_ms + ?, last_seen = ? WHERE id = ?").bind(gone, t, p.id), await log(db, p, 'done', 'Marked as submitted')]);
          return json({ status: 'done', exits: p.exits });
        }
        return json({ status: p.status, exits: p.exits, deadline: deadlineOf(s, p) });
      }
    }
    return bad('Not found', 404);
  } catch (err) {
    return bad('Something went wrong. Please try again.', 500);
  }
}
