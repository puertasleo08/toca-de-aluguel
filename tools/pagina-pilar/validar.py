import json
import re
import sys
from collections import Counter
from pathlib import Path

s = (Path(__file__).resolve().parents[2] / sys.argv[1]).read_text(encoding="utf-8")
tags = {t: (len(re.findall(rf"<{t}\b", s)), len(re.findall(rf"</{t}\s*>", s)))
        for t in ("div", "section", "article", "ul", "ol", "li", "nav", "dl", "button", "a", "p", "h2", "h3", "table", "svg", "iframe", "figure", "script")}
print("tags desbalanceadas:", {k: v for k, v in tags.items() if v[0] != v[1]} or "nenhuma")
levels = [int(l) for l in re.findall(r"<h([1-6])\b", s)]
print("H1:", levels.count(1), "| saltos de heading:", [(a, b) for a, b in zip(levels, levels[1:]) if b > a + 1] or "nenhum")
print("ids duplicados:", [k for k, v in Counter(re.findall(r'\sid="([^"]+)"', s)).items() if v > 1] or "nenhum")
ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
print("JSON-LD:", [g["@type"] for g in ld["@graph"]])
faq = next(g for g in ld["@graph"] if g["@type"] == "FAQPage")["mainEntity"]
vis = re.findall(r"<summary[^>]*>\s*(.*?)\s*<svg.*?</summary>\s*<p[^>]*>\s*(.*?)\s*</p>", s, re.S)
print("FAQ visível == schema:", len(vis) == len(faq) and all(
    re.sub(r"\s+", " ", q).strip() == f["name"] and re.sub(r"\s+", " ", a).strip() == f["acceptedAnswer"]["text"] for (q, a), f in zip(vis, faq)), len(vis))
corpo = s[s.index("<main"):s.index("</main>")]
ids_h2 = re.findall(r'<h2[^>]*?\s+id="([^"]+)"', corpo.replace("\n", " "))
print("ordem H2:", " > ".join(i.replace("-heading", "") for i in ids_h2))
hrefs, ids = set(re.findall(r'href="#([^"]+)"', s)), set(re.findall(r'\sid="([^"]+)"', s))
print("âncoras quebradas:", sorted(hrefs - ids) or "nenhuma")
imgs = re.findall(r"<img\b[^>]*>", s, re.S)
print("imgs sem width/height/alt:", sum(not all(a in i for a in ("width=", "height=", 'alt="')) for i in imgs))
print("cards:", s.count("data-quartos="), "| botões de filtro:", s.count("data-filtro-grupo="), "| links de bairro p/ mapa:", len(re.findall(r'<a href="#mapa-cidade" data-mapa=', s)),
      "| botões do mapa:", len(re.findall(r'<button type="button" data-mapa="[^"]+"[^>]*aria-pressed', s)), "| CTAs WhatsApp com pulso:", s.count("animate-[brilho-whatsapp"))
