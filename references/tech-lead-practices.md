# Práticas de Tech Lead em front-end — referência completa

Atuar como Tech Lead no ecossistema de front-end exige balancear rigor técnico, produtividade do time e entrega de valor para o usuário final. O papel deixa de ser apenas escrever código para ser o viabilizador de padrões escaláveis.

## Arquitetura e manutenibilidade

- **Separation of Concerns**: isole lógica de negócio, chamadas de rede e UI. Mantenha componentes o mais puros e desacoplados possível (padrões como Container/Presentational ou Custom Hooks).
- **Estrutura por domínio/feature**: prefira organizar diretórios por domínio de negócio (`features/checkout/`, `features/auth/`) em vez de agrupamento puramente técnico (`components/`, `reducers/`). Isso facilita code splitting e modularização futura.
- **Design System & Component Library**: centralize tokens visuais (cores, espaçamentos, tipografia) e componentes atômicos. Evite redundâncias e garanta consistência visual entre squads.
- **State Management consciente**: não use stores globais (Redux, Zustand) para tudo. Diferencie **Server State** (gerenciado por ferramentas como TanStack Query/SWR) de **Client/UI State** local — misturar os dois é a causa mais comum de bugs de cache e re-render desnecessário.

## Qualidade de código e governança

- **Automação estrita de lint e formatação**: configure ESLint, Prettier e Husky (com lint-staged) para que estilo e erros comuns nem passem do commit.
- **TypeScript rigoroso**: use tipos estritos (`noImplicitAny`, `strictNullChecks`). Evite `any` liberado na base; modele contratos de API com validação em runtime (Zod).
- **Estratégia de testes pragmática**: invista na base da pirâmide com testes unitários para funções puras e utilitários, e foque a maior parte do esforço de UI em testes de integração/comportamento (Testing Library) e E2E críticos (Playwright/Cypress) — testando comportamento e acessibilidade, não detalhes de implementação.
- **Code reviews construtivos**: foque os reviews em arquitetura, segurança, casos de borda e legibilidade. Deixe syntax check para as ferramentas automáticas.

## Performance e experiência do usuário (UX/DX)

- **Core Web Vitals como métrica de time**: monitore LCP, INP e CLS continuamente em dashboards (CI e RUM), não só em auditorias pontuais.
- **Otimização de assets**: implemente code splitting por rota, lazy loading de imagens com formatos modernos (WebP/AVIF), pré-carregamento de fontes e tree shaking ativo no bundler (Vite, Rsbuild ou Next.js).
- **Acessibilidade (a11y) desde a concepção**: adote semântica HTML correta, suporte completo a navegação por teclado, labels adequados e contraste validado via linters (`eslint-plugin-jsx-a11y`) e ferramentas como axe-core — a11y verificada no fim do projeto sempre custa mais caro para corrigir.

## Liderança e processos técnicos

- **ADRs (Architecture Decision Records)**: documente as decisões arquiteturais relevantes (por que escolher React Query? por que migrar o bundler?). Isso evita discussões repetitivas e contextualiza novos membros do time.
- **Gestão de dívida técnica**: negocie uma fatia fixa de cada ciclo de desenvolvimento (ex.: 15% a 20%) dedicada a refatoração, atualização de dependências e melhoria de pipelines — dívida técnica não negociada explicitamente tende a nunca ser paga.
- **Onboarding e DX**: garanta que um novo desenvolvedor consiga clonar o repositório e rodar o projeto localmente com um único comando (`pnpm dev` / `docker compose up`), sem depender de documentação desatualizada.
