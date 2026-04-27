"""Config flow per Classeviva."""
from __future__ import annotations

import logging
from typing import Any

import requests
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_STUDENT_NAME,
    API_BASE_URL,
    API_HEADERS,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, description={"suggested_value": ""}): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_STUDENT_NAME, default="Studente"): str,
    }
)


def try_login(username: str, password: str) -> dict | None:
    """Prova a fare il login e restituisce i dati o None se fallisce."""
    payload = {
        "uid": username,
        "pass": password,
        "pin": "",
        "target": "famiglia" if username.upper().startswith("S") else "studente",
    }
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            headers=API_HEADERS,
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 422:
            return None  # Credenziali errate
        raise
    except Exception:
        raise


class ClassevivaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestisce il flusso di configurazione per Classeviva."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Gestisce il primo passo: inserimento credenziali."""
        errors: dict[str, str] = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME].strip()
            password = user_input[CONF_PASSWORD]

            try:
                result = await self.hass.async_add_executor_job(
                    try_login, username, password
                )
                if result is None:
                    errors["base"] = "invalid_auth"
                else:
                    # Login riuscito — crea la voce
                    student_name = user_input.get(CONF_STUDENT_NAME, "Studente")
                    return self.async_create_entry(
                        title=f"Classeviva — {student_name}",
                        data={
                            CONF_USERNAME: username,
                            CONF_PASSWORD: password,
                            CONF_STUDENT_NAME: student_name,
                        },
                    )
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "username_hint": "Inserisci il tuo codice utente Classeviva (es. S1234567X oppure il codice fiscale)"
            },
        )
