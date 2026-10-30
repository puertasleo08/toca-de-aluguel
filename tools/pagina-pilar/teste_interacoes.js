(async () => {
  try {
    const espera = (ms) => new Promise((r) => setTimeout(r, ms));
    const r = {};
    const barra = document.querySelector(".fixed.inset-x-0.bottom-0");
    const util = innerHeight - barra.offsetHeight;
    const fim = (sel) => Math.round(document.querySelector(sel).getBoundingClientRect().bottom);
    r.topo = { util: Math.round(util), fimIndicadores: fim("dl[aria-label]"), fimFiltros: fim('nav[aria-label="Filtros rápidos de imóveis"]') };
    r.largura = document.documentElement.scrollWidth + " de " + document.documentElement.clientWidth;
    const pequenos = [...document.querySelectorAll("main a, main button")].filter((e) => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height < 40 && !e.closest('nav[aria-label="Trilha de navegação"]'); });
    r.alvosMenores40px = pequenos.map((e) => e.textContent.trim().slice(0, 20));

    const status = () => document.getElementById("filtro-status").textContent;
    const total = document.querySelectorAll("[data-quartos]").length;
    r.filtros = {};
    for (const b of document.querySelectorAll("[data-filtro-grupo]")) {
      if (b.dataset.filtroValor === "todos") continue;
      document.getElementById("filtro-limpar").hidden || document.getElementById("filtro-limpar").click();
      b.click();
      r.filtros[b.textContent.trim()] = status().replace("Mostrando ", "");
    }
    document.getElementById("filtro-limpar").click();
    r.limpo = status();
    const atalho = document.querySelector("[data-atalho]");
    atalho.click();
    r.atalho = atalho.textContent.trim() + " -> " + status();
    document.getElementById("filtro-limpar").click();

    const barras = [...document.querySelectorAll("[data-barra]")];
    for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { scrollTo(0, y); await espera(60); }
    await espera(600);
    r.barrasAnimadas = barras.filter((b) => b.style.animationPlayState === "running").length + "/" + barras.length;

    const mapa = document.getElementById("mapa-iframe");
    const quadro = document.getElementById("mapa-quadro");
    r.mapa = {};
    for (const link of [...document.querySelectorAll("a[data-mapa]")].slice(0, 3)) {
      document.getElementById("bairros-vizinhos").scrollIntoView();
      await espera(300);
      link.click();
      await espera(1300);
      const b = quadro.getBoundingClientRect();
      r.mapa[link.textContent.trim()] = decodeURIComponent(mapa.src.split("q=")[1].split("&")[0]) + " | na tela: " + (b.top >= 0 && b.bottom <= innerHeight) + " | botão ativo: " + [...document.querySelectorAll("button[data-mapa][aria-pressed=true]")].map((x) => x.textContent.trim()).join(",");
    }
    r.legenda = document.getElementById("mapa-legenda").textContent;
    r.totalCards = total;
    scrollTo(0, 0);
    await espera(800);
    return JSON.stringify(r, null, 1);
  } catch (e) {
    return "ERRO " + e.message;
  }
})()
