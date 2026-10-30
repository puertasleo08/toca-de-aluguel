import html as H
import json
import re
import sys
from pathlib import Path

arquivo, nw_arq = sys.argv[1], sys.argv[2]
s = (Path(__file__).resolve().parents[2] / arquivo).read_text(encoding="utf-8")
art = s[s.index('<article class="min-w-0'):s.index('<aside class="lateral')]
art = re.sub(r"<svg\b.*?</svg>", "", art, flags=re.S)
art = re.sub(r"<iframe\b.*?</iframe>", "", art, flags=re.S)
art = re.sub(r"<img\b[^>]*?alt=\"([^\"]*)\"[^>]*>", r'<img alt="\1">', art, flags=re.S)
art = re.sub(r"<a\b[^>]*?href=\"([^\"]*)\"[^>]*>", lambda m: '<a href="#">' if m.group(1).startswith("http") else f'<a href="{m.group(1)}">', art, flags=re.S)
art = re.sub(r"<(?!img|a\b)(\w+)\b[^>]*>", r"<\1>", art)
art = re.sub(r"</?(span|div|button|dl|nav|figure|figcaption|header|details|summary)\s*>", " ", art)
art = re.sub(r"<dt>|<dd>", " ", art).replace("</dt>", ":").replace("</dd>", ".")
art = re.sub(r"</a\s*>", "</a>", art)
art = re.sub(r"\s+", " ", art)
title = re.search(r"<title>(.*?)</title>", s).group(1)
desc = re.search(r'name="description"\s*content="([^"]+)"', s).group(1)
(Path(__file__).resolve().parents[2] / "_nw_payload.html").write_text(art, encoding="utf-8")
print("TITLE:", title, len(title))
print("DESC:", desc, len(desc))
print("palavras:", len(H.unescape(re.sub(r"<[^>]+>", " ", art)).split()))

d = json.load(open(nw_arq, encoding="utf-8"))
print("meta NW:", d["metrics"])
texto = " " + re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", art))).lower() + " "
h2s = " | ".join(x.lower() for x in re.findall(r"<h2>(.*?)</h2>", art))
h1 = re.search(r"<h1>(.*?)</h1>", art).group(1).lower()


def conta(t, alvo):
    return len(re.findall(r"(?<![\wà-ú])" + re.escape(t) + r"(?![\wà-ú])", alvo))


print("== conteúdo: faltando (0) ou abaixo do mínimo")
for linha in (d["terms_txt"]["content_basic_w_ranges"] + "\n" + d["terms_txt"]["content_extended_w_ranges"]).splitlines():
    termo, faixa = linha.rsplit(":", 1)
    lo = int(faixa.strip().rstrip("x").split("-")[0])
    n = conta(termo.strip(), texto)
    if n < lo:
        print(f"  {termo.strip():42} tem {n}  (mín {lo})")
for nome, lista, alvo in [("title", "title", title.lower()), ("desc", "desc_title", desc.lower()), ("h1", "h1", h1)]:
    print(f"== {nome} faltando:", [t for t in d["terms_txt"][lista].splitlines() if conta(t, alvo) == 0])
print("== h2 (top 30) faltando:", [t for t in d["terms_txt"]["h2"].splitlines()[:30] if conta(t, h2s) == 0])
