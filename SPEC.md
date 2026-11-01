# SPEC — Fase 1: attività settimanali, punti e reward

## Obiettivo

Un'app locale con cui i genitori preparano la lista settimanale delle attività delle
figlie, assegnano punti e gestiscono reward settimanali, per ciclo e di squadra.
Il genitore scrive in italiano; le figlie leggono la lista stampata in olandese.

## Utenti

- **Fase 1: solo genitori.** Creano profili, attività e reward, avviano e chiudono le
  settimane, segnano i completamenti, registrano i reward scelti e consegnati, stampano
  la lista.
- Le figlie non usano l'app: ricevono il foglio stampato.
- Esiste una sola famiglia, senza login.

## Termini

- **Settimana:** un periodo numerato in sequenza (Settimana 1, 2, 3…) che il genitore
  **avvia e chiude a mano**, come uno sprint di Jira. L'app non usa date, giorni della
  settimana né calendario. A differenza di Jira, ciò che non è stato completato non passa
  alla settimana successiva.
- **Attività:** qualcosa da fare (es. "Fare il letto"), con titolo, descrizione
  facoltativa, punti base, figlie assegnate e numero di volte per settimana (N, minimo 1).
  Le figlie decidono quando svolgerla durante la settimana.
- **Completamento:** la registrazione che una figlia ha svolto una delle N volte di
  un'attività in una settimana, con i punti effettivamente assegnati.
- **Ciclo:** 4 settimane consecutive: C1 = settimane 1–4, C2 = 5–8, e così via.
- **Periodo:** settimana o ciclo.

## Funzionalità

Ogni criterio ha un codice (es. `ATT-3`) da riusare nel nome del test pytest
corrispondente.

### 1. Profili delle figlie

- `PRF-1` **Dato** nessun profilo, **quando** creo "Anna" con un colore, **allora** Anna
  compare nell'elenco delle figlie attive.
- `PRF-2` **Dato** il profilo di Anna con completamenti passati, **quando** lo archivio,
  **allora** non compare più nelle viste e nella stampa, e i suoi completamenti e reward
  restano nello storico.
- `PRF-3` **Dato** un profilo, **quando** lo salvo, **allora** è un'entità separata da
  qualsiasi account e porta il `family_id` della famiglia.

### 2. Settimane

- `SET-1` **Dato** nessuna settimana, **quando** avvio una settimana, **allora** viene
  creata la Settimana 1, aperta.
- `SET-2` **Dato** la Settimana 3 aperta, **quando** provo ad avviarne un'altra,
  **allora** l'operazione viene rifiutata: può esserci una sola settimana aperta.
- `SET-3` **Dato** la Settimana 3 aperta, **quando** la chiudo e avvio la successiva,
  **allora** viene creata la Settimana 4.
- `SET-4` **Dato** la Settimana 3 chiusa, **quando** aggiungo, modifico o cancello un
  completamento di quella settimana, **allora** l'operazione riesce e i totali di
  settimana e ciclo vengono ricalcolati (chiudere non blocca le modifiche).
- `SET-5` **Dato** nessuna settimana aperta (es. vacanze), **quando** passa del tempo,
  **allora** non succede nulla: nessuna attività, nessun punto, nessuna soglia.
- `SET-6` **Dato** la Settimana 4 aperta senza completamenti, **quando** annullo l'avvio,
  **allora** la Settimana 4 viene eliminata, la Settimana 3 resta chiusa e il prossimo
  avvio crea di nuovo la Settimana 4.
- `SET-7` **Dato** la Settimana 4 aperta con almeno un completamento, **quando** provo ad
  annullare l'avvio, **allora** l'operazione viene rifiutata.

### 3. Attività

- `ATT-1` **Dato** un'attività una tantum per la Settimana 5, **quando** apro la
  Settimana 5, **allora** compare; nelle altre settimane no.
- `ATT-2` **Dato** un'attività ricorrente "2 volte" dalla Settimana 5 senza settimana di
  fine, **quando** apro la Settimana 5 o una successiva, **allora** compare con
  contatore 0/2.
- `ATT-3` **Dato** un'attività ricorrente con settimana di fine 8, **quando** apro la
  Settimana 9, **allora** non compare.
- `ATT-4` **Dato** un'attività senza N indicato, **quando** la salvo, **allora** vale
  1 volta per settimana; N = 0 viene rifiutato.
