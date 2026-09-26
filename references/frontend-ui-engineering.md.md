---
name: frontend-ui-engineering
description: Guia de referência para atuar como Tech Lead / Design Engineer na criação e revisão de interfaces front-end — páginas web, painéis administrativos, dashboards, landing pages e design systems. Cobre acabamento visual de nível produto (Linear, Raycast, Vercel, Supabase) para eliminar a "síndrome do template genérico" / "cara de IA", o stack de componentes copy-paste recomendado (shadcn/ui, Radix, Tailwind, Motion) e as práticas de Tech Lead para arquitetura, qualidade de código, performance e governança de time. Usar sempre que o usuário pedir para criar, redesenhar, revisar ou dar feedback sobre uma UI, tela, painel, dashboard, landing page, componente, design system ou "deixar a interface com cara de produto" — mesmo que ele não use as palavras "design" ou "front-end" explicitamente.
---

# Frontend UI Engineering — Guia de Tech Lead / Design Engineer

Este guia assume um papel duplo, porque os dois lados se sustentam mutuamente: **craft visual** (a interface parecer feita por um produto de ponta, não gerada por IA) e **rigor de engenharia** (a base de código escalar, ser mantível e performática). Uma UI bonita sobre uma arquitetura frágil não sobrevive; uma arquitetura sólida com UI genérica não convence ninguém a usar o produto.

## Quando aplicar este guia

- Criar ou redesenhar telas, páginas, painéis, dashboards ou componentes.
- Revisar/dar feedback em uma UI já existente ("por que isso parece feito por IA?").
- Definir ou avaliar o stack de front-end de um projeto.
- Decisões de arquitetura, qualidade de código, performance ou processo de um time/projeto de front-end.
- Buscar referências visuais ou ferramentas de prototipação.

## 1. Diagnóstico rápido: a "síndrome do template genérico"

O maior sintoma de uma UI feita em modo "vibe coding" sem direção de design é: inputs cinzas sem padding de respiro, `border-radius` padrão do framework, fontes genéricas do sistema (ou Roboto solta sem peso definido), ausência de microinterações, e cores lavadas sem hierarquia visual. Antes de escrever qualquer código de UI, identifique se o resultado provável cairia nesse padrão — se sim, aplique os 4 pilares abaixo antes de continuar.

O segredo não é reinventar a roda a cada projeto, e sim usar o stack de Design Engineering certo (seção 3) com intenção nos 4 pilares abaixo.

## 2. Os 4 pilares visuais (acabamento de produto)

### 2.1 Tipografia com caráter
Abandone as fontes padrão do framework. A identidade de um projeto moderno começa na fonte:
- **SaaS / Tech / Clean**: Geist (Vercel), Inter Display, Satoshi, Plus Jakarta Sans.
- **Dev tools / Terminal / Brutalism**: Geist Mono, JetBrains Mono, Space Mono.

Ajuste o `letter-spacing`: títulos em negrito geralmente pedem `-0.02em` a `-0.04em` para ficarem compactos e sofisticados em vez de "largados".

### 2.2 Hierarquia de profundidade (surface elevation)
Esqueça sombras chapadas (`shadow-md` puro aplicado em tudo). Use bordas sutis com opacidade + sombras difusas:
- Bordas em dark mode: `border border-white/[0.08]` ou `border-white/[0.12]`.
- Glassmorphism dosado (não em tudo): `backdrop-blur-md bg-neutral-900/60`.
- Gradientes radiais sutis de background para quebrar o preto puro (`#000000`) ou o branco puro.

### 2.3 Microinterações e física
A diferença entre um botão estático e um botão de produto profissional é o feedback tátil: transição suave de escala no clique (`active:scale-[0.98]`), foco visível acessível estilizado (`focus-visible`) e transições de estado (via Motion/Framer Motion). Sem isso, a interface parece estática mesmo com o visual certo.

### 2.4 Densidade de informação e respiro
IA e código apressado tendem a aglomerar elementos sem espaçamento consistente. Adote uma escala matemática (múltiplos de 4px ou 8px: `gap-2`, `gap-4`, `p-6`) e mantenha consistência implacável entre seções — espaçamento inconsistente é tão visível quanto cor errada.

## 3. Stack de componentes e ferramentas

| Camada | Ferramenta recomendada | Por quê |
|---|---|---|
| Estilização | Tailwind CSS v4 | Rapidez, zero CSS morto no bundle, suporte nativo a design tokens |
| Componentes base | shadcn/ui (sobre Radix UI) | Componentes acessíveis, código dentro do projeto, sem lock-in de pacote externo |
| Animações | Motion (ex-Framer Motion) | Layout shifts, entrada/saída, física de gestos |
| Formulários e validação | React Hook Form + Zod | Performance sem re-render excessivo, schemas type-safe |
| Notificações | Sonner | Toasts com empilhamento dinâmico e animação polida |
| Ícones | Lucide Icons (padrão) ou Phosphor Icons (mais variação: bold/duotone/thin) | Consistência e leveza |
| Cores | Radix Colors / Tailwind Neutral (slate, zinc, neutral) | Evita preto/branco absoluto chapado em telas inteiras |

Para acabamento visual além do shadcn/ui base (hero sections, glow, bordas animadas, efeitos 3D, inputs/selects refinados), consulte `references/stack-and-libraries.md` — tem a lista completa de bibliotecas copy-paste (Magic UI, Aceternity UI, Origin UI, Motion Primitives) e quando usar cada uma.

## 4. Checklist final antes de entregar (regra de ouro)

Depois que a estrutura inicial da tela existir (gerada por IA ou não), sempre passe o pente fino:

1. **Estados dos botões**: hover, `focus-visible`, `active:scale-95`, spinner de loading elegante — não só o estado padrão.
2. **Copy real**: substitua todo texto placeholder genérico por microcopy alinhado ao contexto do produto (rótulos claros em botões, tooltips úteis, mensagens de erro específicas).
3. **Empty states e skeletons**: nunca deixe tela em branco durante carregamento ou lista vazia sem ilustração/orientação — isso entrega mais amadorismo do que qualquer erro visual.

Nenhuma entrega de UI está completa sem passar por este checklist, mesmo sob pressão de prazo.

## 5. Atuando como Tech Lead (arquitetura e governança)

Quando a tarefa é sobre o projeto/time como um todo — não uma tela isolada — o papel deixa de ser só escrever código e passa a ser viabilizar padrões escaláveis. Cobre: separação de responsabilidades, estrutura por domínio/feature, design system centralizado, gestão consciente de estado (server state vs. client state), automação de lint/format, TypeScript rigoroso, estratégia de testes, Core Web Vitals, otimização de assets, acessibilidade desde a concepção, ADRs e gestão de dívida técnica.

Consulte `references/tech-lead-practices.md` para o guia completo antes de propor arquitetura, revisar código em nível de time, ou discutir processo — não improvise essas decisões sem checar o guia, porque são decisões caras de reverter depois.

## 6. Referências visuais e ferramentas de prototipação

Quando faltar direção visual concreta (não só estrutural), use `references/inspiration-tools.md` — lista ferramentas de geração/prototipação de UI (v0, Google Stitch, Subframe, Antigravity) e bancos de referência visual (Aceternity UI, 21st.dev, Dribbble, Pinterest, Mobbin) para calibrar um estilo específico antes de codificar, em vez de partir do zero com o default do framework.
