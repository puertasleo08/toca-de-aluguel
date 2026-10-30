"""Aplica a estrutura do piloto apartamentos-curitiba.html a outra página pilar."""
import re
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parents[2]
PILOTO = (RAIZ / "apartamentos-curitiba.html").read_text(encoding="utf-8")

FOCO = "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-orange focus-visible:ring-offset-2"
GLASS = "rounded-2xl border border-white/60 bg-white/70 shadow-sm backdrop-blur-md"
CHIP = f"inline-flex min-h-10 shrink-0 items-center whitespace-nowrap rounded-full border border-blue-950/12 bg-white/80 px-4 py-2 text-sm font-semibold text-blue-950 transition-all hover:border-brand-orange/50 hover:text-brand-orange {FOCO} active:scale-95"
BOTAO = f"inline-flex min-h-10 shrink-0 items-center whitespace-nowrap rounded-full border border-blue-950/12 bg-white px-4 py-2 text-sm font-semibold text-blue-950 transition-all hover:border-brand-orange/50 aria-pressed:border-brand-orange aria-pressed:bg-brand-orange aria-pressed:text-white {FOCO} active:scale-95"
ROLAGEM = "flex gap-2 overflow-x-auto pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
BARRA = "origin-left rounded-full animate-[crescer_1.2s_cubic-bezier(0.22,1,0.36,1)_both] motion-reduce:animate-none"
KPI = "rounded-2xl border border-orange-500/40 bg-white/90 px-3.5 py-3 shadow-[0_0_25px_-5px_rgba(249,115,22,0.25)] backdrop-blur-md transition-all duration-300 animate-[brilho-laranja_4s_ease-in-out_infinite] hover:-translate-y-0.5 hover:border-orange-500/70 hover:shadow-[0_0_32px_-2px_rgba(249,115,22,0.45)] motion-reduce:animate-none sm:p-4"
CARD = "group flex flex-col overflow-hidden rounded-2xl border border-white/70 bg-white/60 shadow-[0_20px_40px_-28px_rgba(11,31,58,0.35)] backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-orange-400/50 hover:shadow-[0_0_34px_-6px_rgba(249,115,22,0.4)]"
VER = f"inline-flex min-h-10 items-center rounded-lg bg-gradient-to-r from-brand-orange to-amber-500 px-3.5 py-2 text-sm font-semibold text-white shadow-[0_8px_20px_-8px_rgba(249,115,22,0.75)] transition-all duration-200 hover:-translate-y-0.5 hover:from-orange-600 hover:to-brand-orange hover:shadow-[0_0_26px_rgba(249,115,22,0.6)] {FOCO} active:scale-95"
WA_HOVER = "hover:-translate-y-0.5 hover:bg-[#1ebe5d] hover:shadow-[0_0_30px_rgba(37,211,102,0.6)]"
WA_PULSO = "animate-[brilho-whatsapp_2.8s_ease-in-out_infinite] motion-reduce:animate-none"
LINK = f"inline-flex min-h-10 items-center font-semibold text-blue-950 underline decoration-brand-orange/40 underline-offset-4 hover:text-brand-orange {FOCO}"
H2 = "text-2xl font-extrabold tracking-[-0.03em] text-blue-950 sm:text-3xl"

CSS = PILOTO[PILOTO.index("      @keyframes crescer {"):PILOTO.index("      details > summary::-webkit-details-marker {")]
i_js = PILOTO.index('    <script>\n      (() => {\n        const lista = document.getElementById("lista-apartamentos");')
JS = PILOTO[i_js:PILOTO.index("    </script>\n", i_js) + len("    </script>\n")]


def wa(texto):
    return "https://wa.me/5589959014753?text=" + quote(texto, safe="")


def brl(v):
    return f"R$ {v:,}".replace(",", ".")