- `ATT-5` **Dato** un'attività assegnata ad Anna e Sofia, **quando** la creo, **allora**
  esiste un solo testo con una sola traduzione, e compare nella lista di entrambe.
- `ATT-6` **Dato** un'attività da 10 punti con completamenti passati da 10, **quando**
  porto i punti base a 15, **allora** i completamenti passati restano a 10 e i nuovi
  propongono 15.
- `ATT-7` **Dato** un'attività "3 volte" con settimane passate da 3 completamenti,
  **quando** la porto a 2 volte, **allora** le settimane passate restano invariate e
  nella settimana aperta il contatore è su 2.
- `ATT-8` **Dato** 5 attività di Anna, di cui 2 già assegnate anche a Sofia, **quando**
  uso "Assegna tutte le attività di Anna anche a Sofia", **allora** Sofia ha tutte e 5 le
  attività, senza duplicati e senza nuove traduzioni.
- `ATT-9` **Dato** un'attività assegnata ad Anna e Sofia con completamenti passati di
  entrambe, **quando** uso "Separa per Sofia", **allora** nasce una nuova attività solo
  di Sofia con gli stessi testi e le stesse impostazioni, l'originale resta solo di Anna,
  i completamenti passati di Sofia restano sull'originale e i suoi totali non cambiano.
- `ATT-10` **Dato** un'attività separata con `ATT-9`, **quando** viene creata, **allora**
  riusa la traduzione esistente (anche se manuale) senza chiamare il modello.
- `ATT-11` **Dato** un'attività una tantum per la Settimana 5 non completata (o completata
  solo in parte), **quando** chiudo la Settimana 5 e avvio la 6, **allora** non compare
  nella Settimana 6: scade, le caselle mancanti valgono 0 e se serve va ricreata a mano.

### 4. Completamenti e punti

- `CMP-1` **Dato** un'attività da 10 punti nella Settimana 5, **quando** segno una volta
  come fatta per Anna, **allora** viene creato un completamento da 10 punti legato alla
  Settimana 5, con `recorded_by` = genitore e `status` = `confirmed`.
- `CMP-2` **Dato** un'attività da 10 punti, **quando** segno un completamento con 5 punti
  (fatta a metà) o con 15 (bonus), **allora** il completamento salva i punti indicati.
- `CMP-3` **Dato** un completamento, **quando** inserisco punti negativi, **allora** il
  salvataggio viene rifiutato.
- `CMP-4` **Dato** un'attività "3 volte", **quando** segno 3 completamenti, **allora** il
  contatore mostra 3/3; un quarto completamento nella stessa settimana viene rifiutato.
- `CMP-5` **Dato** caselle non completate, **quando** chiudo la settimana, **allora**
  valgono 0 punti e non tolgono punti (non esistono penalità).
- `CMP-6` **Dato** un completamento, **quando** lo creo, modifico o cancello, **allora**
  lo storico registra azione, valori prima/dopo e autore.

### 5. Cicli e soglie

- `PER-1` **Dato** le settimane 1–9, **quando** calcolo i cicli, **allora** C1 = 1–4,
  C2 = 5–8, C3 inizia con la 9.
- `PER-2` **Dato** un completamento nella Settimana 6, **quando** calcolo i totali,
  **allora** i suoi punti contano per la Settimana 6 e per il ciclo C2.
- `PER-3` **Dato** una soglia settimanale e una per ciclo, **quando** le configuro,
  **allora** valgono uguali per tutte le figlie e restano sempre le stesse (nessuna
  riduzione per assenze).

### 6. Reward individuali

- `RWD-1` **Dato** gli elenchi di reward settimanali e per ciclo, **quando** creo un
  reward, **allora** ha un testo IT e viene tradotto come le attività.
- `RWD-2` **Dato** Anna a 48 punti con soglia settimanale 50, **quando** segno un
  completamento da 5, **allora** la settimana risulta sbloccata per Anna.
- `RWD-3` **Dato** Anna a 190 punti nel ciclo con soglia di ciclo 200, **quando** segno un
  completamento da 10 nella terza settimana del ciclo, **allora** il ciclo risulta
  sbloccato subito, senza aspettare la chiusura della quarta settimana.
- `RWD-4` **Dato** Anna con 120 punti e soglia 50, **quando** guardo la settimana,
  **allora** è sbloccato un solo reward (un reward per periodo).
- `RWD-5` **Dato** una settimana sbloccata, **quando** registro il reward scelto da Anna,
  **allora** risulta "scelto, da consegnare"; **quando** lo segno consegnato, **allora**
  risulta "consegnato".
