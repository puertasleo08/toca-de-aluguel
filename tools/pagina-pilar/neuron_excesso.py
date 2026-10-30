"""Lista termos do NeuronWriter usados acima da faixa recomendada no _nw_payload.html.
Uso: python neuron_excesso.py <nw_json>"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
d = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
texto = re.sub(r"<[^>]+>", " ", (RAIZ / "_nw_payload.html").read_text(encoding="utf-8")).lower()
texto = re.sub(r"\s+", " ", texto)
for t in d["terms"]["content_basic"] + d["terms"].get("content_extended", []):
    faixa = t.get("sugg_usage") or [1, 1]
    n = len(re.findall(r"(?<![\wà-ú])" + re.escape(t["t"].lower()) + r"(?![\wà-ú])", texto))
    if n > faixa[1]:
        print(f"{t['t']:<35} tem {n:>3}  (faixa {faixa[0]}–{faixa[1]})")
