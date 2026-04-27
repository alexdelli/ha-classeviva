"""Integrazione Classeviva per Home Assistant."""
from __future__ import annotations

import logging
from datetime import timedelta

import requests

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    API_BASE_URL,
    API_HEADERS,
    DEFAULT_SCAN_INTERVAL,
    CONF_USERNAME,
    CONF_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura Classeviva da una voce di configurazione."""
    coordinator = ClassevivaCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Rimuovi una voce di configurazione."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class ClassevivaCoordinator(DataUpdateCoordinator):
    """Coordinatore per il recupero dati da Classeviva."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Inizializza il coordinatore."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=DEFAULT_SCAN_INTERVAL),
        )
        self.entry = entry
        self._token = None
        self._student_id = None

    def _login(self) -> bool:
        """Effettua il login e salva il token."""
        username = self.entry.data[CONF_USERNAME]
        password = self.entry.data[CONF_PASSWORD]

        # Classeviva vuole il codice fiscale oppure "S" + codice utente
        # Prova prima il formato standard
        payload = {
            "uid": username,
            "pass": password,
            "pin": "",
            "target": "famiglia" if username.startswith("S") else "studente",
        }

        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/login",
                headers=API_HEADERS,
                json=payload,
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            self._token = data.get("token")
            self._student_id = data.get("ident")
            return True
        except Exception as err:
            _LOGGER.error("Errore durante il login a Classeviva: %s", err)
            return False

    def _get_headers(self) -> dict:
        """Restituisce gli header con il token di autenticazione."""
        headers = API_HEADERS.copy()
        headers["Z-Auth-Token"] = self._token
        return headers

    def _fetch_agenda(self) -> list:
        """Recupera l'agenda dei prossimi 30 giorni."""
        from datetime import date, timedelta as td
        today = date.today()
        end = today + td(days=30)
        begin_str = today.strftime("%Y%m%d")
        end_str = end.strftime("%Y%m%d")

        try:
            response = requests.get(
                f"{API_BASE_URL}/students/{self._student_id}/agenda/all/{begin_str}/{end_str}",
                headers=self._get_headers(),
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            eventi = data.get("agenda", [])

            risultati = []
            for ev in eventi:
                risultati.append({
                    "data": ev.get("evtDatetimeBegin", "")[:10],
                    "materia": ev.get("subjectDesc", ev.get("authorName", "Evento")),
                    "note": ev.get("notes", ""),
                    "tipo": "compito" if ev.get("evtCode") == "AGHW" else "verifica" if ev.get("evtCode") == "AGNT" else "evento",
                })
            # Ordina per data
            risultati.sort(key=lambda x: x["data"])
            return risultati[:15]  # Mostra al massimo i prossimi 15 eventi
        except Exception as err:
            _LOGGER.warning("Errore nel recupero agenda: %s", err)
            return []

    def _fetch_voti(self) -> list:
        """Recupera gli ultimi voti."""
        try:
            response = requests.get(
                f"{API_BASE_URL}/students/{self._student_id}/grades",
                headers=self._get_headers(),
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            grades = data.get("grades", [])

            risultati = []
            for v in grades:
                # Salta voti non numerici o assenti
                valore = v.get("decimalValue")
                if valore is None:
                    valore = v.get("displayValue", "—")
                else:
                    valore = str(valore)

                risultati.append({
                    "data": v.get("evtDate", ""),
                    "materia": v.get("subjectDesc", ""),
                    "voto": valore,
                    "tipo": v.get("componentDesc", ""),
                    "nota": v.get("notesForFamily", ""),
                })
            # Ordina per data decrescente (più recenti prima)
            risultati.sort(key=lambda x: x["data"], reverse=True)
            return risultati[:20]
        except Exception as err:
            _LOGGER.warning("Errore nel recupero voti: %s", err)
            return []

    def _fetch_comunicazioni(self) -> list:
        """Recupera le comunicazioni dalla bacheca."""
        try:
            response = requests.get(
                f"{API_BASE_URL}/students/{self._student_id}/noticeboard",
                headers=self._get_headers(),
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])

            risultati = []
            for item in items:
                risultati.append({
                    "data": item.get("cntValidFrom", "")[:10],
                    "titolo": item.get("cntTitle", ""),
                    "categoria": item.get("cntCategory", ""),
                    "letta": item.get("readStatus", False),
                })
            risultati.sort(key=lambda x: x["data"], reverse=True)
            return risultati[:10]
        except Exception as err:
            _LOGGER.warning("Errore nel recupero comunicazioni: %s", err)
            return []

    async def _async_update_data(self):
        """Aggiorna tutti i dati da Classeviva."""
        try:
            # Esegui il login e il fetch in un thread separato (non blocca HA)
            logged_in = await self.hass.async_add_executor_job(self._login)
            if not logged_in:
                raise UpdateFailed("Login a Classeviva fallito. Controlla le credenziali.")

            agenda = await self.hass.async_add_executor_job(self._fetch_agenda)
            voti = await self.hass.async_add_executor_job(self._fetch_voti)
            comunicazioni = await self.hass.async_add_executor_job(self._fetch_comunicazioni)

            return {
                "agenda": agenda,
                "voti": voti,
                "comunicazioni": comunicazioni,
            }
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Errore imprevisto: {err}") from err