class Pagina:
    def __init__(self, arquivo):
        self.p = RAIZ / arquivo
        self.s = self.p.read_text(encoding="utf-8")

    def trocar(self, velho, novo, n=1):
        assert self.s.count(velho) == n, (self.p.name, self.s.count(velho), velho[:100])
        self.s = self.s.replace(velho, novo)

    def trocar_re(self, padrao, novo, n=1):
        self.s, k = re.subn(padrao, novo, self.s, flags=re.S)
        assert k == n, (self.p.name, k, padrao[:100])

    def secao(self, heading_id):
        i = self.s.index(f'aria-labelledby="{heading_id}"')
        ini = self.s.rindex("            <section", 0, i)
        fim = self.s.index("\n            </section>\n", i) + len("\n            </section>\n")
        return ini, fim

    def salvar(self):
        self.p.write_text(self.s, encoding="utf-8")


def kpis(itens):
    corpo = "".join(f"""
                <div class="{KPI}">
                  <dt class="text-[11px] font-semibold uppercase tracking-wide text-slate-500">{rot}</dt>
                  <dd class="mt-0.5 text-base font-extrabold tracking-[-0.02em] text-blue-950 sm:text-xl">{val}<span class="text-xs font-semibold text-slate-500">{suf}</span></dd>
                </div>""" for rot, val, suf in itens)
    return corpo


def card(c, cidade):
    selo_cls = "bg-brand-orange/95" if c["selo"] == "Alto padrão" else "bg-blue-950/85 backdrop-blur-sm"
    return f"""
                <article
                  data-quartos="{c['q']}"
                  data-preco="{c['preco']}"
                  data-tags="{c['tags']}"
                  class="{CARD}"
                >
                  <div class="relative overflow-hidden">
                    <img
                      src="https://images.unsplash.com/{c['img']}?auto=format&fit=crop&w=800&q=75"
                      alt="{c['alt']}"
                      width="800"
                      height="500"
                      class="aspect-[16/10] w-full object-cover transition-transform duration-500 group-hover:scale-[1.03]"
                      loading="lazy"
                      decoding="async"
                    />
                    <span
                      class="absolute left-3 top-3 rounded-lg {selo_cls} px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wide text-white"
                      >{c['selo']}</span
                    >
                  </div>
                  <div class="flex flex-1 flex-col p-5">
                    <h3 class="text-lg font-bold tracking-[-0.02em] text-blue-950">
                      {c['titulo']}
                    </h3>
                    <p class="mt-1.5 text-sm text-slate-500">
                      {c['sub']}
                    </p>
                    <p class="mt-4 text-sm text-slate-600">
                      {c['det']}
                    </p>
                    <div class="mt-auto flex items-end justify-between gap-3 pt-6">
                      <p>
                        <span
                          class="text-xl font-extrabold tracking-[-0.02em] text-blue-950"
                          >{brl(c['preco'])}</span
                        >
                        <span class="text-sm text-slate-500">{c.get('periodo', '/mês')}</span>
                        <span class="block text-xs text-slate-400"
                          >{c['extra']}</span
                        >
                      </p>
                      <a
                        href="{wa(c['msg'])}"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="{VER}"
                        >Ver Detalhes</a
                      >
                    </div>
                  </div>
                </article>"""


