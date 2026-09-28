(() => {
  document.querySelectorAll("[data-menu]").forEach((menu) => {
    const botao = menu.querySelector("[data-menu-button]");
    const definir = (aberto) => {
      botao.setAttribute("aria-expanded", String(aberto));
      menu.toggleAttribute("data-open", aberto);
    };

    botao.addEventListener("click", () => definir(botao.getAttribute("aria-expanded") !== "true"));
    menu.addEventListener("mouseenter", () => botao.setAttribute("aria-expanded", "true"));
    menu.addEventListener("mouseleave", () => definir(false));
    menu.addEventListener("focusout", (e) => {
      if (!menu.contains(e.relatedTarget)) definir(false);
    });
    menu.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        definir(false);
        botao.focus();
      }
    });
    document.addEventListener("click", (e) => {
      if (!menu.contains(e.target)) definir(false);
    });
  });

  document.querySelectorAll("[data-mobile-toggle]").forEach((botao) => {
    const painel = document.getElementById(botao.getAttribute("aria-controls"));
    const definir = (aberto) => {
      painel.hidden = !aberto;
      botao.setAttribute("aria-expanded", String(aberto));
      botao.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
    };

    botao.addEventListener("click", () => definir(painel.hidden));
    painel.addEventListener("click", (e) => {
      if (e.target.closest("a")) definir(false);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !painel.hidden) {
        definir(false);
        botao.focus();
      }
    });
  });
})();
