"""Gera apartamento-santo-amaro.html a partir da casca de coberturas-rio-de-janeiro.html e insere o link nos menus do site.
Dados: tools/pagina-pilar/dados/santo-amaro_* e chacara-santo-antonio_* (coleta de 30/10/2026)."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from replicar import (BARRA, CHIP, FOCO, GLASS, H2, LINK, RAIZ, ROLAGEM, WA_HOVER, WA_PULSO, destaques, kpis, mapa, painel, vizinhos, wa)

SLUG = "apartamento-santo-amaro"
URL = f"https://www.tocadealuguel.com.br/{SLUG}"
H1 = "Apartamento em Santo Amaro, SP: Preços, Bairros e Oportunidades"
TITULO = "Apartamento à Venda em Santo Amaro, São Paulo (SP): Preços"
DESC = "Apartamento à venda em Santo Amaro, São Paulo (SP): mediana de R$ 640 mil e m² a R$ 11,2 mil no QuintoAndar e VivaReal. Veja apartamentos em Santo Amaro e ofertas."
MSG = "Olá! Vim pela página de apartamento em Santo Amaro e quero falar com um corretor."
FOTOS = "./assets/REVIEW/SANTO-AMARO"
CHECK = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="mt-1 shrink-0 text-brand-orange" aria-hidden="true"><path d="M20 6 9 17l-5-5" /></svg>'
PIN = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-brand-orange" aria-hidden="true"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0" /><circle cx="12" cy="10" r="3" /></svg>'
SETA = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0 text-brand-orange transition-transform group-open:rotate-180" aria-hidden="true"><path d="m6 9 6 6 6-6" /></svg>'
BALAO = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z" /></svg>'
P = '<p class="text-sm leading-relaxed text-slate-600 sm:text-base">'
NOTA = '<p class="text-xs leading-relaxed text-slate-500">'

cfg = dict(
    cidade="Santo Amaro",
    cidade_uf="Santo Amaro, São Paulo",
    mapa_sufixo="São Paulo - SP",
    mapa_inicial="Santo Amaro, São Paulo - SP",
    zoom_inicial=13,
    rotulo_itens="apartamentos",
    h2_destaques="Apartamento à venda em Santo Amaro: destaques de 1, 2 e 3 quartos",
    grupos=[
        ("Quartos", "quartos", [("todos", "Todos"), ("1", "1 quarto"), ("2", "2 quartos"), ("3", "3+")]),
        ("Preço", "preco", [("todos", "Todos"), ("ate", "Até R$ 500 mil"), ("acima", "Acima de R$ 500 mil")]),
        ("Extras", "extra", [("pets", "Aceita pets"), ("piscina", "Piscina"), ("mobiliado", "Mobiliado")]),
    ],
    msg_vazio="Olá! Vim pela página de apartamento em Santo Amaro e quero opções com o meu perfil.",
    nota_destaques="Anúncios reais publicados no QuintoAndar e no VivaReal em outubro de 2026. Disponibilidade, valores e condições de cada imóvel são confirmados pelo corretor parceiro no atendimento.",
    cards=[
        dict(q=1, preco=470000, tags="pets piscina vaga", img="photo-1560448204-e02f11c3d0e2", selo="Venda", periodo="", extra="Condomínio + IPTU R$ 790/mês",
             alt="Sala de apartamento compacto com sofá e janela ampla, exemplo de apartamento de 1 quarto com piscina no condomínio",
             titulo="1 quarto com piscina e vaga", sub="36 m² · 1 quarto · 1 vaga · Avenida Vereador José Diniz",
             det="Disponível para compra, aceita pets e tem piscina no condomínio, perto do Brooklin e do Campo Belo.", msg="Olá! Tenho interesse no apartamento de 1 quarto com piscina em Santo Amaro (R$ 470 mil)."),
        dict(q=2, preco=485000, tags="pets piscina vaga", img="photo-1554995207-c18c203602cb", selo="Venda", periodo="", extra="Condomínio + IPTU R$ 875/mês",
             alt="Sala com sofá caramelo, plantas e luminárias pendentes em apartamento de 2 quartos que aceita animais",
             titulo="2 quartos pet-friendly com piscina", sub="58 m² · 2 quartos · 1 vaga · Rua Maria José da Conceição",
             det="Condomínio com piscina e permissão para animais, uma das combinações mais buscadas no bairro.", msg="Olá! Tenho interesse no apartamento de 2 quartos com piscina em Santo Amaro (R$ 485 mil)."),
        dict(q=2, preco=500000, tags="mobiliado vaga", img="photo-1493809842364-78817add7ffb", selo="Venda", periodo="", extra="Condomínio + IPTU R$ 1.022/mês",
             alt="Sala de estar com sofá azul, piso de taco e janela ampla em apartamento mobiliado de 2 quartos pronto para morar",
             titulo="2 quartos mobiliado com varanda", sub="60 m² · 2 quartos · 2 vagas · Rua Maria José da Conceição",
             det="Pronto para morar, com varanda e academia no condomínio.", msg="Olá! Tenho interesse no apartamento mobiliado de 2 quartos em Santo Amaro (R$ 500 mil)."),
        dict(q=2, preco=590000, tags="vaga", img="photo-1502672260266-1c1ef2d93688", selo="Venda", periodo="", extra="+ condomínio R$ 620/mês",
             alt="Sala de estar iluminada com janelas altas em apartamento de 2 quartos à venda no centro de Santo Amaro, perto do Largo Treze",
             titulo="2 quartos no centro de Santo Amaro", sub="53 m² · 2 quartos · 1 vaga · Praça Dom Francisco de Souza",
             det="Perto do comércio do Largo Treze e das estações Largo Treze e Santo Amaro.", msg="Olá! Tenho interesse no apartamento de 2 quartos no centro de Santo Amaro (R$ 590 mil)."),
        dict(q=3, preco=1383000, tags="vaga", img="photo-1586023492125-27b2c045efd7", selo="Venda", periodo="", extra="+ condomínio R$ 1.400/mês",
             alt="Living integrado com cozinha em apartamento familiar de 3 quartos",
             titulo="3 quartos com 2 vagas", sub="125 m² · 3 quartos · 2 vagas · Rua Coronel Luís Barroso",
             det="Planta familiar a poucos minutos do Largo Treze.", msg="Olá! Tenho interesse no apartamento de 3 quartos em Santo Amaro (R$ 1,38 milhão)."),
        dict(q=3, preco=1998000, tags="vaga", img="photo-1600607687939-ce8a6c25118c", selo="Alto padrão", periodo="", extra="+ condomínio R$ 2.000/mês",
             alt="Sala ampla de apartamento de alto padrão com decoração clara, perfil dos imóveis à venda na Rua Borba Gato, em Santo Amaro",
             titulo="3 quartos na Rua Borba Gato", sub="148 m² · 3 quartos · 3 vagas · Rua Borba Gato",
             det="Alto padrão perto da Estação Borba Gato da Linha 5-Lilás.", msg="Olá! Tenho interesse no apartamento de 3 quartos na Rua Borba Gato (R$ 1,998 milhão)."),
    ],
    h3_faixas="Faixa de preço dos anúncios",
    sub_faixas="Percentual e número de anúncios por faixa (27 anúncios do VivaReal)",
    selo_faixa="mais comum",
    faixas=[("Até R$ 400 mil", 26, 7), ("R$ 400 a 600 mil", 19, 5), ("R$ 600 a 900 mil", 37, 10), ("R$ 900 mil a 1,5 milhão", 11, 3), ("Acima de R$ 1,5 milhão", 7, 2)],
    h3_tipos="Quartos, preço mediano e metragem",
    sub_tipos="Proporção da amostra e valores medianos de cada tipologia",
    tipos=[("1 quarto", 22, "R$ 424,5 mil · 35 m²"), ("2 quartos", 59, "R$ 667,5 mil · 59,5 m²"), ("3 quartos ou mais", 19, "R$ 1,38 mi · 125 m²")],
    nota_tipos="O apartamento de 2 quartos domina a oferta, a cerca de R$ 11,1 mil por m². Nos de 3 quartos ou mais, o m² sobe para R$ 13,5 mil.",
    rotulo_perfil="Perfil do bairro",
    h2_vizinhos="Bairros vizinhos e regiões de influência: Campo Belo, Alto da Boa Vista e Granja Julieta",
    txt_vizinhos="Compare os preços médios (medianas) e o metro quadrado antes de visitar. Quem quer pagar menos fica no centro de Santo Amaro; quem procura imóvel maior olha o Alto da Boa Vista e a Granja Julieta; e quem trabalha na Berrini ou na Vila Olímpia costuma comparar com o Campo Belo e o Brooklin.",
    nota_vizinhos="Medianas da busca do VivaReal por bairro (Chácara Santo Antônio: QuintoAndar) em 30/10/2026. As buscas por bairro incluem ruas vizinhas, então parte dos anúncios do Alto da Boa Vista tem endereço em Santo Amaro.",
    barra_campo="v",
    bairros=[
        dict(nome="Santo Amaro", regiao="8.743 à venda · VivaReal", valor="R$ 640 mil", valor_suf=" · R$ 11,2 mil/m²", v=640, selo="Mais acessível", tom="baixo"),
        dict(nome="Campo Belo", regiao="9.852 à venda · VivaReal", valor="R$ 889 mil", valor_suf=" · R$ 13,1 mil/m²", v=889, selo="Mais anúncios", tom="medio"),
        dict(nome="Chácara Santo Antônio", regiao="394 à venda · QuintoAndar", valor="R$ 900 mil", valor_suf=" · R$ 14,1 mil/m²", v=900, selo="m² mais alto", tom="alto", slug="chacara-santo-antonio"),
        dict(nome="Granja Julieta", regiao="863 à venda · VivaReal", valor="R$ 1,28 mi", valor_suf=" · R$ 12,8 mil/m²", v=1275, selo="Perto de parque", tom="medio", slug="granja-julieta"),
        dict(nome="Alto da Boa Vista", regiao="2.388 à venda · VivaReal", valor="R$ 1,34 mi", valor_suf=" · R$ 10,7 mil/m²", v=1337, selo="Imóveis maiores", tom="alto", slug="alto-da-boa-vista"),
    ],
    h2_mapa="Mapa de Santo Amaro, São Paulo (SP): Largo Treze, avenidas, parques e estações",
    txt_mapa="Veja a distância entre o apartamento e a sua rotina: do Largo Treze à Avenida Giovanni Gronchi, do Parque Severo Gomes à Avenida Washington Luís, que leva ao Aeroporto de Congonhas. Toque em um bairro, avenida ou estação para centralizar o mapa.",
    pontos=[
        ("Bairros", ["Santo Amaro", "Chácara Santo Antônio", "Alto da Boa Vista", "Granja Julieta", "Campo Belo", "Brooklin"]),
        ("Avenidas", ["Avenida Giovanni Gronchi", "Avenida Washington Luís", "Avenida Santo Amaro", "Avenida Adolfo Pinheiro", "Avenida João Dias"]),
        ("Pontos de referência", ["Largo Treze de Maio", "Parque Severo Gomes", "Mercado Municipal de Santo Amaro", "Catedral de Santo Amaro", "Shopping Morumbi"]),
        ("Metrô e CPTM", ["Estação Santo Amaro", "Estação Largo Treze", "Estação Adolfo Pinheiro", "Estação Alto da Boa Vista", "Estação Borba Gato", "Estação Granja Julieta", "Estação João Dias", "Estação Socorro", "Estação Jurubatuba"]),
    ],
)

KPIS = [("Preço mediano", "R$ 640 mil", ""), ("m² mediano", "R$ 11,2 mil", ""), ("Condomínio", "R$ 630", "/mês"), ("À venda", "8.743", " anúncios")]
ATALHOS = [("quartos:1", "#destaques", "1 quarto"), ("quartos:2", "#destaques", "2 quartos"), ("quartos:3", "#destaques", "3+ quartos"), ("preco:ate", "#destaques", "Até R$ 500 mil"),
           ("extra:pets", "#destaques", "Aceita pets"), ("", "#bairros-vizinhos", "Bairros"), ("", "#mapa-cidade", "Mapa")]
CARROSSEL = [
    ("catedral-santo-amaro.webp", 554, 554, "Catedral de Santo Amaro, igreja histórica de fachada amarela no centro do bairro, perto do Largo Treze e de apartamentos à venda"),
    ("vista-aerea-predios-zona-sul-sao-paulo.webp", 547, 365, "Vista aérea de prédios residenciais da Zona Sul de São Paulo, região com grande oferta de apartamento à venda"),
    ("calcadao-comercio-santo-amaro.webp", 638, 480, "Calçadão de comércio no centro de Santo Amaro, com lojas, clínicas e movimento de pedestres"),
    ("ponte-estaiada-zona-sul-sao-paulo.webp", 365, 547, "Ponte Estaiada sobre o Rio Pinheiros, cartão-postal da Zona Sul a poucos quilômetros de Santo Amaro"),
]
RESUMO = [
    "Preço mediano de R$ 640 mil, cerca de R$ 11,2 mil por m² e condomínio de R$ 630 por mês.",
    "Apartamentos de 2 quartos são 59% da oferta, com mediana de R$ 667,5 mil para 59,5 m².",
    "Compactos de 1 e 2 quartos saem por R$ 390 mil na mediana.",
    "Chácara Santo Antônio tem o m² mais alto da região: R$ 14,1 mil.",
    "Linha 5-Lilás do metrô e Linha 9-Esmeralda da CPTM cortam o distrito.",
]
TABELA = [
    ("Preço mediano de venda", "R$ 640.000", "R$ 390.000"),
    ("Faixa de preços observada", "R$ 230 mil a R$ 3,85 milhões", "R$ 300 mil a R$ 505 mil"),
    ("Preço mediano por m²", "R$ 11,2 mil", "R$ 10,9 mil"),
    ("Área mediana", "53 m²", "36 m²"),
    ("Custo mensal mediano", "R$ 630 de condomínio", "R$ 585 de condomínio + IPTU"),
    ("Com vaga na garagem", "93% dos anúncios", "43% dos anúncios"),
    ("Anúncios analisados", "27 de 8.743", "21 de 106"),
]
COMODIDADES = [
    ("Vaga na garagem", 93, "25 de 27"),
    ("Mobiliado", 43, "9 de 21"),
    ("Aceita pets", 38, "8 de 21"),
    ("Piscina no condomínio", 29, "6 de 21"),
    ("Varanda ou varanda gourmet", 19, "4 de 21"),
    ("Academia no condomínio", 14, "3 de 21"),
    ("Churrasqueira no condomínio", 10, "2 de 21"),
]
PERFIS = [
    ("chacara-santo-antonio", "Chácara Santo Antônio",
     "Polo de escritórios e prédios residenciais perto da Avenida das Nações Unidas, a Marginal Pinheiros, e do Shopping Morumbi. O QuintoAndar lista 394 apartamentos à venda no bairro, com mediana de R$ 900 mil para 64 m² e o m² mais caro da região, R$ 14,1 mil. A faixa vai de R$ 347 mil a R$ 4,72 milhões."),
    ("borba-gato", "Borba Gato",
     "Não é um bairro oficial: o nome vem da Rua Borba Gato e da Estação Borba Gato da Linha 5-Lilás, na Avenida Santo Amaro, entre o Alto da Boa Vista e o Brooklin. Os portais não têm busca própria para a região; um exemplo da amostra é um apartamento de 3 quartos e 148 m² por R$ 1,998 milhão."),
    ("alto-da-boa-vista", "Alto da Boa Vista",
     "Bairro residencial de ruas arborizadas e ótima localização entre o centro de Santo Amaro e o Brooklin, com 2.388 apartamentos à venda no VivaReal. A mediana é de R$ 1,34 milhão para 120 m², cerca de R$ 10,7 mil por m², e a Estação Alto da Boa Vista da Linha 5-Lilás fica a poucos passos."),
    ("granja-julieta", "Granja Julieta",
     "Endereço do Parque Severo Gomes, a principal área verde da região, e da Estação Granja Julieta da CPTM, com 863 apartamentos à venda no VivaReal. A mediana é de R$ 1,28 milhão para 103 m², perto de R$ 12,8 mil por m², com plantas de 2 e 3 quartos e 2 vagas."),
]
PASSOS = [
    ("Defina bairro, orçamento e custos fixos",
     "Use R$ 640 mil e R$ 630 de condomínio como referência. Na venda de apartamento em São Paulo, reserve também o ITBI de 3% cobrado na capital, a escritura e o registro do imóvel."),
    ("Compare transporte e rotina no mapa",
     "Veja a distância até as estações da Linha 5-Lilás e da Linha 9-Esmeralda, até a Avenida Santo Amaro e até o trabalho, na Berrini, na Vila Olímpia ou no Itaim."),
    ("Fale com um corretor parceiro",
     "Pelo WhatsApp, você recebe opções para comprar ou alugar e agenda visitas. O corretor (CRECI) confere a matrícula e as certidões antes da proposta ou do contrato."),
]
FAQ = [
    ("Quanto custa um apartamento em Santo Amaro?",
     "Na amostra de outubro de 2026, o apartamento à venda no distrito teve preço mediano de R$ 640 mil, cerca de R$ 11,2 mil por metro quadrado. Metade dos anúncios ficou entre R$ 383 mil e R$ 880 mil."),
    ("Qual é o valor do condomínio em Santo Amaro?",
     "O condomínio mediano foi de R$ 630 por mês. Em apartamentos de 125 a 189 m², os anúncios da amostra cobravam de R$ 1,4 mil a R$ 2,1 mil por mês."),
    ("Quais bairros de Santo Amaro têm mais apartamentos à venda?",
     "Na região, o Campo Belo soma 9.852 anúncios no VivaReal, o Alto da Boa Vista tem 2.388 e a Granja Julieta, 863. A Chácara Santo Antônio tem 394 apartamentos à venda no QuintoAndar."),
    ("Santo Amaro tem metrô?",
     "Sim. A Linha 5-Lilás tem as estações Santo Amaro, Largo Treze, Adolfo Pinheiro, Alto da Boa Vista e Borba Gato. A Linha 9-Esmeralda da CPTM para em Granja Julieta, João Dias, Santo Amaro, Socorro e Jurubatuba."),
    ("Dá para comprar apartamento em Santo Amaro por até R$ 400 mil?",
     "Sim. Na amostra do VivaReal, 26% dos anúncios custavam até R$ 400 mil. Entre os compactos de 1 e 2 quartos, a mediana foi de R$ 390 mil para 36 m²."),
    ("É possível alugar apartamento em Santo Amaro?",
     "Sim. Os corretores parceiros da Toca de Aluguel também buscam apartamentos para alugar em Santo Amaro, de acordo com o bairro, o orçamento e o prazo, e conduzem a garantia locatícia e o contrato."),
]


def secao(hid, titulo, corpo, extra_cls="space-y-6", sid=""):
    return f"""
            <section{f' id="{sid}"' if sid else ''} aria-labelledby="{hid}" class="{'scroll-mt-32 ' if sid else ''}{extra_cls}">
              <h2
                id="{hid}"
                class="{H2}"
              >
                {titulo}
              </h2>{corpo}
            </section>
