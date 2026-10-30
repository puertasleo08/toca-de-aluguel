from collections import Counter
from statistics import median

iw = [
    (4100000, "Leblon", 229, 3, 2493, ["piscina", "churrasqueira", "segurança 24h"]),
    (1625000, "Recreio dos Bandeirantes", 326, 5, 1700, ["jardim", "churrasqueira"]),
    (2720000, "Jardim Oceânico", 232, 3, 0, ["varanda", "churrasqueira"]),
    (1360000, "Barra Olímpica", 160, 3, 2300, ["portaria 24 horas", "churrasqueira", "piscina"]),
    (5076893, "Botafogo", 250, 3, 3062, ["academia", "piscina"]),
    (2300000, "Barra da Tijuca", 251, 3, 3150, ["varanda gourmet", "segurança 24 horas"]),
    (2675000, "Barra da Tijuca", 267, 3, 2153, ["piscina", "churrasqueira"]),
    (1936000, "Barra da Tijuca", 146, 3, 100, ["piscina", "churrasqueira"]),
    (1050000, "Olaria", 520, 3, 0, ["permite animais"]),
    (2650000, "Humaitá", 138, 3, 1950, ["varanda"]),
    (1550000, "Vila Isabel", 485, 5, 3294, ["churrasqueira", "piscina"]),
    (1350000, "Recreio dos Bandeirantes", 213, 2, 980, ["piscina", "terraço"]),
    (2600000, "Jardim Oceânico", 330, 3, 1900, ["piscina", "churrasqueira"]),
    (390000, "Engenho Novo", 127, 2, 780, ["varanda"]),
    (3500000, "Barra da Tijuca", 325, 5, 4000, ["churrasqueira", "piscina"]),
    (1469000, "Recreio dos Bandeirantes", 400, 4, 1700, ["churrasqueira"]),
    (2000000, "Recreio dos Bandeirantes", 201, 3, 590, ["piscina", "sauna"]),
]
zap_raw = [(35000000, 290, 3, 7500), (7650000, 489, 3, 2100), (11000000, 174, 3, 4844), (3300000, 176, 2, 4300), (4500000, 140, 2, 2000),
           (4500000, 228, 3, 3525), (2450000, 135, 3, 3400), (3325000, 166, 4, 3800), (6900000, 264, 4, 2500), (3600000, 176, 6, 2800),
           (3000000, 141, 2, 3076), (5400000, 189, 2, 2500), (3750000, 162, 2, 4400), (4500000, 140, 2, 2000), (4500000, 139, 2, 2500),
           (6000000, 178, 3, 1548), (3200000, 271, 3, 2800), (6000000, 178, 3, 1548), (3000000, 141, 2, 3076), (4200000, 194, 2, 2200)]
zap = list(dict.fromkeys(zap_raw))
print("cidade n", len(iw), "mediana", median(x[0] for x in iw), "| leblon n", len(zap), "mediana", median(x[0] for x in zap))
for nome, dados, faixas in [("cidade", [x[0] for x in iw], [(0, 1e6, "até R$ 1 mi"), (1e6, 2e6, "R$ 1 a 2 mi"), (2e6, 3e6, "R$ 2 a 3 mi"), (3e6, 5e6, "R$ 3 a 5 mi"), (5e6, 1e9, "acima de R$ 5 mi")]),
                            ("leblon", [x[0] for x in zap], [(0, 3e6, "até R$ 3 mi"), (3e6, 4e6, "R$ 3 a 4 mi"), (4e6, 5e6, "R$ 4 a 5 mi"), (5e6, 7e6, "R$ 5 a 7 mi"), (7e6, 1e9, "acima de R$ 7 mi")])]:
    for a, b, r in faixas:
        c = sum(a <= v < b for v in dados)
        print(nome, r, c, f"{c / len(dados):.0%}")
q = Counter(min(x[3], 4) for x in iw)
print("quartos cidade", {k: f"{v} ({v / len(iw):.0%})" for k, v in sorted(q.items())})
for k in (2, 3, 4):
    v = [x for x in iw if min(x[3], 4) == k]
    print(f"  {k}{'+' if k == 4 else ''}q: n={len(v)} mediana {median(x[0] for x in v)} área {median(x[2] for x in v)} R$/m² {round(median(x[0] / x[2] for x in v))}")
grupos = {"Barra da Tijuca (com Jardim Oceânico e Barra Olímpica)": ("Barra da Tijuca", "Jardim Oceânico", "Barra Olímpica"), "Recreio dos Bandeirantes": ("Recreio dos Bandeirantes",)}
for g, nomes in grupos.items():
    v = [x for x in iw if x[1] in nomes]
    print(g, "n", len(v), "mediana", median(x[0] for x in v), "R$/m²", round(median(x[0] / x[2] for x in v)), "área", median(x[2] for x in v))
print("leblon R$/m²", round(median(x[0] / x[1] for x in zap)), "área", median(x[1] for x in zap), "quartos", Counter(x[2] for x in zap))
for x in iw:
    if x[1] in ("Botafogo", "Humaitá", "Vila Isabel", "Olaria", "Engenho Novo", "Leblon"):
        print("  único:", x[1], x[0], x[2], "m²", round(x[0] / x[2]), "/m²")
cm = Counter()
for x in iw:
    for f in set(x[5]):
        f = {"segurança 24h": "segurança/portaria 24h", "segurança 24 horas": "segurança/portaria 24h", "portaria 24 horas": "segurança/portaria 24h",
             "varanda gourmet": "varanda/terraço", "varanda": "varanda/terraço", "terraço": "varanda/terraço"}.get(f, f)
        cm[f] += 1
print("comodidades (de 17):", cm.most_common())
