"""AgentReplay - record every step of an AI agent and replay it in a web page."""
import contextvars, functools, json, sys, time

_events = []
_depth = contextvars.ContextVar("depth", default=0)


def _safe(x):
    try:
        json.dumps(x)
        return x
    except TypeError:
        return repr(x)[:2000]


def step(name=None, **meta):
    """Decorator: records the input, output, error and duration of a function."""
    def deco(fn):
        label = name or fn.__name__

        @functools.wraps(fn)
        def wrapper(*a, **k):
            d = _depth.get()
            tok = _depth.set(d + 1)
            ev = {"name": label, "depth": d, "meta": meta,
                  "input": _safe({"args": list(a), "kwargs": k}), "t0": time.time()}
            _events.append(ev)
            try:
                out = fn(*a, **k)
                ev["output"] = _safe(out)
                return out
            except Exception as e:
                ev["error"] = f"{type(e).__name__}: {e}"
                raise
            finally:
                ev["ms"] = round((time.time() - ev["t0"]) * 1000, 1)
                _depth.reset(tok)
        return wrapper
    return deco


def save(path="run.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_events, f, ensure_ascii=False, indent=2)
    return path


def clear():
    _events.clear()


PAGE = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>AgentReplay</title>
<style>
body{font:15px system-ui;margin:0;background:#0f1115;color:#e6e6e6;padding:16px}
h1{font-size:18px}.c{background:#1a1d24;border-radius:8px;padding:10px 12px;margin:8px 0;border-left:4px solid #4f8cff}
.c.err{border-color:#ff5d5d}.bar{height:4px;background:#4f8cff;border-radius:2px;margin-top:6px}
pre{white-space:pre-wrap;word-break:break-word;font-size:12px;color:#9aa4b2;margin:4px 0}
.m{color:#9aa4b2;font-size:12px}
</style><h1>AgentReplay</h1><div id=app></div>
<script>
const ev=__DATA__;
const mx=Math.max(...ev.map(e=>e.ms||0),1);
const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const j=x=>esc(typeof x==='string'?x:JSON.stringify(x,null,1));
document.getElementById('app').innerHTML=ev.map((e,i)=>
 `<div class="c ${e.error?'err':''}" style="margin-left:${e.depth*18}px">
 <b>#${i+1} ${esc(e.name)}</b> <span class=m>${e.ms} ms</span>
 <pre>in: ${j(e.input)}</pre>
 ${e.error?`<pre style="color:#ff8a8a">error: ${esc(e.error)}</pre>`:`<pre>out: ${j(e.output)}</pre>`}
 <div class=bar style="width:${Math.max(2,(e.ms||0)/mx*100)}%"></div></div>`).join('');
</script>"""


def report(json_path="run.json", html_path="run.html"):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(PAGE.replace("__DATA__", blob))
    return html_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python agentreplay.py run.json [run.html]")
    print(report(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "run.html"))
