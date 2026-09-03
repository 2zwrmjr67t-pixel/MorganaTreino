# Protocolo Morgana — instruções para o Claude

App PWA estático (`index.html`) de acompanhamento de treino/dieta/medidas. Sem
backend: os dados manuais ficam em `localStorage` no aparelho, e os dados
registrados por conversa (ver abaixo) ficam versionados neste repositório em
`data/nutrition/`, lidos pelo app em tempo real via `raw.githubusercontent.com`.

## Rotina de registro de alimentação por chat

Quando o usuário, em qualquer conversa nesta sessão, descrever o que comeu
("comi X", "tomei um shake de Y", "almocei Z"), sem que ele precise pedir
explicitamente ou usar um comando — isso é o fluxo principal do app:

1. **Interprete os itens.** Separe a fala em itens de alimento com quantidade
   (ex.: "2 ovos mexidos e uma fatia de pão integral" → 2 itens). Se a
   quantidade não for dita, assuma uma porção padrão razoável e deixe isso
   claro na resposta ao usuário.
2. **Estime os macros.** Use seu conhecimento nutricional (referências tipo
   TACO/USDA) para estimar kcal, proteína (g), carboidrato (g) e gordura (g)
   por item, arredondados para inteiros. Não é preciso buscar fonte externa.
   Sinalize ao usuário, na resposta em chat (não no JSON), estimativas mais
   incertas com `[Inferência]`, conforme a preferência dele por transparência
   de incerteza.
3. **Determine a refeição (slot).** Slots válidos, na ordem do app:
   `cafe` (Café da Manhã), `lm` (Lanche Manhã), `almoco` (Almoço), `lt`
   (Lanche Tarde), `janta` (Janta), `ceia` (Ceia). Se o usuário não disser
   qual refeição, infira pelo horário atual; se ficar ambíguo, pergunte.
4. **Determine a data.** Padrão: hoje (fuso do usuário, Rio Grande do Sul,
   `America/Sao_Paulo`). Só use outra data se ele disser explicitamente
   ("ontem", "sexta-feira").
5. **Grave com o script**, um item por chamada:
   ```
   python3 scripts/log_meal.py --date YYYY-MM-DD --slot <slot> \
     --name "<nome do item>" --kcal <int> --protein <int> --carbs <int> --fat <int> \
     [--time HH:MM]
   ```
   Não edite `data/nutrition/*.json` manualmente — o script garante JSON
   válido e mantém `data/nutrition/index.json` atualizado. Ver
   `data/nutrition/README.md` para o schema.
6. **Commit e push.** Depois de rodar o script para todos os itens da
   mensagem, faça um único commit cobrindo os arquivos alterados em
   `data/nutrition/` e dê push.

   **Autorização permanente:** para commits que tocam *exclusivamente*
   arquivos em `data/nutrition/**` (dados de alimentação, sem código), o
   usuário pré-autoriza push direto para `main`, sem branch de feature nem
   PR — são lançamentos de dados pessoais, não mudanças de código, e o app
   lê diretamente de `main`. Se a sessão estiver em outra branch por padrão
   da plataforma, dê push assim mesmo direto para `main`:
   ```
   git add data/nutrition/
   git commit -m "diet: registra <resumo curto>"
   git push origin HEAD:main
   ```
   Essa autorização **não** se estende a mudanças em `index.html`, scripts,
   ou qualquer outro código — essas seguem o fluxo normal de branch/PR.
7. **Confirme para o usuário** em 1–2 frases: o que foi lançado, o total de
   kcal/macros da mensagem, e o total acumulado do dia (some manualmente ou
   leia os arquivos do dia) — sem precisar abrir o app.

Exemplo mental: "comi 2 ovos e um whey de manhã" → 2 chamadas ao script no
slot `cafe`, data de hoje, commit único, push em `main`, resposta curta com
os macros.

## Via Claude Chat (sem terminal)

Esta rotina pressupõe Claude Code (terminal + git). Para registrar
alimentação a partir de uma conversa comum no claude.ai (sem Claude Code),
veja `docs/registro-via-claude-chat.md` — mesmo schema, mesma pasta
`data/nutrition/`, mas escrevendo os arquivos via ferramentas do conector
GitHub em vez de rodar `scripts/log_meal.py`.

## Reprogramar o app web

O app (`index.html`) busca `data/nutrition/index.json` e os arquivos de dia
relevantes direto do GitHub (`REMOTE_OWNER`/`REMOTE_REPO`/`REMOTE_BRANCH` no
topo do `<script>`), mescla com os lançamentos manuais do `localStorage` e
soma tudo em `dayTotals()`. Mudanças de código no `index.html` seguem o fluxo
normal (branch de feature + push conforme instruído pela sessão).