def destaques(cfg):
    grupos = "".join(f"""
                <div class="flex items-center gap-3">
                  <span class="w-16 shrink-0 text-xs font-semibold uppercase tracking-wide text-slate-500">{rot}</span>
                  <div class="{ROLAGEM} min-w-0 flex-1">{''.join(f'''
                    <button type="button" data-filtro-grupo="{g}" data-filtro-valor="{v}" aria-pressed="{'true' if v == 'todos' else 'false'}" class="{BOTAO}">{t}</button>''' for v, t in ops)}
                  </div>
                </div>""" for rot, g, ops in cfg["grupos"])
    n = len(cfg["cards"])
    return f"""
            <section id="destaques" aria-labelledby="destaques-heading" class="scroll-mt-32 space-y-6">
              <h2
                id="destaques-heading"
                class="{H2}"
              >
                {cfg['h2_destaques']}
              </h2>

              <div class="{GLASS} space-y-3 p-3 sm:p-4" role="group" aria-label="Filtrar imóveis em destaque">{grupos}
                <div class="flex items-center justify-between gap-3 border-t border-slate-200/70 pt-3">
                  <p id="filtro-status" class="text-sm text-slate-500" aria-live="polite">Mostrando {n} de {n} {cfg['rotulo_itens']}</p>
                  <button type="button" id="filtro-limpar" class="min-h-10 rounded-lg px-2 text-sm font-semibold text-brand-orange hover:underline {FOCO}" hidden>Limpar filtros</button>
                </div>
              </div>

              <div id="lista-apartamentos" class="grid gap-6 sm:grid-cols-2">{''.join(card(c, cfg['cidade']) for c in cfg['cards'])}
              </div>
              <div id="filtro-vazio" class="rounded-2xl border border-dashed border-slate-300 bg-white/60 p-6 text-center" hidden>
                <p class="text-sm font-semibold text-blue-950">Nenhum destaque com esse perfil agora.</p>
                <p class="mt-1 text-sm text-slate-600">Os corretores parceiros têm mais opções fora desta vitrine.</p>
                <a href="{wa(cfg['msg_vazio'])}" target="_blank" rel="noopener noreferrer" class="mt-4 inline-flex min-h-10 items-center rounded-lg bg-[#25D366] px-4 py-2 text-sm font-semibold text-white shadow-[0_10px_26px_-10px_rgba(37,211,102,0.8)] transition-all duration-200 {WA_HOVER} {FOCO}">Pedir opções no WhatsApp</a>
              </div>
              <p class="text-xs leading-relaxed text-slate-500">
                {cfg['nota_destaques']}
              </p>
            </section>
"""


def painel(cfg):
    maior = max(pct for _, pct, _ in cfg["faixas"])
    faixas = "".join(f"""
                    <li>
                      <div class="flex items-baseline justify-between gap-3 text-sm">
                        <span class="font-semibold text-blue-950">{rot}{f' <span class="ml-1 rounded-full bg-orange-50 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-brand-orange-hot">{cfg["selo_faixa"]}</span>' if pct == maior else ''}</span>
                        <span class="shrink-0 tabular-nums text-slate-500">{pct}% · {n}</span>
                      </div>
                      <div class="mt-1.5 h-2.5 rounded-full bg-slate-200/70" aria-hidden="true">
                        <div data-barra class="h-2.5 w-[{round(pct / maior * 100)}%] {BARRA} {'bg-gradient-to-r from-brand-orange to-amber-400' if pct == maior else 'bg-blue-950/80'}"></div>
                      </div>
                    </li>""" for rot, pct, n in cfg["faixas"])
    cores = ["bg-blue-950", "bg-brand-orange", "bg-amber-400", "bg-emerald-500"]
    segs = "".join(f'<div data-barra class="h-full w-[{pct}%] {cores[i]} {BARRA}"></div>' for i, (_, pct, _) in enumerate(cfg["tipos"]))
    leg = "".join(f"""
                    <li class="flex items-center justify-between gap-3 py-2.5 text-sm">
                      <span class="flex items-center gap-2 font-semibold text-blue-950"><span class="h-2.5 w-2.5 shrink-0 rounded-full {cores[i]}" aria-hidden="true"></span>{rot} <span class="font-normal text-slate-500">({pct}%)</span></span>
                      <span class="shrink-0 text-right tabular-nums text-slate-600">{dir_}</span>
                    </li>""" for i, (rot, pct, dir_) in enumerate(cfg["tipos"]))
    return f"""              <div class="grid gap-4 lg:grid-cols-2">
                <div class="{GLASS} p-5 sm:p-6">
                  <h3 class="text-base font-bold tracking-[-0.02em] text-blue-950">
                    {cfg['h3_faixas']}
                  </h3>
                  <p class="mt-1 text-xs text-slate-500">{cfg['sub_faixas']}</p>
                  <ul class="mt-5 space-y-3.5" role="list">{faixas}
                  </ul>
                </div>
                <div class="{GLASS} p-5 sm:p-6">
                  <h3 class="text-base font-bold tracking-[-0.02em] text-blue-950">
                    {cfg['h3_tipos']}
                  </h3>
                  <p class="mt-1 text-xs text-slate-500">{cfg['sub_tipos']}</p>
                  <div class="mt-5 flex h-4 gap-0.5 overflow-hidden rounded-full bg-slate-200/70" aria-hidden="true">{segs}</div>
                  <ul class="mt-3 divide-y divide-slate-200/70" role="list">{leg}
                  </ul>
                  <p class="mt-3 text-xs leading-relaxed text-slate-500">
                    {cfg['nota_tipos']}
                  </p>
                </div>
              </div>
"""


