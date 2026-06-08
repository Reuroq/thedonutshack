"""gen.py — generate bakery imagery for The Donut Shack via OpenAI gpt-image-2.
Usage: python design/gen.py <out.png> "<prompt>" [size]   (size default 1536x1024)
"""
import base64, json, os, sys, urllib.request


def _key():
    for p in (r"C:\Users\dwayn\OneDrive\Desktop\WorkShield\.env",):
        try:
            for line in open(p, encoding="utf-8"):
                if line.strip().startswith("OPENAI_API_KEY"):
                    return line.split("=", 1)[1].strip().strip('"')
        except FileNotFoundError:
            pass
    return os.environ.get("OPENAI_API_KEY", "")


def gen(out, prompt, size="1536x1024"):
    body = json.dumps({"model": "gpt-image-2", "prompt": prompt, "size": size, "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
                                 headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        d = json.loads(r.read())
    png = base64.b64decode(d["data"][0]["b64_json"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(png)
    print(f"wrote {out} ({len(png)} bytes)")


if __name__ == "__main__":
    gen(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "1536x1024")
