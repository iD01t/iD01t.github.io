#!/usr/bin/env python3
"""
CSV -> JSON converter for iD01t eBooks catalog.
Headers: title, price_cad, pages, image, url, preview_url, tags, date, description
Usage: python tools/csv_to_json.py input.csv assets/data/ebooks.json
"""
import csv, json, sys, os
def norm_header(s): return s.strip().lower().replace(" ", "_")
def to_number(v):
    try: return float(v)
    except Exception: return None
def main():
    if len(sys.argv)<3:
        print("Usage: csv_to_json.py input.csv output.json"); sys.exit(1)
    inp,outp=sys.argv[1],sys.argv[2]; rows=[]
    with open(inp, newline='', encoding='utf-8') as f:
        rdr=csv.DictReader(f)
        for row in rdr:
            r={norm_header(k):(v.strip() if isinstance(v,str) else v) for k,v in row.items()}
            item={"title":r.get("title",""),
                  "price_cad":to_number(r.get("price_cad","") or r.get("price","")),
                  "pages":int(float(r.get("pages","0") or 0)) if (r.get("pages") or "").strip() else None,
                  "image":r.get("image",""),"url":r.get("url",""),"preview_url":r.get("preview_url",""),
                  "tags":[t.strip() for t in (r.get("tags","").split(",") if r.get("tags") else []) if t.strip()],
                  "date":r.get("date",""),"description":r.get("description","")}
            rows.append(item)
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    with open(outp,"w",encoding="utf-8") as f: json.dump(rows,f,ensure_ascii=False,indent=2)
    print(f"Wrote {len(rows)} items to {outp}")
if __name__=="__main__": main()
