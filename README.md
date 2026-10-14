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

| Quando | Comando | Período | Tema padrão |
|---|---|---|---|
| Fim do dia | `/bonfire day` | hoje | end-of-day |
| Fim da semana | `/bonfire` ou `/bonfire week` | 7 dias | bonfire |
| Fim da sprint | `/bonfire sprint` | 15 dias | mdr-terminal |
| Fim do mês | `/bonfire month` | 30 dias | typewriter |
| Tudo que existe | `/bonfire all` | desde o log mais antigo | typewriter |
| Pular a pergunta do tema | `/bonfire week --theme captains-log` | | o escolhido |
| Só alguns projetos | `/bonfire day --paths ~/worktest/floripa_game` | | |
| Projeto com nome no card | `/bonfire all --paths ~/worktest/floripa_game --alias "Floripa Game"` | | |

A skill mostra os números antes, pergunta o tema, salva o PNG em
`~/Pictures/bonfire/<data>-<período>-<tema>.png` e oferece legendas para o post.
Por privacidade o card mostra só "N projects"; `--alias` troca isso por um nome que
você digita (nunca vem do path).
Temas: os ids em `data/themes.json`.

- "Semana" = últimos 7 dias contando hoje: rodar sempre no mesmo dia (ex.: sexta)
  para comparar semanas.
- Sem Claude (sem preview nem legenda, sem gastar tokens):

  ```sh
  cd ~/worktest/bonfire
  python3 recap.py --days 7 --out /tmp/recap.json   # 1, 7, 15, 30 ou all
  python3 render.py /tmp/recap.json --theme bonfire --out ~/Pictures/bonfire/week.png
  ```

  `render.py` aceita `--alias "Nome"`.

- "Tudo" vai até onde os logs existem: o Claude Code limpa sessões antigas
  (`cleanupPeriodDays` em `~/.claude/settings.json`). Em 14/10/2026 havia logs desde
  26/08 (50 dias).
- Acima de 7 dias o heatmap do card soma por dia da semana (seg a dom × 24 horas).

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

Temas em `data/themes.json` (fundo, cor, título por período); layout em
`card/card.html` + `card/card.css`; fonte Pixelify Sans (OFL) em `assets/fonts/`.

Skill: `skills/bonfire/SKILL.md` (ver "Uso" acima).

Achievements: regras em `data/achievements.json`, avaliadas por `achievements.py`
e incluídas no JSON do recap.

## Deploy

Nenhum: roda local (uso pessoal). `git push` só atualiza o repositório.