"""


def cabecalho():
    atalhos = "".join(f'\n                  <a href="{h}"{f" data-atalho={chr(34)}{d}{chr(34)}" if d else ""} class="{CHIP}">{t}</a>' for d, h, t in ATALHOS)
    seta = lambda lado, d, rot: f"""
                <button
                  type="button"
                  class="absolute {lado} top-1/2 z-10 flex -translate-y-1/2 items-center justify-center rounded-full bg-brand-orange p-2 text-white shadow-lg backdrop-blur-md transition-all hover:scale-110 hover:bg-white hover:text-brand-orange {FOCO}"
                  aria-label="{rot}"
                  aria-controls="carrossel-santo-amaro"
                  onclick="const c = document.getElementById('carrossel-santo-amaro'); c.scrollBy({{ left: {'-' if d < 0 else ''}(c.firstElementChild.offsetWidth + 16), behavior: 'smooth' }})"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{'m15 18-6-6 6-6' if d < 0 else 'm9 18 6-6-6-6'}"/></svg>
                </button>"""
    fotos = "".join(f"""
                  <img
                    src="{FOTOS}/{arq}"
                    alt="{alt}"
                    width="{w}"
                    height="{h}"
                    class="aspect-[2/1] w-[86%] shrink-0 snap-start rounded-2xl sm:aspect-video sm:w-full sm:snap-center sm:rounded-[1.75rem] bg-brand-mist object-cover{' shadow-[0_32px_64px_-24px_rgba(11,31,58,0.35)]' if i == 0 else ''}"
                    decoding="async"
                    {'fetchpriority="high"' if i == 0 else 'loading="lazy"'}
                  />""" for i, (arq, w, h, alt) in enumerate(CARROSSEL))
    return f"""            <header>
              <p
                class="mb-4 text-xs font-semibold uppercase tracking-[0.18em] text-brand-orange"
              >
                Guia de mercado · Santo Amaro, Zona Sul de São Paulo
              </p>
              <h1
                class="text-[1.6rem] font-extrabold leading-[1.12] tracking-[-0.035em] text-blue-950 sm:text-5xl sm:leading-[1.08]"
              >
                {H1}
              </h1>
              <div
                class="mt-4 hidden h-1 w-16 rounded-full bg-brand-orange sm:block"
                aria-hidden="true"
              ></div>
              <p class="mt-5 text-[0.95rem] leading-relaxed text-slate-600 sm:mt-6 sm:text-lg">
                Procurando apartamento em Santo Amaro? Reunimos anúncios reais
                desse distrito da Zona Sul de São Paulo para você comparar preço,
                metragem e bairro antes da visita. Em outubro de 2026, o
                apartamento à venda saiu por
                <strong class="font-semibold text-blue-950">R$ 640 mil</strong>
                na mediana, cerca de
                <strong class="font-semibold text-blue-950">R$ 11,2 mil por m²</strong>.
              </p>

              <dl class="mt-5 grid grid-cols-2 gap-2.5 sm:mt-6 sm:grid-cols-4 sm:gap-3" aria-label="Indicadores dos apartamentos à venda em Santo Amaro">{kpis(KPIS)}
              </dl>

              <nav class="mt-4 sm:mt-5" aria-label="Filtros rápidos de imóveis">
                <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Filtros rápidos</p>
                <div class="mt-2 {ROLAGEM}">{atalhos}
                </div>
              </nav>

              <figure class="mt-6 sm:mt-8">
                <div class="group relative">{seta('left-2 sm:-left-4', -1, 'Foto anterior')}{seta('right-2 sm:-right-4', 1, 'Próxima foto')}
                <div
                  id="carrossel-santo-amaro"
                  class="flex snap-x snap-mandatory gap-4 overflow-x-auto overscroll-x-contain scroll-smooth pb-2 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden {FOCO.replace('ring-offset-2', 'ring-offset-4')} rounded-[1.75rem]"
                  tabindex="0"
                  role="region"
                  aria-roledescription="carrossel"
                  aria-label="Fotos de Santo Amaro e da Zona Sul de São Paulo, deslize para o lado"
                >{fotos}
                </div>
                </div>
                <figcaption
                  class="mt-2 flex items-center justify-center gap-1.5 text-xs font-medium text-slate-500"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3.5 w-3.5" aria-hidden="true"><polyline points="18 8 22 12 18 16"/><polyline points="6 8 2 12 6 16"/><line x1="2" x2="22" y1="12" y2="12"/></svg>
                  Deslize para ver as {len(CARROSSEL)} fotos
                </figcaption>
              </figure>
            </header>
