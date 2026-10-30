from collections import Counter
from statistics import mean, median, quantiles

# (source, rent, condo, area, bedrooms, neighborhood, amenities)
qa = [(3300, 839, 110, 3, "Rebouças", ["Mobiliado", "vaga"]), (3500, 840, 24, 1, "Batel", ["Mobiliado", "pets"]),
      (2910, 629, 55, 2, "Pinheirinho", ["Piscina", "pets", "vaga"]), (1700, 460, 50, 1, "Cajuru", ["Mobiliado", "vaga"]),
      (2000, 300, 39, 1, "Cidade Industrial", ["Mobiliado", "vaga"]), (3900, 850, 89, 3, "Mossunguê", ["Mobiliado"]),
      (2600, 423, 40, 1, "Centro", ["Mobiliado", "vaga"]), (2200, 449, 45, 1, "Cajuru", ["Mobiliado", "pets"])]
zap = [(4450, 1168, 65, 1, "Bigorrilho", ["vaga"]), (6000, 750, 98, 2, "Cidade Industrial", ["vaga", "sem fiador"]),
       (3700, 450, 50, 1, "Bigorrilho", ["vaga", "sem fiador"]), (2600, 210, 40, 1, "Boa Vista", ["vaga"]),
       (1690, 800, 41, 2, "Santa Cândida", ["vaga"]), (1400, 480, 48, 2, "Campo de Santana", ["vaga"]),
       (3900, 735, 80, 2, "Centro", ["vaga"]), (1650, 528, 45, 1, "Centro", []), (2400, 460, 96, 3, "Água Verde", ["vaga"]),
       (2400, 500, 66, 3, "Novo Mundo", ["vaga"]), (2800, 500, 66, 3, "Novo Mundo", ["vaga"])]
cnm = [(3900, 700, 138, 3, "Cristo Rei"), (1990, 840, 42, 1, "Mercês"), (2300, 815, 125, 3, "Cristo Rei"),
       (3000, 775, 78, 3, "Cabral"), (1900, 750, 70, 2, "Bacacheri"), (2100, None, 33, 1, "Centro"),
       (12650, None, 200, 4, "Ecoville"), (1390, 500, 46, 2, "Alto Boqueirão"), (7200, 760, 101, 3, "Batel"),
       (7900, 1500, None, 1, "Batel"), (2700, 800, 250, 4, "Sítio Cercado"), (6200, 750, 101, 2, "Juvevê"),
       (2450, 700, 225, 2, "Hauer"), (2250, 200, 30, 1, "Cristo Rei"), (3700, 1000, 148, 3, "Cristo Rei"),
       (3700, 750, 66, 2, "Jardim Botânico"), (2450, 600, 45, 1, "Centro"), (4500, 900, 138, 3, "Guaíra"),
       (2500, 300, 36, 1, "Centro"), (3400, 720, 63, 2, "Centro"), (3800, 900, 150, 3, "Batel"),
       (2890, 440, 75, 2, "Centro"), (1800, 350, 55, 2, "Campo Comprido")]
jba = [(1500, 44, 1, "Centro", []), (2800, 43, 2, "Água Verde", ["vaga"]), (1800, 55, 3, "Uberaba", ["vaga"]),
       (1500, 47, 2, "Sítio Cercado", []), (1550, 45, 2, "Vargem Grande", ["vaga"]), (2900, 45, 2, "Água Verde", ["vaga"]),
       (2000, 67, 2, "Atuba", ["vaga"]), (2200, 52, 2, "Novo Mundo", ["vaga"]), (2300, 42, 2, "Uberaba", ["vaga"]),
       (3600, 75, 2, "Água Verde", ["vaga"])]

rows = [("QA",) + r for r in qa] + [("ZAP",) + r for r in zap] + [("CNM",) + r + ([],) for r in cnm] + \
       [("JBA", r[0], None) + r[1:] for r in jba]

rents = sorted(r[1] for r in rows)
q = quantiles(rents, n=4)
print("n", len(rents), "median", median(rents), "p25", q[0], "p75", q[2], "min", rents[0], "max", rents[-1], "mean", round(mean(rents)))
for s in ["QA", "ZAP", "CNM", "JBA"]:
    print(s, "median rent", median(r[1] for r in rows if r[0] == s))
condos = [r[2] for r in rows if r[2]]
print("condo n", len(condos), "median", median(condos), "p25/p75", quantiles(condos, n=4)[0], quantiles(condos, n=4)[2])
areas = [r[3] for r in rows if r[3]]
print("area median", median(areas))
bd = Counter(min(r[4], 3) for r in rows)
print("bedrooms", {k: f"{v / len(rows):.0%}" for k, v in sorted(bd.items())})
for b in (1, 2, 3):
    print(f"{b}q median rent", median(r[1] for r in rows if min(r[4], 3) == b))
nb = Counter(r[5] for r in rows)
srcs = {n: len({r[0] for r in rows if r[5] == n}) for n in nb}
print("neighborhoods", [(n, c, srcs[n]) for n, c in nb.most_common(8)])
for n in ["Centro", "Água Verde", "Batel", "Cristo Rei", "Bigorrilho"]:
    print(n, "median rent", median(r[1] for r in rows if r[5] == n))
print("amenities", Counter(a for r in rows for a in r[6]).most_common())
