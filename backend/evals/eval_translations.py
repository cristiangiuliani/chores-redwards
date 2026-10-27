"""Eval delle traduzioni IT→NL con i modelli TranslateGemma via Ollama.

Uso (da backend/):
    uv run python evals/eval_translations.py

Questa stringa tra tripli apici è una "docstring": la prima stringa di un
file/funzione è la sua documentazione (come un blocco /** ... */ in PHP,
ma Python la rende accessibile a runtime con `__doc__` e `help()`).
"""

# --- Import -----------------------------------------------------------------
# In Python ogni file è un modulo; `import x` è simile a `use` in PHP, ma
# carica davvero il modulo (non c'è autoloader). Ruff ordina gli import:
# prima la libreria standard, poi le librerie esterne (httpx).
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import httpx

# --- Costanti ---------------------------------------------------------------
# Python non ha `const`: per convenzione i nomi MAIUSCOLI sono costanti
# (nessuno lo impedisce a runtime, è un accordo tra programmatori).

OLLAMA_URL = "http://localhost:11434"
MODELS: list[str] = ["translategemma:4b", "translategemma:12b"]

# `Path(__file__)` è il percorso di questo file (come __FILE__ in PHP).
# `.parent` è la cartella che lo contiene (come __DIR__ / dirname()).
# L'operatore `/` su un Path concatena i percorsi in modo portabile.
EVALS_DIR = Path(__file__).parent
SENTENCES_FILE = EVALS_DIR / "sentences.txt"
RESULTS_FILE = EVALS_DIR / "results.md"

# Senza GPU il 12b è lento: diamo un timeout generoso (secondi).
TIMEOUT_SECONDS = 600.0

# Formato di prompt ufficiale di TranslateGemma.
# Le stringhe adiacenti tra parentesi vengono unite dal compilatore (come
# 'a' . 'b' in PHP, ma senza operatore): utile per rispettare le 88 colonne.
# `{context}` e `{text}` sono segnaposto che riempiremo con `.format(...)`.
#
# Il contesto non fa parte del formato ufficiale: lo aggiungiamo dopo la
# prima frase per aiutare il modello a scegliere il senso giusto
# (es. "Strumento" = strumento musicale, "Compiti" = compiti per casa).
CONTEXT = (
    "The texts come from a calendar of activities and chores for girls aged 8 to 10."
)

PROMPT_TEMPLATE = (
    "You are a professional Italian (it) to Dutch (nl) translator. "
    "Your goal is to accurately convey the meaning and nuances of the "
    "original Italian text while adhering to Dutch grammar, vocabulary, "
    "and cultural sensitivities. {context}\n"
    "Produce only the Dutch translation, without any additional "
    "explanations or commentary. Please translate the following Italian "
    "text into Dutch:\n"
    "\n"
    "\n"
    "{text}"
)

WARMUP_TEXT = "Ciao"


# --- Modello dati -----------------------------------------------------------
# `@dataclass` è un decoratore: genera automaticamente __init__, __repr__ e
# __eq__ a partire dai campi dichiarati. È l'equivalente di una classe PHP 8
# con "constructor property promotion", ma ancora più corta.
# `frozen=True` rende l'oggetto immutabile (come `readonly class` in PHP 8.2).
@dataclass(frozen=True)
class TranslationResult:
    model: str
    sentence: str
    translation: str
    seconds: float
    tokens_per_second: float


# --- Funzioni ---------------------------------------------------------------
# `def nome(param: tipo) -> tipo_ritorno:` è come
# `function nome(tipo $param): tipo_ritorno` in PHP.
# I type hint in Python NON sono verificati a runtime: servono a editor e
# type checker (mypy/pyright). Il corpo è delimitato dall'indentazione,
# non dalle graffe.


def read_sentences(path: Path) -> list[str]:
    """Legge le frasi, una per riga, saltando le righe vuote."""
    # `read_text` legge tutto il file (come file_get_contents).
    lines = path.read_text(encoding="utf-8").splitlines()
    # List comprehension: crea una lista trasformando/filtrando un'altra.
    # Equivale a array_filter(array_map('trim', $lines)) in PHP.
    return [line.strip() for line in lines if line.strip()]


def build_prompt(text: str) -> str:
    # Argomenti nominati (`chiave=valore`), come i named arguments di PHP 8.
    return PROMPT_TEMPLATE.format(context=CONTEXT, text=text)


def generate(client: httpx.Client, model: str, prompt: str) -> dict:
    """Chiama /api/generate di Ollama e restituisce il JSON della risposta."""
    # In Python un dict letterale `{...}` è l'array associativo di PHP.
    # Le chiavi sono stringhe tra virgolette; True/False/None con maiuscola.
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,  # una sola risposta JSON invece di uno stream
        "options": {"temperature": 0},
    }
    # httpx.Client.post(..., json=...) serializza il dict in JSON e imposta
    # l'header Content-Type, come farebbe Guzzle con l'opzione 'json'.
    response = client.post("/api/generate", json=payload)
    # Solleva un'eccezione se lo status è 4xx/5xx (come 'http_errors' in Guzzle).
    response.raise_for_status()
    return response.json()