"""


def resumo():
    itens = "".join(f"""
                <li class="flex gap-3">
                  {CHECK}
                  <span>{t}</span>
                </li>""" for t in RESUMO)
    return f"""
            <section
              aria-labelledby="resumo-heading"
              class="rounded-2xl border border-white/50 bg-white/60 p-6 shadow-sm backdrop-blur-md sm:p-8"
            >
              <div class="flex items-center gap-3">
                <span
                  class="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-blue-950 text-brand-orange"
                  aria-hidden="true"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 17 2 2 4-4" /><path d="m3 7 2 2 4-4" /><path d="M13 6h8" /><path d="M13 12h8" /><path d="M13 18h8" /></svg>
                </span>
                <h2
                  id="resumo-heading"
                  class="text-lg font-bold tracking-[-0.02em] text-blue-950"
                >
                  Resumo rápido
                </h2>
              </div>
              <ul
                class="mt-5 space-y-3 text-sm leading-relaxed text-slate-600 sm:text-base"
                role="list"
              >{itens}
              </ul>
            </section>
"""


def precos():
    faixas_banho = [("1 banheiro", 35, 7), ("2 banheiros", 40, 8), ("3 banheiros ou mais", 25, 5)]
    banheiros = "".join(f"""
                  <li>
                    <div class="flex items-baseline justify-between gap-3 text-sm">
                      <span class="font-semibold text-blue-950">{rot}</span>
                      <span class="shrink-0 tabular-nums text-slate-500">{pct}% · {n}</span>
                    </div>
                    <div class="mt-1.5 h-2.5 rounded-full bg-slate-200/70" aria-hidden="true">
                      <div data-barra class="h-2.5 w-[{round(pct / 40 * 100)}%] {BARRA} {'bg-brand-orange' if pct == 40 else 'bg-blue-950/80'}"></div>
                    </div>
                  </li>""" for rot, pct, n in faixas_banho)
    linhas = "".join(f"""
                    <tr>
                      <th scope="row" class="px-5 py-3 font-semibold text-blue-950">{a}</th>
                      <td class="px-5 py-3">{b}</td>
                      <td class="px-5 py-3">{c}</td>
                    </tr>""" for a, b, c in TABELA)
    corpo = f"""
              {P}
                Santo Amaro é um dos maiores mercados de apartamento à venda da
                Zona Sul de São Paulo: só no VivaReal, a busca pelo distrito soma
                8.743 anúncios. A faixa de R$ 230 mil a R$ 3,85 milhões cobre
                desde studios de 24 m² até apartamentos de 4 quartos e 189 m². Há
                opções de 24 m² com 1 quarto e 1 banheiro por
                R$ 360 mil e de 25 m² por R$ 281 mil.
              </p>

