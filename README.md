# bonfire

Um "Strava para devs": lê o uso local do Claude Code (diário ou semanal), gera um
resumo **só com números agregados** (nada de prompts, paths ou código), calcula
achievements e renderiza um card PNG com fundos temáticos de save points de games
e séries (bonfire, bench, máquina de escrever, captain's log…) para postar.

Status: **planejamento**. Ver [docs/PLANO.md](docs/PLANO.md) e
[docs/PROMPTS-ARTE.md](docs/PROMPTS-ARTE.md).

## Produção

Ainda não publicado. A ideia é distribuir como plugin do Claude Code (skill +
script + fundos); uma galeria estática no Netlify é opcional, para depois.

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

Skill `/bonfire` (coleta, preview, escolha do tema, PNG em `~/Pictures/bonfire/`):
`skills/bonfire/SKILL.md`. Para usar em qualquer projeto, linkar uma vez:

```sh
ln -s ~/worktest/bonfire/skills/bonfire ~/.claude/skills/bonfire
```

Depois: `/bonfire`, `/bonfire day`, `/bonfire week --theme captains-log`.

Achievements: regras em `data/achievements.json`, avaliadas por `achievements.py`
e incluídas no JSON do recap.

## Deploy

A definir.
