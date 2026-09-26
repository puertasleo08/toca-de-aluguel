# Stack e bibliotecas — referência completa

A era de bibliotecas monolíticas (Material UI, Bootstrap) ficou para trás. O ecossistema atual é baseado em **código sob seu controle** (copy-paste) e **primitivas headless** (acessibilidade pronta, estilo livre).

## Base estrutural e formulários

- **shadcn/ui** — a base padrão da indústria. Usa Radix UI (acessibilidade nativa) + Tailwind. O código fica dentro do projeto para customização total, sem lock-in de pacote externo. Ponto de partida padrão para qualquer projeto novo.
- **Radix UI Primitives / Base UI** — garante navegação por teclado, foco preso em modais e acessibilidade ARIA sem precisar codificar do zero. shadcn/ui é construído sobre isso; use diretamente quando precisar de um primitivo que o shadcn/ui não cobre.

## Acabamento visual e microinterações

Use estas bibliotecas para o que shadcn/ui não cobre — elas resolvem especificamente o problema de "cara de template":

- **Magic UI** — biblioteca open-source voltada para Design Engineers, com mais de 150 componentes focados em landing pages: efeitos de brilho, bordas animadas, grids. Ideal para hero sections e páginas de marketing.
- **Aceternity UI** — focada em efeitos 3D, spotlight cards, tracing beams e backgrounds dinâmicos. Transforma uma página simples em algo com apelo visual imediato; usar com moderação (um efeito de destaque por página, não vários).
- **Origin UI** — variações refinadas de inputs, botões, sliders e selects baseados em shadcn/ui, com detalhes de UX já resolvidos. Bom para elevar formulários que ficariam genéricos com o shadcn/ui puro.
- **Motion Primitives** — componentes animados com Motion prontos para copiar e colar, focados em microinterações refinadas (não em efeitos grandes).

## Ícones

- **Lucide Icons** — conjunto limpo, consistente e leve. Padrão de fato quando o projeto já usa Tailwind/shadcn.
- **Phosphor Icons** — melhor quando o app precisa de estilos variados (bold, duotone, thin) para diferenciar hierarquia por peso do ícone, não só por tamanho.

## Cores e contraste

- **Radix Colors / Tailwind Neutral** — evite preto absoluto (`#000`) em telas inteiras; prefira escalas neutras balanceadas (`slate`, `zinc`, `neutral`), que têm contraste calibrado em cada step da escala.
- **Coolors** e **Realtime Colors** — para testar contraste e esquemas de cor diretamente sobre wireframes reais antes de codificar, evitando escolher paleta só olhando swatches isolados.

## Quando usar o quê

| Necessidade | Biblioteca |
|---|---|
| Base de componentes de um projeto novo | shadcn/ui |
| Primitivo de acessibilidade que falta no shadcn/ui | Radix UI Primitives |
| Hero section / landing page com brilho e bordas animadas | Magic UI |
| Efeito 3D / spotlight / background dinâmico (com moderação) | Aceternity UI |
| Input/select/slider mais refinado que o shadcn/ui puro | Origin UI |
| Microinteração pontual (não um efeito grande) | Motion Primitives |
| Ícones em app padrão Tailwind | Lucide Icons |
| Ícones com necessidade de variação de peso/estilo | Phosphor Icons |
| Paleta neutra de base | Radix Colors / Tailwind Neutral |
| Validar contraste antes de codificar | Coolors / Realtime Colors |
