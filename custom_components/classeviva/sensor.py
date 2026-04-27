"""Sensori Classeviva per Home Assistant."""
from __future__ import annotations

import logging
from datetime import date

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ClassevivaCoordinator
from .const import DOMAIN, CONF_STUDENT_NAME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Crea i sensori Classeviva."""
    coordinator: ClassevivaCoordinator = hass.data[DOMAIN][entry.entry_id]
    student_name = entry.data.get(CONF_STUDENT_NAME, "Studente")

    async_add_entities([
        ClassevivaAgendaSensor(coordinator, entry, student_name),
        ClassevivaVotiSensor(coordinator, entry, student_name),
        ClassevivaComunicazioniSensor(coordinator, entry, student_name),
    ])


class ClassevivaBaseSensor(CoordinatorEntity, SensorEntity):
    """Sensore base Classeviva."""

    def __init__(
        self,
        coordinator: ClassevivaCoordinator,
        entry: ConfigEntry,
        student_name: str,
        sensor_type: str,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._student_name = student_name
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": f"Classeviva — {self._student_name}",
            "manufacturer": "Spaggiari",
            "model": "Classeviva",
        }


class ClassevivaAgendaSensor(ClassevivaBaseSensor):
    """Sensore per l'agenda compiti e verifiche."""

    def __init__(self, coordinator, entry, student_name):
        super().__init__(coordinator, entry, student_name, "agenda")
        self._attr_name = f"Classeviva Agenda — {student_name}"
        self._attr_icon = "mdi:calendar-check"

    @property
    def native_value(self) -> str:
        """Restituisce il numero di eventi nei prossimi 7 giorni."""
        if not self.coordinator.data:
            return "0"
        agenda = self.coordinator.data.get("agenda", [])
        today = date.today().isoformat()
        week_later = date.today().replace(day=date.today().day + 7).isoformat() if date.today().day <= 24 else date.today().isoformat()
        # Conta eventi nei prossimi 7 giorni
        count = sum(1 for ev in agenda if ev["data"] >= today)
        return str(count)

    @property
    def extra_state_attributes(self) -> dict:
        """Restituisce l'elenco completo degli eventi."""
        if not self.coordinator.data:
            return {"eventi": []}
        return {"eventi": self.coordinator.data.get("agenda", [])}


class ClassevivaVotiSensor(ClassevivaBaseSensor):
    """Sensore per i voti."""

    def __init__(self, coordinator, entry, student_name):
        super().__init__(coordinator, entry, student_name, "voti")
        self._attr_name = f"Classeviva Voti — {student_name}"
        self._attr_icon = "mdi:school"

    @property
    def native_value(self) -> str:
        """Restituisce la media dei voti numerici."""
        if not self.coordinator.data:
            return "N/D"
        voti = self.coordinator.data.get("voti", [])
        valori_numerici = []
        for v in voti:
            try:
                valori_numerici.append(float(v["voto"].replace(",", ".")))
            except (ValueError, AttributeError):
                pass
        if not valori_numerici:
            return "N/D"
        media = sum(valori_numerici) / len(valori_numerici)
        return f"{media:.2f}"

    @property
    def extra_state_attributes(self) -> dict:
        """Restituisce l'elenco completo dei voti."""
        if not self.coordinator.data:
            return {"voti": []}
        return {"voti": self.coordinator.data.get("voti", [])}


class ClassevivaComunicazioniSensor(ClassevivaBaseSensor):
    """Sensore per le comunicazioni scuola-famiglia."""

    def __init__(self, coordinator, entry, student_name):
        super().__init__(coordinator, entry, student_name, "comunicazioni")
        self._attr_name = f"Classeviva Comunicazioni — {student_name}"
        self._attr_icon = "mdi:bell-ring"

    @property
    def native_value(self) -> str:
        """Restituisce il numero di comunicazioni non lette."""
        if not self.coordinator.data:
            return "0"
        comunicazioni = self.coordinator.data.get("comunicazioni", [])
        non_lette = sum(1 for c in comunicazioni if not c.get("letta", True))
        return str(non_lette)

    @property
    def extra_state_attributes(self) -> dict:
        """Restituisce l'elenco completo delle comunicazioni."""
        if not self.coordinator.data:
            return {"comunicazioni": []}
        return {"comunicazioni": self.coordinator.data.get("comunicazioni", [])}