def unload(client: httpx.Client, model: str) -> None:
    """Scarica il modello dalla RAM (keep_alive=0) prima di passare al prossimo."""
    client.post("/api/generate", json={"model": model, "keep_alive": 0})


def translate(client: httpx.Client, model: str, sentence: str) -> TranslationResult:
    """Traduce una frase misurando il tempo lato script e i token/s di Ollama."""
    # perf_counter() è un orologio monotono ad alta risoluzione, adatto a
    # misurare intervalli (come hrtime(true) in PHP, ma in secondi float).
    start = time.perf_counter()
    data = generate(client, model, build_prompt(sentence))
    seconds = time.perf_counter() - start

    # eval_duration è in nanosecondi: lo convertiamo in secondi.
    # `data["chiave"]` solleva KeyError se manca (PHP darebbe un warning);
    # `data.get("chiave", default)` è l'equivalente di `$data['k'] ?? default`.
    eval_count: int = data.get("eval_count", 0)
    eval_seconds = data.get("eval_duration", 0) / 1e9
    # Espressione condizionale: `a if cond else b` è il ternario `cond ? a : b`.
    tokens_per_second = eval_count / eval_seconds if eval_seconds > 0 else 0.0

    return TranslationResult(
        model=model,
        sentence=sentence,
        translation=data.get("response", "").strip(),
        seconds=seconds,
        tokens_per_second=tokens_per_second,
    )


def md_cell(text: str) -> str:
    """Rende sicuro un testo dentro una cella di tabella Markdown."""
    return text.replace("|", "\\|").replace("\n", " ")


def write_results(path: Path, results: list[TranslationResult]) -> None:
    """Scrive i risultati in una tabella Markdown (sovrascrive il file)."""
    # f-string: `f"...{espressione}..."` interpola valori, come
    # "...{$var}..." in PHP, ma accetta qualsiasi espressione.
    # `{x:.2f}` formatta con 2 decimali (come sprintf('%.2f', $x)).
    lines = [
        "# Risultati eval traduzioni IT→NL",
        "",
        f"Generato il {datetime.now():%Y-%m-%d %H:%M}",
        "",
        f"Contesto nel prompt: {CONTEXT}",
        "",
        "| Modello | Frase (IT) | Traduzione (NL) | Secondi | Token/s | Rating |",
        "|---|---|---|---:|---:|---|",
    ]
    # Il `for ... in ...` di Python è il foreach di PHP.
    for r in results:
        lines.append(
            f"| {r.model} | {md_cell(r.sentence)} | {md_cell(r.translation)} "
            f"| {r.seconds:.2f} | {r.tokens_per_second:.1f} |  |"
        )
    # "\n".join(lista) è implode("\n", $array): attenzione, in Python il
    # metodo sta sul separatore, non sulla lista.
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    sentences = read_sentences(SENTENCES_FILE)
    # print() scrive su stdout; len() è count() / strlen() in PHP.
    print(f"{len(sentences)} frasi da {SENTENCES_FILE.name}")

    results: list[TranslationResult] = []

    # `with` è un "context manager": garantisce la chiusura del client
    # (connessioni HTTP) all'uscita dal blocco, anche in caso di eccezione.
    # Pensalo come un try/finally automatico.
    with httpx.Client(base_url=OLLAMA_URL, timeout=TIMEOUT_SECONDS) as client:
        # try/except è il try/catch di PHP; si possono catturare più tipi.
        try:
            for model in MODELS:
                # Riscaldamento: carica il modello in RAM, risultato ignorato.
                print(f"[{model}] riscaldamento...")
                generate(client, model, build_prompt(WARMUP_TEXT))

                # enumerate() restituisce coppie (indice, valore), come
                # foreach ($arr as $i => $v); `start=1` fa partire da 1.
                # `a, b = ...` è il destructuring, come [$a, $b] = ... in PHP.
                for i, sentence in enumerate(sentences, start=1):
                    result = translate(client, model, sentence)
                    results.append(result)
                    print(
                        f"[{model} {i}/{len(sentences)}] "
                        f"{result.seconds:.2f}s {result.tokens_per_second:.1f} tok/s"
                    )

                unload(client, model)
        except httpx.ConnectError:
            # file=sys.stderr scrive sullo standard error (come fwrite(STDERR,...)).
            print(
                f"Impossibile connettersi a Ollama su {OLLAMA_URL}. "
                "Avvialo con `ollama serve`.",
                file=sys.stderr,
            )
            return 1
        except httpx.HTTPStatusError as exc:
            # `as exc` dà un nome all'eccezione, come catch (Exception $exc).
            if exc.response.status_code == 404:
                print(
                    "Modello non trovato. Scaricalo con `ollama pull <modello>`.\n"
                    f"Dettaglio: {exc.response.text}",
                    file=sys.stderr,
                )
                return 1
            # `raise` senza argomenti rilancia l'eccezione corrente.
            raise

    write_results(RESULTS_FILE, results)
    print(f"Risultati scritti in {RESULTS_FILE}")
    return 0


# Questo blocco gira solo se il file è eseguito direttamente, non quando è
# importato da un altro modulo. In PHP non c'è un equivalente diretto: è come
# separare "libreria" e "script" nello stesso file.
# sys.exit(codice) termina con quel codice di uscita (come exit(1) in PHP).
if __name__ == "__main__":
    sys.exit(main())
