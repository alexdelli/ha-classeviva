"""Costanti per l'integrazione Classeviva."""

DOMAIN = "classeviva"

# Configurazione
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_STUDENT_NAME = "student_name"

# Intervallo di aggiornamento (in minuti)
DEFAULT_SCAN_INTERVAL = 60

# API Classeviva
API_BASE_URL = "https://web.spaggiari.eu/rest/v1"
API_HEADERS = {
    "User-Agent": "CVVS/std/4.1.7 Android/10",
    "Z-Dev-ApiKey": "Tg1NWEwNGIgIC0K",
    "Content-Type": "application/json",
    "Z-If-None-Match": "*",
}

# Nomi dei sensori
SENSOR_AGENDA = "classeviva_agenda"
SENSOR_VOTI = "classeviva_voti"
SENSOR_COMUNICAZIONI = "classeviva_comunicazioni"
