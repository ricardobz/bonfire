# bonfire

Um "Strava para devs": lê o uso local do Claude Code (diário ou semanal), gera um
resumo **só com números agregados** (nada de prompts, paths ou código), calcula
achievements e renderiza um card PNG com fundos temáticos de save points de games
e séries (bonfire, bench, máquina de escrever, captain's log…) para postar.

Status: **funcionando, uso pessoal** (16 temas). Ver [docs/PLANO.md](docs/PLANO.md) e
[docs/PROMPTS-ARTE.md](docs/PROMPTS-ARTE.md).

## Produção

Não publicado: por enquanto é só para uso pessoal. O nome `bonfire` colide com o
plugin `vieko/bonfire` (memória entre sessões); se um dia virar plugin, escolher um
nome mais distinto antes. O repositório `ricardobz/bonfire` no GitHub é público.

## Uso

Instalar a skill uma vez (vale para qualquer projeto; abrir uma sessão nova depois):

```sh
ln -s ~/worktest/bonfire/skills/bonfire ~/.claude/skills/bonfire
```

| Quando | Comando | Tema padrão |
|---|---|---|
| Fim do dia | `/bonfire day` | end-of-day |
| Fim da semana | `/bonfire` ou `/bonfire week` | bonfire |
| Pular a pergunta do tema | `/bonfire week --theme captains-log` | o escolhido |
| Só alguns projetos | `/bonfire day --paths ~/worktest/floripa_game` | |

A skill mostra os números antes, pergunta o tema, salva o PNG em
`~/Pictures/bonfire/<data>-<day|week>-<tema>.png` e oferece legendas para o post.
Temas: os ids em `data/themes.json`.

- "Semana" = últimos 7 dias contando hoje: rodar sempre no mesmo dia (ex.: sexta)
  para comparar semanas.
- Sem Claude (sem preview nem legenda, sem gastar tokens):

  ```sh
  cd ~/worktest/bonfire
  python3 recap.py --days 7 --out /tmp/recap.json
  python3 render.py /tmp/recap.json --theme bonfire --out ~/Pictures/bonfire/week.png
  ```

- O Claude Code apaga logs de sessão com mais de 30 dias (`cleanupPeriodDays` em
  `~/.claude/settings.json`), então o histórico disponível é no máximo esse.
- O card só tem layout para 1 e 7 dias; `--days 30` funciona no coletor, mas o card
  (heatmap e título) ainda não suporta mês nem "tudo".

## Rodar localmente

Só Python 3 (stdlib). O coletor imprime o JSON agregado:

```sh
python3 recap.py --days 7                       # semana, todas as pastas
python3 recap.py --days 1 --paths ~/worktest/x  # hoje, só essas pastas
python3 -m unittest discover tests              # inclui o teste de vazamento
```

Card PNG (1080x1920, precisa do Google Chrome ou Chromium; `BONFIRE_CHROME` aponta
outro binário):

```sh
python3 recap.py --days 7 --out recap_week.json
python3 render.py recap_week.json --theme bonfire --out card.png
```

Temas em `data/themes.json` (fundo, cor, título por dia/semana); layout em
`card/card.html` + `card/card.css`; fonte Pixelify Sans (OFL) em `assets/fonts/`.

Skill: `skills/bonfire/SKILL.md` (ver "Uso" acima).

Achievements: regras em `data/achievements.json`, avaliadas por `achievements.py`
e incluídas no JSON do recap.

## Deploy

Nenhum: roda local (uso pessoal). `git push` só atualiza o repositório.