- `RWD-6` **Dato** reward scelti e non consegnati in periodi diversi, **quando** apro
  l'elenco dei reward da consegnare, **allora** li vedo tutti, con la settimana o il
  ciclo di provenienza.
- `RWD-7` **Dato** una settimana sbloccata con reward scelto, **quando** cancello un
  completamento e i punti scendono sotto soglia, **allora** compare un avviso sul periodo
  e il reward non viene annullato.

### 7. Obiettivo di squadra

- `SQD-1` **Dato** attività con il flag "conta per l'obiettivo di squadra", **quando**
  calcolo l'obiettivo del ciclo, **allora** contano solo i punti di quelle attività.
- `SQD-2` **Dato** una soglia di squadra di 100 e 2 figlie attive, **quando** calcolo le
  quote, **allora** ciascuna deve fare 50.
- `SQD-3` **Dato** Anna a 90 e Sofia a 30 punti di squadra, **quando** calcolo
  l'obiettivo, **allora** non è raggiunto (una non compensa l'altra).
- `SQD-4` **Dato** Anna a 50 e Sofia a 50, **quando** calcolo l'obiettivo, **allora** è
  raggiunto e si sblocca un reward comune dall'elenco dei reward di squadra, con scelta e
  consegna registrate come in `RWD-5` (senza figlia associata).
- `SQD-5` **Dato** una sola figlia attiva, **quando** calcolo l'obiettivo, **allora** non
  c'è obiettivo di squadra.
- `SQD-6` **Dato** un completamento di un'attività di squadra, **quando** calcolo le
  soglie individuali, **allora** i suoi punti contano anche per settimana e ciclo della
  figlia.
- `SQD-7` **Dato** un obiettivo di squadra raggiunto e riscattato, **quando** una modifica
  retroattiva porta una figlia sotto quota, **allora** compare un avviso e il reward non
  viene annullato.

### 8. Lista settimanale

- `VIS-1` **Dato** una settimana, **quando** la apro per Anna, **allora** vedo il numero
  della settimana e la lista delle sue attività, ognuna con punti, N caselle e
  contatore. Nessun giorno e nessuna data.
- `VIS-2` **Dato** una settimana, **quando** la apro per tutte le figlie, **allora** ogni
  attività indica la figlia, con caselle e contatori separati per ciascuna.
- `VIS-3` **Dato** la Settimana 6, **quando** la apro, **allora** il riepilogo mostra
  "Settimana 6 — ciclo 2, settimana 2 di 4", i punti della settimana e del ciclo, le
  soglie, lo stato dei reward e l'avanzamento di ciascuna figlia sulla propria quota di
  squadra.
- `VIS-4` **Dato** un'attività di squadra, **quando** compare nella lista, **allora** ha
  l'icona di squadra.
- `VIS-5` **Dato** settimane passate, **quando** navigo indietro, **allora** posso aprirle
  e modificarne i completamenti (`SET-4`).

### 9. Stampa

- `STM-1` **Dato** la settimana di Anna, **quando** la stampo, **allora** ottengo un
  foglio A4 dal browser (CSS di stampa) con nome, numero della settimana, lista delle
  attività con N caselle da spuntare a mano e punti, icona di squadra, soglia
  settimanale e reward settimanali tra cui scegliere. Nessuna data.
- `STM-2` **Dato** tutte le traduzioni `ok` o `manual`, **quando** stampo, **allora**
  tutti i testi del foglio sono in olandese.
- `STM-3` **Dato** almeno un testo `pending` o `failed`, **quando** avvio la stampa,
  **allora** l'app elenca quei testi con le azioni "riprova", "traduci a mano" e "stampa
  comunque".
- `STM-4` **Dato** la scelta "stampa comunque", **quando** il foglio viene generato,
  **allora** i testi senza traduzione compaiono in italiano, evidenziati.

## Bilinguismo e traduzione

### Cosa viene tradotto

- In olandese: titolo e descrizione delle attività, testi dei reward (settimanali, per
  ciclo, di squadra). Sono i testi che le figlie leggono.
- **Non** vengono tradotti dal modello: nomi delle figlie e interfaccia dell'app.
  L'interfaccia usa i file i18n (IT, NL), mai stringhe hardcoded.
- Le traduzioni sono indicizzate per (testo, lingua): aggiungere una lingua non richiede
  modifiche allo schema.

### Quando

