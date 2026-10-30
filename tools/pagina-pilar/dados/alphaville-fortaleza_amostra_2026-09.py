from collections import Counter
from statistics import median

casas = [(2800000, 310, 4, 4), (3800000, 440, 4, 4), (2995000, 330, 4, 4), (2990000, 400, 5, 5), (3900000, 525, 5, 5), (3500000, 408, 4, 4),
         (3100000, 376, 4, 4), (3450000, 365, 4, 4), (3500000, 350, 4, 4), (4100000, 390, 4, 0), (4950000, 290, 3, 3), (5900000, 600, 5, 5),
         (12000000, 600, 5, 5), (5200000, 501, 5, 5), (6000000, 505, 5, 5), (4900000, 430, 5, 5), (5100000, 470, 5, 5), (6000000, 600, 5, 5),
         (3500000, 500, 4, 0), (4000000, 467, 5, 4)]
p = [c[0] for c in casas]
print("n", len(casas), "mediana", median(p))
for a, b, r in [(0, 3e6, "até R$ 3 mi"), (3e6, 4e6, "R$ 3 a 4 mi"), (4e6, 5e6, "R$ 4 a 5 mi"), (5e6, 6e6, "R$ 5 a 6 mi"), (6e6, 1e9, "R$ 6 mi ou mais")]:
    c = sum(a <= v < b for v in p)
    print(r, c, f"{c / len(p):.0%}")
q = Counter(c[2] for c in casas)
print("quartos", {k: f"{v} ({v / len(casas):.0%})" for k, v in sorted(q.items())})
for k in (3, 4, 5):
    v = [c for c in casas if c[2] == k]
    print(f"  {k}q n={len(v)} mediana {median(c[0] for c in v)} área {median(c[1] for c in v)} R$/m² {round(median(c[0] / c[1] for c in v))}")
for a, b, r in [(0, 350, "até 350 m²"), (350, 450, "350 a 450 m²"), (450, 550, "450 a 550 m²"), (550, 9999, "550 m² ou mais")]:
    c = sum(a <= x[1] < b for x in casas)
    print("área", r, c, f"{c / len(casas):.0%}")
