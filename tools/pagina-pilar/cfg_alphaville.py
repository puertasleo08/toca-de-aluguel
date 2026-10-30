import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from replicar import aplicar


def msg(txt):
    return f"Olá! Quero saber sobre {txt} à venda em Alphaville Fortaleza."


cfg = dict(
    cidade="Alphaville Fortaleza",
    cidade_uf="Alphaville Fortaleza, CE",
    mapa_sufixo="CE",
    mapa_inicial="Alphaville Fortaleza, Eusébio - CE",
    zoom_inicial=13,
    fim_intro='<strong class="font-semibold text-blue-950">R$ 3,95 milhões</strong>',
    aria_kpis="Indicadores das casas à venda em Alphaville Fortaleza",
    kpis=[("Preço mediano", "R$ 3,95 mi", ""), ("Entrada", "R$ 2,8 mi", ""), ("m² mediano", "R$ 9,6 mil", ""), ("Área mediana", "435 m²", "")],
    atalhos=[("quartos:4", "#destaques", "4 suítes"), ("quartos:5", "#destaques", "5 suítes"), ("preco:ate", "#destaques", "Até R$ 4 mi"),
             ("extra:piscina", "#destaques", "Com piscina"), ("", "#bairros-vizinhos", "Entorno"), ("", "#mapa-cidade", "Mapa")],
    h2_destaques="Destaques: casas à venda em Alphaville Fortaleza, de 4 e 5 suítes",
    rotulo_itens="casas",
    corte_preco=4000000,
    grupos=[("Suítes", "quartos", [("todos", "Todas"), ("4", "4 suítes"), ("5", "5 suítes")]),
            ("Preço", "preco", [("todos", "Qualquer"), ("ate", "Até R$ 4 mi"), ("acima", "Acima de R$ 4 mi")]),
            ("Extras", "extra", [("piscina", "Com piscina"), ("gourmet", "Espaço gourmet")])],
    msg_vazio="Olá! Vim pela página de casas em Alphaville Fortaleza e quero opções com o meu perfil.",
    nota_destaques="Exemplos com base nas medianas e em anúncios reais da amostra. Disponibilidade, valores e condições de cada casa são confirmados pelo corretor parceiro no atendimento.",
    cards=[
        dict(q=4, preco=2950000, tags="piscina", img="photo-1600585154340-be6161a56a0c", selo="Alto padrão", periodo="", extra="+ condomínio R$ 1.400/mês",
             alt="Casa contemporânea de dois pavimentos com fachada em madeira, grandes vãos de vidro e jardim iluminado, exemplo de casa de alto padrão à venda no Alphaville",
             titulo="Casa 4 Suítes — Alphaville Fortaleza", sub="330 m² · Piscina e churrasqueira · 3 vagas", det="4 quartos (4 suítes) · 5 banheiros · 3 vagas",
             msg=msg("casas de 4 suítes")),
        dict(q=5, preco=2990000, tags="", img="photo-1600596542815-ffad4c1539a9", selo="Venda", periodo="", extra="Condomínio sob consulta",
             alt="Casa em condomínio com área verde e gramado, perfil das casas de 5 suítes à venda em Alphaville Fortaleza na faixa de entrada do mercado",
             titulo="Casa 5 Suítes — Entrada do Mercado", sub="400 m² · 5 suítes pelo preço de 4", det="5 quartos (5 suítes)",
             msg=msg("casas de 5 suítes na faixa de entrada")),
        dict(q=4, preco=3600000, tags="piscina gourmet", img="photo-1512917774080-9991f1c4c750", selo="Venda", periodo="", extra="+ condomínio R$ 1.600/mês",
             alt="Área externa com piscina privativa e portas de vidro para a sala, padrão de lazer das casas em condomínio de luxo em Fortaleza",
             titulo="Casa 4 Suítes com Piscina — Alphaville Fortaleza", sub="420 m² · Varanda gourmet · Lote de 450 m²", det="4 quartos (4 suítes) · 5 banheiros · 4 vagas",
             msg=msg("casas de 4 suítes com piscina")),
        dict(q=5, preco=5300000, tags="gourmet", img="photo-1600047509807-ba8f99d2cdde", selo="Venda", periodo="", extra="+ condomínio R$ 1.800/mês",
             alt="Casa moderna com volume revestido em madeira, gramado e caminho de pedras, estilo das residências de alto padrão no Alphaville em Fortaleza",
             titulo="Casa 5 Suítes — Alphaville Fortaleza", sub="500 m² · Espaço gourmet · Escritório", det="5 quartos (5 suítes) · 6 banheiros · 4 vagas",
             msg=msg("casas de 5 suítes")),
        dict(q=5, preco=6200000, tags="", img="photo-1600566753190-17f0baa2a6c3", selo="Alto padrão", periodo="", extra="+ condomínio R$ 1.800/mês",
             alt="Residência de arquitetura contemporânea com fachada de madeira e vidro e acesso amplo para carros, referência de casa de luxo para comprar em Alphaville",
             titulo="Casa de Luxo 5 Suítes — Alphaville Fortaleza", sub="600 m² · Hidromassagem e lareira · 6 vagas", det="5 quartos (5 suítes) · 7 banheiros · 6 vagas",
             msg=msg("casas de luxo de 5 suítes")),
        dict(q=5, preco=12000000, tags="", img="photo-1613490493576-7fde63acd811", selo="Alto padrão", periodo="", extra="Condomínio sob consulta",
             alt="Sobrado com varanda ampla, referência das casas de luxo de 600 m² à venda no topo do mercado de Alphaville Fortaleza",
             titulo="Casa 5 Suítes — Topo do Mercado", sub="600 m² · A mais cara da amostra", det="5 quartos (5 suítes)",
             msg=msg("casas de luxo no topo do mercado")),
    ],
    h3_faixas="Distribuição de preços das casas",
    sub_faixas="Percentual e número de casas por faixa de preço (20 casas à venda)",
    selo_faixa="mais comum",
    faixas=[("Até R$ 3 milhões", 15, 3), ("R$ 3 a 4 milhões", 35, 7), ("R$ 4 a 5 milhões", 20, 4), ("R$ 5 a 6 milhões", 15, 3), ("R$ 6 milhões ou mais", 15, 3)],
    h3_tipos="Quartos, preço mediano e área das casas",
    sub_tipos="Proporção da amostra e valores medianos de cada tamanho",
    tipos=[("3 quartos", 5, "R$ 4,95 mi · 290 m² · 1 casa"), ("4 quartos", 45, "R$ 3,5 mi · 376 m²"), ("5 quartos", 50, "R$ 5,15 mi · 503 m²")],
    nota_tipos="Metade das casas tem 5 quartos. Na mediana, a 5ª suíte acrescenta cerca de R$ 1,65 milhão ao preço e 127 m² de área construída.",
    id_perfis="territorio-heading",
    slugs_perfis=["residenciais", "cidade-alpha", "entorno"],
    rotulo_perfil="Saiba mais",
    h2_vizinhos="Regiões de influência e bairros vizinhos de Alphaville Fortaleza: Eusébio, Cidade Alpha e 4º Anel",
    txt_vizinhos=("O Alphaville Fortaleza fica no eixo Fortaleza–Eusébio, e a rotina de quem mora ali passa pelo comércio do Eusébio, "
                  "pelo 4º Anel Viário e pelos shoppings da região. Veja o tempo de deslocamento a partir do Alphaville Ceará 5, "
                  "na Cidade Alpha."),
    nota_vizinhos=("Tempos de deslocamento informados pelo Grupo Alphaville a partir do Alphaville Ceará 5, na Cidade Alpha. O trajeto "
                   "real varia conforme o residencial e o trânsito."),
    barra_campo="v",
    bairros=[
        dict(nome="Cidade Alpha", regiao="Eusébio · lançamento Ceará 5", valor="Base", valor_suf=" · ponto de partida", v=1, selo="Território", tom="alto", slug="cidade-alpha"),
        dict(nome="Centro de Eusébio", regiao="Comércio e serviços", valor="5 min", valor_suf=" de carro", v=5, selo="Mais perto", tom="baixo"),
        dict(nome="4º Anel Viário", regiao="Acesso rápido a Fortaleza", valor="6 min", valor_suf=" de carro", v=6, selo="Acesso", tom="baixo"),
        dict(nome="Shopping Eusébio", regiao="Compras e serviços", valor="10 min", valor_suf=" de carro", v=10, selo="Compras", tom="medio"),
        dict(nome="Terrazo Shopping", regiao="Compras e lazer", valor="12 min", valor_suf=" de carro", v=12, selo="Compras", tom="medio"),
    ],
    h2_mapa="Mapa de Alphaville Fortaleza (CE): acessos, compras e lazer",
    txt_mapa=("Confira a distância entre o residencial, a capital e a sua rotina — do 4º Anel Viário à Avenida Washington Soares, que "
              "liga a região aos bairros nobres de Fortaleza. Toque em um ponto de referência para centralizar o mapa."),
    pontos=[("Regiões", ["Alphaville Fortaleza", "Cidade Alpha", "Centro de Eusébio", "Lagoa Redonda"]),
            ("Vias de acesso", ["4º Anel Viário", "CE-040", "Avenida Washington Soares"]),
            ("Compras", ["Shopping Eusébio", "Terrazo Shopping", "Shopping Iguatemi Bosque"]),
            ("Lazer", ["Beach Park", "Praia do Futuro"])],
    ordem=["destaques-heading", "resumo-heading", "precos-heading", "vizinhos-heading", "clube-heading", "territorio-heading",
           "mapa-heading", "video-heading", "como-comprar-heading", "faq-heading", "conclusao-heading"],
    trocas=[('"dateModified": "2026-09-29T08:00:00-03:00"', '"dateModified": "2026-10-30T19:00:00-03:00"')],
)

if __name__ == "__main__":
    aplicar("casas-alphaville-fortaleza.html", cfg)
    print("ok")
