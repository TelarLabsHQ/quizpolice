"""Adds <lastmod> to public/sitemap.xml: the date each page last changed, from git (or today if it has changes not yet committed).
Google uses lastmod to decide which pages to recrawl first, so it must be honest: it moves only when a page's file changes.
Shared by all Telar Labs sites; called at the end of each build."""
import os, re, subprocess, datetime

def _changed(root, rel):
    try:
        if subprocess.run(['git', 'status', '--porcelain', '--', rel], cwd=root, capture_output=True, text=True).stdout.strip():
            return datetime.date.today().isoformat()
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', rel], cwd=root, capture_output=True, text=True).stdout.strip()
        return out or datetime.date.today().isoformat()
    except Exception:
        return None

def stamp(public):
    public = os.path.abspath(public); sm = os.path.join(public, 'sitemap.xml')
    if not os.path.exists(sm): return
    root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=public, capture_output=True, text=True).stdout.strip() or public
    xml = re.sub(r'\s*<lastmod>[^<]*</lastmod>', '', open(sm).read())
    def one(m):
        loc = m.group(1); path = re.sub(r'^https?://[^/]+', '', loc) or '/'
        f = os.path.join(public, path.lstrip('/'), 'index.html') if path.endswith('/') else os.path.join(public, path.lstrip('/'))
        if not os.path.exists(f): return m.group(0)
        d = _changed(root, os.path.relpath(f, root))
        return m.group(0) + (f'<lastmod>{d}</lastmod>' if d else '')
    open(sm, 'w').write(re.sub(r'<loc>([^<]+)</loc>', one, xml))

if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]: stamp(p)
