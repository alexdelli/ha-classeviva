# 📚 Classeviva per Home Assistant — Guida all'installazione

## Cosa fa questa integrazione?
Connette Home Assistant al registro elettronico Classeviva e mostra:
- 📅 **Agenda**: compiti e verifiche in programma
- 📊 **Voti**: ultimi voti con media automatica
- 📬 **Comunicazioni**: bacheca scuola-famiglia

---

## PASSO 1 — Copia i file

Copia la cartella `classeviva` (quella con tutti i file .py dentro) nella tua 
cartella di Home Assistant:

```
/config/custom_components/classeviva/
```

Puoi farlo in 3 modi:
- **Con Samba/SMB**: se hai l'addon Samba Share attivo, la trovi come cartella di rete
- **Con File Editor**: addon di HA che ti permette di gestire i file dall'interfaccia web
- **Con SSH**: se hai accesso SSH al tuo HA

La struttura finale deve essere:
```
/config/
  custom_components/
    classeviva/
      __init__.py
      config_flow.py
      const.py
      manifest.json
      sensor.py
      strings.json
```

---

## PASSO 2 — Riavvia Home Assistant

Dopo aver copiato i file, **riavvia Home Assistant**.
Vai su: Impostazioni → Sistema → Riavvia

---

## PASSO 3 — Aggiungi l'integrazione

1. Vai su **Impostazioni → Dispositivi e servizi**
2. Clicca **"+ Aggiungi integrazione"** (in basso a destra)
3. Cerca **"Classeviva"**
4. Inserisci:
   - **Codice utente**: il tuo codice Classeviva (es. `S1234567X` per i genitori, 
     oppure il codice fiscale per gli studenti)
   - **Password**: la tua password Classeviva
   - **Nome studente**: come vuoi chiamarlo in HA (es. "Marco")

---

## PASSO 4 — Aggiungi la scheda alla dashboard

1. Vai nella tua **Dashboard** di Home Assistant
2. Clicca i **3 puntini** in alto a destra → "Modifica dashboard"
3. Clicca **"+"** per aggiungere una scheda
4. Scorri in fondo e scegli **"Manuale"**
5. Copia e incolla il contenuto del file `lovelace_card.yaml`
6. ⚠️ **IMPORTANTE**: sostituisci tutte le occorrenze di `studente` con il nome
   che hai inserito nel passo precedente, in minuscolo e senza spazi 
   (es. se hai scritto "Marco", diventa `marco`)

   I sensori si chiameranno:
   - `sensor.classeviva_agenda_marco`
   - `sensor.classeviva_voti_marco`
   - `sensor.classeviva_comunicazioni_marco`

---

## PASSO 5 — Verifica

Dopo qualche minuto, i sensori dovrebbero popolarsi.
Puoi verificarli andando su:
**Impostazioni → Dispositivi e servizi → Classeviva → [numero] entità**

---

## Problemi comuni

### "Credenziali non valide"
- Assicurati di usare le stesse credenziali dell'app o del sito web Classeviva
- I genitori usano di solito un codice che inizia con `S` oppure il codice fiscale

### "Impossibile connettersi"
- Verifica che HA abbia accesso a internet
- Prova ad aprire `https://web.spaggiari.eu` dal browser per vedere se il sito è raggiungibile

### I sensori mostrano dati vecchi
- I dati si aggiornano automaticamente ogni ora
- Puoi forzare l'aggiornamento andando su Impostazioni → Dispositivi e servizi → Classeviva → "Aggiorna"

### La scheda mostra "sensor.classeviva_agenda_studente" invece dei dati
- Hai dimenticato di sostituire `studente` con il nome corretto nella scheda Lovelace

---

## Note sulla privacy
Le credenziali vengono salvate in modo sicuro nel file `config/.storage/core.config_entries` 
di Home Assistant e non vengono mai inviate a servizi esterni tranne a Classeviva.