def vizinhos(cfg):
    itens = []
    for b in cfg["bairros"]:
        links = (f'<a href="#bairro-{b["slug"]}" class="{LINK}">{cfg.get("rotulo_perfil", "Perfil do bairro")}</a>' if b.get("slug") else "")
        links += f'<a href="#mapa-cidade" data-mapa="{b["nome"]}, {cfg["mapa_sufixo"]}" data-mapa-zoom="14" class="{LINK}">{b["nome"]} no mapa</a>'
        selo = b["selo"]
        cor = {"alto": "bg-orange-50 text-brand-orange-hot", "medio": "bg-blue-50 text-blue-900", "baixo": "bg-emerald-50 text-emerald-700"}[b["tom"]]
        itens.append(f"""
                <li class="{GLASS} min-w-0 p-4">
                  <div class="flex items-start justify-between gap-3">
                    <div class="min-w-0">
                      <p class="text-base font-bold tracking-[-0.02em] text-blue-950">{b['nome']}</p>
                      <p class="text-xs text-slate-500">{b['regiao']}</p>
                    </div>
                    <span class="shrink-0 rounded-full px-2 py-0.5 text-[11px] font-bold {cor}">{selo}</span>
                  </div>
                  <p class="mt-3 text-xl font-extrabold tracking-[-0.02em] text-blue-950">{b['valor']}<span class="text-xs font-semibold text-slate-500">{b['valor_suf']}</span></p>
                  <div class="mt-2 h-2 rounded-full bg-slate-200/70" aria-hidden="true">
                    <div data-barra class="h-2 w-[{max(8, round(b[cfg['barra_campo']] / max(x[cfg['barra_campo']] for x in cfg['bairros']) * 100))}%] {BARRA} {'bg-brand-orange' if b['tom'] == 'alto' else 'bg-blue-950/80' if b['tom'] == 'medio' else 'bg-emerald-500'}"></div>
                  </div>
                  <p class="mt-1 flex flex-wrap gap-x-4 text-sm">{links}</p>
                </li>""")
    return f"""
            <section id="bairros-vizinhos" aria-labelledby="vizinhos-heading" class="scroll-mt-32 space-y-6">
              <h2
                id="vizinhos-heading"
                class="{H2}"
              >
                {cfg['h2_vizinhos']}
              </h2>
              <p class="text-sm leading-relaxed text-slate-600 sm:text-base">
                {cfg['txt_vizinhos']}
              </p>
              <ul class="grid grid-cols-1 gap-3 sm:grid-cols-2" role="list">{''.join(itens)}
              </ul>
              <p class="text-xs leading-relaxed text-slate-500">
                {cfg['nota_vizinhos']}
              </p>
            </section>
"""


