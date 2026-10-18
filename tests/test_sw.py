import os; CHROME=os.environ.get("CHROME") or None  # set CHROME=/path/to/chrome to use system Chrome; default = Playwright Chromium
import shutil,time
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    c=b.new_context(); p=c.new_page(); errs=[]; p.on("pageerror",lambda e:errs.append(str(e)))
    p.goto("http://localhost:8765/index.html"); p.wait_for_function("navigator.serviceWorker.controller!==null",timeout=15000)
    print("SW controlling:",True)
    c.set_offline(True); p.reload(); print("offline load ok:", 'pc-v27' in p.content())
    c.set_offline(False)
    shutil.copy("sw.js","/tmp/pc_sw.bak"); open("sw.js","w").write(open("/tmp/pc_sw.bak").read().replace('var V="','var V="t-'))
    p.reload(); p.wait_for_selector("#upd",state="visible",timeout=20000); print("update prompt shown:",True)
    p.click("#upd"); time.sleep(3); p.wait_for_load_state()
    print("after refresh SW cache:", p.evaluate("caches.keys()"))
    shutil.copy("/tmp/pc_sw.bak","sw.js"); print("errors:",errs); b.close()
