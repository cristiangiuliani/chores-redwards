# SPEC — Fase 1: attività settimanali, punti e reward

## Obiettivo

Un'app locale con cui i genitori preparano la lista settimanale delle attività delle
figlie, assegnano punti e gestiscono reward settimanali e per ciclo.
Il genitore scrive in italiano; le figlie leggono la lista stampata in olandese.

## Utenti

- **Fase 1: solo genitori.** Creano profili, attività e reward, avviano e chiudono le
  settimane, segnano i completamenti, registrano i reward scelti, stampano la lista.
- Le figlie non usano l'app: ricevono il foglio stampato.
- Esiste una sola famiglia, senza login.

## Termini

- **Settimana:** un periodo numerato in sequenza (Settimana 1, 2, 3…) che il genitore
  **avvia e chiude a mano**, come uno sprint di Jira. L'app non usa date, giorni della
  settimana né calendario. A differenza di Jira, ciò che non è stato completato non passa
  alla settimana successiva. Se nessuna settimana è aperta (es. vacanze) non succede
  nulla: nessuna attività, nessun punto, nessuna soglia.
- **Attività:** qualcosa da fare (es. "Fare il letto"), con titolo, descrizione
  facoltativa, punti base, figlie assegnate e numero di volte per settimana (N, minimo 1).
  Le figlie decidono quando svolgerla durante la settimana. Ogni attività si ripete ogni
  settimana finché non viene archiviata; non ha settimana di inizio né di fine.
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

### 2. Settimane

- `SET-1` **Dato** nessuna settimana, **quando** avvio una settimana, **allora** viene
  creata la Settimana 1, aperta.
- `SET-2` **Dato** la Settimana 3 aperta, **quando** provo ad avviarne un'altra,
  **allora** l'operazione viene rifiutata: può esserci una sola settimana aperta.
- `SET-3` **Dato** la Settimana 3 aperta, **quando** la chiudo e avvio la successiva,
  **allora** viene creata la Settimana 4.
- `SET-4` **Dato** la Settimana 3 chiusa, **quando** provo ad aggiungere, modificare o
  cancellare un suo completamento, **allora** l'operazione viene rifiutata: una
  settimana chiusa è in sola lettura.
- `SET-5` **Dato** la Settimana 3 chiusa, la Settimana 4 non ancora avviata e nessun
  reward della Settimana 3 ancora scelto, **quando** riapro la Settimana 3, **allora**
  torna aperta e modificabile, e i reward che la chiusura aveva sbloccato tornano
  "in corso". Se la Settimana 3 è l'ultima di un ciclo, vale lo stesso per il reward di
  ciclo.
- `SET-6` **Dato** la Settimana 3 chiusa, **quando** provo a riaprirla con la Settimana 4
  già avviata, oppure con un reward della Settimana 3 (o del suo ciclo, se ne è l'ultima
  settimana) già scelto, **allora** l'operazione viene rifiutata.

### 3. Attività

- `ATT-1` **Dato** la Settimana 5 aperta, **quando** creo un'attività "2 volte",
  **allora** compare subito nella Settimana 5 con contatore 0/2, e in tutte le
  settimane successive.
- `ATT-2` **Dato** nessuna settimana aperta (Settimana 4 chiusa), **quando** creo
  un'attività, **allora** compare a partire dalla Settimana 5, al suo avvio.
- `ATT-3` **Dato** un'attività senza N indicato, **quando** la salvo, **allora** vale
  1 volta per settimana; N = 0 viene rifiutato.
- `ATT-4` **Dato** un'attività assegnata ad Anna e Sofia, **quando** la creo, **allora**
  esiste un solo testo con una sola traduzione, e compare nella lista di entrambe.
- `ATT-5` **Dato** un'attività da 10 punti con completamenti passati da 10, **quando**
  porto i punti base a 15, **allora** i completamenti passati restano a 10 e i nuovi
  propongono 15.
