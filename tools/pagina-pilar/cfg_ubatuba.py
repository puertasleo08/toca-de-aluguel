import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from replicar import aplicar, RAIZ

FAQ_PRECO_VELHO = "Na amostra analisada pela Toca de Aluguel para um fim de semana de outubro de 2026, a diária mediana de uma casa para alugar em Ubatuba ficou em R$ 769, com metade das casas entre R$ 476 e R$ 998 por noite. O pacote de fim de semana, com 2 diárias para 4 adultos, teve mediana de R$ 1.714."
FAQ_PRECO_NOVO = "Na amostra analisada pela Toca de Aluguel para o fim de semana de 6 a 8 de novembro de 2026, a diária mediana de uma casa para alugar em Ubatuba ficou em R$ 470, com metade das casas entre R$ 275 e R$ 720 por noite. O pacote de fim de semana, com 2 diárias para 4 adultos, teve mediana de R$ 940. Em feriados e na alta temporada, os valores sobem."
FAQ_PETS_VELHO = "Sim. Cerca de dois terços das casas de temporada analisadas aceitam pets. Ar-condicionado aparece em 41% delas e piscina privativa em 25%."
FAQ_PETS_NOVO = "Sim. Das 490 casas de temporada listadas em Ubatuba no Booking.com, 63% aceitam pets. Ar-condicionado aparece em 42% delas e piscina privativa em 24%."


def msg(praia, q):
    return f"Olá! Quero saber sobre casas de {q} quartos para temporada {praia} em Ubatuba."


