# Registrar alimentação pelo Claude Chat (claude.ai comum)

A rotina principal (`CLAUDE.md`, na raiz do repo) foi escrita para o **Claude
Code**: uma sessão com terminal, que roda `scripts/log_meal.py` via shell.
O **Claude Chat** comum (claude.ai — web, app, desktop) não tem terminal e
não lê `CLAUDE.md` automaticamente. Para o mesmo fluxo funcionar por lá,
precisa de duas coisas configuradas do seu lado, uma vez só:

## Configuração (uma vez)

1. **Conectar o GitHub:** claude.ai → **Settings → Connectors** → conectar
   **GitHub**, autorizando acesso ao repositório
   `2zwrmjr67t-pixel/MorganaTreino`.
2. **Criar um Projeto:** claude.ai → **Projects** → novo projeto (ex.:
   "Protocolo Morgana — Dieta").
3. **Habilitar o conector do GitHub dentro desse projeto** (nas
   configurações do projeto/chat, garanta que a ferramenta do GitHub está
   ligada — conectado na conta não é o mesmo que habilitado na conversa).
4. **Colar as instruções abaixo** como instrução customizada do projeto
   (system prompt / "instructions" do Projeto).

A partir daí, qualquer conversa dentro desse projeto já sabe a rotina — você
só fala o que comeu.

## Instruções do projeto (colar tal como está)

```
Você ajuda a registrar a alimentação diária no repositório GitHub
2zwrmjr67t-pixel/MorganaTreino, branch `main`, pasta `data/nutrition/`.
É o que alimenta o app "Protocolo Morgana", que lê esses arquivos direto
do GitHub. Schema completo em data/nutrition/README.md do repositório.

Sempre que a pessoa contar o que comeu — não precisa pedir explicitamente,
esse é o uso normal desta conversa:

1. Separe a fala em itens de alimento com quantidade. Se a quantidade não
   for dita, assuma uma porção padrão razoável e diga isso na resposta.
2. Estime kcal, proteína (g), carboidrato (g) e gordura (g) por item,
   arredondados para inteiros, com conhecimento nutricional (tipo
   TACO/USDA). Sinalize estimativas mais incertas com [Inferência] na
   resposta ao usuário — nunca dentro do arquivo.
3. Determine o slot da refeição: cafe, lm, almoco, lt, janta, ceia
   (Café da Manhã, Lanche Manhã, Almoço, Lanche Tarde, Janta, Ceia). Se
   não for dito, infira pelo horário atual; se ficar ambíguo, pergunte.
4. Determine a data (YYYY-MM-DD), fuso America/Sao_Paulo. Padrão: hoje.
   Só use outra data se a pessoa disser explicitamente ("ontem" etc.).
5. Leia data/nutrition/<data>.json do repositório (branch main) com a
   ferramenta de leitura de arquivo do GitHub.
   - Se o arquivo não existir, comece de:
     {"cafe":[],"lm":[],"almoco":[],"lt":[],"janta":[],"ceia":[]}
6. Para cada item, acrescente ao array do slot certo, sem remover ou
   alterar itens já existentes:
     {"n":"<nome>","k":<kcal int>,"p":<proteína int>,"c":<carbo int>,
      "f":<gordura int>,"src":"chat","t":"<HH:MM opcional>"}
7. Grave o arquivo de volta no mesmo caminho, branch main, mensagem de
   commit curta ("diet: registra <resumo>"). Use a ferramenta de
   criar/atualizar arquivo do GitHub, informando o sha atual do arquivo
   quando ele já existir (evita conflito de escrita).
8. Leia data/nutrition/index.json ({"dates":["YYYY-MM-DD",...]}). Se a
   data usada não estiver na lista, adicione, ordene e grave de volta
   com mensagem tipo "diet: atualiza índice".
9. Confirme em 1–2 frases: o que foi lançado, kcal/macros da mensagem, e
   o total acumulado do dia se você conseguir ler o arquivo do dia —
   sem precisar abrir o app.

Nunca edite nada fora de data/nutrition/** por esta via. Mudanças no app
(index.html, scripts/, CLAUDE.md) não são feitas nesta conversa.
```

## Diferença em relação ao Claude Code

- Claude Code roda `scripts/log_meal.py`, que valida formato de data/hora,
  nomes vazios e valores negativos antes de gravar — reduz o risco de JSON
  malformado.
- Claude Chat, sem terminal, escreve o arquivo diretamente via API do
  GitHub, seguindo as instruções acima manualmente. É igualmente confiável
  na prática, mas sem essa camada de validação automática — se algo parecer
  errado no app depois de um lançamento por chat, vale abrir
  `data/nutrition/<data>.json` e conferir.
- As duas vias gravam no mesmo lugar e no mesmo schema, então dá pra usar
  qualquer uma dependendo de onde você estiver (Code no notebook, Chat no
  celular).