{painel(cfg)}
              <div
                class="overflow-x-auto rounded-2xl border border-white/50 bg-white/60 shadow-sm backdrop-blur-md"
              >
                <table class="w-full min-w-[30rem] text-left text-sm">
                  <caption class="sr-only">
                    Indicadores da amostra do VivaReal e dos compactos anunciados no QuintoAndar
                  </caption>
                  <thead class="bg-blue-950 text-white">
                    <tr>
                      <th scope="col" class="px-5 py-3 font-semibold">Indicador</th>
                      <th scope="col" class="px-5 py-3 font-semibold">Santo Amaro · VivaReal</th>
                      <th scope="col" class="px-5 py-3 font-semibold">Compactos · QuintoAndar</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-200/70 text-slate-600">{linhas}
                  </tbody>
                </table>
              </div>
              {P}
                Na prática, metade dos apartamentos em Santo Amaro fica entre
                R$ 383 mil e R$ 880 mil. No QuintoAndar, a vitrine do bairro mostra primeiro os
                compactos de 1 e 2 quartos, com mediana de R$ 390 mil: boa porta
                de entrada para quem quer comprar o primeiro imóvel ou investir
                para alugar. Quem procura apartamento para comprar abaixo de
                R$ 500 mil encontra unidades de 30 m², 43 m² e até 58 m² com 1
                vaga na garagem.
              </p>
              <div class="{GLASS} p-5 sm:p-6">
                <h3 class="text-base font-bold tracking-[-0.02em] text-blue-950">
                  Banheiros e suítes nos anúncios
                </h3>
                <p class="mt-1 text-xs text-slate-500">Percentual e número de anúncios por banheiros (20 anúncios da página 3 do VivaReal)</p>
                <ul class="mt-5 space-y-3.5" role="list">{banheiros}
                </ul>
                <p class="mt-4 text-sm leading-relaxed text-slate-600">
                  Exemplos reais: 32 m² com 1 quarto, 1 banheiro e 1 vaga por
                  R$ 358 mil; 57 m² com 2 quartos e 1 banheiro por R$ 420 mil; e
                  136 m² com 3 suítes e 5 banheiros por R$ 1,75 milhão. Quem
                  precisa de apartamento com 1 suíte encontra plantas de 96 m² a
                  209 m² entre R$ 1,23 milhão e R$ 1,8 milhão.
                </p>
              </div>
              {NOTA}
                Metodologia: levantamento da Toca de Aluguel em 30 de outubro de
                2026 com anúncios públicos de apartamentos à venda — 27 anúncios
                únicos da busca do VivaReal por Santo Amaro (8.743 no total), mais
                20 da página 3 para banheiros e suítes, e 21
                anúncios da busca do QuintoAndar no bairro (106 no total), que
                prioriza imóveis compactos. Valores de referência; preço final e
                condições são confirmados pelo corretor responsável.
              </p>"""
    return secao("precos-heading", "Quanto custa um apartamento em Santo Amaro: preço, m² e condomínio", corpo)


def perfis():
    cards = "".join(f"""
                <div
                  id="bairro-{slug}"
                  class="scroll-mt-32 rounded-2xl border border-white/50 bg-white/60 p-6 shadow-sm backdrop-blur-md"
                >
                  {PIN}
                  <h3
                    class="mt-3 text-base font-bold tracking-[-0.02em] text-blue-950"
                  >
                    {nome}
                  </h3>
                  <p class="mt-2 text-sm leading-relaxed text-slate-600">
                    {txt}
                  </p>
                  <a href="#mapa-cidade" data-mapa="{nome}, São Paulo - SP" data-mapa-zoom="14" class="{LINK} mt-1 text-sm">{nome} no mapa</a>
                </div>""" for slug, nome, txt in PERFIS)
    corpo = f"""
              {P}
                Quatro regiões concentram a procura por apartamento em Santo
                Amaro fora do centro histórico: a Chácara Santo Antônio, o eixo da
                Borba Gato, o Alto da Boa Vista e a Granja Julieta.
              </p>
              <div class="grid gap-6 sm:grid-cols-2">{cards}
              </div>
              {P}
                Socorro e Jurubatuba, ao sul, e Vila Andrade e Panamby, do outro
                lado do Rio Pinheiros, também têm apartamento à venda. Nesses
                bairros, peça ao corretor parceiro os valores atuais de cada
                imóvel antes de agendar a visita.
              </p>"""
    return secao("bairros-heading", "Bairros com mais oferta de apartamento à venda em Santo Amaro", corpo)


def video():
    corpo = f"""
              <div
                class="rounded-3xl border border-white/50 bg-white/60 p-4 shadow-[0_20px_40px_-28px_rgba(11,31,58,0.35)] backdrop-blur-md sm:p-6"
              >
                <div class="aspect-video w-full overflow-hidden rounded-2xl bg-blue-950 shadow-lg">
                  <iframe
                    width="560"
                    height="315"
                    src="https://www.youtube.com/embed/i07W9cXBIK8?si=cb1pyAcGWgplYdQ6"
                    title="YouTube video player"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    referrerpolicy="strict-origin-when-cross-origin"
                    allowfullscreen
                    class="block h-full w-full"
                    loading="lazy"
                  ></iframe>
                </div>
                <p class="mt-5 text-sm leading-relaxed text-slate-600 sm:text-base">
                  Antes de escolher o seu apartamento em Santo Amaro, dê o play e
                  conheça as ruas, o comércio e o ritmo do bairro. Em poucos
                  minutos, você sente se a região combina com a sua rotina e
                  chega à visita mais seguro da decisão.
                </p>
              </div>"""
    return secao("video-heading", "Conheça Santo Amaro em vídeo antes da visita", corpo)


def comodidades():
    maior = max(p for _, p, _ in COMODIDADES)
    lis = "".join(f"""
                <li>
                  <div class="flex items-baseline justify-between gap-3 text-sm">
                    <span class="font-semibold text-blue-950">{rot}</span>
                    <span class="shrink-0 tabular-nums text-slate-500">{pct}% · {fonte}</span>
                  </div>
                  <div class="mt-1.5 h-2.5 rounded-full bg-slate-200/70" aria-hidden="true">
                    <div data-barra class="h-2.5 w-[{round(pct / maior * 100)}%] {BARRA} {'bg-brand-orange' if pct == maior else 'bg-blue-950/80'}"></div>
                  </div>
                </li>""" for rot, pct, fonte in COMODIDADES)
    corpo = f"""
              {P}
                Vaga na garagem é quase regra: aparece em 93% dos anúncios do
                VivaReal. Nos compactos do QuintoAndar, apartamento mobiliado,
                aceita pets e piscina no condomínio são os diferenciais que mais
                se repetem, em combinações como varanda e churrasqueira ou 2
                quartos e piscina no condomínio.
              </p>
              <ul class="{GLASS} space-y-3.5 p-5 sm:p-6" role="list" aria-label="Comodidades dos apartamentos à venda em Santo Amaro">{lis}
              </ul>
              {P}
                A proximidade do metrô não é um filtro dos portais, por isso não
                entra nas barras. Mas o endereço conta: a Avenida Adolfo Pinheiro,
                por onde passa a Linha 5-Lilás, e a Avenida João Dias somam 8 dos
                27 anúncios da amostra. Para morar próximo à estação, use o mapa
                e meça a distância até a parada mais perto.
              </p>
              {NOTA}
                Fonte: vaga na garagem em 27 anúncios do VivaReal; demais itens
                nos títulos de 21 anúncios de compactos do QuintoAndar.
              </p>"""
    return secao("comodidades-heading", "Comodidades mais buscadas: vaga na garagem, varanda, piscina no condomínio, metrô e aceita pets", corpo)


def como():
    itens = "".join(f"""
                <li
                  class="flex gap-4 rounded-2xl border border-white/50 bg-white/60 backdrop-blur-md p-5"
                >
                  <span
                    class="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-950 text-sm font-bold text-white"
                    aria-hidden="true"
                    >{i}</span
                  >
                  <div>
                    <h3 class="text-base font-bold tracking-[-0.02em] text-blue-950">
                      {t}
                    </h3>
                    <p class="mt-1 text-sm leading-relaxed text-slate-600">
                      {d}
                    </p>
                  </div>
                </li>""" for i, (t, d) in enumerate(PASSOS, 1))
    return secao("como-comprar-heading", "Como comprar ou alugar apartamento em Santo Amaro, Zona Sul de SP", f"""
              <ol class="space-y-4" role="list">{itens}
              </ol>""")


def faq():
    itens = "".join(f"""
                <details
                  class="group rounded-2xl border border-white/50 bg-white/60 p-5 backdrop-blur-md open:bg-white/80"
                >
                  <summary
                    class="flex cursor-pointer list-none items-center justify-between gap-4 rounded-lg text-base font-bold tracking-[-0.02em] text-blue-950 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-orange"
                  >
                    {q}
                    {SETA}
                  </summary>
                  <p class="mt-3 text-sm leading-relaxed text-slate-600">
                    {a}
                  </p>
                </details>""" for q, a in FAQ)
    return secao("faq-heading", "Perguntas frequentes sobre apartamento em Santo Amaro", f"""
              <div class="space-y-3">{itens}
              </div>""")


def conclusao():
    return f"""
            <section
              aria-labelledby="conclusao-heading"
              class="rounded-3xl bg-blue-950 p-8 text-slate-300 shadow-[0_32px_64px_-24px_rgba(11,31,58,0.5)] sm:p-10"
            >
              <h2
                id="conclusao-heading"
                class="text-2xl font-extrabold tracking-[-0.03em] text-white sm:text-3xl"
              >
                Conclusão: seu apartamento em Santo Amaro está a uma conversa
              </h2>
              <p class="mt-4 text-sm leading-relaxed sm:text-base">
                Com localização privilegiada, preço mediano de R$ 640 mil, metrô e
                trem no bairro e oferta
                que vai dos compactos do Largo Treze aos apartamentos amplos do
                Alto da Boa Vista, Santo Amaro tem opções para cada orçamento.
                Conte ao corretor parceiro o que você procura e receba as
                melhores ofertas para comprar ou alugar.
              </p>
              <a
                href="{wa(MSG)}"
                target="_blank"
                rel="noopener noreferrer"
                class="mt-6 inline-flex items-center gap-2 rounded-xl bg-[#25D366] px-6 py-3.5 text-sm font-bold text-white shadow-[0_14px_34px_-10px_rgba(37,211,102,0.85)] transition-all duration-200 {WA_HOVER} {WA_PULSO} focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#25D366] focus-visible:ring-offset-2 focus-visible:ring-offset-blue-950 active:scale-95"
              >
                {BALAO}
                Falar com corretor no WhatsApp
              </a>
            </section>
