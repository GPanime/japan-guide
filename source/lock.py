"""Password lock for the published page.

build_site.py builds the full page, then lock() turns it into a small password screen holding the page encrypted
(AES-GCM, key from the password with PBKDF2-SHA256, page gzip-compressed first). Typing the password decrypts it in
the browser. "Remember this device" keeps the derived key in the browser's localStorage for 30 days, so the page opens
straight away on that device until then. The password itself is never stored in the page or in the repo.

The password comes from the GUIDE_PASSWORD environment variable, or from source/.guide_password (git-ignored).
This is a casual lock: it keeps the page private from anyone without the password, but the source in the public
GitHub repo (data.py, photos) is still readable there.
"""
import base64, gzip, hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
SALT = b"japan.zhunior.com guide v1"   # fixed, so a remembered device stays unlocked across updates
ITER = 250_000
REMEMBER_DAYS = 30


def password():
    pw = os.environ.get("GUIDE_PASSWORD")
    f = os.path.join(HERE, ".guide_password")
    if not pw and os.path.exists(f):
        pw = open(f).read().strip()
    return pw or None


def _b64(b):
    return base64.b64encode(b).decode()


def lock(html, pw, head_meta):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key = hashlib.pbkdf2_hmac("sha256", pw.encode(), SALT, ITER, dklen=32)
    iv = os.urandom(12)
    ct = AESGCM(key).encrypt(iv, gzip.compress(html.encode(), 9), None)
    return SHELL.replace("__META__", head_meta).replace("__SALT__", _b64(SALT)).replace("__ITER__", str(ITER)) \
        .replace("__IV__", _b64(iv)).replace("__CT__", _b64(ct)).replace("__DAYS__", str(REMEMBER_DAYS))


SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
__META__
<style>
:root { --bg: #FFF8EE; --card: #FFFFFF; --ink: #2B211C; --muted: #7A6A60; --line: #EADBCB; --accent: #D9483B; --field: #FFFDF8; }
@media (prefers-color-scheme: dark) { :root { --bg: #1C1613; --card: #28201C; --ink: #F4E8DA; --muted: #B9A595; --line: #3E3330; --accent: #E8604E; --field: #1F1916; } }
* { box-sizing: border-box; }
html, body { margin: 0; min-height: 100%; background: var(--bg); color: var(--ink); font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
main { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px 16px; }
form { width: 100%; max-width: 360px; background: var(--card); border: 1.5px solid var(--line); border-radius: 20px; padding: 28px 24px; text-align: center; }
.mark { width: 64px; height: 64px; margin: 0 auto 10px; }
h1 { font-size: 22px; margin: 0 0 4px; }
p { margin: 0 0 18px; color: var(--muted); font-size: 14.5px; }
input[type=password] { width: 100%; font-size: 17px; padding: 12px 14px; border-radius: 12px; border: 1.5px solid var(--line); background: var(--field); color: var(--ink); }
input[type=password]:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
label.rem { display: flex; gap: 8px; align-items: center; justify-content: center; margin: 12px 0 16px; font-size: 14px; color: var(--muted); }
button { width: 100%; font-size: 16px; font-weight: 700; padding: 12px; border: 0; border-radius: 12px; background: var(--accent); color: #fff; cursor: pointer; }
button:disabled { opacity: .6; cursor: wait; }
.err { color: var(--accent); font-size: 14px; min-height: 20px; margin: 10px 0 0; }
</style>
</head><body>
<main>
<form id="lock" autocomplete="on">
  <img class="mark" src="favicon.svg" alt="">
  <h1>Japan Trip Guide</h1>
  <p>This guide is private. Enter the password to open it.</p>
  <input type="text" name="username" value="guide" autocomplete="username" hidden>
  <input id="pw" type="password" autocomplete="current-password" placeholder="Password" aria-label="Password" required autofocus>
  <label class="rem"><input id="rem" type="checkbox" checked> Remember this device for __DAYS__ days</label>
  <button id="go" type="submit">Open the guide</button>
  <div class="err" id="err" role="alert"></div>
  <noscript><p class="err">This guide needs JavaScript turned on to open.</p></noscript>
</form>
</main>
<script>
(function () {
  var SALT = "__SALT__", ITER = __ITER__, IV = "__IV__", CT = "__CT__", DAYS = __DAYS__, STORE = "jpguide-key";
  function bytes(b64) { var s = atob(b64), a = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
  function b64(a) { var s = ""; for (var i = 0; i < a.length; i++) s += String.fromCharCode(a[i]); return btoa(s); }
  function saved() { try { var v = JSON.parse(localStorage.getItem(STORE) || "null"); return v && v.until > Date.now() ? v.key : null; } catch (e) { return null; } }
  function save(key) { try { localStorage.setItem(STORE, JSON.stringify({ key: key, until: Date.now() + DAYS * 864e5 })); } catch (e) {} }
  function forget() { try { localStorage.removeItem(STORE); } catch (e) {} }
  async function derive(pw) {
    var base = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveBits"]);
    var bits = await crypto.subtle.deriveBits({ name: "PBKDF2", salt: bytes(SALT), iterations: ITER, hash: "SHA-256" }, base, 256);
    return new Uint8Array(bits);
  }
  async function unlock(raw) {
    var key = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
    var zipped = await crypto.subtle.decrypt({ name: "AES-GCM", iv: bytes(IV) }, key, bytes(CT));
    var html = await new Response(new Blob([zipped]).stream().pipeThrough(new DecompressionStream("gzip"))).text();
    document.open(); document.write(html); document.close();
  }
  var form = document.getElementById("lock"), err = document.getElementById("err"), go = document.getElementById("go"),
      pwin = document.getElementById("pw"), rem = document.getElementById("rem");
  var k = saved();
  if (k) { form.hidden = true; unlock(bytes(k)).catch(function () { forget(); form.hidden = false; }); }
  form.addEventListener("submit", async function (e) {
    e.preventDefault(); err.textContent = ""; go.disabled = true;
    var keep = rem.checked, raw;
    try { raw = await derive(pwin.value); await unlock(raw); }
    catch (x) { err.textContent = "That password didn't work. Try again."; go.disabled = false; return; }
    if (keep) save(b64(raw)); else forget();
  });
})();
</script>
</body></html>
"""
