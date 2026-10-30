import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from replicar import aplicar, BARRA, GLASS


def msg(onde):
    return f"Olá! Quero saber sobre coberturas à venda {onde}, no Rio de Janeiro."


cfg = dict(
    cidade="Rio de Janeiro",
    cidade_uf="Rio de Janeiro, RJ",
    mapa_sufixo="Rio de Janeiro - RJ",
    zoom_inicial=11,
    fim_intro='<strong class="font-semibold text-blue-950">R$ 4,5 milhões</strong>.',
    aria_kpis="Indicadores das coberturas à venda no Rio de Janeiro",
    kpis=[("Preço mediano", "R$ 2 mi", " · cidade"), ("Leblon", "R$ 4,5 mi", " · mediana"),
          ("m² mediano", "R$ 9,2 mil", ""), ("Condomínio", "R$ 2 mil", "/mês")],
    atalhos=[("quartos:3", "#destaques", "3+ quartos"), ("preco:ate", "#destaques", "Até R$ 3 mi"), ("extra:piscina", "#destaques", "Com piscina"),
             ("extra:zonasul", "#destaques", "Zona Sul"), ("", "#bairros-vizinhos", "Bairros"), ("", "#mapa-cidade", "Mapa")],
    h2_destaques="Destaques: cobertura à venda no Rio de Janeiro, da Zona Sul ao Recreio",
    rotulo_itens="coberturas",
    corte_preco=3000000,
    grupos=[("Quartos", "quartos", [("todos", "Todos"), ("2", "2 quartos"), ("3", "3+ quartos")]),
            ("Preço", "preco", [("todos", "Qualquer"), ("ate", "Até R$ 3 mi"), ("acima", "Acima de R$ 3 mi")]),
            ("Extras", "extra", [("piscina", "Com piscina"), ("zonasul", "Zona Sul")])],
    msg_vazio="Olá! Vim pela página de coberturas no Rio de Janeiro e quero opções com o meu perfil.",
    nota_destaques="Exemplos com base nas medianas e em anúncios reais da amostra. A disponibilidade, os valores e a possibilidade de locação de cada unidade são confirmados pelo corretor parceiro no atendimento.",
    cards=[
        dict(q=3, preco=4500000, tags="piscina zonasul", img="photo-1600573472550-8090b5e0745e", selo="Alto padrão", periodo="", extra="+ condomínio R$ 2.800/mês",
             alt="Sala com escada vazada e parede de vidro aberta para terraço com piscina, típica de cobertura duplex à venda no Leblon",
             titulo="Cobertura Duplex 3 Quartos — Leblon", sub="180 m² · Terraço com piscina · Perto da praia", det="3 quartos · 3 banheiros · 2 vagas",
             msg=msg("no Leblon")),
        dict(q=3, preco=3900000, tags="zonasul", img="photo-1502005229762-cf1b2da7c5d6", selo="Venda", periodo="", extra="+ condomínio R$ 2.500/mês",
             alt="Escada de madeira iluminada por pendentes ligando os dois andares de uma cobertura duplex à venda em Botafogo",
             titulo="Cobertura Duplex 3 Quartos — Botafogo", sub="250 m² · Vista para o Cristo · Perto do metrô", det="3 quartos · 2 banheiros · 2 vagas",
             msg=msg("em Botafogo")),
        dict(q=3, preco=2650000, tags="zonasul", img="photo-1600210492486-724fe5c67fb0", selo="Venda", periodo="", extra="+ condomínio R$ 1.950/mês",
             alt="Sala ampla com poltronas brancas e parede de quadros, estilo das coberturas à venda no Humaitá, vizinho de Botafogo",
             titulo="Cobertura 3 Quartos — Humaitá", sub="138 m² · Varanda · Perto da Lagoa", det="3 quartos · 2 banheiros · 1 vaga",
             msg=msg("no Humaitá")),
        dict(q=3, preco=2600000, tags="piscina", img="photo-1512917774080-9991f1c4c750", selo="Venda", periodo="", extra="+ condomínio R$ 2.100/mês",
             alt="Deck com piscina privativa e portas de vidro para a sala, estilo de cobertura com piscina para comprar na Barra da Tijuca",
             titulo="Cobertura 3 Quartos — Barra da Tijuca", sub="250 m² · Piscina e churrasqueira · Jardim Oceânico", det="3 quartos · 3 banheiros · 2 vagas",
             msg=msg("na Barra da Tijuca")),
        dict(q=4, preco=1550000, tags="", img="photo-1600607687939-ce8a6c25118c", selo="Venda", periodo="", extra="+ condomínio R$ 1.700/mês",
             alt="Living integrado com lareira e porta de vidro para a varanda, referência para quem quer comprar cobertura no Recreio dos Bandeirantes",
             titulo="Cobertura 4 Quartos — Recreio dos Bandeirantes", sub="280 m² · Terraço gourmet · Perto da praia", det="4 quartos · 3 banheiros · 2 vagas",
             msg=msg("no Recreio dos Bandeirantes")),
        dict(q=2, preco=1350000, tags="piscina", img="photo-1554995207-c18c203602cb", selo="Venda", periodo="", extra="+ condomínio R$ 980/mês",
             alt="Sala com sofá caramelo, plantas e luminárias pendentes em cobertura de 2 quartos com piscina e terraço à venda no Recreio",
             titulo="Cobertura 2 Quartos — Recreio dos Bandeirantes", sub="213 m² · Piscina e terraço", det="2 quartos · 2 banheiros · 2 vagas",
             msg=msg("de 2 quartos no Recreio dos Bandeirantes")),
    ],
    h3_faixas="Distribuição de preços das coberturas na cidade",
    sub_faixas="Percentual e número de anúncios por faixa de preço (17 anúncios com preço)",
    selo_faixa="mais comum",
    faixas=[("Até R$ 1 milhão", 6, 1), ("R$ 1 a 2 milhões", 41, 7), ("R$ 2 a 3 milhões", 35, 6), ("R$ 3 a 5 milhões", 12, 2), ("Acima de R$ 5 milhões", 6, 1)],
    h3_tipos="Quartos, preço mediano e metragem das coberturas",
    sub_tipos="Proporção da amostra da cidade e valores medianos de cada tipologia",
    tipos=[("2 quartos", 12, "R$ 870 mil · 170 m²"), ("3 quartos", 65, "R$ 2,6 mi · 232 m²"), ("4 ou mais", 24, "R$ 1,59 mi · 363 m²")],
    nota_tipos="As coberturas de 4 quartos ou mais saem mais baratas na mediana porque estão concentradas no Recreio e na Zona Norte, onde o m² custa menos da metade da Barra.",
    slugs_perfis=["leblon", "barra-da-tijuca", "recreio"],
    h2_vizinhos="Bairros vizinhos e regiões de influência: do Leblon ao Recreio",
    txt_vizinhos=("Compare o preço mediano e o metro quadrado de cada bairro antes de visitar. Quem não fecha no Leblon costuma olhar "
                  "Botafogo e Humaitá, com vista para o Cristo e metrô perto; quem quer terraço maior pelo mesmo valor segue para a "
                  "Barra da Tijuca e o Recreio dos Bandeirantes."),
    nota_vizinhos=("Leblon: 17 anúncios únicos do ZAP Imóveis. Demais bairros: 17 anúncios do Imovelweb em toda a cidade. Bairros com "
                   "um único anúncio têm valor apenas indicativo."),
    barra_campo="v",
    bairros=[
        dict(nome="Leblon", regiao="Zona Sul · praia e Mirante", valor="R$ 4,5 mi", valor_suf=" · R$ 21,6 mil/m²", v=4500, selo="17 anúncios", tom="alto", slug="leblon"),
        dict(nome="Botafogo", regiao="Zona Sul · metrô e vista do Cristo", valor="R$ 5,1 mi", valor_suf=" · R$ 20,3 mil/m²", v=5077, selo="1 anúncio", tom="alto"),
        dict(nome="Humaitá", regiao="Zona Sul · perto da Lagoa", valor="R$ 2,65 mi", valor_suf=" · R$ 19,2 mil/m²", v=2650, selo="1 anúncio", tom="alto"),
        dict(nome="Barra da Tijuca", regiao="Zona Oeste · inclui Jardim Oceânico", valor="R$ 2,6 mi", valor_suf=" · R$ 10 mil/m²", v=2600, selo="7 anúncios", tom="medio", slug="barra-da-tijuca"),
        dict(nome="Recreio dos Bandeirantes", regiao="Zona Oeste · terraços amplos", valor="R$ 1,55 mi", valor_suf=" · R$ 5,7 mil/m²", v=1547, selo="4 anúncios", tom="baixo", slug="recreio"),
        dict(nome="Vila Isabel", regiao="Zona Norte · coberturas grandes", valor="R$ 1,55 mi", valor_suf=" · R$ 3,2 mil/m²", v=1550, selo="1 anúncio", tom="baixo"),
        dict(nome="Olaria", regiao="Zona Norte · 520 m²", valor="R$ 1,05 mi", valor_suf=" · R$ 2 mil/m²", v=1050, selo="1 anúncio", tom="baixo"),
        dict(nome="Engenho Novo", regiao="Zona Norte · entrada", valor="R$ 390 mil", valor_suf=" · R$ 3,1 mil/m²", v=390, selo="1 anúncio", tom="baixo"),
    ],
    h2_mapa="Mapa do Rio de Janeiro (RJ): praias, bairros e centros comerciais",
    txt_mapa=("Compare a distância entre a cobertura, a praia e a sua rotina — do Mirante do Leblon à Pedra do Pontal, passando pela "
              "Lagoa Rodrigo de Freitas e pela Avenida das Américas. Toque em um bairro ou ponto de referência para centralizar o mapa."),
    pontos=[("Bairros", ["Leblon", "Ipanema", "Lagoa", "Botafogo", "Humaitá", "Barra da Tijuca", "Jardim Oceânico", "Recreio dos Bandeirantes"]),
            ("Praias e mirantes", ["Praia do Leblon", "Mirante do Leblon", "Praia do Recreio", "Pedra do Pontal"]),
            ("Avenidas e vias", ["Avenida Delfim Moreira", "Avenida das Américas", "Lagoa Rodrigo de Freitas"]),
            ("Centros comerciais", ["Shopping Leblon", "BarraShopping", "Village Mall"])],
    ordem=["destaques-heading", "resumo-heading", "precos-heading", "vizinhos-heading", "comodidades-heading", "bairros-heading",
           "mapa-heading", "video-heading", "como-comprar-heading", "faq-heading", "conclusao-heading"],
    trocas=[('"dateModified": "2026-09-29T08:00:00-03:00"', '"dateModified": "2026-10-30T18:30:00-03:00"')],
)

