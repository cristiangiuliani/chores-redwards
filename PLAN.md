# Piano di sviluppo — calendario delle figlie

Contesto per Claude Code: il progetto è anche un percorso di studio di 12 settimane
(1 ora al giorno, lun–gio pratica, venerdì retrospettiva; inizio 26 ottobre 2026).
Questo file stabilisce le **fasi del prodotto** e in quali settimane si lavora a cosa.
Requisiti di dettaglio: vedi SPEC.md.

## Fasi del prodotto

| Fase | Settimane | Contenuto | Dove sono i requisiti |
|---|---|---|---|
| **Fase 1** — solo genitori | 2–10 | Profili, settimane numerate, attività ricorrenti, completamenti e punti, cicli e soglie, reward individuali, lista settimanale, stampa in olandese, traduzione locale, attività da linguaggio naturale, riepilogo in olandese, astrazione del provider del modello | SPEC.md |
| **Fase 2** — accesso delle figlie | 11–12 | Accesso con PIN, vista per le figlie, segnare le attività fatte, deploy gratuito | SPEC-phase2.md (da scrivere in settimana 11) |
| **Backlog** — senza data | — | Funzionalità rimandate, da pianificare dopo la settimana 12 | Sezione "Backlog" di SPEC.md |

Regole:
- "Fase 1" e "Fase 2" hanno lo stesso significato in tutti i documenti del progetto.
- Il backlog non ha un numero di fase finché non viene pianificato.
- Durante la fase 1 non si implementa nulla della fase 2 o del backlog, nemmeno "già che ci siamo".

## Backlog (rimandato, senza data)

- Attività una tantum.
- Obiettivo di squadra con reward condivisi.
- Tracciamento della consegna dei reward.
- Modifica dei completamenti di settimane chiuse.
- Servizi remoti di qualsiasi tipo (traduzione, hosting dei modelli, notifiche).

## Settimane

| Sett. | Tema di studio | Lavoro sul prodotto |
|---|---|---|
| 1 | Fondamenta: repo, Ollama, CLAUDE.md, contesto, permessi | Scheletro del repo, test dei modelli di traduzione, SPEC.md fase 1 |
| 2 | Workflow disciplinato + Python: plan mode, esplora-pianifica-implementa-verifica, TDD | Modello dati, CRUD FastAPI con pytest |
| 3 | Prima versione, review critica del codice generato | Lista settimanale, punti e reward, stampa in olandese, interfaccia IT/NL |
| 4 | Personalizzazione: slash command, skill, hooks | Skill per testi bilingui, hook per formatter, traduzioni mancanti, test |
| 5 | MCP: Playwright, SQLite, GitHub | Test dell'interfaccia e della stampa con Playwright |
| 6 | Costruire un MCP server Python | MCP server sopra il calendario |
| 7 | Subagent e parallelismo, git worktree | — |
| 8 | Git e automazione: branch/PR, GitHub Actions, Claude Code headless | CI con lint e test |
| 9 | AI nell'app: traduzione | Client Ollama + TranslateGemma, traduzione in background, cache, glossario, correzioni manuali, set di 30 frasi |
| 10 | AI nell'app: avanzato | Linguaggio naturale → attività (output strutturato), riepilogo in olandese, astrazione del provider |
| 11 | Fase 2 | SPEC-phase2.md, accesso con PIN, vista figlie, test end-to-end |
| 12 | Deploy e consolidamento | Deploy gratuito, riordino CLAUDE.md/skills/hooks, PLAYBOOK.md |

## Decisioni ancora aperte sulle fasi

1. **Deploy e traduzione locale.** Il modello di traduzione richiede ~8 GB di RAM e gira
   solo sul Mac. Un deploy gratuito (settimana 12) non può ospitarlo. Opzioni: l'app online
   usa le traduzioni già fatte in locale e salvate nel database; oppure in fase 2 si
   traduce solo quando il Mac è acceso; oppure il deploy resta in rete di casa.
   Da decidere in settimana 11.
2. **Vincoli tecnici:** Mac Intel con macOS 12, 16 GB di RAM, nessuna GPU; Ollama fermo
   alla v0.12.3; solo strumenti open e gratuiti; nessuna API a pagamento, quindi niente
   Claude in CI.
