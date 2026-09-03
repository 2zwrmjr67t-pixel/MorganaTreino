# data/nutrition/

Log de alimentação registrado via conversa com o Claude, lido pelo app (`index.html`) em
tempo real via `raw.githubusercontent.com` — não depende de onde o app está hospedado.

## Arquivos

- `index.json` — lista de datas (`YYYY-MM-DD`) que possuem registro. O app só tenta buscar
  os dias listados aqui, evitando requisições desnecessárias.
- `<YYYY-MM-DD>.json` — itens do dia, agrupados pelos mesmos slots de refeição do app:

```json
{
  "cafe":   [{ "n": "Ovos mexidos (2 un)", "k": 180, "p": 14, "c": 2, "f": 13, "src": "chat", "t": "08:15" }],
  "lm":     [],
  "almoco": [],
  "lt":     [],
  "janta":  [],
  "ceia":   []
}
```

Campos por item: `n` nome, `k` kcal, `p` proteína (g), `c` carboidrato (g), `f` gordura (g),
`src` sempre `"chat"` (identifica origem), `t` horário opcional `HH:MM`.

## Como um item chega aqui

Não edite estes arquivos à mão. Use `scripts/log_meal.py` (ver `CLAUDE.md` na raiz do repo
para a rotina completa) — ele garante JSON válido e mantém `index.json` sincronizado.

## Como o app consome

`index.html` busca `index.json` e, para os dias relevantes, `<data>.json` via HTTPS direto
do GitHub (branch `main`), mescla com os lançamentos manuais feitos no próprio app
(`localStorage`) e soma tudo nos totais do dia / semana / mês. Itens vindos do chat aparecem
com a etiqueta "chat" e só podem ser ocultados localmente (a fonte da verdade continua sendo
este diretório).