cfg = dict(
    cidade="Ubatuba",
    cidade_uf="Ubatuba, SP",
    mapa_sufixo="Ubatuba - SP",
    zoom_inicial=11,
    fim_intro='<strong class="font-semibold text-blue-950">R$ 1.714</strong>.',
    aria_kpis="Indicadores do aluguel de casas por temporada em Ubatuba",
    kpis=[("Diária mediana", "R$ 470", "/noite"), ("Faixa central", "R$ 275–720", ""),
          ("Fim de semana", "R$ 940", " · 2 diárias"), ("Casas no portal", "490", "")],
    atalhos=[("quartos:2", "#destaques", "2 quartos"), ("quartos:3", "#destaques", "3+ quartos"), ("preco:ate", "#destaques", "Até R$ 500/noite"),
             ("extra:piscina", "#destaques", "Com piscina"), ("extra:praia", "#destaques", "Perto da praia"),
             ("", "#bairros-vizinhos", "Praias"), ("", "#mapa-cidade", "Mapa")],
    h2_destaques="Destaques: casas para alugar em Ubatuba por temporada",
    rotulo_itens="casas",
    corte_preco=500,
    grupos=[("Quartos", "quartos", [("todos", "Todos"), ("2", "2 quartos"), ("3", "3+ quartos")]),
            ("Diária", "preco", [("todos", "Qualquer"), ("ate", "Até R$ 500"), ("acima", "Acima de R$ 500")]),
            ("Extras", "extra", [("piscina", "Com piscina"), ("praia", "Perto da praia")])],
    msg_vazio="Olá! Vim pela página de casas em Ubatuba e quero opções de temporada com o meu perfil.",
    nota_destaques="Exemplos baseados em casas reais da amostra de novembro de 2026, com diária sem taxas. Disponibilidade e valores para as suas datas são confirmados pelo corretor parceiro.",
    cards=[
        dict(q=2, preco=261, tags="praia", img="photo-1493809842364-78817add7ffb", selo="Temporada", periodo="/noite", extra="Mínimo de 2 diárias",
             alt="Sala de estar com sofá azul e piso de taco em casa de 2 quartos para alugar a 500 m da Praia do Sapê, em Ubatuba",
             titulo="Casa 2 Quartos — Praia do Sapê", sub="46 m² · A 500 m da praia", det="2 quartos · até 4 hóspedes",
             msg=msg("perto da Praia do Sapê", 2)),
        dict(q=2, preco=315, tags="praia", img="photo-1600596542815-ffad4c1539a9", selo="Temporada", periodo="/noite", extra="Mínimo de 2 diárias",
             alt="Casa de temporada em condomínio com área verde, perfil das casas para alugar perto da Praia da Maranduba, em Ubatuba",
             titulo="Casa 2 Quartos — Maranduba", sub="71 m² · Condomínio a 500 m da praia", det="2 quartos · até 4 hóspedes",
             msg=msg("na Praia da Maranduba", 2)),
        dict(q=2, preco=470, tags="piscina", img="photo-1522708323590-d24dbb6b0267", selo="Temporada", periodo="/noite", extra="Mínimo de 2 diárias",
             alt="Sala integrada com cozinha e poltrona vermelha em cobertura de 2 quartos com piscina para alugar na Praia Grande, em Ubatuba",
             titulo="Cobertura 2 Quartos — Praia Grande", sub="150 m² · Piscina · Perto do Itaguá", det="2 quartos · até 4 hóspedes",
             msg=msg("na Praia Grande", 2)),
        dict(q=3, preco=626, tags="praia", img="photo-1613490493576-7fde63acd811", selo="Temporada", periodo="/noite", extra="Mínimo de 2 diárias",
             alt="Sobrado de temporada com varanda ampla a 250 m da Praia das Toninhas, casa de 3 quartos para alugar em Ubatuba",
             titulo="Casa 3 Quartos — Toninhas", sub="210 m² · A 250 m da praia", det="3 quartos · até 6 hóspedes",
             msg=msg("na Praia das Toninhas", 3)),
        dict(q=4, preco=817, tags="", img="photo-1510798831971-661eb04b3739", selo="Temporada", periodo="/noite", extra="Mínimo de 2 diárias",
             alt="Casa de praia com varanda voltada para o mar, exemplo de casa de 4 quartos para alugar na Praia do Lázaro, em Ubatuba",
             titulo="Casa 4 Quartos — Praia do Lázaro", sub="Perto do Saco da Ribeira", det="4 quartos · grupos grandes",
             msg=msg("na Praia do Lázaro", 4)),
        dict(q=5, preco=1000, tags="piscina", img="photo-1564013799919-ab600027ffc6", selo="Alto padrão", periodo="/noite", extra="Mínimo de 2 diárias",
             alt="Casa de praia com piscina aquecida e jardim, perfil das casas de 5 quartos para alugar no Perequê-Mirim, em Ubatuba",
             titulo="Casa 5 Quartos — Perequê-Mirim", sub="300 m² · Piscina aquecida", det="5 quartos · famílias e grupos",
             msg=msg("no Perequê-Mirim", 5)),
    ],
    h3_faixas="Distribuição da diária",
    sub_faixas="Percentual e número de casas por faixa de diária (25 casas, sem taxas)",
    selo_faixa="mais comum",
    faixas=[("Até R$ 300", 32, 8), ("R$ 300 a R$ 500", 20, 5), ("R$ 500 a R$ 800", 28, 7), ("R$ 800 a R$ 1.200", 12, 3), ("Acima de R$ 1.200", 8, 2)],
    h3_tipos="Casas por número de quartos e diária mediana",
    sub_tipos="Proporção da amostra e diária mediana de cada tamanho",
    tipos=[("1 quarto", 12, "R$ 500 · 3 casas"), ("2 quartos", 60, "R$ 315 · 15 casas"), ("3 quartos", 8, "R$ 920 · 2 casas"), ("4 ou mais", 20, "R$ 970 · 5 casas")],
    nota_tipos="As casas de 2 quartos dominam a oferta e têm as diárias mais baixas. Com poucas casas de 1 e de 3 quartos na amostra, essas medianas são indicativas.",
    slugs_perfis=["maranduba", "lazaro", "enseada"],
    h2_vizinhos="Praias vizinhas e regiões de influência: da Maranduba à Praia Grande",
    txt_vizinhos=("Compare a oferta de casas de temporada em cada praia antes de reservar. Quem não encontra vaga na Maranduba costuma "
                  "olhar o Lázaro e a Enseada, no mesmo trecho sul da Rio-Santos; quem quer bares e restaurantes a pé fica entre as "
                  "Toninhas, a Praia Grande e o centro."),
    nota_vizinhos="Número de casas de temporada por praia no filtro do Booking.com, que listava 490 casas em Ubatuba em novembro de 2026.",
    barra_campo="n",
    bairros=[
        dict(nome="Praia da Maranduba", regiao="Sul · mar calmo para famílias", valor="48", valor_suf=" casas no filtro", n=48, selo="10% da oferta", tom="alto", slug="maranduba"),
        dict(nome="Praia do Lázaro", regiao="Sul · perto do Saco da Ribeira", valor="28", valor_suf=" casas no filtro", n=28, selo="6% da oferta", tom="alto", slug="lazaro"),
        dict(nome="Praia das Toninhas", regiao="Centro-sul · bares e restaurantes", valor="25", valor_suf=" casas no filtro", n=25, selo="5% da oferta", tom="alto"),
        dict(nome="Praia Perequê-Mirim", regiao="Sul · vizinha da Enseada", valor="15", valor_suf=" casas no filtro", n=15, selo="3% da oferta", tom="medio"),
        dict(nome="Praia da Enseada", regiao="Sul · comércio perto", valor="13", valor_suf=" casas no filtro", n=13, selo="3% da oferta", tom="medio", slug="enseada"),
        dict(nome="Centro de Ubatuba", regiao="Centro · Aquário e Projeto Tamar", valor="6", valor_suf=" casas no filtro", n=6, selo="1% da oferta", tom="medio"),
        dict(nome="Praia Grande", regiao="Centro-sul · vizinha do Tenório", valor="5", valor_suf=" casas no filtro", n=5, selo="1% da oferta", tom="medio"),
    ],
    h2_mapa="Mapa de Ubatuba (SP): praias, passeios e acessos",
    txt_mapa=("Antes de reservar, confira a distância entre a casa, a praia e os passeios — do Saco da Ribeira, de onde saem os barcos "
              "para a Ilha Anchieta, ao Projeto Tamar no Itaguá. Toque em uma praia ou em um ponto de referência para centralizar o mapa."),
    pontos=[("Praias", ["Praia da Maranduba", "Praia do Lázaro", "Praia das Toninhas", "Praia da Enseada", "Praia Grande", "Praia de Itamambuca", "Praia do Félix"]),
            ("Passeios e natureza", ["Projeto Tamar Ubatuba", "Aquário de Ubatuba", "Ilha Anchieta", "Saco da Ribeira"]),
            ("Vias de acesso", ["Rodovia Rio-Santos", "Rodovia Oswaldo Cruz"]),
            ("Centro", ["Centro de Ubatuba", "Orla do Itaguá"])],
    comodidades=[("Cozinha", 97, 475), ("Estacionamento", 88, 431), ("Wi-Fi grátis", 87, 427), ("Aceita pets", 63, 308),
                 ("Ar-condicionado", 42, 204), ("Piscina", 27, 133), ("Piscina privativa", 24, 119), ("Beira-mar", 14, 71), ("Vista do mar", 8, 39)],
    aria_comodidades="Comodidades das casas de temporada em Ubatuba",
    ordem=["destaques-heading", "resumo-heading", "precos-heading", "vizinhos-heading", "comodidades-heading", "bairros-heading",
           "mapa-heading", "video-heading", "como-alugar-heading", "faq-heading", "conclusao-heading"],
    trocas=[
        ("diária mediana de R$ 769, praias com mais casas", "diária mediana de R$ 470, praias com mais casas"),
        ('"dateModified": "2026-09-27T08:00:00-03:00"', '"dateModified": "2026-10-30T18:00:00-03:00"'),
        ('<strong class="font-semibold text-blue-950">R$ 769</strong>', '<strong class="font-semibold text-blue-950">R$ 470</strong>'),
        ('<strong class="font-semibold text-blue-950">R$ 1.714</strong>', '<strong class="font-semibold text-blue-950">R$ 940</strong>'),
        ("Diária mediana de R$ 769; metade das casas fica entre R$ 476 e R$ 998 por noite.", "Diária mediana de R$ 470; metade das casas fica entre R$ 275 e R$ 720 por noite."),
        ("Fim de semana (2 diárias, 4 adultos) com mediana de R$ 1.714.", "Fim de semana (2 diárias, 4 adultos) com mediana de R$ 940."),
        ("Maranduba, Lázaro e Enseada são as praias com mais casas de temporada.", "Maranduba, Lázaro e Toninhas são as praias com mais casas de temporada."),
        ("2 em cada 3 casas aceitam pets.", "63% das casas aceitam pets."),
        ('<td class="px-5 py-3">R$ 769/noite</td>', '<td class="px-5 py-3">R$ 470/noite</td>'),
        ("R$ 476 a R$ 998 por noite</td>", "R$ 275 a R$ 720 por noite</td>"),
        ("R$ 1.714 (mediana)</td>", "R$ 940 (mediana)</td>"),
        ("2 quartos R$ 700 · 3 quartos R$ 900 · 4 quartos R$ 995", "2 quartos R$ 315 · 3 quartos R$ 920 · 4 ou mais R$ 970"),
        ("1 (12%) · 2 (44%) · 3 (16%) · 4 ou mais (28%)", "1 (12%) · 2 (60%) · 3 (8%) · 4 ou mais (20%)"),
        ("89% das casas de temporada</td>", "88% das casas de temporada</td>"),
        ('<dd class="font-semibold text-blue-950">R$ 769</dd>', '<dd class="font-semibold text-blue-950">R$ 470</dd>'),
        ('<dd class="font-semibold text-blue-950">R$ 1.714</dd>', '<dd class="font-semibold text-blue-950">R$ 940</dd>'),
    ],
    trocas_re=[
        (re.escape(FAQ_PRECO_VELHO), FAQ_PRECO_NOVO, 2),
        (re.escape(FAQ_PETS_VELHO), FAQ_PETS_NOVO, 2),
        (r"reúne 283 opções na cidade", "reúne 490 opções na cidade", 1),
        (r"cerca de R\$ 340 por noite, enquanto casas amplas com piscina\s+passam de R\$ 2\.000\.", "cerca de R$ 190 por noite, enquanto casas amplas com piscina\n                passam de R$ 1.800.", 1),
        (r"Metodologia: levantamento da Toca de Aluguel com as diárias de 25.*?confirmado pelo corretor responsável\.",
         "Metodologia: levantamento da Toca de Aluguel com as diárias de 25\n                casas de temporada exibidas no Booking.com para o fim de semana\n                de 6 a 8 de novembro de 2026 (4 adultos, valores sem taxas) e com\n                os filtros das 490 casas de temporada listadas em Ubatuba. Feriados\n                e alta temporada costumam ter diárias mais altas; o valor final é\n                confirmado pelo corretor responsável.", 1),
        (r"Cozinha equipada aparece em 98% das casas de temporada e\s+estacionamento em 89%", "Cozinha equipada aparece em 97% das casas de temporada e\n                estacionamento em 88%", 1),
        (r"com 22 casas de temporada no filtro da\s+praia", "com 48 casas de temporada no filtro da\n                    praia", 1),
        (r"com 15 casas no filtro", "com 28 casas no filtro", 1),
        (r"Reúne 9 casas de temporada no filtro", "Reúne 13 casas de temporada no filtro", 1),
        (r"Três praias concentram a maior oferta de casas de temporada da\s+cidade, e cada uma atende um perfil diferente de viajante\.",
         "Maranduba e Lázaro lideram a oferta de casas de temporada, e a\n                Enseada é a base mais tranquila do sul. Cada praia atende um perfil\n                diferente de viajante.", 1),
        (r"mediana de R\$ 769 por noite como referência", "mediana de R$ 470 por noite como referência", 1),
        (r"Com diária mediana de R\$ 769 e oferta concentrada nas praias da\s+Maranduba, do Lázaro e da Enseada",
         "Com diária mediana de R$ 470 e oferta concentrada nas praias da\n                Maranduba, do Lázaro e das Toninhas", 1),
    ],
)

if __name__ == "__main__":
    pg = aplicar("casas-ubatuba.html", cfg)
    sobra = [t for t in ("769", "1.714", "R$ 476", "R$ 998", "283", "outubro de 2026") if t in pg.s]
    print("ok | valores antigos restantes:", sobra or "nenhum")
