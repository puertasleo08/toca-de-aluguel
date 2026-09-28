(() => {
  const ROTAS = [
    {
      nome: "Apartamentos em Porto Alegre",
      url: "/apartamentos-porto-alegre",
      detalhe: "Aluguel residencial · RS",
      tags: "poa rs rio grande do sul apartamento apartamentos",
    },
    {
      nome: "Apartamentos em Curitiba",
      url: "/apartamentos-curitiba",
      detalhe: "Aluguel residencial · PR",
      tags: "cwb pr parana apartamento apartamentos",
    },
    {
      nome: "Casas em Ubatuba",
      url: "/casas-ubatuba",
      detalhe: "Temporada e férias · SP",
      tags: "sp litoral norte praia temporada ferias casa casas",
    },
    {
      nome: "Anunciar: leads para corretores",
      url: "/anunciar",
      detalhe: "Para corretores e imobiliárias",
      tags: "anunciar corretor corretores imobiliaria leads captacao trafego",
    },
  ];

  const IGNORAR = new Set(["de", "da", "do", "das", "dos", "em", "no", "na", "para", "pra", "a", "o", "e", "alugar", "aluguel"]);
  const normalizar = (texto) =>
    texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();

  const filtrar = (consulta) => {
    const termos = normalizar(consulta).split(/\s+/).filter((t) => t && !IGNORAR.has(t));
    if (!termos.length) return ROTAS;
    return ROTAS.filter((rota) => {
      const alvo = normalizar(`${rota.nome} ${rota.detalhe} ${rota.tags}`);
      return termos.every((t) => alvo.includes(t));
    });
  };

  const icone = () => {
    const ns = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("width", "16");
    svg.setAttribute("height", "16");
    svg.setAttribute("fill", "none");
    svg.setAttribute("stroke", "currentColor");
    svg.setAttribute("stroke-width", "2");
    svg.setAttribute("stroke-linecap", "round");
    svg.setAttribute("stroke-linejoin", "round");
    svg.setAttribute("aria-hidden", "true");
    const path = document.createElementNS(ns, "path");
    path.setAttribute("d", "M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0");
    const circle = document.createElementNS(ns, "circle");
    circle.setAttribute("cx", "12");
    circle.setAttribute("cy", "10");
    circle.setAttribute("r", "3");
    svg.append(path, circle);
    return svg;
  };

  document.querySelectorAll("[data-search]").forEach((raiz) => {
    const form = raiz.querySelector("form");
    const input = raiz.querySelector("[data-search-input]");
    const lista = raiz.querySelector("[data-search-list]");
    let resultados = [];
    let ativo = -1;

    const fechar = () => {
      lista.hidden = true;
      input.setAttribute("aria-expanded", "false");
      input.removeAttribute("aria-activedescendant");
      ativo = -1;
    };

    const marcar = (indice) => {
      const opcoes = lista.querySelectorAll("[role='option']");
      opcoes.forEach((op, i) => {
        const selecionada = i === indice;
        op.setAttribute("aria-selected", String(selecionada));
        op.firstElementChild.classList.toggle("bg-white", selecionada);
        op.firstElementChild.classList.toggle("ring-1", selecionada);
      });
      ativo = indice;
      if (indice >= 0 && opcoes[indice]) {
        input.setAttribute("aria-activedescendant", opcoes[indice].id);
        opcoes[indice].scrollIntoView({ block: "nearest" });
      } else {
        input.removeAttribute("aria-activedescendant");
      }
    };

    const renderizar = () => {
      resultados = filtrar(input.value);
      lista.replaceChildren();

      if (!resultados.length) {
        const vazio = document.createElement("li");
        vazio.setAttribute("role", "presentation");
        vazio.className = "px-3 py-3 text-sm text-slate-500";
        vazio.textContent = `Nenhuma página para “${input.value.trim()}”. Fale com um corretor pelo WhatsApp.`;
        lista.append(vazio);
      }

      resultados.forEach((rota, i) => {
        const item = document.createElement("li");
        item.id = `${lista.id}-${i}`;
        item.setAttribute("role", "option");
        item.setAttribute("aria-selected", "false");

        const link = document.createElement("a");
        link.href = rota.url;
        link.tabIndex = -1;
        link.className =
          "flex items-center gap-3 rounded-xl px-3 py-2.5 ring-brand-orange/30 transition-colors hover:bg-white/90";

        const badge = document.createElement("span");
        badge.className =
          "inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-blue-950 text-brand-orange";
        badge.append(icone());

        const textos = document.createElement("span");
        textos.className = "min-w-0";
        const nome = document.createElement("span");
        nome.className = "block truncate text-sm font-semibold text-blue-950";
        nome.textContent = rota.nome;
        const detalhe = document.createElement("span");
        detalhe.className = "block text-xs text-slate-500";
        detalhe.textContent = rota.detalhe;
        textos.append(nome, detalhe);

        link.append(badge, textos);
        item.append(link);
        lista.append(item);
      });

      lista.hidden = false;
      input.setAttribute("aria-expanded", "true");
      marcar(-1);
    };

    input.addEventListener("input", renderizar);
    input.addEventListener("focus", renderizar);

    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (lista.hidden) renderizar();
        if (!resultados.length) return;
        const passo = e.key === "ArrowDown" ? 1 : -1;
        marcar((ativo + passo + resultados.length) % resultados.length);
      } else if (e.key === "Escape") {
        fechar();
      }
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const destino = resultados[ativo] || filtrar(input.value)[0];
      if (destino) window.location.href = destino.url;
    });

    document.addEventListener("click", (e) => {
      if (!raiz.contains(e.target)) fechar();
    });
  });

  document.querySelectorAll("[data-search-toggle]").forEach((botao) => {
    const painel = document.getElementById(botao.getAttribute("aria-controls"));
    botao.addEventListener("click", () => {
      const abrir = painel.hidden;
      painel.hidden = !abrir;
      botao.setAttribute("aria-expanded", String(abrir));
      if (abrir) painel.querySelector("[data-search-input]").focus();
    });
  });
})();
