# 🎒 Classeviva per Home Assistant

Integrazione non ufficiale per visualizzare i dati del registro elettronico **Classeviva (Spaggiari)** direttamente in Home Assistant.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Versione](https://img.shields.io/badge/versione-1.4.4-blue)
![HA minimo](https://img.shields.io/badge/Home%20Assistant-2023.1.0+-green)

---

## ✨ Funzionalità

- 📅 **Agenda** — compiti e verifiche giorno per giorno con navigazione settimanale
- 📊 **Voti** — media per materia e ultimi 3 voti, ordinati dalla media più alta
- 📬 **Comunicazioni** — bacheca scuola-famiglia con evidenziazione messaggi non letti e link allegati
- 🔄 Aggiornamento automatico ogni ora
- 👨‍👩‍👧 Supporto per più studenti (aggiungi più volte l'integrazione)

---

## 📦 Dipendenze — cosa installare prima

Le schede Lovelace richiedono **custom:button-card**.

### Installazione button-card tramite HACS
1. Apri **HACS** in Home Assistant
2. Vai su **Frontend**
3. Cerca **"Button Card"** di RomRider e installala
4. Riavvia Home Assistant

🔗 Repository: [https://github.com/custom-cards/button-card](https://github.com/custom-cards/button-card)

---

## 📦 Installazione integrazione tramite HACS

1. Apri HACS → **Integrazioni** → 3 puntini → **"Repository personalizzati"**
2. Inserisci l'URL di questo repository, categoria **"Integration"**
3. Cerca **"Classeviva"** e installala → **Riavvia Home Assistant**
4. Vai su **Impostazioni → Dispositivi e servizi → + Aggiungi integrazione** → cerca **"Classeviva"**

---

## ⚙️ Configurazione

| Campo | Descrizione |
|-------|-------------|
| **Codice utente** | Genitori: codice tipo `G1234567X` o `X1234567X`. Studenti: `S1234567X` |
| **Password** | La password del sito [web.spaggiari.eu](https://web.spaggiari.eu) |
| **Nome studente** | Nome a tua scelta per identificare i sensori (es. `Marco`) |

> **Nota per i genitori**: il codice inizia con `G` (Genitore 1) o `X` (Genitore 2). L'integrazione ricava automaticamente l'ID dello studente.

---

## 📡 Sensori creati

| Sensore | Valore | Attributi |
|---------|--------|-----------|
| `sensor.classeviva_[nome]_classeviva_agenda_[nome]` | N° eventi prossimi 30gg | Lista eventi: data, materia, tipo, note |
| `sensor.classeviva_[nome]_classeviva_voti_[nome]` | Media voti generale | Lista voti: data, materia, voto, tipo, nota |
| `sensor.classeviva_[nome]_classeviva_comunicazioni_[nome]` | N° non lette | Lista comunicazioni: titolo, categoria, data, letta, event_code, pub_id, ha_allegato |

---

## 🖥️ Schede Lovelace

Le schede si trovano nei file allegati a questa release:
- `card_agenda.yaml` — agenda settimanale con navigazione
- `card_voti.yaml` — voti per materia con media
- `card_comunicazioni.yaml` — comunicazioni con allegati

Esempio
<img width="1579" height="746" alt="Screenshot 2026-04-27 alle 23 28 36" src="https://github.com/user-attachments/assets/ec95ba3a-1d6e-473c-b99a-1c2aed68c078" />


> ⚠️ In tutte le card sostituisci `studente` con il nome inserito durante la configurazione (in minuscolo).

---

## ❓ Problemi comuni

**"Credenziali non valide"** → Verifica su [web.spaggiari.eu](https://web.spaggiari.eu). Genitori: codice con `G` o `X`.

**"Impossibile connettersi"** → Verifica la connessione internet di Home Assistant.

**I dati non si aggiornano** → Aggiornamento ogni ora. Forza da Impostazioni → Dispositivi e servizi → Classeviva → Aggiorna.

**La scheda è vuota** → Verifica che `custom:button-card` sia installato da HACS → Frontend.

---

## ⚠️ Disclaimer

Questa è un'integrazione **non ufficiale** e non è affiliata con Spaggiari Spa. Usa le API pubbliche di Classeviva allo stesso modo dell'app ufficiale. L'autore non è responsabile per eventuali violazioni dei termini di servizio.

---

## 📄 Licenza

MIT — vedi [LICENSE](LICENSE)