"""


def lateral():
    return f"""
          <aside class="lateral hidden lg:col-span-4 lg:block" aria-label="Falar com corretor">
            <div
              class="sticky top-32 rounded-3xl border border-orange-500/40 bg-white/90 p-6 shadow-[0_0_40px_-10px_rgba(249,115,22,0.35)] backdrop-blur-lg transition-shadow duration-300 hover:shadow-[0_0_48px_-6px_rgba(249,115,22,0.5)]"
            >
              <p
                class="text-xs font-semibold uppercase tracking-[0.16em] text-brand-orange"
              >
                Atendimento exclusivo
              </p>
              <p class="mt-2 text-xl font-extrabold tracking-[-0.02em] text-blue-950">
                Apartamentos em Santo Amaro
              </p>
              <p class="mt-3 text-sm leading-relaxed text-slate-600">
                Quer comprar ou alugar um apartamento? Fale com nossos corretores
                parceiros e receba opções selecionadas para o seu perfil.
              </p>
              <dl class="mt-5 space-y-2 border-y border-slate-200/70 py-4 text-sm">
                <div class="flex justify-between gap-4">
                  <dt class="text-slate-500">Preço mediano</dt>
                  <dd class="font-semibold text-blue-950">R$ 640 mil</dd>
                </div>
                <div class="flex justify-between gap-4">
                  <dt class="text-slate-500">m² mediano</dt>
                  <dd class="font-semibold text-blue-950">R$ 11,2 mil</dd>
                </div>
                <div class="flex justify-between gap-4">
                  <dt class="text-slate-500">Condomínio mediano</dt>
                  <dd class="font-semibold text-blue-950">R$ 630</dd>
                </div>
              </dl>
              <a
                href="{wa(MSG)}"
                target="_blank"
                rel="noopener noreferrer"
                class="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-[#25D366] px-5 py-3.5 text-sm font-bold text-white shadow-[0_14px_34px_-10px_rgba(37,211,102,0.85)] transition-all duration-200 {WA_HOVER} {WA_PULSO} focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#25D366] focus-visible:ring-offset-2 active:scale-[0.98]"
              >
                {BALAO}
                Falar com corretor no WhatsApp
              </a>
              <p class="mt-3 text-center text-xs text-slate-400">
                Atendimento com corretores parceiros (CRECI)
              </p>
            </div>
          </aside>"""


def jsonld():
    org = {
        "@type": "RealEstateAgent", "@id": "https://www.tocadealuguel.com.br/#organization", "name": "Toca de Aluguel", "url": "https://www.tocadealuguel.com.br/",
        "logo": "https://www.tocadealuguel.com.br/assets/logo.png", "image": "https://www.tocadealuguel.com.br/assets/logo.png",
        "description": "Imobiliária digital que conecta quem busca apartamento em Santo Amaro, São Paulo, para comprar ou alugar, a corretores parceiros com CRECI, com atendimento direto pelo WhatsApp.",
        "telephone": "+5589959014753", "sameAs": ["https://wa.me/5589959014753"],
        "contactPoint": {"@type": "ContactPoint", "telephone": "+5589959014753", "contactType": "customer service", "availableLanguage": ["Portuguese"], "areaServed": "BR"},
        "areaServed": [{"@type": "Country", "name": "Brasil"}, {"@type": "City", "name": "São Paulo", "containedInPlace": {"@type": "State", "name": "São Paulo"}}],
        "knowsAbout": ["apartamento em Santo Amaro", "apartamento à venda em Santo Amaro", "imóveis na Zona Sul de São Paulo", "venda e locação de apartamentos"],
        "priceRange": "$$",
    }
    grafo = [
        org,
        {"@type": "WebSite", "@id": "https://www.tocadealuguel.com.br/#website", "name": "Toca de Aluguel", "url": "https://www.tocadealuguel.com.br/", "inLanguage": "pt-BR",
         "publisher": {"@id": "https://www.tocadealuguel.com.br/#organization"}},
        {"@type": "BreadcrumbList", "@id": f"{URL}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://www.tocadealuguel.com.br/"},
            {"@type": "ListItem", "position": 2, "name": "Apartamento em Santo Amaro", "item": URL}]},
        {"@type": "Article", "@id": f"{URL}#article", "headline": H1,
         "description": "Guia de mercado com preço mediano, metro quadrado, condomínio, bairros e comodidades dos apartamentos à venda e para alugar em Santo Amaro, São Paulo.",
         "image": f"https://www.tocadealuguel.com.br/assets/REVIEW/SANTO-AMARO/{CARROSSEL[0][0]}",
         "datePublished": "2026-10-30T08:00:00-03:00", "dateModified": "2026-10-30T20:00:00-03:00", "inLanguage": "pt-BR",
         "author": {"@id": "https://www.tocadealuguel.com.br/#organization"}, "publisher": {"@id": "https://www.tocadealuguel.com.br/#organization"},
         "isPartOf": {"@id": "https://www.tocadealuguel.com.br/#website"}, "mainEntityOfPage": URL,
         "about": {"@type": "Place", "name": "Santo Amaro", "containedInPlace": {"@type": "City", "name": "São Paulo"}}},
        {"@type": "FAQPage", "@id": f"{URL}#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    corpo = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)
    return "    <script type=\"application/ld+json\">\n" + "\n".join("      " + l for l in corpo.splitlines()) + "\n    </script>\n"


DESKTOP = 'class="block rounded-lg px-2 py-1.5 text-sm text-slate-700 transition-colors hover:bg-brand-sand hover:text-brand-orange focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-orange focus-visible:ring-offset-2"'
DESKTOP_ATUAL = 'aria-current="page" class="block rounded-lg px-2 py-1.5 text-sm font-semibold text-brand-orange transition-colors hover:bg-brand-sand hover:text-brand-orange focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-orange focus-visible:ring-offset-2"'
MOVEL = 'class="flex items-center justify-between gap-3 rounded-xl border border-slate-200/70 bg-white px-4 py-3.5 transition-all active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-orange focus-visible:ring-offset-2"'
MOVEL_ATUAL = 'aria-current="page" class="flex items-center justify-between gap-3 rounded-xl border border-brand-orange/50 bg-orange-50 px-4 py-3.5 transition-all active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-orange focus-visible:ring-offset-2"'


def inserir_links(s, atual):
    if f'href="/{SLUG}"' in s:
        return s
    d = f"""
                    <li>
                      <a href="/{SLUG}" {DESKTOP_ATUAL if atual else DESKTOP}>São Paulo (Santo Amaro)</a>
                    </li>"""
    s, k = re.subn(r'(<a href="/casas-alphaville-fortaleza"[^>]*>Fortaleza \(Alphaville\)</a>\n\s*</li>)', lambda m: m.group(1) + d, s)
    assert k == 1, ("desktop", k)
    m_ = f"""
              <li>
                <a href="/{SLUG}" {MOVEL_ATUAL if atual else MOVEL}>
                  <span>
                    <span class="block text-base font-semibold text-blue-950">São Paulo (Santo Amaro)</span>
                    <span class="block text-xs text-slate-500">Apartamentos à venda · SP</span>
                  </span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0 text-brand-orange" aria-hidden="true"><path d="m9 18 6-6-6-6" /></svg>
                </a>
              </li>"""
    s, k = re.subn(r'(<a href="/casas-alphaville-fortaleza" (?:aria-current="page" )?class="flex items-center.*?</a>\n\s*</li>)', lambda m: m.group(1) + m_, s, flags=re.S)
    assert k == 1, ("movel", k)
    r = """
            <li>
              <a
                href="/apartamento-santo-amaro"
                class="transition-colors hover:text-brand-orange focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-orange"
                >Apartamentos à venda em Santo Amaro (SP)</a
              >
            </li>"""
    s, k = re.subn(r'(href="/apartamentos-porto-alegre"\n\s*class="transition-colors[^"]*"\n\s*>Apartamentos para alugar em Porto Alegre</a\n\s*>\n\s*</li>)', lambda m: m.group(1) + r, s)
    assert k == 1, ("rodape", k)
    return s


def gerar():
    rio = (RAIZ / "coberturas-rio-de-janeiro.html").read_text(encoding="utf-8")
    head = f"""    <title>{TITULO}</title>
    <meta
      name="description"
      content="{DESC}"
    />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="theme-color" content="#0B1F3A" />
    <meta property="og:type" content="article" />
    <meta property="og:locale" content="pt_BR" />
    <meta property="og:site_name" content="Toca de Aluguel" />
    <meta
      property="og:title"
      content="{TITULO}"
    />
    <meta
      property="og:description"
      content="Guia de mercado: preços, bairros, condomínio e comodidades dos apartamentos à venda e para alugar em Santo Amaro, Zona Sul de São Paulo."
    />
    <meta
      property="og:image"
      content="https://www.tocadealuguel.com.br/assets/REVIEW/SANTO-AMARO/{CARROSSEL[0][0]}"
    />
    <meta name="twitter:card" content="summary_large_image" />
    <link
      rel="canonical"
      href="{URL}"
    />
