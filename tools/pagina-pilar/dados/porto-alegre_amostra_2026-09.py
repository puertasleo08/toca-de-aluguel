from collections import Counter
from statistics import mean, median

zap = dict(
    prices=[2750, 9000, 1150, 1370, 1150, 2350, 1450, 1200, 1900, 2500, 950, 1500, 1700, 1300, 990, 1650, 1000, 1500, 3200, 5000, 2400, 4000],
    condo=[451, 1900, 245, 454, 245, 460, 438, 530, 525, 690, 568, 660, 280, 580, 512, 600, 650, 600, 600, 900, 670, 700],
    hoods=["Jardim Botânico", "Bela Vista", "Jardim Leopoldina", "Humaitá", "Floresta", "Rio Branco", "Centro Histórico", "Vila Nova", "Morro Santana", "Centro Histórico", "São Geraldo", "Centro Histórico", "Menino Deus", "Santo Antônio", "Cidade Baixa", "Centro Histórico", "Independência", "Floresta", "Centro Histórico", "Menino Deus", "Costa e Silva", "Cidade Baixa", "Jardim Botânico", "Jardim Botânico", "Jardim Botânico", "Jardim Botânico", "Jardim Botânico", "Floresta", "Costa e Silva"],
    beds=[1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2],
    areas=[47, 152, 43, 59, 45, 44, 48, 40, 54, 35, 34, 42, 38, 65, 60, 38, 71, 70, 43, 40, 44, 38, 47, 40, 60, 110],
    amen=["vaga", "churrasqueira", "mobiliado", "piscina", "elevador", "sacada", "varanda", "vaga", "área de serviço", "internet", "armário", "lavanderia", "escritório", "climatização", "academia", "vaga", "segurança", "paisagismo", "copa", "recreação", "salão de festas"],
)
multi = dict(
    prices=[4600, 3500, 3500, 3300, 3800, 3500, 3000, 2600, 7300, 7500, 6900, 10500],
    condo=[790, 600, 604, 570, 850, 671, 835, 450, 1540, 1545, 1567, 1122],
    hoods=["Petrópolis", "Santana", "Jardim Lindóia", "Partenon", "Auxiliadora", "Três Figueiras", "São Geraldo", "Moinhos de Vento", "Três Figueiras", "Três Figueiras", "Três Figueiras", "Jardim Europa"],
    beds=[3, 2, 2, 3, 1, 1, 1, 2, 2, 2, 2, 3],
    areas=[92, 66, 61, 70, 47, 38, 64, 62, 86, 86, 86, 142],
    amen=["vaga"] * 12,
)
iw = dict(
    prices=[3600, 1100, 2860, 1110, 2150, 4300, 1417, 1700, 1150, 1360, 1200, 1450, 9200, 3600, 3100, 1200, 6700, 8900, 9000],
    condo=[250, 397, 750, 517, 120, 733, 357, 450, 350, 580, 320, 400, 776, 330, 500],
    hoods=["Bom Jesus", "Centro Histórico", "Partenon", "Centro Histórico", "Passo da Areia", "Passo da Areia", "Azenha", "Centro Histórico", "Centro Histórico", "Humaitá", "Petrópolis", "Santa Tereza", "Centro Histórico", "Centro Histórico", "Centro Histórico", "Azenha"],
    beds=[1, 1, 3, 2, 2, 2, 1, 2, 2, 1, 1, 2, 3, 1, 1, 2, 2, 3, 1, 2, 2, 2, 1, 1, 1, 1, 1],
    areas=[49, 21, 72, 70, 51, 75, 44, 74, 25, 60, 70, 48, 95, 26, 38, 40, 54, 69, 69, 40, 40, 31],
    amen=["churrasqueira", "gás central", "mobiliado", "piscina", "espaço gourmet", "elevador", "sacada", "varanda", "quiosque", "salão de festas", "playground", "brinquedoteca", "academia", "portaria 24 horas", "lavanderia", "quintal", "aceita pets"],
)

def q(v, p):
    s = sorted(v)
    k = (len(s) - 1) * p
    f = int(k)
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)

allp = zap["prices"] + multi["prices"] + iw["prices"]
allc = zap["condo"] + multi["condo"] + iw["condo"]
alla = zap["areas"] + multi["areas"] + iw["areas"]
allb = zap["beds"] + multi["beds"] + iw["beds"]
print("N prices", len(allp), "mean", round(mean(allp)), "median", median(allp), "p25", q(allp, .25), "p75", q(allp, .75), "min", min(allp), "max", max(allp))
for name, d in (("zap", zap), ("multi", multi), ("iw", iw)):
    print(name, "median rent", median(d["prices"]), "median condo", median(d["condo"]))
print("condo median", median(allc), "p25", q(allc, .25), "p75", q(allc, .75))
print("area median", median(alla))
print("beds", Counter(allb))
hoods = Counter(zap["hoods"] + multi["hoods"] + iw["hoods"])
print("hoods", hoods.most_common(8))
print("amen", Counter(zap["amen"] + multi["amen"] + iw["amen"]).most_common(10))
