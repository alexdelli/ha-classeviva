# 🎒 Classeviva per Home Assistant

Integrazione non ufficiale per visualizzare i dati del registro elettronico **Classeviva (Spaggiari)** direttamente in Home Assistant.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Versione](https://img.shields.io/badge/versione-1.0.0-blue)
![HA minimo](https://img.shields.io/badge/Home%20Assistant-2023.1.0+-green)

---

## ✨ Funzionalità

- 📅 **Agenda** — compiti e verifiche in programma (prossimi 30 giorni)
- 📊 **Voti** — ultimi voti con calcolo automatico della media
- 📬 **Comunicazioni** — bacheca scuola-famiglia con conteggio messaggi non letti
- 🔄 Aggiornamento automatico ogni ora
- 👨‍👩‍👧 Supporto per più studenti (aggiungi più volte l'integrazione)

---

## 📦 Installazione tramite HACS

1. Apri HACS in Home Assistant
2. Vai su **Integrazioni** → clicca i **3 puntini** in alto a destra → **"Repository personalizzati"**
3. Inserisci l'URL di questo repository e scegli la categoria **"Integration"**
4. Clicca **"Aggiungi"**, poi cerca **"Classeviva"** e installala
5. **Riavvia Home Assistant**
6. Vai su **Impostazioni → Dispositivi e servizi → + Aggiungi integrazione** → cerca **"Classeviva"**

---

## ⚙️ Configurazione

Durante la configurazione ti verranno chiesti:

| Campo | Descrizione |
|-------|-------------|
| **Codice utente** | Il tuo username Classeviva. I genitori usano un codice tipo `S1234567X`, gli studenti il codice fiscale |
| **Password** | La password del sito [web.spaggiari.eu](https://web.spaggiari.eu) |
| **Nome studente** | Un nome a tua scelta per riconoscere i sensori in HA (es. `Marco`) |

---

## 📡 Sensori creati

Dopo la configurazione, vengono creati **3 sensori** (il suffisso dipende dal nome inserito):

| Sensore | Valore | Attributi |
|---------|--------|-----------|
| `sensor.classeviva_agenda_[nome]` | N° eventi prossimi 30gg | Lista eventi con data, materia, tipo, note |
| `sensor.classeviva_voti_[nome]` | Media voti | Lista voti con data, materia, voto, tipo, nota |
| `sensor.classeviva_comunicazioni_[nome]` | N° non lette | Lista comunicazioni con titolo, categoria, data, stato lettura |

---

## 🖥️ Scheda Lovelace

Copia questo YAML in una scheda "Manuale" della tua dashboard (sostituisci `[nome]` con il nome dello studente in minuscolo):

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      ## 🎒 Classeviva — Registro Elettronico
  - type: markdown
    content: >
      ## 📅 Agenda — Prossimi compiti e verifiche
      {% set eventi = state_attr('sensor.classeviva_agenda_[nome]', 'eventi') %}
      {% if eventi and eventi | length > 0 %}
      | Data | Materia | Tipo | Note |
      |------|---------|------|------|
      {% for ev in eventi %}
      | **{{ ev.data }}** | {{ ev.materia }} | {{ ev.tipo | capitalize }} | {{ ev.note[:60] }} |
      {% endfor %}
      {% else %}
      _Nessun evento in programma_ ✅
      {% endif %}
  - type: markdown
    content: >
      ## 📊 Ultimi voti — Media: {{ states('sensor.classeviva_voti_[nome]') }}
      {% set voti = state_attr('sensor.classeviva_voti_[nome]', 'voti') %}
      {% if voti and voti | length > 0 %}
      | Data | Materia | Voto | Tipo |
      |------|---------|------|------|
      {% for v in voti[:10] %}
      | {{ v.data }} | {{ v.materia }} | {% if v.voto | float(0) >= 6 %}✅{% else %}⚠️{% endif %} **{{ v.voto }}** | {{ v.tipo }} |
      {% endfor %}
      {% else %}
      _Nessun voto disponibile_
      {% endif %}
  - type: markdown
    content: >
      ## 📬 Comunicazioni (non lette: {{ states('sensor.classeviva_comunicazioni_[nome]') }})
      {% set com = state_attr('sensor.classeviva_comunicazioni_[nome]', 'comunicazioni') %}
      {% if com and com | length > 0 %}
      {% for c in com %}
      ---
      {% if not c.letta %}🔴{% else %}✅{% endif %} **{{ c.titolo }}** — _{{ c.data }}_
      {% endfor %}
      {% else %}
      _Nessuna comunicazione_
      {% endif %}
```

---

## ❓ Problemi comuni

**"Credenziali non valide"**
→ Verifica le credenziali su [web.spaggiari.eu](https://web.spaggiari.eu). I genitori usano il codice che inizia con `S`.

**"Impossibile connettersi"**
→ Verifica che Home Assistant abbia accesso a internet e che il sito Spaggiari sia raggiungibile.

**I dati non si aggiornano**
→ L'aggiornamento avviene ogni ora. Puoi forzarlo da Impostazioni → Dispositivi e servizi → Classeviva → Aggiorna.

---

## ⚠️ Disclaimer

Questa è un'integrazione **non ufficiale** e non è affiliata con Spaggiari Spa. Usa le API pubbliche di Classeviva allo stesso modo dell'app ufficiale. L'autore non è responsabile per eventuali violazioni dei termini di servizio.

---

## 📄 Licenza

MIT — vedi [LICENSE](LICENSE)