def mapa(cfg):
    ul = f"-mx-1 mt-3 flex gap-2 overflow-x-auto px-1 pb-1 [scrollbar-width:none] sm:mx-0 sm:flex-wrap sm:overflow-visible sm:px-0 [&::-webkit-scrollbar]:hidden"
    grupos = "".join(f"""
                <div class="min-w-0 {GLASS} p-4">
                  <h3 class="text-sm font-bold tracking-[-0.02em] text-blue-950">{g}</h3>
                  <ul class="{ul}" role="list">{''.join(f'''
                    <li><button type="button" data-mapa="{n}, {cfg['mapa_sufixo']}"{' data-mapa-zoom="14"' if g == 'Bairros' else ''} aria-pressed="false" class="{BOTAO}">{n}</button></li>''' for n in nomes)}
                  </ul>
                </div>""" for g, nomes in cfg["pontos"])
    ini = cfg.get("mapa_inicial", cfg["mapa_sufixo"])
    return f"""
            <section id="mapa-cidade" aria-labelledby="mapa-heading" class="scroll-mt-32 space-y-6">
              <h2
                id="mapa-heading"
                class="{H2}"
              >
                {cfg['h2_mapa']}
              </h2>
              <p class="text-sm leading-relaxed text-slate-600 sm:text-base">
                {cfg['txt_mapa']}
              </p>
              <div class="rounded-3xl border border-white/50 bg-white/60 p-3 shadow-[0_20px_40px_-28px_rgba(11,31,58,0.35)] backdrop-blur-md sm:p-4">
                <div id="mapa-quadro" class="relative aspect-[4/3] w-full scroll-mt-32 overflow-hidden rounded-2xl bg-brand-mist sm:aspect-video">
                  <iframe
                    id="mapa-iframe"
                    src="https://maps.google.com/maps?q={quote(ini)}&z={cfg.get('zoom_inicial', 12)}&output=embed"
                    title="Mapa interativo de {cfg['cidade_uf']} no Google Maps"
                    class="absolute inset-0 h-full w-full border-0"
                    loading="lazy"
                    referrerpolicy="no-referrer-when-downgrade"
                    allowfullscreen
                  ></iframe>
                </div>
                <div class="mt-3 flex flex-wrap items-center justify-between gap-2 px-1 text-xs">
                  <p id="mapa-legenda" class="text-slate-500" aria-live="polite">Exibindo: {cfg['cidade_uf']}</p>
                  <div class="flex items-center gap-4">
                    <button type="button" data-mapa="{ini}" data-mapa-zoom="{cfg.get('zoom_inicial', 12)}" class="min-h-10 font-semibold text-blue-950 hover:text-brand-orange {FOCO}">Visão geral</button>
                    <a id="mapa-externo" href="https://www.google.com/maps/search/?api=1&query={quote(ini)}" target="_blank" rel="noopener noreferrer" class="inline-flex min-h-10 items-center font-semibold text-brand-orange hover:underline {FOCO}">Abrir no Google Maps</a>
                  </div>
                </div>
              </div>
              <div class="grid gap-4 sm:grid-cols-2">{grupos}
              </div>
            </section>
"""