- `ATT-6` **Dato** 5 attività di Anna, di cui 2 già assegnate anche a Sofia, **quando**
  uso "Assegna tutte le attività di Anna anche a Sofia", **allora** Sofia ha tutte e 5 le
  attività, senza duplicati e senza nuove traduzioni.
- `ATT-7` **Dato** un'attività con completamenti nella Settimana 5 aperta, **quando** la
  archivio, **allora** resta nella Settimana 5 con i suoi completamenti, non compare
  dalla Settimana 6 in poi e i punti già assegnati restano nei totali.
- `ATT-8` **Dato** un'attività senza completamenti nella Settimana 5 aperta, **quando** la
  archivio, **allora** sparisce subito dalla Settimana 5, dalla lista e dalla stampa.
- `ATT-9` **Dato** un'attività archiviata, **quando** guardo le settimane chiuse in cui
  compariva, **allora** la vedo ancora con i suoi completamenti.

### 4. Completamenti e punti

- `CMP-1` **Dato** un'attività da 10 punti nella Settimana 5, **quando** segno una volta
  come fatta per Anna, **allora** viene creato un completamento da 10 punti legato alla
  Settimana 5.
- `CMP-2` **Dato** un'attività da 10 punti, **quando** segno un completamento con 5 punti
  (fatta a metà) o con 15 (bonus), **allora** il completamento salva i punti indicati.
- `CMP-3` **Dato** un completamento, **quando** inserisco punti negativi, **allora** il
  salvataggio viene rifiutato.
- `CMP-4` **Dato** un'attività "3 volte", **quando** segno 3 completamenti, **allora** il
  contatore mostra 3/3; un quarto completamento nella stessa settimana è accettato, il
  contatore mostra 4/3 e i punti contano per settimana e ciclo.
- `CMP-5` **Dato** caselle non completate, **quando** chiudo la settimana, **allora**
  valgono 0 punti e non tolgono punti (non esistono penalità).

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
  completamento da 5, **allora** la settimana risulta "in corso" con l'avanzamento;
  **quando** chiudo la settimana, **allora** risulta sbloccata per Anna.
- `RWD-3` **Dato** Anna a 210 punti nel ciclo con soglia di ciclo 200 già durante la terza
  settimana, **quando** guardo il ciclo, **allora** risulta "in corso" con l'avanzamento;
  **quando** chiudo la quarta settimana del ciclo, **allora** il ciclo risulta sbloccato.
- `RWD-4` **Dato** Anna con 120 punti e soglia 50, **quando** chiudo la settimana,
  **allora** è sbloccato un solo reward (un reward per periodo).
- `RWD-5` **Dato** un periodo (settimana o ciclo) chiuso e sbloccato per Anna, **quando**
  registro il reward scelto, **allora** l'operazione riesce e il periodo risulta
  "reward scelto" con il reward indicato: il blocco della settimana chiusa vale solo per
  i completamenti.
- `RWD-6` **Dato** un periodo aperto con Anna sopra soglia, **quando** provo a registrare
  il reward scelto, **allora** l'operazione viene rifiutata: i reward si scelgono solo a
  periodo chiuso.

### 7. Lista settimanale

- `VIS-1` **Dato** una settimana, **quando** la apro per Anna, **allora** vedo il numero
  della settimana e la lista delle sue attività, ognuna con punti, N caselle e
  contatore. Nessun giorno e nessuna data.
- `VIS-2` **Dato** una settimana, **quando** la apro per tutte le figlie, **allora** ogni
  attività indica la figlia, con caselle e contatori separati per ciascuna.
- `VIS-3` **Dato** la Settimana 6, **quando** la apro, **allora** il riepilogo mostra
  "Settimana 6 — ciclo 2, settimana 2 di 4", i punti della settimana e del ciclo, le
  soglie, lo stato dei reward e l'avanzamento di ciascuna figlia.

### 8. Stampa