"""
    a, b = rio.index("    <title>"), rio.index('    <link rel="icon"')
    s = rio[:a] + head + rio[b:]
    a = s.index('    <script type="application/ld+json">')
    b = s.index("    </script>\n", a) + len("    </script>\n")
    s = s[:a] + jsonld() + s[b:]

    s = s.replace('<a href="/coberturas-rio-de-janeiro" aria-current="page" class="block rounded-lg px-2 py-1.5 text-sm font-semibold text-brand-orange',
                  '<a href="/coberturas-rio-de-janeiro" class="block rounded-lg px-2 py-1.5 text-sm text-slate-700', 1)
    s = s.replace('<a href="/coberturas-rio-de-janeiro" aria-current="page" class="flex items-center justify-between gap-3 rounded-xl border border-brand-orange/50 bg-orange-50',
                  '<a href="/coberturas-rio-de-janeiro" class="flex items-center justify-between gap-3 rounded-xl border border-slate-200/70 bg-white', 1)
    assert 'aria-current="page"' not in s[:s.index("<main")], "menu do Rio ainda marcado"
    s = inserir_links(s, atual=True)

    cfg["corte_preco"] = 500000
    artigo = (cabecalho() + destaques(cfg) + resumo() + precos() + vizinhos(cfg) + perfis() + mapa(cfg) + video() + comodidades() + como() + faq() + conclusao())
    a = s.index('            <li aria-current="page" class="font-semibold text-blue-950">')
    b = s.index("            </li>", a)
    s = s[:a] + '            <li aria-current="page" class="font-semibold text-blue-950">\n              Apartamento em Santo Amaro\n' + s[b:]
    a = s.index("            <header>\n", s.index('<article class="min-w-0'))
    b = s.rindex("\n          </article>", 0, s.index('<aside class="lateral')) + 1
    s = s[:a] + artigo + s[b:]
    a = s.index('\n          <aside class="lateral')
    b = s.index("          </aside>", a) + len("          </aside>")
    s = s[:a] + lateral() + s[b:]

    rio_wa = re.search(r'https://wa\.me/5589959014753\?text=[^"]*corretor\.', rio).group(0)
    s = s.replace(rio_wa, wa(MSG))
    corpo = s[s.index("<main"):s.index("<footer")]
    assert not re.search(r"Rio%20de%20Janeiro|Rio de Janeiro|cobertura", corpo), "conteúdo do Rio sobrou"
    s = s.replace("preco <= 3000000 : preco > 3000000", "preco <= 500000 : preco > 500000")
    s = s.replace("${cards.length} coberturas`", "${cards.length} apartamentos`")
    assert "3000000" not in s and "coberturas`" not in s
    destino = RAIZ / f"{SLUG}.html"
    destino.write_text(s, encoding="utf-8")
    print("gerado", destino.name, len(s))


def menus():
    for f in sorted(RAIZ.glob("*.html")):
        if f.name == f"{SLUG}.html":
            continue
        s = f.read_text(encoding="utf-8")
        if "casas-alphaville-fortaleza" not in s:
            continue
        novo = inserir_links(s, atual=False)
        if novo != s:
            f.write_text(novo, encoding="utf-8")
            print("menu atualizado:", f.name)


if __name__ == "__main__":
    gerar()
    if "--menus" in sys.argv:
        menus()
