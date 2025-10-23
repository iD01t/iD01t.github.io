#!/usr/bin/env python3
import os, re, sys, io
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
TAG = '<script src="/assets/js/landing-enhancer.js"></script>'
def inject(path):
    with io.open(path,"r",encoding="utf-8",errors="ignore") as f: t=f.read()
    if "landing-enhancer.js" in t: return False
    new = re.sub(r"</body\s*>", TAG+"\n</body>", t, flags=re.I)
    if new == t: new = t+"\n"+TAG+"\n"
    with io.open(path,"w",encoding="utf-8") as f: f.write(new); return True
def main():
    n=0
    for sub in ("books","audiobooks",""):
        base = os.path.join(ROOT,sub) if sub else ROOT
        if not os.path.isdir(base): continue
        for dp, dn, files in os.walk(base):
            for fn in files:
                if fn.lower().endswith(".html"):
                    p=os.path.join(dp,fn)
                    if any(x in p.replace("\\","/") for x in ("/.git/","/node_modules/")): continue
                    if inject(p): n+=1; print("Injected:", p)
    print("Done. Files modified:",n)
if __name__=="__main__": main()