- `STM-1` **Dato** la settimana di Anna, **quando** la stampo, **allora** ottengo un
  foglio A4 dal browser con nome, numero della settimana, lista delle attività
  con N caselle da spuntare a mano e punti, soglia settimanale e reward settimanali tra
  cui scegliere. Nessuna data.
- `STM-2` **Dato** tutte le traduzioni `ok` o `manual`, **quando** stampo, **allora**
  tutti i testi del foglio sono in olandese.
- `STM-3` **Dato** almeno un testo della settimana `pending` o `failed`, **quando** provo
  a stampare, **allora** la stampa viene bloccata e l'app elenca i testi mancanti, con
  le azioni "riprova" e "traduci a mano" per sbloccarla.

### 9. AI nell'app (settimana di studio 10) — criteri da scrivere

- Creazione di attività da linguaggio naturale (output strutturato).
- Riepilogo generato: testo in olandese scritto dal modello locale per le figlie, a
  partire dai dati della settimana. È diverso dal riepilogo della settimana di `VIS-3`.
- Astrazione del provider del modello. In fase 1 collega solo modelli locali (Ollama);
  i provider remoti restano nel Backlog (vedi "Fuori ambito").

## Bilinguismo e traduzione

### Cosa viene tradotto

- In olandese: titolo e descrizione delle attività, testi dei reward (settimanali e per
  ciclo). Sono i testi che le figlie leggono.
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

- `pending` → `ok` | `failed`
- `failed` → `pending` con "riprova"
- qualsiasi stato → `manual` se il genitore corregge
- Una traduzione è legata al testo IT, non all'attività: cambiare il testo di
  un'attività non modifica né archivia la traduzione del testo precedente.

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
- `TRD-9` **Dato** "Compiti in autonomia" con traduzione `manual`, usato da due
  attività, **quando** cambio il testo IT della prima in "Compiti da sola", **allora** la
  prima riceve la traduzione del nuovo testo (dalla cache o nuova automatica), mentre la
  correzione manuale di "Compiti in autonomia" resta invariata e continua a valere per la
  seconda attività.
- `TRD-10` **Dato** una nuova voce di glossario, **quando** la salvo, **allora** vale solo
  per le traduzioni future; le automatiche esistenti si ritraducono solo con un'azione
  esplicita, le `manual` mai.
- `TRD-11` **Dato** il glossario "compiti → huiswerk", **quando** traduco "Fare i compiti",
  **allora** il prompt inviato al modello contiene la voce del glossario.

## Fuori ambito

- **Backlog:** attività una tantum; obiettivo di squadra con reward condivisi;
  tracciamento della consegna dei reward; modifica dei completamenti di settimane chiuse
  oltre a `SET-5`; servizi remoti di qualsiasi tipo (traduzione, hosting dei modelli, notifiche). Il
  modello di traduzione richiede ~8 GB di RAM e gira solo in locale.
- **Fase 2:** PIN, accesso delle figlie all'app, deploy.
- Più famiglie e login dei genitori.
- Date, giorni della settimana, orari, calendario reale: le settimane sono solo numerate.
- Pause e assenze: per le vacanze non si avvia la settimana; le soglie non si riducono.
- Più settimane aperte contemporaneamente.
- Modificare un'attività solo per una settimana.
- Ricorrenze ogni N settimane.
- Penalità e saldi negativi; negozio di punti da spendere.
- Soglie diverse per figlia; più livelli di soglia nello stesso periodo.
- PDF generato dal server; stampa del ciclo.
- Notifiche e promemoria.

## Domande aperte

1. **Togliere un'attività da una sola settimana.** Serve un "non questa settimana", così
   da toglierla dalla lista e dalla stampa? Oggi basta non segnarla (vale 0).
2. **Limite al bonus:** c'è un massimo ai punti assegnabili a un singolo completamento?
3. **Timeout della traduzione:** 60 s va bene?
4. **Riepilogo generato:** come arriva alle figlie in fase 1, uno per figlia o uno unico,
   quando si genera, se il genitore può correggerlo. Da decidere in settimana di studio 10.