- Al salvataggio di un testo nuovo o modificato. Il salvataggio è **immediato**; la
  traduzione gira in background con TranslateGemma 12B in locale (Ollama), 5–15 s per
  testo (vedi `backend/evals/results.md`).
- Prima di chiamare il modello si controlla la cache su (testo IT normalizzato, lingua).
  Una traduzione `manual` ha la precedenza su quella automatica.
- Il glossario di famiglia (termine IT → termine NL) viene incluso nel prompt.

### Stati

`pending` → `ok` | `failed`; qualsiasi stato → `manual` se il genitore corregge.

### Criteri

- `TRD-1` **Dato** Ollama attivo, **quando** salvo un'attività, **allora** la risposta
  arriva senza attendere la traduzione, con stato `pending`, e diventa `ok` al termine.
- `TRD-2` **Dato** Ollama spento, **quando** salvo un'attività, **allora** il salvataggio
  riesce e la traduzione passa a `failed`.
- `TRD-3` **Dato** una traduzione che non risponde entro il timeout (proposta: 60 s),
  **quando** il timeout scade, **allora** passa a `failed`.
- `TRD-4` **Dato** una traduzione `failed`, **quando** premo "riprova" con Ollama attivo,
  **allora** torna `pending` e poi `ok`.
- `TRD-5` **Dato** traduzioni `pending` al momento dell'arresto, **quando** il backend
  riparte, **allora** vengono riprese.
- `TRD-6` **Dato** un testo IT già tradotto in cache, **quando** creo un'altra attività
  con lo stesso testo, **allora** riusa la traduzione senza chiamare il modello.
- `TRD-7` **Dato** una traduzione automatica, **quando** la correggo a mano, **allora**
  diventa `manual`, non viene mai sovrascritta automaticamente e l'app propone di
  aggiungere un termine al glossario.
- `TRD-8` **Dato** una correzione manuale di "Compiti in autonomia", **quando** un'altra
  attività usa lo stesso testo IT, **allora** riceve la correzione manuale.
- `TRD-9` **Dato** una traduzione `manual`, **quando** modifico il testo IT, **allora**
  parte una nuova traduzione automatica e la manuale viene archiviata (consultabile e
  ripristinabile), mai cancellata.
- `TRD-10` **Dato** una nuova voce di glossario, **quando** la salvo, **allora** vale solo
  per le traduzioni future; le automatiche esistenti si ritraducono solo con un'azione
  esplicita, le `manual` mai.
- `TRD-11` **Dato** il glossario "compiti → huiswerk", **quando** traduco "Fare i compiti",
  **allora** il prompt inviato al modello contiene la voce del glossario.

## Fuori ambito

- **Fase 2:** PIN, accesso delle figlie all'app, deploy. Già predisposti nel modello dati:
  profilo separato dagli account, `recorded_by` e `status` sui completamenti, storico
  delle modifiche, `family_id` su tutte le tabelle.
- **Fase 3–4:** servizi remoti di qualsiasi tipo (traduzione, hosting, notifiche). Il
  modello di traduzione richiede ~8 GB di RAM e gira solo in locale.
- Più famiglie e login dei genitori.
- Date, giorni della settimana, orari, calendario reale: le settimane sono solo numerate.
- Pause e assenze: per le vacanze non si avvia la settimana; le soglie non si riducono.
- Più settimane aperte contemporaneamente.
- Saltare o modificare un'attività per una sola settimana; modifiche "da qui in poi"
  (vedi Domande aperte).
- Ricorrenze ogni N settimane.
- Penalità e saldi negativi; negozio di punti da spendere.
- Soglie diverse per figlia; più livelli di soglia nello stesso periodo.
- PDF generato dal server; stampa del ciclo o dell'obiettivo di squadra.
- Notifiche e promemoria.

## Domande aperte

1. **Togliere un'attività da una sola settimana.** Serve un "non questa settimana", così
   da toglierla dalla lista e dalla stampa? Oggi basta non segnarla (vale 0).
2. **Cancellare un'attività con completamenti.** Archiviazione (sparisce dalle settimane
   future, lo storico resta) o cancellazione vera? Proposta: solo archiviazione.
3. **Limite al bonus:** c'è un massimo ai punti assegnabili a un singolo completamento?
4. **Timeout della traduzione:** 60 s va bene?
5. **Archiviare una figlia a metà ciclo:** la quota di squadra si ricalcola sulle figlie
   rimaste da subito o dal ciclo successivo?