def aplicar(arquivo, cfg):
    pg = Pagina(arquivo)
    t = pg.trocar
    tr = pg.trocar_re

    # CSS e layout do topo
    t("      details > summary::-webkit-details-marker {", CSS + "      details > summary::-webkit-details-marker {")
    t('<article class="space-y-12 lg:col-span-8">', '<article class="min-w-0 space-y-12 lg:col-span-8">')
    t('class="relative mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-14 lg:px-8"', 'class="relative mx-auto max-w-6xl px-4 py-6 sm:px-6 sm:py-14 lg:px-8"')
    t('class="mb-8 text-xs text-slate-500"', 'class="mb-5 text-xs text-slate-500 sm:mb-8"')
    t('class="text-4xl font-extrabold leading-[1.08] tracking-[-0.035em] text-blue-950 sm:text-5xl"',
      'class="text-[1.85rem] font-extrabold leading-[1.1] tracking-[-0.035em] text-blue-950 sm:text-5xl sm:leading-[1.08]"')
    t('class="mt-4 h-1 w-16 rounded-full bg-brand-orange"', 'class="mt-4 hidden h-1 w-16 rounded-full bg-brand-orange sm:block"')
    t('<p class="mt-6 text-base leading-relaxed text-slate-600 sm:text-lg">', '<p class="mt-5 text-[0.95rem] leading-relaxed text-slate-600 sm:mt-6 sm:text-lg">')

    # Indicadores + filtros rápidos depois da introdução
    atalhos = "".join(f'\n                  <a href="{h}"{f" data-atalho={chr(34)}{d}{chr(34)}" if d else ""} class="{CHIP}">{txt}</a>' for d, h, txt in cfg["atalhos"])
    topo = f"""
              <dl class="mt-5 grid grid-cols-2 gap-2.5 sm:mt-6 sm:grid-cols-4 sm:gap-3" aria-label="{cfg['aria_kpis']}">{kpis(cfg['kpis'])}
              </dl>

              <nav class="mt-4 sm:mt-5" aria-label="Filtros rápidos de imóveis">
                <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Filtros rápidos</p>
                <div class="mt-2 {ROLAGEM}">{atalhos}
                </div>
              </nav>
"""
    i = pg.s.index("              </p>\n", pg.s.index(cfg["fim_intro"])) + len("              </p>\n")
    pg.s = pg.s[:i] + topo + pg.s[i:]

    # Carrossel compacto
    t('              <figure class="mt-8">', '              <figure class="mt-6 sm:mt-8">')
    passo = "(c.firstElementChild.offsetWidth + 16)"
    t("c.scrollBy({ left: -c.clientWidth, behavior: 'smooth' })", f"c.scrollBy({{ left: -{passo}, behavior: 'smooth' }})")
    t("c.scrollBy({ left: c.clientWidth, behavior: 'smooth' })", f"c.scrollBy({{ left: {passo}, behavior: 'smooth' }})")
    t('class="flex snap-x snap-mandatory gap-4 overflow-x-auto scroll-smooth pb-2', 'class="flex snap-x snap-mandatory gap-4 overflow-x-auto overscroll-x-contain scroll-smooth pb-2')
    n_fotos = pg.s.count("aspect-video w-full shrink-0 snap-center rounded-[1.75rem]")
    assert n_fotos >= 3, n_fotos
    pg.s = pg.s.replace("aspect-video w-full shrink-0 snap-center rounded-[1.75rem]",
                        "aspect-[2/1] w-[86%] shrink-0 snap-start rounded-2xl sm:aspect-video sm:w-full sm:snap-center sm:rounded-[1.75rem]")

    # Destaques novos (o bloco antigo sai)
    a, b = pg.secao("destaques-heading")
    pg.s = pg.s[:a] + pg.s[b:]
    ini_art = pg.s.index("            </header>\n") + len("            </header>\n")
    pg.s = pg.s[:ini_art] + destaques(cfg) + pg.s[ini_art:]

    # Painel visual de preços no lugar dos cards de fatos
    a = pg.s.index('              <ul\n                class="grid grid-cols-2 gap-4 sm:grid-cols-3"')
    b = pg.s.index("              </ul>\n", a) + len("              </ul>\n")
    pg.s = pg.s[:a] + painel(cfg) + pg.s[b:]
    t('<table class="w-full text-left text-sm">', '<table class="w-full min-w-[30rem] text-left text-sm">')

    # Perfis de bairro com âncoras
    a, b = pg.secao(cfg.get("id_perfis", "bairros-heading"))
    bloco = pg.s[a:b]
    perfil = '                <div\n                  class="rounded-2xl border border-white/50 bg-white/60 p-6 shadow-sm backdrop-blur-md"\n                >'
    assert bloco.count(perfil) == len(cfg["slugs_perfis"]), bloco.count(perfil)
    for slug in cfg["slugs_perfis"]:
        bloco = bloco.replace(perfil, f'                <div\n                  id="bairro-{slug}"\n                  class="scroll-mt-32 rounded-2xl border border-white/50 bg-white/60 p-6 shadow-sm backdrop-blur-md"\n                >', 1)
    pg.s = pg.s[:a] + bloco + vizinhos(cfg) + mapa(cfg) + pg.s[b:]

    # Comodidades em barras, quando houver dado por anúncio
    if cfg.get("comodidades"):
        maior = max(pct for _, pct, _ in cfg["comodidades"])
        lis = "".join(f"""
                <li>
                  <div class="flex items-baseline justify-between gap-3 text-sm">
                    <span class="font-semibold text-blue-950">{rot}</span>
                    <span class="shrink-0 tabular-nums text-slate-500">{pct}% dos anúncios · {n}</span>
                  </div>
                  <div class="mt-1.5 h-2.5 rounded-full bg-slate-200/70" aria-hidden="true">
                    <div data-barra class="h-2.5 w-[{round(pct / maior * 100)}%] {BARRA} {'bg-brand-orange' if pct == maior else 'bg-blue-950/80'}"></div>
                  </div>
                </li>""" for rot, pct, n in cfg["comodidades"])
        a = pg.s.index('              <ul class="flex flex-wrap gap-2.5" role="list">')
        b = pg.s.index("              </ul>\n", a) + len("              </ul>\n")
        pg.s = pg.s[:a] + f'              <ul class="{GLASS} space-y-3.5 p-5 sm:p-6" role="list" aria-label="{cfg["aria_comodidades"]}">{lis}\n              </ul>\n' + pg.s[b:]

    # Seções extras específicas da cidade (ex.: comparativo de tipologias)
    for heading_id, html, depois_de in cfg.get("secoes_extras", []):
        a, b = pg.secao(depois_de)
        pg.s = pg.s[:b] + "\n" + html.strip("\n") + "\n" + pg.s[b:]

    # Brilho nos CTAs de WhatsApp
    def realcar_wa(m):
        cls = m.group(1)
        cls = re.sub(r"shadow-\[[^\]]+\]", "shadow-[0_14px_34px_-10px_rgba(37,211,102,0.85)]", cls)
        cls = cls.replace("hover:bg-[#128C7E]", f"{WA_HOVER} {WA_PULSO}").replace("font-semibold", "font-bold")
        return f'class="{cls}"'

    ini_main, fim_main = pg.s.index('<main id="conteudo"'), pg.s.index("<footer")
    trecho = pg.s[ini_main:fim_main]
    trecho, k = re.subn(r'class="((?:mt-\d+ )?(?:inline-)?flex[^"]*bg-\[#25D366\][^"]*shadow-\[[^"]*hover:bg-\[#128C7E\][^"]*)"', realcar_wa, trecho)
    assert k >= 2, k
    trecho = trecho.replace('class="sticky top-32 rounded-3xl border border-white/60 bg-white/70 p-6 shadow-[0_20px_40px_-28px_rgba(11,31,58,0.35)] backdrop-blur-lg"',
                            'class="sticky top-32 rounded-3xl border border-orange-500/40 bg-white/90 p-6 shadow-[0_0_40px_-10px_rgba(249,115,22,0.35)] backdrop-blur-lg transition-shadow duration-300 hover:shadow-[0_0_48px_-6px_rgba(249,115,22,0.5)]"')
    pg.s = pg.s[:ini_main] + trecho + pg.s[fim_main:]
    barra_movel = pg.s[pg.s.index("</main>"):pg.s.index("<footer")]
    nova = re.sub(r'class="(flex w-full items-center justify-center gap-2 rounded-xl bg-\[#25D366\][^"]*)"', lambda m: realcar_wa(m).replace('class="flex w-full', 'class="flex min-h-12 w-full'), barra_movel, count=1)
    pg.s = pg.s.replace(barra_movel, nova)

    # Ordem final das seções
    ini = pg.s.index("            </header>\n") + len("            </header>\n")
    fim = pg.s.rindex("\n          </article>", 0, pg.s.index('<aside class="lateral')) + 1
    miolo = pg.s[ini:fim]
    blocos = re.findall(r"            <section\b.*?\n            </section>\n", miolo, re.S)
    assert re.sub(r"\s", "", "".join(blocos)) == re.sub(r"\s", "", miolo), "conteúdo fora das seções"
    por_id = {re.search(r'aria-labelledby="([^"]+)"', x).group(1): x for x in blocos}
    assert sorted(cfg["ordem"]) == sorted(por_id), (sorted(por_id), sorted(cfg["ordem"]))
    pg.s = pg.s[:ini] + "\n" + "\n".join(por_id[k] for k in cfg["ordem"]) + pg.s[fim:]

    # Script de interação
    js = JS.replace('const legenda = document.getElementById("mapa-legenda");', 'const legenda = document.getElementById("mapa-legenda");')
    js = js.replace("${local.replace(\" - PR\", \", PR\")}", "${local.replace(/ - ([A-Z]{2})$/, \", $1\")}")
    js = js.replace("`Mostrando ${visiveis} de ${cards.length} apartamentos`", f"`Mostrando ${{visiveis}} de ${{cards.length}} {cfg['rotulo_itens']}`")
    js = js.replace('(estado.preco === "ate3000" ? preco <= 3000 : preco > 3000)', f'(estado.preco === "ate" ? preco <= {cfg["corte_preco"]} : preco > {cfg["corte_preco"]})')
    t('    <script src="./assets/menu.js" defer></script>', js + '    <script src="./assets/menu.js" defer></script>')

    for velho, novo in cfg.get("trocas", []):
        t(velho, novo)
    for item in cfg.get("trocas_re", []):
        tr(*item)
    pg.salvar()
    return pg
