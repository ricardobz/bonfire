# Plano: bonfire

Ideias e plano da sessão de concepção (2026-10-13).

## A ideia

- Análise **diária ou semanal** do uso do Claude Code: todas as sessões da máquina
  ou só as pastas que o usuário apontar.
- Gera um resumo estilo Strava para devs compartilharem, com **achievements**.
- **Sem expor nada**: só números agregados.
- Fundos prontos para escolher na hora de postar, gerados pelo Codex, com
  referências a **save points de games** e a **séries**.

## Formato: skill fina + script

- **Script Python (só stdlib)** lê os logs e gera um JSON **só com agregados**. O
  Claude nunca lê o conteúdo das conversas. Isso garante a privacidade, sai barato
  e o resultado é determinístico.
- **Template HTML do card**: fundo do tema + números por cima, exportado para PNG
  via headless Chrome.
- **Skill `/bonfire`** (`/bonfire day`, `/bonfire week --theme bonfire`): roda o
  script, mostra o preview dos dados, pergunta o tema, renderiza o PNG e,
  opcionalmente, escreve uma frase de efeito **a partir dos números**.
- Para outros devs: empacotar como **plugin** do Claude Code (skill + script +
  fundos).
- Prior art: `ccusage` faz tokens e custo no terminal, mas não tem card nem
  achievements. Esse é o diferencial.

### Fonte dos dados

`~/.claude/projects/<pasta-codificada>/*.jsonl`: um arquivo por sessão, com
timestamps, tool calls e uso de tokens por mensagem. O nome da pasta é o path do
projeto com `/` trocado por `-` (ex.: `-home-beckert-worktest-bonfire`). Filtrar
por pasta é só escolher quais diretórios ler.

## Métricas (sem conteúdo)

- Sessões; tempo ativo (somando só os trechos sem pausas longas); streak de dias
- Tokens in/out; taxa de cache hit
- Tool calls por tipo (Edit, Write, Bash, Read…)
- Nº de arquivos tocados (só a contagem); linguagens por extensão
- Modelos usados; horário de pico; sessão mais longa; subagents disparados
- Heatmap da semana

**Privacidade:** nomes de projeto **ocultos por padrão** (viram "3 projetos"), com
alias opcional. Nunca sai nenhum prompt, path, nome de arquivo ou código. O
preview do JSON aparece antes de renderizar.

## Achievements (primeira lista)

| Achievement | Regra |
|---|---|
| Night Owl | sessão depois das 2h |
| Early Bird | sessão antes das 6h |
| Marathon | sessão com mais de 4h |
| Speedrun | tarefa fechada em menos de 10 min |
| Streak 7 | 7 dias seguidos |
| Polyglot | 5 ou mais linguagens |
| Delegator | 10 ou mais subagents |
| Cache Lord | cache hit acima de 90% |
| Weekend Warrior | sábado e domingo |
| Read the Manual | mais Read do que Edit + Write |

## Temas de fundo

### Games: save points

| # | Tema | Referência | Uso sugerido |
|---|---|---|---|
| 1 | Bonfire | Dark Souls ("Bonfire Lit") | semanal, tema principal |
| 2 | Site of Grace | Elden Ring (feixe dourado) | |
| 3 | Bench | Hollow Knight (banco numa caverna azul) | |
| 4 | Typewriter | Resident Evil (safe room) | |
| 5 | End of day | Stardew Valley (tela de resumo do dia) | ⭐ diário |
| 6 | Mountain campfire | Celeste | |
| 7 | Save star | Undertale ("filled with determination") | |
| 8 | Save crystal | Final Fantasy | |
| 9 | Sculptor's idol | Sekiro | |
| 10 | Healing center / PC | Pokémon ("progresso salvo") | |

### Séries

| # | Tema | Referência | Uso sugerido |
|---|---|---|---|
| 1 | Captain's Log | Star Trek ("Stardate…") | ⭐ semanal |
| 2 | MDR terminal | Severance (Lumon, "work-life balance") | |
| 3 | Awards night | The Office (Dundies = achievements) | |
| 4 | D&D table | Stranger Things (conversa com a Pleceboia) | |
| 5 | fsociety terminal | Mr. Robot | |
| 6 | Ticket rail | The Bear ("Yes, chef") | |

⚠️ **Direitos autorais:** *evocar* em vez de copiar. Nada de logo, personagem ou
nome de franquia na imagem. Os nomes dos temas no código são genéricos (`bonfire`,
`bench`, `typewriter`, `captains-log`…).

### Formatos de imagem

- 1080x1920 (9:16, celular/stories), formato base (2026-10-13)
- 1080x1350 (retrato: Instagram/LinkedIn), opcional
- 1200x675 (X/Twitter), opcional

Todo fundo precisa de **espaço negativo** para o texto (centro e parte de baixo).

## Passos (um commit cada)

1. [x] **Coletor**: `recap.py --days 1|7 --paths ...` gera o JSON agregado, mais
   um teste de que nenhum texto de conversa vaza.
2. [x] **Achievements**: regras num arquivo de dados, fácil de estender.
3. [x] **Card**: template HTML com temas (fundo + paleta + fonte) e PNG via
   headless Chrome. Verificar com screenshot.
4. [x] **Skill `/bonfire`**: o wrapper, com preview e escolha de tema.
5. [x] **Fundos**: prompts em [PROMPTS-ARTE.md](PROMPTS-ARTE.md); Ricardo gera no
   Codex, Claude integra.
6. [ ] *(Depois)* Empacotar como plugin, escrever o README, talvez uma galeria
   estática no Netlify. Quando estiver no ar, adicionar no portfolio
   (ricardobz.dev).
7. **Períodos e projeto** (2026-10-14): além de dia e semana, `sprint` (15 dias,
   tema padrão `mdr-terminal`), `month` (últimos 30 dias, `typewriter`) e `all`
   (tudo que restar nos logs, `typewriter`); acima de 7 dias o heatmap soma por dia
   da semana. `--alias` mostra um nome digitado no lugar de "N projects".
   - [x] A. Coletor (`--days 15|30|all`, `period.kind`) + card (títulos, heatmap, alias)
   - [x] B. Skill (`/bonfire sprint|month|all`, `--alias`) + README

## Decisões em aberto

- ~~Por onde começar~~: **semanal** primeiro (2026-10-13).
- ~~Primeira leva de temas~~: `bonfire`, `end-of-day`, `captains-log`, `bench`.
- Só uso pessoal ou plugin para outros devs desde já? Isso muda o cuidado com a
  privacidade e com os paths.
- O nome `bonfire` foi escolhido; `savepoint` foi a alternativa mais universal.
  Conferir colisão de nome no GitHub e no marketplace de plugins antes de publicar.
