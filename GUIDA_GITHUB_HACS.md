# 🚀 Guida: come pubblicare su GitHub e installare via HACS

## PARTE 1 — Pubblica su GitHub

### Passo 1: Crea il repository su GitHub

1. Vai su https://github.com e accedi
2. Clicca il **"+"** in alto a destra → **"New repository"**
3. Compila così:
   - **Repository name**: `ha-classeviva`
   - **Description**: `Integrazione Home Assistant per Classeviva (registro elettronico)`
   - **Public** (deve essere pubblico per funzionare con HACS)
   - Spunta **"Add a README file"**: NO (lo abbiamo già noi)
4. Clicca **"Create repository"**

---

### Passo 2: Carica i file su GitHub

Sul tuo nuovo repository vuoto, clicca **"uploading an existing file"** (link blu al centro della pagina).

Trascina o seleziona TUTTI i file e cartelle del pacchetto che hai scaricato:
```
hacs.json
README.md
LICENSE
custom_components/
  classeviva/
    __init__.py
    config_flow.py
    const.py
    manifest.json
    sensor.py
    strings.json
    translations/
      it.json
      en.json
```

⚠️ **Attenzione**: GitHub non accetta cartelle trascinate direttamente dal browser.
   Usa uno di questi metodi alternativi:

**Metodo A — GitHub Desktop (più semplice):**
1. Scarica GitHub Desktop da https://desktop.github.com
2. Clicca "Clone" sul tuo repository appena creato
3. Scegli una cartella sul tuo PC
4. Copia i file dentro quella cartella
5. In GitHub Desktop, clicca "Commit to main" → "Push origin"

**Metodo B — Caricamento manuale cartella per cartella:**
1. Carica prima i file nella root (hacs.json, README.md, LICENSE)
2. Poi entra nella cartella `custom_components/classeviva/` che GitHub ti mostrerà
3. Carica i file .py, manifest.json, strings.json
4. Crea la cartella `translations` e carica it.json e en.json

---

### Passo 3: Crea un Release (versione)

HACS richiede almeno un "Release" per funzionare correttamente:

1. Nel tuo repository, clicca **"Releases"** (colonna destra) → **"Create a new release"**
2. Compila:
   - **Tag**: `v1.0.0`
   - **Release title**: `v1.0.0 — Prima versione`
   - **Description**: `Prima release dell'integrazione Classeviva per Home Assistant`
3. Clicca **"Publish release"**

---

## PARTE 2 — Installa tramite HACS

### Passo 1: Aggiungi il repository a HACS

1. Apri Home Assistant → vai su **HACS** (nel menu laterale)
2. Clicca i **3 puntini** in alto a destra
3. Scegli **"Repository personalizzati"**
4. Nel campo URL incolla l'indirizzo del tuo repository GitHub:
   ```
   https://github.com/TUO_USERNAME/ha-classeviva
   ```
   (sostituisci `TUO_USERNAME` con il tuo nome utente GitHub)
5. Categoria: **Integration**
6. Clicca **"Aggiungi"**

---

### Passo 2: Installa l'integrazione

1. Cerca **"Classeviva"** nella sezione Integrazioni di HACS
2. Clicca sull'integrazione → **"Scarica"**
3. Conferma la versione e clicca **"Scarica"**
4. **Riavvia Home Assistant** quando richiesto

---

### Passo 3: Configura l'integrazione

1. Vai su **Impostazioni → Dispositivi e servizi**
2. Clicca **"+ Aggiungi integrazione"**
3. Cerca **"Classeviva"**
4. Inserisci le credenziali e il nome dello studente
5. Fatto! ✅

---

## Struttura finale del repository GitHub

Il tuo repository dovrà avere esattamente questa struttura:

```
ha-classeviva/                  ← root del repository
├── hacs.json                   ← configurazione HACS
├── README.md                   ← pagina descrittiva
├── LICENSE                     ← licenza MIT
└── custom_components/
    └── classeviva/
        ├── __init__.py         ← logica principale
        ├── config_flow.py      ← configurazione guidata
        ├── const.py            ← costanti
        ├── manifest.json       ← info integrazione
        ├── sensor.py           ← sensori
        ├── strings.json        ← testi interfaccia
        └── translations/
            ├── it.json         ← italiano
            └── en.json         ← inglese
```

---

## Condividere con altri (opzionale)

Una volta che il repository è pubblico e funzionante, chiunque può aggiungerlo
a HACS con lo stesso URL del tuo repository. Puoi condividere il link così:

> "Aggiungi questo repository a HACS come integrazione personalizzata:
> `https://github.com/TUO_USERNAME/ha-classeviva`"
