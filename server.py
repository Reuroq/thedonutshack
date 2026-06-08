"""server.py — The Donut Shack: serves the generated site + captures booking/catering leads.
Rebuilds the static site from data on boot. Runtime is fastapi-only."""
import datetime, json, os, re, time
from collections import defaultdict, deque
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import dsdata as D
import sitegen as S
import lead_capture

ROOT = Path(__file__).parent
app = FastAPI(title="The Donut Shack")
app.mount("/static", StaticFiles(directory="static"), name="static")
SEO = (ROOT / "static" / "seo").resolve()
LEADS = ROOT / "data" / "leads.jsonl"
_HITS: dict[str, deque] = defaultdict(deque)


def _ip(r: Request) -> str:
    return (r.headers.get("cf-connecting-ip") or r.headers.get("x-forwarded-for", "").split(",")[0].strip()
            or (r.client.host if r.client else "unknown"))


def _rate_ok(ip, limit=12, window=300):
    now = time.time(); q = _HITS[ip]
    while q and q[0] < now - window:
        q.popleft()
    if len(q) >= limit:
        return False
    q.append(now); return True


@app.middleware("http")
async def _headers(request: Request, call_next):
    resp = await call_next(request)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; "
        "img-src 'self' data: https://www.googletagmanager.com https://www.google-analytics.com; "
        "connect-src 'self' https://www.google-analytics.com https://*.google-analytics.com https://www.googletagmanager.com; "
        "base-uri 'self'; frame-ancestors 'self'")
    return resp


def _seo(rel):
    p = (SEO / rel).resolve()
    if not str(p).startswith(str(SEO)) or not p.exists():
        raise HTTPException(404, "Not found")
    return FileResponse(p)


@app.get("/")
async def home(): return _seo("index.html")

@app.get("/donuts")
async def donuts(): return _seo("donuts.html")

@app.get("/events")
async def events(): return _seo("events.html")

@app.get("/story")
async def story(): return _seo("story.html")

@app.get("/book")
async def book(): return _seo("book.html")


@app.post("/api/book")
async def api_book(request: Request):
    if not _rate_ok(_ip(request)):
        raise HTTPException(429, f"Too many requests — please call {D.PHONE}.")
    cl = request.headers.get("content-length")
    if cl and cl.isdigit() and int(cl) > 8192:
        raise HTTPException(413, "Request too large.")
    try:
        d = await request.json()
    except Exception:
        raise HTTPException(400, "Invalid request.")
    if not isinstance(d, dict):
        raise HTTPException(400, "Invalid request.")

    def clip(k, n=400):
        return str(d.get(k, "") or "").replace("\r", " ").replace("\n", " ").strip()[:n]

    contact = clip("contact", 160)
    lead = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "name": clip("name", 120), "occasion": clip("occasion", 60), "event_date": clip("event_date", 40),
            "headcount": clip("headcount", 40), "area": clip("area", 80), "source": clip("source", 40),
            "message": clip("message", 1500), "ip": _ip(request)[:60]}
    lead["email"] = contact if "@" in contact else ""
    lead["phone"] = "" if "@" in contact else contact
    if not lead["name"] or not contact:
        raise HTTPException(400, "Name and a way to reach you are required.")
    lead_capture.capture("The Donut Shack", lead)
    try:
        LEADS.parent.mkdir(parents=True, exist_ok=True)
        with LEADS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(lead, ensure_ascii=False) + "\n")
    except OSError:
        pass
    return {"ok": True}


@app.get("/sitemap.xml")
async def sitemap(): return FileResponse("static/sitemap.xml", media_type="application/xml")

@app.get("/robots.txt")
async def robots(): return FileResponse("static/robots.txt", media_type="text/plain")

@app.get("/api/health")
async def health(): return {"status": "ok", "app": "The Donut Shack", "flavors": len(D.FLAVORS)}


@app.on_event("startup")
async def _build():
    try:
        S.build()
        print("[startup] The Donut Shack site rebuilt.")
    except Exception as e:
        print(f"[startup] build skipped: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8833")))