COMOD = [("Piscina", 59, 10), ("Churrasqueira", 59, 10), ("Varanda ou terraço", 29, 5), ("Segurança ou portaria 24 h", 18, 3)]
lis = "".join(f"""
                <li>
                  <div class="flex items-baseline justify-between gap-3 text-sm">
                    <span class="font-semibold text-blue-950">{r}</span>
                    <span class="shrink-0 tabular-nums text-slate-500">{p}% dos anúncios · {n}</span>
                  </div>
                  <div class="mt-1.5 h-2.5 rounded-full bg-slate-200/70" aria-hidden="true">
                    <div data-barra class="h-2.5 w-[{round(p / 59 * 100)}%] {BARRA} {'bg-brand-orange' if p == 59 else 'bg-blue-950/80'}"></div>
                  </div>
                </li>""" for r, p, n in COMOD)
BARRAS_COMOD = f"""
              <ul class="{GLASS} space-y-3.5 p-5 sm:p-6" role="list" aria-label="Comodidades citadas nos anúncios de cobertura no Rio de Janeiro">{lis}
              </ul>
              <p class="text-xs leading-relaxed text-slate-500">
                Percentual dos 17 anúncios de cobertura do Imovelweb na cidade que citam cada item.
              </p>"""

if __name__ == "__main__":
    pg = aplicar("coberturas-rio-de-janeiro.html", cfg)
    s = pg.s
    a = s.index('aria-labelledby="comodidades-heading"')
    p_fim = s.index("</p>", s.index("<p", a)) + len("</p>")
    s = s[:p_fim] + BARRAS_COMOD + s[p_fim:]
    pg.s = s
    pg.salvar()
    print("ok")
